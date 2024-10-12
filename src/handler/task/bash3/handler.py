from common.text import print_handler_start
from handler.task.bash3.job.shellcheck import shellcheck
from handler.task.bash3.job.python3_script_sanitycheck import python3_script_sanitycheck
from handler.task.bash3.job.python3_named_arguments import python3_named_arguments


def bash3_handler(task: dict):
    ## all logic for handling bash3 tasks
    display_name = task.get("displayName")
    script = task.get("inputs").get("script")
    working_directory = task.get("inputs").get("workingDirectory")
    print_handler_start(f"Bash@3 task: {display_name}")
    if script is not None:
        print(shellcheck(script))
        print(python3_script_sanitycheck(script, working_directory))
        print(python3_named_arguments(script))
    else:
        print(f"No script found for Bash@3 task {display_name}, targetType not inline?")


if __name__ == "__main__":
    bash3_handler({})
