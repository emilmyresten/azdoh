import yaml
from pathlib import Path
import re
import uuid

from shell import execute

example_yaml = """
steps:
  - task: Bash@3
    displayName: Copy prometheusrule.yaml from build repo to ${{ parameters.pipelineDir }}/${{ parameters.helmChartRelativeDir }}/templates
    inputs:
      targetType: inline
      script: |
        #!/bin/sh

        # Order is important because loop will "break" after first found entry
        Rules=("${{ parameters.buildArtifactsDir }}/helm/${{ parameters.env }}/prometheusrules.yaml" "${{ parameters.buildArtifactsDir }}/helm/prometheusrules.yaml")

        # Remove prometheusrules.yaml from previous environment
        rm ${{ parameters.pipelineDir }}/${{ parameters.helmChartRelativeDir }}/templates/prometheusrules.yaml

        for rule in ${Rules[*]}; do
          echo $rule
          if [ -f $rule ];
          then
            echo "Found rule: $rule"
            cp $rule ${{ parameters.pipelineDir }}/${{ parameters.helmChartRelativeDir }}/templates
            ls -al ${{ parameters.pipelineDir }}/${{ parameters.helmChartRelativeDir }}/templates
            break
          fi
        done
"""


def write_to_tmp(script: str) -> Path:
    tmp_dir = Path("tmp")
    tmp_dir.mkdir(exist_ok=True)
    tmp_file = Path("tmp/tmp_file")
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
    This prevents shellcheck from irrelevant complaints
    """
    expressions = find_azdopipe_expressions(script)
    replacements = [
        {"original": expression, "replacement": str(uuid.uuid4())}
        for expression in expressions
    ]
    return replace_all(script, replacements)


def shellcheck(script) -> str:
    santized_script = sanitize(script)
    tmp_file = write_to_tmp(santized_script)
    result = execute(f"shellcheck {tmp_file.absolute()}", return_output=True)
    cleanup_tmp(tmp_file)
    return result


def main() -> str:
    y = yaml.safe_load(example_yaml)
    return y


if __name__ == "__main__":
    script = main()["steps"][0]["inputs"]["script"]
    print(shellcheck(script))
