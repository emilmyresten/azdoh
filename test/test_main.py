from click.testing import CliRunner

from azdoh.common.text import find_azdo_expressions
from azdoh.handler.task.bash3.job.shellcheck import sanitize
from azdoh.main import main


## System tests: run azdoh on an example yaml and assert on the output. Just mock the open() call in azdoh.main, rest of the script should be pure functions.


def test_find_azdo_expressions():
    result = find_azdo_expressions(
        "${{ parameter.azdo }}${{ parameter.expression }} ${{ parameter.azdo }}"
    )
    assert "${{ parameter.azdo }}" in result and "${{ parameter.expression }}" in result


def test_sanitize():
    result = sanitize("${{ parameter.someParam }}")
    assert "${{ parameter.someParam }}" not in result
