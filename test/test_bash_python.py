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
        main, ["-f", "azdo/tasks/bash3/python-in-bash/happy-flow.yml"]
    )
    log_messages = [
        {"msg": log.message, "src": log.pathname.split("/")[-1]}
        for log in caplog.records
    ]

    assert {
        "msg": "[{'path': '/Users/emilmyresten/Development/personal/python/azdoh/test/example_project/src/pkg/example_python.py', 'exists': True}]",
        "src": "python3_script_sanitycheck.py",
    } in log_messages
    assert {"msg": "OK", "src": "python3_named_arguments.py"} in log_messages
    assert result.exit_code == 0


def test_non_existing_file(caplog):
    caplog.set_level(logging.INFO)

    test_dir = Path(__file__).parent
    os.chdir((test_dir / "example_project").absolute())

    result = CliRunner().invoke(
        main, ["-f", "azdo/tasks/bash3/python-in-bash/non-existing-file.yml"]
    )
    log_messages = [
        {"msg": log.message, "src": log.pathname.split("/")[-1]}
        for log in caplog.records
    ]

    assert {
        "msg": "[{'path': '/Users/emilmyresten/Development/personal/python/azdoh/test/example_project/src/pkg/non-existant.py', 'exists': False}]",
        "src": "python3_script_sanitycheck.py",
    } in log_messages
    assert {"msg": "OK", "src": "python3_named_arguments.py"} not in log_messages
    assert result.exit_code == 0


def test_with_expr_in_path(caplog):
    caplog.set_level(logging.INFO)

    test_dir = Path(__file__).parent
    os.chdir((test_dir / "example_project").absolute())

    result = CliRunner().invoke(
        main, ["-f", "azdo/tasks/bash3/python-in-bash/with-expr-in-path.yml"]
    )
    log_messages = [
        {"msg": log.message, "src": log.pathname.split("/")[-1]}
        for log in caplog.records
    ]

    assert {
        "msg": "[{'path': '/Users/emilmyresten/Development/personal/python/azdoh/test/example_project/src/pkg/example_python.py', 'exists': True}]",
        "src": "python3_script_sanitycheck.py",
    } in log_messages
    assert {"msg": "OK", "src": "python3_named_arguments.py"} not in log_messages
    assert result.exit_code == 0


def test_without_working_directory(caplog):
    caplog.set_level(logging.INFO)

    test_dir = Path(__file__).parent
    os.chdir((test_dir / "example_project").absolute())

    result = CliRunner().invoke(
        main, ["-f", "azdo/tasks/bash3/python-in-bash/without-working-directory.yml"]
    )
    log_messages = [
        {"msg": log.message, "src": log.pathname.split("/")[-1]}
        for log in caplog.records
    ]

    assert {
        "msg": "[{'path': '/Users/emilmyresten/Development/personal/python/azdoh/test/example_project/src/pkg/example_python.py', 'exists': True}]",
        "src": "python3_script_sanitycheck.py",
    } in log_messages
    assert {"msg": "OK", "src": "python3_named_arguments.py"} not in log_messages
    assert result.exit_code == 0


def test_with_named_args(caplog):
    caplog.set_level(logging.INFO)

    test_dir = Path(__file__).parent
    os.chdir((test_dir / "example_project").absolute())

    result = CliRunner().invoke(
        main, ["-f", "azdo/tasks/bash3/python-in-bash/with-named-args.yml"]
    )
    log_messages = [
        {"msg": log.message, "src": log.pathname.split("/")[-1]}
        for log in caplog.records
    ]

    assert {
        "msg": "[{'path': '/Users/emilmyresten/Development/personal/python/azdoh/test/example_project/src/pkg/example_python.py', 'exists': True}]",
        "src": "python3_script_sanitycheck.py",
    } in log_messages
    assert {"msg": "OK", "src": "python3_named_arguments.py"} in log_messages
    assert result.exit_code == 0


def test_without_args(caplog):
    caplog.set_level(logging.INFO)

    test_dir = Path(__file__).parent
    os.chdir((test_dir / "example_project").absolute())

    result = CliRunner().invoke(
        main, ["-f", "azdo/tasks/bash3/python-in-bash/without-args.yml"]
    )
    log_messages = [
        {"msg": log.message, "src": log.pathname.split("/")[-1]}
        for log in caplog.records
    ]

    assert {
        "msg": "[{'path': '/Users/emilmyresten/Development/personal/python/azdoh/test/example_project/src/pkg/example_python.py', 'exists': True}]",
        "src": "python3_script_sanitycheck.py",
    } in log_messages
    assert {
        "msg": "No python script with args found",
        "src": "python3_named_arguments.py",
    } in log_messages
    assert result.exit_code == 0
