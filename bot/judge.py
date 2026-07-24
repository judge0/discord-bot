"""Judge0 Python SDK integration and source-code helpers."""

from __future__ import annotations

import asyncio
import re

import judge0
from judge0 import LanguageAlias, MaxWaitTime, Submission

LANGUAGES = {
    language.name.lower().replace("_", "-"): language for language in LanguageAlias
}

LANGUAGE_SYNONYMS = {
    "c#": "csharp",
    "c++": "cpp",
    "c-sharp": "csharp",
    "f-sharp": "fsharp",
    "golang": "go",
    "js": "javascript",
    "node": "javascript",
    "py": "python",
    "python-3": "python3",
    "sh": "bash",
    "ts": "typescript",
}

LANGUAGE_DISPLAY_NAMES = {
    "c": "C",
    "c3": "C3",
    "cpp": "C++",
    "cpp-clang": "C++ (Clang)",
    "cpp-gcc": "C++ (GCC)",
    "csharp": "C#",
    "csharp-dotnet": "C# (.NET)",
    "csharp-mono": "C# (Mono)",
    "fsharp": "F#",
    "javascript": "JavaScript",
    "mpi-c": "MPI C",
    "mpi-cpp": "MPI C++",
    "mpi-python": "MPI Python",
    "objective-c": "Objective-C",
    "php": "PHP",
    "python2-pypy": "Python 2 (PyPy)",
    "python3-pypy": "Python 3 (PyPy)",
    "python-for-ml": "Python for ML",
    "python-pypy": "Python (PyPy)",
    "sqlite": "SQLite",
}

_FENCED_CODE = re.compile(
    r"\A```[^\n`]*\n(?P<source>.*?)(?:\n)?```\Z",
    flags=re.DOTALL,
)


class SubmissionTimeoutError(TimeoutError):
    """Raised when Judge0 does not finish a submission in time."""


def _language_key(value: str) -> str:
    return re.sub(r"[\s_]+", "-", value.strip().casefold())


def resolve_language(value: str) -> tuple[str, LanguageAlias]:
    """Resolve user input to a canonical name and Judge0 language alias."""
    key = _language_key(value)
    canonical_name = LANGUAGE_SYNONYMS.get(key, key)
    try:
        return canonical_name, LANGUAGES[canonical_name]
    except KeyError as error:
        raise ValueError(f"Unsupported language: {value}") from error


def display_language(canonical_name: str) -> str:
    """Return a human-readable language name."""
    return LANGUAGE_DISPLAY_NAMES.get(
        canonical_name,
        canonical_name.replace("-", " ").title(),
    )


def language_choices(current: str, limit: int = 25) -> list[tuple[str, str]]:
    """Return filtered display/canonical language pairs for autocomplete."""
    needle = _language_key(current)
    synonyms_by_language: dict[str, set[str]] = {
        language: set() for language in LANGUAGES
    }
    for synonym, language in LANGUAGE_SYNONYMS.items():
        synonyms_by_language[language].add(synonym)

    def search_terms(language: str) -> set[str]:
        return {
            language,
            display_language(language).casefold(),
            *synonyms_by_language[language],
        }

    matches = [
        language
        for language in LANGUAGES
        if not needle or any(needle in term for term in search_terms(language))
    ]
    matches.sort(
        key=lambda language: (
            not any(term.startswith(needle) for term in search_terms(language)),
            display_language(language).casefold(),
        )
    )
    return [(display_language(language), language) for language in matches[:limit]]


def strip_code_fence(value: str) -> str:
    """Remove an optional Discord Markdown code fence from source code."""
    source = value.strip()
    fenced_match = _FENCED_CODE.fullmatch(source)
    if fenced_match:
        return fenced_match.group("source")
    if len(source) >= 2 and source.startswith("`") and source.endswith("`"):
        return source[1:-1]
    return source


class Judge0Service:
    """Run synchronous Judge0 Python SDK operations without blocking Discord."""

    def __init__(self, *, timeout_seconds: float, max_concurrent: int) -> None:
        self.timeout_seconds = timeout_seconds
        self._semaphore = asyncio.Semaphore(max_concurrent)

    async def execute(
        self,
        *,
        source_code: str,
        language: LanguageAlias,
        stdin: str | None = None,
    ) -> Submission:
        """Create a submission and wait for it on a worker thread."""
        async with self._semaphore:
            return await asyncio.to_thread(
                self._execute_sync,
                source_code=source_code,
                language=language,
                stdin=stdin,
            )

    def _execute_sync(
        self,
        *,
        source_code: str,
        language: LanguageAlias,
        stdin: str | None,
    ) -> Submission:
        submission = judge0.async_run(
            source_code=source_code,
            language=language,
            stdin=stdin,
        )
        if not isinstance(submission, Submission):
            raise RuntimeError("Judge0 returned an unexpected batch response")

        judge0.wait(
            submissions=submission,
            retry_strategy=MaxWaitTime(self.timeout_seconds),
        )
        if not submission.is_done():
            raise SubmissionTimeoutError(
                f"Judge0 did not finish within {self.timeout_seconds:g} seconds"
            )
        return submission
