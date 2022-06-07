import logging

from pytest_zebrunner.zebrunner_logging import ZebrunnerHandler
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from service.ZebrunnerBasePage.ZebrunnerBasePage import ZebrunnerBasePage
from tests import configuration


class JiraPageLocators:
    SERVER_DC_RADIO_BUTTON = (By.XPATH, "//md-radio-button[@value='SERVER_DC']")
    CLOUD_RADIO_BUTTON = (By.XPATH, "//md-radio-button[@value='CLOUD']")

    HOST_FIELD = (By.XPATH, "//input[@id='jiraIntegrationHost']")
    USERNAME_FIELD = (By.XPATH, "//input[@id='jiraIntegrationUsername']")
    TOKEN_FIELD = (By.XPATH, "//input[@id='jiraIntegrationToken']")

    SAVE_BUTTON = (By.XPATH, "//button[text()='Save']")
    CANCEL_BUTTON = (By.XPATH, "//button[text()='Cancel']")
    TEST_BUTTON = (By.XPATH, "//button[contains(@class, 'test-integration')]")

    ENABLE_INTEGRATION_BUTTON = (By.XPATH, "//button[@name='enableIntegration']")
    DELETE_INTEGRATION_BUTTON = (By.XPATH, "//button[@name='deleteIntegration']")

    FOOTER_MESSAGE_TEXT = (By.XPATH, "//div[contains(@class, 'footer-message-text')]")

    ENABLE_TCM_BUTTON = (By.XPATH, "//md-checkbox[@name='xRayCheckbox']")
    JIRA_PLUGIN_DROPDOWN = (By.XPATH, "//dropdown-with-icon")
    ZEPHYR_SQUAD_DROPDOWN_ITEM = (By.XPATH, "//span[text()='Zephyr Squad']/parent::button")
    XRAY_DROPDOWN_ITEM = (By.XPATH, "//span[text()='Xray']/parent::button")

    XRAY_HOST_FIELD = (By.XPATH, "//input[@id='integrationXrayHost']")
    XRAY_ID_FIELD = (By.XPATH, "//input[@id='integrationXrayClientId']")
    XRAY_SECRET_ID_FIELD = (By.XPATH, "//input[@id='integrationXrayClientSecret']")

    ZEPHYR_SQUAD_ACCOUNT_ID_FIELD = (
        By.XPATH,
        "//input[@id='zephyrSquadIntegrationAccountId']",
    )
    ZEPHYR_SQUAD_ACCESS_KEY_FIELD = (
        By.XPATH,
        "//input[@id='zephyrSquadIntegrationAccessKey']",
    )
    ZEPHYR_SQUAD_SECRET_KEY_FIELD = (
        By.XPATH,
        "//input[@id='zephyrSquadIntegrationSecretKey']",
    )


