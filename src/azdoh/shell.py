import subprocess


def execute(command: str, return_output: bool):
    result = subprocess.run(command, shell=True, capture_output=return_output)
    if result.stdout != "":
        return result.stdout.decode()
    else:
        return result.stderr.decode()
