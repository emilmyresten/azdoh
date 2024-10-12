from common.text import find_azdo_expressions
from handler.task.bash3.job.shellcheck import sanitize


def test_find_azdo_expressions():
    result = find_azdo_expressions(
        "${{ parameter.azdo }}${{ parameter.expression }} ${{ parameter.azdo }}"
    )
    assert "${{ parameter.azdo }}" in result and "${{ parameter.expression }}" in result


def test_sanitize():
    result = sanitize("${{ parameter.someParam }}")
    assert "${{ parameter.someParam }}" not in result