class JiraPage(ZebrunnerBasePage):
    logger = logging.getLogger(__name__)
    logger.addHandler(ZebrunnerHandler())

    def test_valid_creds(self, host, username, token):
        self.logger.info("Started method 'test_valid_creds' in 'JiraPage' class")

        self.click(JiraPageLocators.CLOUD_RADIO_BUTTON)
        self.logger.info("'CLOUD_RADIO_BUTTON' was clicked")

        host_field: WebElement = self.get_present_element(JiraPageLocators.HOST_FIELD)
        self.scroll_to_the_center(host_field)
        host_field.clear()
        host_field.send_keys(host)
        self.logger.info(f"'host' was sent to 'host_field'")

        username_field: WebElement = self.get_present_element(
            JiraPageLocators.USERNAME_FIELD
        )
        self.scroll_to_the_center(username_field)
        username_field.clear()
        username_field.send_keys(username)
        self.logger.info(f"'username' was sent to 'username_field'")

        token_field: WebElement = self.get_present_element(JiraPageLocators.TOKEN_FIELD)
        self.scroll_to_the_center(token_field)
        token_field.clear()
        token_field.send_keys(token)
        self.logger.info(f"'token' was sent to 'token_field'")

        test_button: WebElement = self.get_present_element(JiraPageLocators.TEST_BUTTON)
        self.scroll_to_the_center(test_button)
        test_button.click()
        self.logger.info("'test_button' was clicked")

        self.logger.info(
            "Waiting for 'text_to_be_present_in_element' of 'FOOTER_MESSAGE_TEXT'"
        )
        result = WebDriverWait(self, 10).until(
            expected_conditions.text_to_be_present_in_element(
                JiraPageLocators.FOOTER_MESSAGE_TEXT, "Integration is connected."
            )
        )

        self.logger.info("Finishing method 'test_valid_creds' in 'JiraPage' class")
        return result

    def click_save(self):
        self.logger.info("Started method 'click_save' in 'JiraPage' class")
        self.click(JiraPageLocators.SAVE_BUTTON)
        self.logger.info("'SAVE_BUTTON' was clicked")
        self.logger.info("Finished method 'click_save' in 'JiraPage' class")

    def test_valid_creds_xray(self, xray_host, xray_id, xray_secret_id):
        self.logger.info("Started method 'test_valid_creds_xray' in 'JiraPage' class")

        tcm_button: WebElement = self.get_present_element(
            JiraPageLocators.ENABLE_TCM_BUTTON
        )
        if tcm_button.get_attribute("aria-checked") == "false":
            tcm_button.click()
            self.logger.info("'tcm_button' was clicked")

        current_plugin: WebElement = self.get_present_element(
            JiraPageLocators.JIRA_PLUGIN_DROPDOWN
        )
        self.scroll_to_the_center(current_plugin)

        if current_plugin.text.find("Xray") == -1:
            self.logger.info("'Xray' is not current plugin.")
            self.click(JiraPageLocators.JIRA_PLUGIN_DROPDOWN)
            self.logger.info("'JIRA_PLUGIN_DROPDOWN' was clicked")
            self.click(JiraPageLocators.XRAY_DROPDOWN_ITEM)
            self.logger.info("'XRAY_DROPDOWN_ITEM' was clicked")

        xray_host_field: WebElement = self.get_present_element(
            JiraPageLocators.XRAY_HOST_FIELD
        )
        self.scroll_to_the_center(xray_host_field)
        xray_host_field.clear()
        xray_host_field.send_keys(xray_host)
        self.logger.info(f"'{xray_host}' was sent to 'xray_host_field'")

        xray_id_field: WebElement = self.get_present_element(
            JiraPageLocators.XRAY_ID_FIELD
        )
        self.scroll_to_the_center(xray_id_field)
        xray_id_field.clear()
        xray_id_field.send_keys(xray_id)
        self.logger.info(f"'xray_id' was sent to 'xray_id_field'")

        xray_secret_id_field: WebElement = self.get_present_element(
            JiraPageLocators.XRAY_SECRET_ID_FIELD
        )
        self.scroll_to_the_center(xray_secret_id_field)
        xray_secret_id_field.clear()
        xray_secret_id_field.send_keys(xray_secret_id)
        self.logger.info(f"'xray_secret_id' was sent to 'xray_secret_id_field'")

        test_button: WebElement = self.get_present_element(JiraPageLocators.TEST_BUTTON)
        self.scroll_to_the_center(test_button)
        test_button.click()
        self.logger.info("'test_button' was clicked")

        self.logger.info(
            "Waiting for 'text_to_be_present_in_element' of 'FOOTER_MESSAGE_TEXT'"
        )
        result = WebDriverWait(self, 10).until(
            expected_conditions.text_to_be_present_in_element(
                JiraPageLocators.FOOTER_MESSAGE_TEXT, "Integration is connected."
            )
        )

        self.logger.info("Finishing method 'test_valid_creds_xray' in 'JiraPage' class")
        return result

    def test_valid_creds_zephyr_squad(
            self, zephyr_squad_account_id, zephyr_squad_access_key, zephyr_squad_secret_key
    ):
        self.logger.info(
            "Started method 'test_valid_creds_zephyr_squad' in 'JiraPage' class"
        )

        tcm_button: WebElement = self.get_present_element(
            JiraPageLocators.ENABLE_TCM_BUTTON
        )
        if tcm_button.get_attribute("aria-checked") == "false":
            self.logger.info("'tcm_button' is not checked")
            tcm_button.click()
            self.logger.info("'tcm_button' was clicked")

        current_plugin: WebElement = self.get_present_element(
            JiraPageLocators.JIRA_PLUGIN_DROPDOWN
        )
        self.scroll_to_the_center(current_plugin)

        if current_plugin.text.find("Zephyr Squad") == -1:
            self.logger.info("'Zephyr Squad' is not current plugin.")
            self.click(JiraPageLocators.JIRA_PLUGIN_DROPDOWN)
            self.logger.info("'JIRA_PLUGIN_DROPDOWN' was clicked")
            self.click(JiraPageLocators.ZEPHYR_SQUAD_DROPDOWN_ITEM)
            self.logger.info("'ZEPHYR_SQUAD_DROPDOWN_ITEM' was clicked")

        zephyr_squad_account_id_field: WebElement = self.get_present_element(
            JiraPageLocators.ZEPHYR_SQUAD_ACCOUNT_ID_FIELD
        )
        self.scroll_to_the_center(zephyr_squad_account_id_field)
        zephyr_squad_account_id_field.clear()
        zephyr_squad_account_id_field.send_keys(zephyr_squad_account_id)
        self.logger.info(
            f"'{zephyr_squad_account_id}' was sent to 'zephyr_squad_account_id_field'"
        )

        zephyr_squad_access_key_field: WebElement = self.get_present_element(
            JiraPageLocators.ZEPHYR_SQUAD_ACCESS_KEY_FIELD
        )
        self.scroll_to_the_center(zephyr_squad_access_key_field)
        zephyr_squad_access_key_field.clear()
        zephyr_squad_access_key_field.send_keys(zephyr_squad_access_key)
        self.logger.info(
            f"'zephyr_squad_access_key' was sent to 'zephyr_squad_access_key_field'"
        )

        zephyr_squad_secret_key_field: WebElement = self.get_present_element(
            JiraPageLocators.ZEPHYR_SQUAD_SECRET_KEY_FIELD
        )
        self.scroll_to_the_center(zephyr_squad_secret_key_field)
        zephyr_squad_secret_key_field.clear()
        zephyr_squad_secret_key_field.send_keys(zephyr_squad_secret_key)
        self.logger.info(
            f"'zephyr_squad_secret_key' was sent to 'zephyr_squad_secret_key_field'"
        )

        test_button: WebElement = self.get_present_element(JiraPageLocators.TEST_BUTTON)
        self.scroll_to_the_center(test_button)
        test_button.click()
        self.logger.info("'test_button' was clicked")

        self.logger.info(
            "Waiting for 'text_to_be_present_in_element' of 'FOOTER_MESSAGE_TEXT'"
        )
        result = WebDriverWait(self, 10).until(
            expected_conditions.text_to_be_present_in_element(
                JiraPageLocators.FOOTER_MESSAGE_TEXT, "Integration is connected."
            )
        )

        self.logger.info(
            "Finishing method 'test_valid_creds_zephyr_squad' in 'JiraPage' class"
        )
        return result

    def page_url_pattern(self, project_key=None) -> str:
        self.logger.info("Started method 'page_url_pattern' in 'JiraPage' class")
        if project_key is None:
            self.logger.info(
                "Project key was not specified, comparing with regex pattern"
            )
            url = (
                    configuration.get("base_url")
                    + "projects/"
                    + ".{3,6}/"
                    + "integrations/jira"
            )
            self.logger.info("Pattern: " + url)
            self.logger.info("Finishing method 'page_url_pattern' in 'JiraPage' class")
            return url
        else:
            self.logger.info("Project key was specified as: " + project_key)
            url = (
                    configuration.get("base_url")
                    + "projects/"
                    + f"{project_key.upper()}"
                    + "/"
                    + "integrations/jira"
            )
            self.logger.info("Url: " + url)
            self.logger.info("Finishing method 'page_url_pattern' in 'JiraPage' class")
            return url
