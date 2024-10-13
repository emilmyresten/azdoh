### Requirements:
- poetry
- pyenv
- shellcheck


# Run instructions

1. export PYTHONPATH=$(pwd)/src where pwd is project root.
2. poetry shell
3. poetry install
4. poetry run pytest


Azdoh assumes it is being invoked from the project root.


# todo:
- write tests
- check that all parameters used are defined in parameter list?
- ensure that all parameters without default is passed whenever used as template.