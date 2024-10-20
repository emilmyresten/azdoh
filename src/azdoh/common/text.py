import re
import random
import string
import logging


def find_azdo_expressions(text: str) -> list[str]:
    """
    Find occurrances of ${{ }}
    """
    pattern = r"\${{ [A-Za-z0-9.]+ }}"
    matches = re.findall(pattern, text)
    return set(matches)


def find_sanitized_azdo_expressions(text: str) -> list[str]:
    """
    Find occcurances of $AZDO_VAR_[A-Z]{7}
    """
    pattern = r"\$AZDO_VAR_[A-Z]{7}"
    matches = re.findall(pattern, text)
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


def sanitize(
    script: str,
    replacement: str = f"$AZDO_VAR_{''.join(random.choices(string.ascii_uppercase, k=7))}",
) -> str:
    """
    Sanitize script by replacing azure.pipelines specific expressions e.g. ${{ parameters.someParam }} with regular shell variables like $AZDO_VAR_HJLXLAV by default.
    This prevents e.g. shellcheck from irrelevant complaints or regex to fail due to spaces. Keeping the $ signifies that it is still a variable.
    Caller can pass non-default replacement when necessary.
    """
    expressions = find_azdo_expressions(script)
    replacements = [
        {
            "original": expression,
            "replacement": replacement,
        }
        for expression in expressions
    ]
    return replace_all(script, replacements)


def log_handler_start(content: str):
    left_padding = "\n" + " " * 11
    upper_padding = "\n"
    inner = f"{"#" * 10} {content} {"#" * 10}"
    content_length = len(inner)
    start_end_block = "#" * content_length
    padding = f"{"#" * 10} {" " * len(content)} {"#" * 10}"
    logging.info(
        left_padding.join(
            [upper_padding, start_end_block, padding, inner, padding, start_end_block]
        ).strip()
    )


def log_job_start(content: str):
    logging.info(f"{"~" * 10} {content} {"~" * 10}")
