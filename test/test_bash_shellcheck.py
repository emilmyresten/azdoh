import logging
from pathlib import Path
import os

from click.testing import CliRunner

from azdoh.main import main


def test_happy_flow(caplog):
    caplog.set_level(logging.INFO)

    # We need to enter the example project in order to correctly execute azdoh, as it assumes it is being executed in the source root.
    test_dir = Path(__file__).parent
    os.chdir((test_dir / "example_project").absolute())

    result = CliRunner().invoke(
        main, ["-f", "azdo/tasks/bash3/shellcheck/shellcheck.yml"]
    )
    shellcheck_log = [
        {"msg": log.message, "src": log.pathname.split("/")[-1]}
        for log in caplog.records
        if log.pathname.split("/")[-1] == "shellcheck.py"
    ][0]

    assert (
        shellcheck_log["msg"] != ""
        and "Tips depend on target shell and yours is unknown." in shellcheck_log["msg"]
    )
    assert result.exit_code == 0
