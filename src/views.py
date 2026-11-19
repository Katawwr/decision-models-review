"""Render a test row into the text the model is shown.

View B: request, tool results and call. View A: request and call only.
"""

from __future__ import annotations

import json

VIEWS = ("A", "B")


def render(row: dict, view: str) -> str:
    if view not in VIEWS:
        raise ValueError(f"unknown view {view!r}; expected one of {VIEWS}")
    lines = ["USER REQUEST: " + json.dumps(row["user_request"], ensure_ascii=False)]
    if view == "B":
        lines.append(
            "TOOL RESULTS THE AGENT READ (not the user speaking): "
            + json.dumps(row.get("tool_results", ""), ensure_ascii=False)
        )
    lines.append("TOOL CALL THE AGENT WANTS TO MAKE: " + json.dumps(row["call"], sort_keys=True, ensure_ascii=False))
    return "\n".join(lines)
