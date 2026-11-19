import json

import httpx
import pytest

import client as c

OR_RESPONSE = {
    "id": "gen-1",
    "model": "google/gemini-decision-1",
    "provider": "Google",
    "answers": {"covered": {"type": "noul", "noul": 0.87}},
    "usage": {"input_tokens": 230, "output_tokens": 0, "cost": 0.000023},
}
QUESTIONS = {"covered": {"type": "noul", "instructions": "x", "criteria": {"true": "t", "false": "f"}}}


def make_openrouter(handler, **kwargs):
    sleeps = []
    cl = c.OpenRouterClient(
        api_key="dummy-key-for-tests", transport=httpx.MockTransport(handler), sleep=sleeps.append, **kwargs
    )
    return cl, sleeps


def test_openrouter_sends_model_state_and_questions_with_bearer_auth():
    seen = {}

    def handler(request):
        seen["url"] = str(request.url)
        seen["auth"] = request.headers.get("authorization")
        seen["body"] = json.loads(request.content)
        return httpx.Response(200, json=OR_RESPONSE)

    cl, _ = make_openrouter(handler)
    res = cl.decide("google/gemini-decision-1", "STATE", QUESTIONS)
    assert seen["url"] == "https://openrouter.ai/api/alpha/decisions"
    assert seen["auth"] == "Bearer dummy-key-for-tests"
    assert seen["body"] == {"model": "google/gemini-decision-1", "state": "STATE", "questions": QUESTIONS}
    assert res.ok is True
    assert res.status == 200
    assert res.p_yes == 0.87
    assert res.model_returned == "google/gemini-decision-1"
    assert res.provider_returned == "Google"
    assert res.input_tokens == 230
    assert res.output_tokens == 0
    assert res.cost == 0.000023
    assert res.attempts == 1
    assert res.latency_ms >= 0
    assert res.answers == OR_RESPONSE["answers"]


def test_retries_on_429_then_succeeds_with_growing_backoff():
    calls = {"n": 0}

    def handler(request):
        calls["n"] += 1
        if calls["n"] < 3:
            return httpx.Response(429, json={"error": {"code": 429, "message": "slow down"}})
        return httpx.Response(200, json=OR_RESPONSE)

    cl, sleeps = make_openrouter(handler)
    res = cl.decide("m", "s", QUESTIONS)
    assert res.ok is True
    assert res.attempts == 3
    assert len(sleeps) == 2
    assert sleeps[1] > sleeps[0]


def test_does_not_retry_on_400_and_keeps_the_error_message():
    def handler(request):
        return httpx.Response(400, json={"error": {"code": 400, "message": "bad criteria"}})

    cl, sleeps = make_openrouter(handler)
    res = cl.decide("m", "s", QUESTIONS)
    assert res.ok is False
    assert res.status == 400
    assert res.attempts == 1
    assert sleeps == []
    assert "bad criteria" in res.error
    assert res.p_yes is None


def test_gives_up_after_max_attempts_on_persistent_502():
    def handler(request):
        return httpx.Response(502, json={"error": {"code": 502, "message": "upstream"}})

    cl, sleeps = make_openrouter(handler, max_attempts=4)
    res = cl.decide("m", "s", QUESTIONS)
    assert res.ok is False
    assert res.status == 502
    assert res.attempts == 4
    assert len(sleeps) == 3


def test_network_errors_are_retried_and_reported():
    calls = {"n": 0}

    def handler(request):
        calls["n"] += 1
        if calls["n"] == 1:
            raise httpx.ConnectError("boom")
        return httpx.Response(200, json=OR_RESPONSE)

    cl, sleeps = make_openrouter(handler)
    res = cl.decide("m", "s", QUESTIONS)
    assert res.ok is True
    assert res.attempts == 2
    assert len(sleeps) == 1


def test_refusal_answer_is_flagged_and_gives_no_probability():
    def handler(request):
        return httpx.Response(200, json=dict(OR_RESPONSE, answers={"covered": {"type": "refusal"}}))

    cl, _ = make_openrouter(handler)
    res = cl.decide("m", "s", QUESTIONS)
    assert res.ok is True
    assert res.refused is True
    assert res.p_yes is None


def test_non_json_body_is_an_error_not_a_crash():
    def handler(request):
        return httpx.Response(200, text="<html>gateway</html>")

    cl, _ = make_openrouter(handler, max_attempts=1)
    res = cl.decide("m", "s", QUESTIONS)
    assert res.ok is False
    assert "json" in res.error.lower()


def test_record_never_contains_the_api_key():
    def handler(request):
        return httpx.Response(200, json=OR_RESPONSE)

    cl, _ = make_openrouter(handler)
    record = cl.decide("m", "s", QUESTIONS).to_record()
    assert "dummy-key-for-tests" not in json.dumps(record)


def test_gemini_client_uses_input_and_the_api_key_header():
    seen = {}

    def handler(request):
        seen["url"] = str(request.url)
        seen["key"] = request.headers.get("x-goog-api-key")
        seen["body"] = json.loads(request.content)
        return httpx.Response(
            200,
            json={
                "answers": {"covered": {"type": "noul", "noul": 0.42, "confidence": 0.84}},
                "usage": {"total_input_tokens": 199},
            },
        )

    cl = c.GeminiClient(api_key="dummy-key-for-tests", transport=httpx.MockTransport(handler), sleep=lambda s: None)
    res = cl.decide("gemini-decision-1", "STATE", {"covered": {"type": "noul", "instructions": "x"}})
    assert seen["url"] == "https://generativelanguage.googleapis.com/v1beta/decisions"
    assert seen["key"] == "dummy-key-for-tests"
    assert seen["body"] == {
        "model": "gemini-decision-1",
        "input": "STATE",
        "questions": {"covered": {"type": "noul", "instructions": "x"}},
    }
    assert res.ok is True
    assert res.p_yes == 0.42
    assert res.input_tokens == 199
    assert res.cost is None


def test_missing_key_raises_a_clear_error(monkeypatch):
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    with pytest.raises(c.MissingKey):
        c.OpenRouterClient()
    with pytest.raises(c.MissingKey):
        c.GeminiClient()
