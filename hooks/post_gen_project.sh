#! /usr/bin/bash

chmod +x {{ cookiecutter.main_file }}.py
uv venv --python 3.13 {{ cookiecutter.path_to_venv }}
uv pip compile pyproject.toml --python {{ cookiecutter.path_to_venv }}/bin/python --generate-hashes --output-file requirements.txt
uv pip sync --python {{ cookiecutter.path_to_venv }}/bin/python requirements.txt
echo see https://github.com/nextdoorcompany/cookiecutter-python-module
