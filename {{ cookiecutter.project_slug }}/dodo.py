import subprocess
from pathlib import Path

DOIT_CONFIG = {
    "default_tasks": [
        "format",
        "lint",
        "mypy",
        "ruff",
        "test",
        "coverage_with_fail_under",
        "vulture",
    ],
    "continue": True,
}


cwd = Path()
test_files = list(cwd.glob("test*.py"))
python_files = list(cwd.glob("*.py"))

# add any files with doctests to test_files
test_files = test_files + []
test_files_as_txt = " ".join([t.name for t in test_files])


def task_format():
    """Format all Python files."""
    return {
        "actions": [
            ["ruff", "format", "--check", "."],
        ],
        "uptodate": [False],
    }


def task_lint():
    """Run pylint on all Python files."""
    for f in python_files:
        yield {
            "name": f.name,
            "actions": [
                [
                    "pylint",
                    "--output-format=parseable",
                    "--rcfile",
                    "pyproject.toml",
                    f,
                ],
            ],
            "file_dep": [f],
        }


def task_mypy():
    """Type check all Python files."""
    return {
        "actions": [
            ["mypy", "."],
        ],
        "uptodate": [False],
    }


def task_ruff():
    """Run ruff on all Python files."""
    return {
        "actions": [
            ["ruff", "check", "."],
        ],
        "uptodate": [False],
    }


def task_ruff_fix_imports():
    """Fix import sorting using ruff for all Python files."""
    return {
        "actions": [
            ["ruff", "check", "--fix", "--select", "I001", "."],
        ],
        "uptodate": [False],
    }


def task_test():
    """Run pytest on all test files."""
    for f in test_files:
        yield {
            "name": f.name,
            "actions": [["pytest", "--doctest-modules", f]],
            "file_dep": [f],
        }


COVERAGE_ACTIONS = [
    [
        "coverage",
        "run",
        "--branch",
        "-m",
        "pytest",
        test_files_as_txt,
    ],
    ["coverage", "report"],
]


def task_coverage():
    """Run coverage over pytest."""
    return {
        "actions": COVERAGE_ACTIONS,
        "uptodate": [False],
        "verbosity": 2,
    }


def task_coverage_with_fail_under():
    """Run coverage over pytest output only if coverage is below threshold."""
    return {
        "actions": COVERAGE_ACTIONS,
        "uptodate": [False],
    }


def task_vulture():
    """Check all Python files for dead code."""
    return {
        "actions": [
            ["vulture", ".", "vulture_allow.txt"],
        ],
        "uptodate": [False],
    }


def task_vulture_allow():
    """Update vulture allow list."""

    def r():
        p = subprocess.run(
            ["vulture", ".", "--make-whitelist"],
            capture_output=True,
            check=False,
            text=True,
        )
        Path("vulture_allow.txt").write_text(p.stdout)

    return {
        "actions": [r],
        "uptodate": [False],
    }
