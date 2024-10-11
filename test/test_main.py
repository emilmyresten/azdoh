from azdoh import sanitize, find_azdopipe_expressions


def test_find_azdo_expressions():
    result = find_azdopipe_expressions(
        "${{ parameter.azdo }}${{ parameter.expression }} ${{ parameter.azdo }}"
    )
    assert "${{ parameter.azdo }}" in result and "${{ parameter.expression }}" in result


def test_sanitize():
    result = sanitize("${{ parameter.someParam }}")
    assert "${{ parameter.someParam }}" not in result
