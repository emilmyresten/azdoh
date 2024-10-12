import yaml
from handler.task.bash3.handler import bash3_handler
from filesystem.tmp import create_tmp_dir, delete_tmp_dir

"""
The handler is invoked on the given key-value pair, case insensitive.
"""
handlers = {"task": {"bash@3": [bash3_handler]}}


def dispatch(yml, k, v):
    [handler(yml) for handler in handlers[k.lower()][v.lower()]]


def recursive_kv_walk(yml: dict):
    for k, v in yml.items():
        if isinstance(v, dict) or isinstance(v, list):  # depth-first search
            recursive_walk(v)
        elif k.lower() in handlers.keys() and v.lower() in handlers[k.lower()].keys():
            dispatch(yml, k, v)


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
    tmp_dir = create_tmp_dir()
    with open(
        "/Users/emilmyresten/Development/personal/python/azdoh/example_project/azdo/bash3/python-in-bash-script.yml",
        "r",
    ) as f:
        yml = yaml.safe_load(f)
    recursive_walk(yml)
    delete_tmp_dir(tmp_dir)


if __name__ == "__main__":
    main()
