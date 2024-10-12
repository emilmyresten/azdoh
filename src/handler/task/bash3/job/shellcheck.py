import random
import string

from shell import execute
from filesystem.tmp import write_content_to_tmp_file, delete_tmp_file
from common.text import find_azdo_expressions, replace_all, print_job_start


def sanitize(script) -> str:
    """
    Sanitize script by removing azure.pipelines specific expressions e.g. ${{ parameters.someParam }}
    This prevents shellcheck from irrelevant complaints. Keeping the $ signifies that it is still a variable.
    """
    expressions = find_azdo_expressions(script)
    replacements = [
        {
            "original": expression,
            "replacement": f"$PLACEHOLDER_VAR_{''.join(random.choices(string.ascii_uppercase, k=7))}",
        }
        for expression in expressions
    ]
    return replace_all(script, replacements)


def shellcheck(script) -> str:
    """
    Perform shellcheck of script.
    Need to dump to tmp file to properly run shellcheck.
    """
    print_job_start("shellcheck")
    santized_script = sanitize(script)
    tmp_file = write_content_to_tmp_file(santized_script)
    result = execute(f"shellcheck {tmp_file.absolute()}", return_output=True)
    delete_tmp_file(tmp_file)
    return result
