import logging
from pathlib import Path

from azdoh.context import AzdohContext


## template value begins with / is relative from project root, otherwise it is relative to the file itself.
def template_handler(context: AzdohContext, task: dict):
    template_file = task.get("template")
    logging.info(template_file)
    logging.info(context)
