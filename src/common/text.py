import re


def find_azdo_expressions(script: str) -> list[str]:
    """
    Find occurrencese of ${{ }}
    """
    pattern = r"\${{ [A-Za-z.]+ }}"
    matches = re.findall(pattern, script)
    return set(matches)


def replace_all(script: str, replacements: list[dict]) -> str:
    """
    Recursively replace all occurrences of string with replacement by proving replacements on the form [{"original": <value>, "replacement": <replacement-value>}]
    """
    if len(replacements) == 0:
        return script

    replacement = replacements[0]
    return replace_all(
        script.replace(replacement["original"], replacement["replacement"]),
        replacements[1:],
    )


def print_handler_start(content: str):
    upper_padding = "\n\n"
    inner = f"{"#" * 10} {content} {"#" * 10}"
    content_length = len(inner)
    start_end_block = "#" * content_length
    padding = f"{"#" * 10} {" " * len(content)} {"#" * 10}"
    print(upper_padding)
    print(start_end_block)
    print(padding)
    print(inner)
    print(padding)
    print(start_end_block)


def print_job_start(content: str):
    print(f"\n{"~" * 10} {content} {"~" * 10}\n")
