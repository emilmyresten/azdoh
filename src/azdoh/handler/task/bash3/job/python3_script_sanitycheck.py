import re
import logging

from pathlib import Path

from azdoh.common.text import (
    find_azdo_expressions,
    replace_all,
    log_job_start,
    sanitize,
    find_sanitized_azdo_expressions,
)
from azdoh.filesystem.files import check_if_file_exists


def get_relative_working_directory(working_directory: str) -> str:
    """
    Takes a working directory on the form "${{ parameters.pipelineDir }}/src and returns only ./src, i.e it removes dynamic azdo expressions.
    """
    azdo_expressions = find_azdo_expressions(working_directory)
    replacements = [
        {"original": expression, "replacement": "."} for expression in azdo_expressions
    ]
    relative_working_directory = replace_all(working_directory, replacements)
    return relative_working_directory


def prepend_working_directory(path: str, working_directory: str) -> str:
    relative_working_directory = get_relative_working_directory(working_directory)
    return f"{relative_working_directory}/{path}"


def replace_sanitized_azdo_exprs(path: str) -> str:
    """
    This function takes a path, and replaces any sanitized azdo expressions on the form $AZDO_VAR_LZXJLKA with "."
    """
    sanitized_azdo_exprs = find_sanitized_azdo_expressions(path)
    logging.debug(
        f"PYTHON3_SCRIPT_SANITYCHECK | replace_sanitized_azdo_exprs | Found sanitized_azdo_exprs: {sanitized_azdo_exprs}"
    )

    replacements = [
        {"original": azdo_expr, "replacement": "."}
        for azdo_expr in sanitized_azdo_exprs
    ]
    path = replace_all(path, replacements)
    return path


def path_mapper(path: str, working_directory: str) -> Path:
    """
    Perform all necessary operations to reify a path passed to python3
    """
    # Remove trailing newlines if no args are provided to the script
    path = path.strip()

    path = replace_sanitized_azdo_exprs(path)

    if working_directory is not None and not path.startswith("/"):
        path = prepend_working_directory(path, working_directory)
    return Path(path)


def find_python3_script_locations(script: str, working_directory: str) -> list[Path]:
    """
    Find invocation of python3 scripts and return their locations
    """
    pattern = r"python3 (?:-m )?\"?([^ \"]+)?"  ## (?:) creates a non-capturing group, () creates a capturing group
    paths = re.findall(pattern, script)
    if paths:
        return [path_mapper(path, working_directory) for path in paths]
    return []


def python3_script_sanitycheck(script: str, working_directory: str) -> list[dict]:
    """
    Perform sanity check to ensure the files given in the pipeline exist in the project
    """
    log_job_start("Sanity check: does script really exist?")
    sanitized_script = sanitize(script, replacement=".")
    paths = find_python3_script_locations(sanitized_script, working_directory)
    results = [
        {"path": str(path.absolute()), "exists": check_if_file_exists(path)}
        for path in paths
    ]
    logging.info(results)


if __name__ == "__main__":
    script = 'export PYTHONPATH=$(pwd)\npython3 -m ${{ parameters.pipelineDir }}/src/pkg/example_python.py "${{ parameters.buildArtifactsDir }}/${{ parameters.buildPublishFile }}"'
    working_directory = None
    script = sanitize(script)
    python3_script_sanitycheck(script, working_directory)
