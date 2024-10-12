from common.text import print_handler_start
from handler.task.bash3.job.shellcheck import shellcheck
from handler.task.bash3.job.python3_script_sanitycheck import python3_script_sanitycheck


def bash3_handler(task: dict):
    ## all logic for handling bash3 tasks
    display_name = task["displayName"]
    script = task["inputs"]["script"]
    working_directory = task["inputs"]["workingDirectory"]
    print_handler_start(f"Examining Bash@3 task: {display_name}")
    if script is not None:
        print(shellcheck(script))
        print(python3_script_sanitycheck(script, working_directory))
    else:
        print(f"No script found for Bash@3 task {display_name}, targetType not inline?")


if __name__ == "__main__":
    bash3_handler({})
