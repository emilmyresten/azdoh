import re

from pathlib import Path

from common.text import find_azdo_expressions, replace_all, print_job_start
from filesystem.files import check_if_file_exists
from shell import execute


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


def prepend_working_directory(path: str, working_directory: str) -> list[str]:
    relative_working_directory = get_relative_working_directory(working_directory)
    return f"{relative_working_directory}/{path}"


def find_python3_script_locations(script: str, working_directory: str) -> list[Path]:
    """
    Find invocation of python3 scripts and return their locations
    """
    pattern = r"python3 (?:-m )?([^ ]+)"  ## (?:) creates a non-capturing group, () creates a capturing group
    paths = re.findall(pattern, script)
    if paths:
        paths = [
            (
                prepend_working_directory(path, working_directory)
                if working_directory is not None
                and not path.startswith("/")  ## this would mean it's an absolute path
                else path
            )
            for path in paths
        ]  # if path.startswith]
        return [Path(path) for path in paths]
    return []


def python3_script_sanitycheck(script: str, working_directory: str) -> list[dict]:
    """
    Perform sanity check to ensure the files given in the pipeline exist in the project
    """
    print_job_start("Sanity check: does script really exist?")
    paths = find_python3_script_locations(script, working_directory)
    results = [
        {"path": str(path.absolute()), "exists": check_if_file_exists(path)}
        for path in paths
    ]
    return results


if __name__ == "__main__":
    script = 'export PYTHONPATH=$(pwd)\npython3 -m ./pkg/example_python.py "${{ parameters.buildArtifactsDir }}/${{ parameters.buildPublishFile }}"'
    working_directory = "${{ parameters.pipelineDir }}/src"
    paths = find_python3_script_locations(script, working_directory)
    print(execute("pwd", return_output=True))
    for path in paths:
        print(f"{path.absolute()} exists: {check_if_file_exists(path)}")

    print(path)
