"""Gradio demo UI for the Code Review Agent, mounted on FastAPI."""

from __future__ import annotations

import gradio as gr

from code_review_agent.agent import CodeReviewAgent
from code_review_agent.config import CONFIG
from code_review_agent.security import RateLimitError, ValidationError, sanitize_text
from code_review_agent.web import LIMITER, caller_id, make_app, run

_agent: CodeReviewAgent | None = None


def _get_agent() -> CodeReviewAgent:
    global _agent
    if _agent is None:
        _agent = CodeReviewAgent()
    return _agent


def handle(code: str, language: str, request: gr.Request):
    try:
        clean = sanitize_text(code, field="code", min_chars=10)
    except ValidationError as exc:
        yield f"⚠️ {exc}"
        return
    try:
        LIMITER.check(caller_id(request))
    except RateLimitError as exc:
        yield f"⏳ {exc}"
        return
    if not CONFIG.api_key_present:
        yield "⚠️ The demo is not configured (missing API key). See the GitHub repo to run it locally."
        return
    yield "🔎 Reviewing the code…"
    try:
        yield _get_agent().review(clean, language)
    except Exception:  # noqa: BLE001
        yield "⚠️ Something went wrong. Please try again in a moment."


def build_demo() -> gr.Blocks:
    with gr.Blocks(title="Code Review Agent — Day 05", theme=gr.themes.Soft()) as demo:
        gr.Markdown(
            "## 🔬 Code Review Agent\n"
            "Paste source code; get engineering-focused review comments "
            "(correctness, security, performance, design).\n\n"
            "*Day 05 of 14 AI Agents in 14 Days — code reasoning + review.*"
        )
        code = gr.Code(label="Code", language="python", lines=16)
        language = gr.Dropdown(
            label="Language",
            choices=["Auto-detect", "Python", "JavaScript", "TypeScript", "Java", "Go", "Rust", "C++", "C#", "Ruby", "PHP", "SQL"],
            value="Auto-detect",
        )
        run_btn = gr.Button("Review", variant="primary")
        out = gr.Markdown()
        run_btn.click(handle, inputs=[code, language], outputs=out)
    demo.queue(default_concurrency_limit=2, max_size=20)
    return demo


app = make_app(build_demo(), title="Code Review Agent")

if __name__ == "__main__":
    run(app)
