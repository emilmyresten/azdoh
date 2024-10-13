import logging

from azdoh.shell import execute
from azdoh.filesystem.tmp import write_content_to_tmp_file, delete_tmp_file
from azdoh.common.text import log_job_start, sanitize


def shellcheck(script) -> str:
    """
    Perform shellcheck of script.
    Need to dump to tmp file to properly run shellcheck.
    """
    log_job_start("shellcheck")
    tmp_file = write_content_to_tmp_file(script)
    result = execute(f"shellcheck {tmp_file.absolute()}", return_output=True)
    delete_tmp_file(tmp_file)
    logging.info(result)
