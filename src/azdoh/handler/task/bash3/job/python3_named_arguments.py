import logging
import re

from azdoh.common.text import log_job_start


def get_script_arguments(script: str) -> str:
    """
    Gets <argument list> for scripts invoked as python3 <path> <argument list>
    """
    pattern = r"python3 [^\s]+ ([^\n]+)"
    matches = re.findall(pattern, script)
    if matches:
        ## TODO: What to do if we have two python scripts in one bash3 task?
        args = matches[0].strip()
        return args


def get_argument_list(args: str) -> list[str]:
    return args.split(" ")


def check_if_using_named_args(arglist: list[str]) -> bool:
    """
    Checks whether named arguments are used using the heuristic that if so, every other argument begins with --
    """
    maybe_flags = arglist[::2]
    using_named_args = all(maybe_flag.startswith("--") for maybe_flag in maybe_flags)
    return using_named_args


def python3_named_arguments(script: str):
    log_job_start("Use of named arguments in Python script")
    args = get_script_arguments(script)
    if not args:
        logging.info("No python script with args found")
        return

    arglist = get_argument_list(args)
    using_named_args = check_if_using_named_args(arglist)
    if using_named_args:
        logging.info("OK")
    else:
        logging.warning(
            "Not using named arguments - @click.option(--<var_name>, required=True) when writing scripts with click."
        )


if __name__ == "__main__":
    script = 'export PYTHONPATH=$(pwd)\n python3 ./pkg/example_python.py --arg1 "arg1" --arg2 "arg2"\n echo "Done"'
    python3_named_arguments(script)
