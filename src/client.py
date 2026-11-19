"""Clients for the two decision APIs: persistent connection, retries with backoff, timing.

Keys are read from the environment and never stored in results.
"""

from __future__ import annotations

import os
import random
import time
from dataclasses import asdict, dataclass

import httpx

OPENROUTER_URL = "https://openrouter.ai/api/alpha/decisions"
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/decisions"
RETRY_STATUSES = {408, 429, 500, 502, 503, 504, 529}


class MissingKey(RuntimeError):
    pass


@dataclass
class CallResult:
    ok: bool
    status: int | None
    latency_ms: int
    attempts: int
    error: str | None = None
    model_returned: str | None = None
    provider_returned: str | None = None
    input_tokens: int | None = None
    output_tokens: int | None = None
    cost: float | None = None
    p_yes: float | None = None
    refused: bool = False
    answers: dict | None = None
    response_id: str | None = None

    def to_record(self) -> dict:
        return asdict(self)


class _DecisionClient:
    url = ""
    env_var = ""

    def __init__(
        self,
        api_key: str | None = None,
        transport: httpx.BaseTransport | None = None,
        sleep=time.sleep,
        timeout: float = 30.0,
        max_attempts: int = 5,
        base_delay: float = 1.0,
    ):
        key = api_key if api_key is not None else os.environ.get(self.env_var)
        if not key:
            raise MissingKey(f"{self.env_var} is not set in the environment")
        self._sleep = sleep
        self._max_attempts = max_attempts
        self._base_delay = base_delay
        self._http = httpx.Client(timeout=timeout, transport=transport, headers=self._headers(key))

    def _headers(self, key: str) -> dict:
        raise NotImplementedError

    def _body(self, model: str, state, questions: dict) -> dict:
        raise NotImplementedError

    def _delay(self, attempt: int) -> float:
        return self._base_delay * (2 ** (attempt - 1)) + random.uniform(0, 0.25)

    def close(self) -> None:
        self._http.close()

    def decide(self, model: str, state, questions: dict) -> CallResult:
        body = self._body(model, state, questions)
        last: CallResult | None = None
        for attempt in range(1, self._max_attempts + 1):
            started = time.perf_counter()
            try:
                response = self._http.post(self.url, json=body)
            except httpx.HTTPError as exc:
                latency = round((time.perf_counter() - started) * 1000)
                last = CallResult(ok=False, status=None, latency_ms=latency, attempts=attempt,
                                  error=f"{type(exc).__name__}: {exc}")
                if attempt < self._max_attempts:
                    self._sleep(self._delay(attempt))
                    continue
                return last
            latency = round((time.perf_counter() - started) * 1000)
            status = response.status_code
            try:
                data = response.json()
            except ValueError:
                data = None
            if data is None or not isinstance(data, dict):
                last = CallResult(ok=False, status=status, latency_ms=latency, attempts=attempt,
                                  error=f"non-JSON body with status {status}: {response.text[:200]!r}")
            elif status != 200 or "answers" not in data:
                last = CallResult(ok=False, status=status, latency_ms=latency, attempts=attempt,
                                  error=_error_message(status, data))
            else:
                return _success(data, status, latency, attempt)
            if status in RETRY_STATUSES and attempt < self._max_attempts:
                self._sleep(self._delay(attempt))
                continue
            return last
        return last


def _error_message(status: int, data: dict) -> str:
    error = data.get("error")
    if isinstance(error, dict):
        return f"status {status}: {error.get('message')} (code {error.get('code')})"
    return f"status {status}: {str(data)[:200]}"


def _success(data: dict, status: int, latency: int, attempt: int) -> CallResult:
    answers = data.get("answers") or {}
    p_yes = None
    refused = False
    if len(answers) == 1:
        answer = next(iter(answers.values()))
        if isinstance(answer, dict):
            if answer.get("type") == "refusal":
                refused = True
            elif answer.get("noul") is not None:
                p_yes = float(answer["noul"])
    usage = data.get("usage") or {}
    return CallResult(
        ok=True,
        status=status,
        latency_ms=latency,
        attempts=attempt,
        model_returned=data.get("model"),
        provider_returned=data.get("provider"),
        input_tokens=usage.get("input_tokens", usage.get("total_input_tokens")),
        output_tokens=usage.get("output_tokens", usage.get("total_output_tokens")),
        cost=usage.get("cost"),
        p_yes=p_yes,
        refused=refused,
        answers=answers,
        response_id=data.get("id"),
    )


class OpenRouterClient(_DecisionClient):
    url = OPENROUTER_URL
    env_var = "OPENROUTER_API_KEY"

    def _headers(self, key: str) -> dict:
        return {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}

    def _body(self, model: str, state, questions: dict) -> dict:
        return {"model": model, "state": state, "questions": questions}


class GeminiClient(_DecisionClient):
    url = GEMINI_URL
    env_var = "GEMINI_API_KEY"

    def _headers(self, key: str) -> dict:
        return {"x-goog-api-key": key, "Content-Type": "application/json"}

    def _body(self, model: str, state, questions: dict) -> dict:
        return {"model": model, "input": state, "questions": questions}
