import json
import logging
from datetime import datetime
from time import strftime

import requests
from pytest_zebrunner.zebrunner_logging import ZebrunnerHandler

from tests import configuration

logger = logging.getLogger(__name__)
logger.addHandler(ZebrunnerHandler())


def create_test_run_with_integrations(project_key, test_rail_label, xray_label, zephyr_squad_label):

    logger.info("Started method 'create_test_run_with_integrations'")

    test_run_name = "PyTest API run"
    logger.info(f"'test_run_name' is '{test_run_name}'")
    logger.info(
        f"'test_rail_label': '{test_rail_label}', "
        f"'xray_label': '{xray_label}', "
        f"'zephyr_squad_label': '{zephyr_squad_label}'"
    )

    # Authorization
    response_token = requests.post(
        url=configuration.get("base_url") + "api/iam/v1/auth/login",
        json={
            "username": configuration.get("username"),
            "password": configuration.get("password"),
        },
    )
    logger.info(f"'response_token' answered with status '{response_token.status_code}'")
    response_token_dict: dict = json.loads(response_token.text)
    token = response_token_dict.get("authToken")
    header = {"Authorization": "Bearer " + token}

    # Formatted current time (2022-05-11T11:49:18.331+03:00)
    formatted_time = (
        lambda: datetime.now().isoformat()[:-3]
                + strftime("%z")[:3]
                + ":"
                + strftime("%z")[3:5]
    )
    logger.info(f"'formatted_time' is '{formatted_time()}")

    # Check test run
    url_check_test_run = configuration.get("base_url") + "api/projects/v1/projects"
    response_projects = requests.get(url=url_check_test_run, headers=header)
    logger.info(
        f"'response_projects' answered with status '{response_projects.status_code}'"
    )
    response_projects_dict: dict = json.loads(response_projects.text)

    project_id = ""
    for project in response_projects_dict.get("items"):
        if project.get("key") == project_key:
            project_id = str(project.get("id"))
            break
    logger.info(f"'project_id' is '{project_id}'")

    response_projects_test_runs = requests.get(
        url=configuration.get("base_url")
            + f"api/reporting/api/project-test-runs/search?page=1&pageSize=20&projectId={project_id}",
        headers=header,
    )
    logger.info(
        f"'response_projects_test_runs' answered with status '{response_projects_test_runs.status_code}'"
    )

    if response_projects_test_runs.text.find(f'"name":"{test_run_name}"') != -1:
        logger.info("Found project with same 'test_run_name'")
        logger.info("Finishing method 'create_test_run_with_integrations'")
        return

    # Create test run
    url_create_test_run = (
            configuration.get("base_url")
            + f"api/reporting/v1/test-runs?projectKey={project_key.upper()}"
    )

    json_create_test_run = {
        "name": f"{test_run_name}",
        "startedAt": f"{formatted_time()}",
        "framework": "PyTest",
    }

    response_create_test_run = requests.post(
        url_create_test_run, headers=header, json=json_create_test_run
    )
    logger.info(
        f"'response_create_test_run' answered with status '{response_create_test_run.status_code}'"
    )

    # Get test run id from response
    response_dict: dict = json.loads(response_create_test_run.text)
    test_run_id = response_dict.get("id")
    logger.info(f"'test_run_id' is '{test_run_id}'")

    # Create test
    url_create_test = (
            configuration.get("base_url")
            + f"/api/reporting/v1/test-runs/{test_run_id}/tests"
    )

    json_create_test = {
        "name": "Test",
        "className": "com.test.ClassName",
        "methodName": "methodName",
        "startedAt": f"{formatted_time()}",
        "labels": [
            {
                "key": "com.zebrunner.app/tcm.testrail.case-id",
                "value": f"{test_rail_label}",
            },
            {"key": "com.zebrunner.app/tcm.xray.test-key", "value": f"{xray_label}"},
            {
                "key": "com.zebrunner.app/tcm.zephyr.test-case-key",
                "value": f"{zephyr_squad_label}",
            },
        ],
    }

    response_create_test = requests.post(
        url_create_test, headers=header, json=json_create_test
    )
    logger.info(
        f"'response_create_test' answered with status '{response_create_test.status_code}'"
    )

    # Get test id from response
    response_test: dict = json.loads(response_create_test.text)
    test_id = response_test.get("id")
    logger.info(f"'test_id' is '{test_id}'")

    # Finish test
    url_finish_test = url_create_test + f"/{test_id}"

    json_finish_test = {"result": "PASSED", "endedAt": f"{formatted_time()}"}

    response_finish_test = requests.put(
        url_finish_test, headers=header, json=json_finish_test
    )
    logger.info(
        f"'response_finish_test' answered with status '{response_finish_test.status_code}'"
    )

    # Finish test run
    url_finish_test_run = (
            configuration.get("base_url") + f"/api/reporting/v1/test-runs/{test_run_id}"
    )

    json_finish_test_run = {"endedAt": f"{formatted_time()}"}

    response_finish_test_run = requests.put(
        url_finish_test_run, headers=header, json=json_finish_test_run
    )
    logger.info(
        f"'response_finish_test_run' answered with status '{response_finish_test_run.status_code}'"
    )

    logger.info("Finished method 'create_test_run_with_integrations'")
