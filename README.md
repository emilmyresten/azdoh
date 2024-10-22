### Requirements:
infra:
- poetry
- pyenv
- pipx

deps:
- shellcheck


# Run instructions

1. export PYTHONPATH=$(pwd)/src where pwd is project root.
2. poetry shell
3. poetry install
4. poetry run pytest


Azdoh assumes it is being invoked from the project root.


### run as standalone executable:
pipx install . in project root, then invoke azdoh, to reflect new changes use --force


### todo:
in template handler, error if intermediate directory does not exist
warn if file does not exist in python script sanitycheck
