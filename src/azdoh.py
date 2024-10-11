import yaml
from pathlib import Path
import re
import uuid
import random
import string

from shell import execute


def write_to_tmp(script: str) -> Path:
    tmp_dir = Path("tmp")
    tmp_dir.mkdir(exist_ok=True)
    tmp_file = Path(f"tmp/tmp_file-{str(uuid.uuid4())}")
    with open(tmp_file, "w") as tf:
        tf.write(script)
    return tmp_file


def cleanup_tmp(tmp_file: Path):
    tmp_dir = tmp_file.parent
    tmp_file.unlink()
    tmp_dir.rmdir()


def find_azdopipe_expressions(script: str) -> list[str]:
    """
    Find occurrencese of ${{ }}
    """
    pattern = r"\${{ [A-Za-z.]+ }}"
    matches = re.findall(pattern, script)
    return set(matches)


def replace_all(script: str, replacements: list[dict]) -> str:
    """
    Recursively replace all occurrences of original text with replacement
    """
    if len(replacements) == 0:
        return script

    replacement = replacements[0]
    return replace_all(
        script.replace(replacement["original"], replacement["replacement"]),
        replacements[1:],
    )


def sanitize(script) -> str:
    """
    Sanitize script by removing azure.pipelines specific expressions e.g. ${{ parameters.someParam }}
    This prevents shellcheck from irrelevant complaints. Keeping the $ signifies that it is still a variable.
    """
    expressions = find_azdopipe_expressions(script)
    replacements = [
        {
            "original": expression,
            "replacement": f"$VAR_{''.join(random.choices(string.ascii_uppercase, k=7))}",
        }
        for expression in expressions
    ]
    return replace_all(script, replacements)


def shellcheck(script) -> str:
    """
    Perform shellcheck of script.
    Need to dump to tmp file to properly run shellcheck.
    """
    print(f"---- Performing shellcheck ----")
    santized_script = sanitize(script)
    tmp_file = write_to_tmp(santized_script)
    result = execute(f"shellcheck {tmp_file.absolute()}", return_output=True)
    cleanup_tmp(tmp_file)
    return result


def bash3_handler(task: dict):
    ## all logic for handling bash3 tasks
    display_name = task["displayName"]
    script = task["inputs"]["script"]
    print(f"#### Bash@3 task {display_name} ####")
    if script is not None:
        print(shellcheck(script))
    else:
        print(f"No script found for Bash@3 task {display_name}, targetType not inline?")


handlers = {"task": {"bash@3": [bash3_handler]}}


def recursive_kv_walk(yml: dict):
    for k, v in yml.items():
        if isinstance(v, dict) or isinstance(v, list):  # depth-first search
            recursive_walk(v)
        elif k.lower() in handlers.keys() and v.lower() in handlers[k.lower()].keys():
            [handler(yml) for handler in handlers[k.lower()][v.lower()]]


def recursive_walk(yml: dict | list):
    """
    This function recursively walks the parsed dictionary to find tasks for which rules are defined.
    Currently only want to execute shellcheck on Bash@3 tasks
    """
    if isinstance(yml, dict):
        recursive_kv_walk(yml)
    elif isinstance(yml, list):
        for maybe_dict_or_list in yml:
            recursive_walk(maybe_dict_or_list)


def main():
    with open("./example-azdo-file.yml", "r") as f:
        yml = yaml.safe_load(f)
    recursive_walk(yml)


if __name__ == "__main__":
    main()
