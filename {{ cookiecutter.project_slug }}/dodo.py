import subprocess
from pathlib import Path

DOIT_CONFIG = {
    "default_tasks": [
        "format",
        "lint",
        "mypy",
        "ruff",
        "test",
        "toml_lint",
        "coverage_with_fail_under",
        "vulture",
    ],
    "continue": True,
}


cwd = Path()
test_files = list(cwd.glob("test*.py"))
python_files = list(cwd.glob("*.py"))
toml_files = list(cwd.glob("*.toml"))
venv_bin = "{{ cookiecutter.path_to_venv }}/bin/"

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
            "actions": [[venv_bin + "pytest", "--doctest-modules", f]],
            "file_dep": [f],
        }


COVERAGE_ACTIONS = [
    [
        venv_bin + "coverage",
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


def task_toml_lint():
    """Run toml-sort on all toml files."""
    for f in toml_files:
        yield {
            "name": f.name,
            "actions": [
                [
                    "toml-sort",
                    "--spaces-indent-inline-array",
                    "4",
                    "--trailing-comma-inline-array",
                    "--check",
                    f,
                ]
            ],
            "file_dep": [f],
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


def task_compile():
    """Generate requirements.txt file."""
    return {
        "actions": [
            [
                "uv",
                "pip",
                "compile",
                "pyproject.toml",
                "--python",
                venv_bin + "python",
                "--generate-hashes",
                "--quiet",
                "--output-file",
                "requirements.txt",
            ],
        ],
        "uptodate": [False],
    }


def task_compile_with_upgrade():
    """Generate requirements.txt file with updated deps."""
    return {
        "actions": [
            [
                "uv",
                "pip",
                "compile",
                "pyproject.toml",
                "--python",
                venv_bin + "python",
                "--generate-hashes",
                "--upgrade",
                "--quiet",
                "--output-file",
                "requirements.txt",
            ],
        ],
        "uptodate": [False],
    }


def task_sync():
    """Sync venv with requirements.txt."""
    return {
        "actions": [
            [
                "uv",
                "pip",
                "sync",
                "--python",
                venv_bin + "python",
                "requirements.txt",
            ],
        ],
        "uptodate": [False],
    }


def task_rebuild_venv():
    """Build new virtual environment.  Overwrites existing."""
    return {
        "actions": [
            "uv venv --python 3.%(python_minor)s {{ cookiecutter.path_to_venv }}",
            "sed --in-place=.bak s/py3[0-9][0-9]/py3%(python_minor)s/ pyproject.toml",
            "diff -u pyproject.toml.bak pyproject.toml || :",
        ],
        "params": [
            {
                "name": "python_minor",
                "long": "minor",
                "default": {{ cookiecutter.python_minor_version }},
                "help": "Python minor version",
            }
        ],
        "uptodate": [False],
        "verbosity": 2,
    }
