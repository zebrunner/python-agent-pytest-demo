import logging
import os

from pytest_zebrunner.zebrunner_logging import ZebrunnerHandler


def get(config_name):
    logger = logging.getLogger("configuration")
    logger.addHandler(ZebrunnerHandler())

    config_dict = {
        "base_url": os.getenv("TENANT_URL"),
        "username": os.getenv("CREDENTIALS_TENANT_USERNAME"),
        "password": os.getenv("CREDENTIALS_TENANT_PASSWORD"),
        "hub_url": os.getenv("ZEBRUNNER_HUB_URL"),
        "browserName": "chrome",
        "browserVersion": "latest",
        "platform": "linux",
        "platformName": "linux",
        "testrail_url": os.getenv("CREDENTIALS_TESTRAIL_URL"),
        "testrail_username": os.getenv("CREDENTIALS_TESTRAIL_USERNAME"),
        "testrail_password": os.getenv("CREDENTIALS_TESTRAIL_PASSWORD"),
        "jira_host": os.getenv("CREDENTIALS_JIRA_HOST"),
        "jira_username": os.getenv("CREDENTIALS_JIRA_USERNAME"),
        "jira_token": os.getenv("CREDENTIALS_JIRA_TOKEN"),
        "xray_host": os.getenv("CREDENTIALS_XRAY_HOST"),
        "xray_id": os.getenv("CREDENTIALS_XRAY_ID"),
        "xray_secret_id": os.getenv("CREDENTIALS_XRAY_SECRET_ID"),
        "zephyr_squad_account_id": os.getenv("CREDENTIALS_ZEPHYR_SQUAD_ACCOUNT_ID"),
        "zephyr_squad_access_key": os.getenv("CREDENTIALS_ZEPHYR_SQUAD_ACCESS_KEY"),
        "zephyr_squad_secret_key": os.getenv("CREDENTIALS_ZEPHYR_SQUAD_SECRET_KEY"),
    }

    value = config_dict.get(config_name)
    if value is None:
        logger.exception(f"'{config_name}'" + " configuration variable is None")
        raise ValueError(f"'{config_name}'" + " configuration variable is None")
    else:
        return value
