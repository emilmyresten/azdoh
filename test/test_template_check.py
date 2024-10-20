import logging
from pathlib import Path
import os

from click.testing import CliRunner

from azdoh.main import main
from testutil.caplog_util import pprint


def test_happy_flow(caplog):
    caplog.set_level(logging.INFO)

    # We need to enter the example project in order to correctly execute azdoh, as it assumes it is being executed in the source root.
    test_dir = Path(__file__).parent
    os.chdir((test_dir / "example_project").absolute())

    result = CliRunner().invoke(main, ["-f", "azdo/templates/caller.yml"])

    pprint(caplog.records)
    # assert (
    #     shellcheck_log["msg"] != ""
    #     and "Tips depend on target shell and yours is unknown." in shellcheck_log["msg"]
    # )
    # assert result.exit_code == 0
