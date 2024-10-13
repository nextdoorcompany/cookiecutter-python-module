#! /usr/bin/bash

chmod +x {{ cookiecutter.main_file }}.py
uv venv --python 3.13
uv pip compile pyproject.toml --generate-hashes --output-file requirements.txt
uv pip sync requirements.txt
echo see https://github.com/nextdoorcompany/cookiecutter-python-module
