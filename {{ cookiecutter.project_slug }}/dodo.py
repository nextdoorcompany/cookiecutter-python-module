from pathlib import Path

DOIT_CONFIG = {
    "default_tasks": [
        "lint",
        #        "mypy",
        #        "test",
        "ruff",
        #        "coverage_with_fail_under",
        #        "vulture",
    ],
    "continue": True,
}


cwd = Path()
test_files = list(cwd.glob("test*.py"))
python_files = list(cwd.glob("*.py"))


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


# def task_test():
#     "Runs pytest on all test files."
#     for f in test_files:
#         yield {
#             "name": f.name,
#             "actions": [["{{ cookiecutter.path_to_venv }}/bin/python", "-m", "pytest", f]],
#             "file_dep": [f],
#         }


# def task_coverage():
#     "Runs coverage over pytest on the test directory."
#     return {
#         "actions": [
#             ["{{ cookiecutter.path_to_venv }}/bin/coverage", "run", "-m", "pytest", "."],
#             ["{{ cookiecutter.path_to_venv }}/bin/coverage", "report"],
#         ],
#         "uptodate": [False],
#         "verbosity": 2,
#     }


# def task_coverage_with_fail_under():
#     "Runs coverage over pytest on the test directory with no output unless coverage is below threshold."
#     return {
#         "actions": [
#             ["{{ cookiecutter.path_to_venv }}/bin/coverage", "run", "-m", "pytest", "."],
#             ["{{ cookiecutter.path_to_venv }}/bin/coverage", "report"],
#         ],
#         "uptodate": [False],
#     }


# def task_vulture():
#     "Runs vulture on the source directory."
#     return {
#         "actions": [
#             ["{{ cookiecutter.path_to_venv }}/bin/vulture", "."],
#         ],
#         "uptodate": [False],
#     }
