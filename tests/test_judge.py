import judge0
import pytest
from judge0 import LanguageAlias, Status, Submission

from bot.judge import (
    Judge0Service,
    SubmissionTimeoutError,
    language_choices,
    resolve_language,
    strip_code_fence,
)


@pytest.mark.parametrize(
    ("value", "canonical", "expected"),
    [
        ("python", "python", LanguageAlias.PYTHON),
        (" PY ", "python", LanguageAlias.PYTHON),
        ("c++", "cpp", LanguageAlias.CPP),
        ("C_SHARP", "csharp", LanguageAlias.CSHARP),
        ("js", "javascript", LanguageAlias.JAVASCRIPT),
        ("python for ml", "python-for-ml", LanguageAlias.PYTHON_FOR_ML),
    ],
)
def test_resolve_language(
    value: str,
    canonical: str,
    expected: LanguageAlias,
) -> None:
    assert resolve_language(value) == (canonical, expected)


def test_resolve_language_rejects_unknown_value() -> None:
    with pytest.raises(ValueError, match="Unsupported language"):
        resolve_language("not-a-language")


def test_language_choices_include_synonym_matches() -> None:
    choices = language_choices("js")

    assert ("JavaScript", "javascript") in choices
    assert len(choices) <= 25


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("print(42)", "print(42)"),
        ("`print(42)`", "print(42)"),
        ("```python\nprint(42)\n```", "print(42)"),
        ("```\nline 1\nline 2\n```", "line 1\nline 2"),
    ],
)
def test_strip_code_fence(value: str, expected: str) -> None:
    assert strip_code_fence(value) == expected


@pytest.mark.asyncio
async def test_service_executes_with_official_sdk(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captured: dict[str, object] = {}
    submission = Submission(source_code="print(42)")
    submission.status = Status.ACCEPTED
    submission.stdout = "42\n"

    def fake_async_run(**kwargs: object) -> Submission:
        captured.update(kwargs)
        return submission

    def fake_wait(**kwargs: object) -> Submission:
        captured["wait"] = kwargs
        return submission

    monkeypatch.setattr(judge0, "async_run", fake_async_run)
    monkeypatch.setattr(judge0, "wait", fake_wait)
    service = Judge0Service(timeout_seconds=10, max_concurrent=1)

    result = await service.execute(
        source_code="print(42)",
        language=LanguageAlias.PYTHON,
        stdin="input",
    )

    assert result is submission
    assert captured["source_code"] == "print(42)"
    assert captured["language"] is LanguageAlias.PYTHON
    assert captured["stdin"] == "input"
    assert captured["wait"]["submissions"] is submission


@pytest.mark.asyncio
async def test_service_reports_submission_timeout(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    submission = Submission(source_code="while True: pass")
    submission.status = Status.PROCESSING
    monkeypatch.setattr(judge0, "async_run", lambda **kwargs: submission)
    monkeypatch.setattr(judge0, "wait", lambda **kwargs: submission)
    service = Judge0Service(timeout_seconds=0.1, max_concurrent=1)

    with pytest.raises(SubmissionTimeoutError):
        await service.execute(
            source_code="while True: pass",
            language=LanguageAlias.PYTHON,
        )
