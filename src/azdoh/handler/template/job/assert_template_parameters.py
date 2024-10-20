import logging
from pathlib import Path

from azdoh.common.text import log_job_start


def assert_on_keys(actual_parameters: dict, formal_parameters: list[dict]):
    actual_keys = set(actual_parameters.keys())
    formal_keys = set([parameter["name"] for parameter in formal_parameters])
    disjunction = actual_keys.symmetric_difference(formal_keys)
    default_value_fallbacks = [
        formal_parameter
        for formal_parameter in formal_parameters
        if formal_parameter["name"] in disjunction
        and formal_parameter.get("default") is not None
    ]
    missing_parameters = [
        parameter
        for parameter in formal_parameters
        if parameter.get("name") in disjunction and parameter.get("default") is None
    ]
    redundant_parameters = [
        parameter for parameter in actual_keys if parameter not in formal_keys
    ]

    if len(missing_parameters) != 0:
        logging.error(f"Missing required arguments: {missing_parameters}")
    if len(redundant_parameters) != 0:
        logging.warning(f"Redundant arguments: {redundant_parameters}")
    if len(default_value_fallbacks) != 0:
        logging.info(f"Default value fallbacks: {default_value_fallbacks}")
    if (
        len(missing_parameters) == 0
        and len(redundant_parameters) == 0
        and len(default_value_fallbacks) == 0
    ):
        logging.info("OK")


def assert_template_parameters(yml: dict, template_yaml: dict):
    log_job_start("Asserting parameters")

    logging.debug(
        f"TEMPLATE/ASSERT_PARAMETERS | assert_parameters | Got arguments: [yml={yml}, template_yaml={template_yaml}]"
    )

    actual_parameters = yml.get("parameters")
    formal_parameters = template_yaml.get("parameters")
    assert_on_keys(actual_parameters, formal_parameters)
