import logging
from pathlib import Path
import yaml

from azdoh.shell import execute
from azdoh.common.text import log_handler_start
from azdoh.context import AzdohContext
from azdoh.handler.template.job.assert_template_parameters import (
    assert_template_parameters,
)


# The template value begins with / is relative from project root, otherwise it is relative to the file itself.
def resolve_filename(current_file, template_filename):
    """
    If the template filename begins with / the template is located relative to the project root, otherwise relative to the file itself.
    To keep things simple, handle all reading of files as if they are relative to project root, where azdoh is meant to be executed.
    """
    project_root = execute("pwd", return_output=True).strip()

    is_relative_to_project_root = template_filename.startswith("/")
    if is_relative_to_project_root:
        return f"{project_root}{template_filename}"
    else:
        parent_dir = "/".join(current_file.split("/")[:-1])
        return f"{parent_dir}/{template_filename}"


def template_handler(context: AzdohContext, task: dict):
    template_name = task.get("template")
    log_handler_start(f"Template: {context.file} -> {template_name}")

    template_filename = resolve_filename(context.file, template_name)
    logging.info(f"Opening template: {template_filename}")
    with open(Path(template_filename), "r") as the_template:
        template_yml = yaml.safe_load(the_template)
        assert_template_parameters(task, template_yml)
