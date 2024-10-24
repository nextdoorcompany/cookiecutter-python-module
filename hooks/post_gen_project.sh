#! /usr/bin/bash

chmod +x {{ cookiecutter.main_file }}.py
uv venv --python 3.{{ cookiecutter.python_minor_version }} {{ cookiecutter.path_to_venv }}
uv pip compile pyproject.toml --python {{ cookiecutter.path_to_venv }}/bin/python --generate-hashes --quiet --output-file requirements.txt
uv pip sync --python {{ cookiecutter.path_to_venv }}/bin/python requirements.txt
echo
echo see https://github.com/nextdoorcompany/cookiecutter-python-module
echo
doit list
echo
echo run ./{{ cookiecutter.main_file }}.py
echo
echo . eshell-activate
echo
