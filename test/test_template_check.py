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

    result = CliRunner().invoke(main, ["-f", "azdo/templates/caller-happyflow.yml"])

    log_messages = [
        {"msg": log.message, "src": log.pathname.split("/")[-1]}
        for log in caplog.records
    ]

    assert {"msg": "OK", "src": "assert_template_parameters.py"} in log_messages
    assert result.exit_code == 0


def test_defaults(caplog):
    caplog.set_level(logging.INFO)

    # We need to enter the example project in order to correctly execute azdoh, as it assumes it is being executed in the source root.
    test_dir = Path(__file__).parent
    os.chdir((test_dir / "example_project").absolute())

    result = CliRunner().invoke(main, ["-f", "azdo/templates/caller-defaults.yml"])

    log_messages = [
        {"msg": log.message, "src": log.pathname.split("/")[-1]}
        for log in caplog.records
    ]

    assert {
        "msg": "Default value fallbacks: [{'name': 'paramTwo', 'default': False, 'type': 'boolean'}]",
        "src": "assert_template_parameters.py",
    } in log_messages
    assert result.exit_code == 0


def test_missing(caplog):
    caplog.set_level(logging.INFO)

    # We need to enter the example project in order to correctly execute azdoh, as it assumes it is being executed in the source root.
    test_dir = Path(__file__).parent
    os.chdir((test_dir / "example_project").absolute())

    result = CliRunner().invoke(main, ["-f", "azdo/templates/caller-missing.yml"])

    log_messages = [
        {"msg": log.message, "src": log.pathname.split("/")[-1]}
        for log in caplog.records
    ]

    assert {
        "msg": "Missing required arguments: [{'name': 'paramOne', 'type': 'string'}]",
        "src": "assert_template_parameters.py",
    } in log_messages
    assert result.exit_code == 0


def test_redundant(caplog):
    caplog.set_level(logging.INFO)

    # We need to enter the example project in order to correctly execute azdoh, as it assumes it is being executed in the source root.
    test_dir = Path(__file__).parent
    os.chdir((test_dir / "example_project").absolute())

    result = CliRunner().invoke(main, ["-f", "azdo/templates/caller-redundant.yml"])

    log_messages = [
        {"msg": log.message, "src": log.pathname.split("/")[-1]}
        for log in caplog.records
    ]

    assert {
        "msg": "Redundant arguments: ['paramThree']",
        "src": "assert_template_parameters.py",
    } in log_messages
    assert result.exit_code == 0


def test_combo(caplog):
    caplog.set_level(logging.INFO)

    # We need to enter the example project in order to correctly execute azdoh, as it assumes it is being executed in the source root.
    test_dir = Path(__file__).parent
    os.chdir((test_dir / "example_project").absolute())

    result = CliRunner().invoke(main, ["-f", "azdo/templates/caller-combo.yml"])

    log_messages = [
        {"msg": log.message, "src": log.pathname.split("/")[-1]}
        for log in caplog.records
    ]

    pprint(caplog.records)

    assert {
        "msg": "Missing required arguments: [{'name': 'paramOne', 'type': 'string'}]",
        "src": "assert_template_parameters.py",
    } in log_messages
    assert {
        "msg": "Redundant arguments: ['paramThree']",
        "src": "assert_template_parameters.py",
    } in log_messages
    assert {
        "msg": "Default value fallbacks: [{'name': 'paramTwo', 'default': False, 'type': 'boolean'}]",
        "src": "assert_template_parameters.py",
    } in log_messages
    assert {
        "msg": "OK",
        "src": "assert_template_parameters.py",
    } not in log_messages
    assert result.exit_code == 0
