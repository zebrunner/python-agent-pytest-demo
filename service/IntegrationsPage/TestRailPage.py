import logging

from pytest_zebrunner.zebrunner_logging import ZebrunnerHandler
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from service.ZebrunnerBasePage.ZebrunnerBasePage import ZebrunnerBasePage
from tests import configuration


class TestRailPageLocators:
    URL_FIELD = (By.XPATH, "//input[@id='integrationHubUrl']")
    USERNAME_FIELD = (By.XPATH, "//input[@id='integrationUsername']")
    PASSWORD_FIELD = (By.XPATH, "//input[@id='integrationAccessKey']")

    SAVE_BUTTON = (By.XPATH, "//button[text()='Save']")
    CANCEL_BUTTON = (By.XPATH, "//button[text()='Cancel']")
    TEST_BUTTON = (By.XPATH, "//button[contains(@class, 'test-integration')]")

    ENABLE_INTEGRATION_BUTTON = (By.XPATH, "//button[@name='enableIntegration']")
    DELETE_INTEGRATION_BUTTON = (By.XPATH, "//button[@name='deleteIntegration']")

    FOOTER_MESSAGE_TEXT = (By.XPATH, "//div[contains(@class, 'footer-message-text')]")


class TestRailPage(ZebrunnerBasePage):
    logger = logging.getLogger(__name__)
    logger.addHandler(ZebrunnerHandler())

    def test_valid_creds(self, url, username, password):
        self.logger.info("Started method 'test_valid_creds' in 'TestRailPage' class")

        url_field: WebElement = self.get_present_element(TestRailPageLocators.URL_FIELD)
        self.scroll_to_the_center(url_field)
        url_field.clear()
        url_field.send_keys(url)
        self.logger.info(f"'url' was sent to 'url_field'")

        username_field: WebElement = self.get_present_element(
            TestRailPageLocators.USERNAME_FIELD
        )
        self.scroll_to_the_center(username_field)
        username_field.clear()
        username_field.send_keys(username)
        self.logger.info(f"'username' was sent to 'username_field'")

        password_field: WebElement = self.get_present_element(
            TestRailPageLocators.PASSWORD_FIELD
        )
        self.scroll_to_the_center(password_field)
        password_field.clear()
        password_field.send_keys(password)
        self.logger.info(f"'password' was sent to 'password_field'")

        self.click(TestRailPageLocators.TEST_BUTTON)
        self.logger.info("'TEST_BUTTON' was clicked")

        self.logger.info(
            "Waiting for 'text_to_be_present_in_element' of 'FOOTER_MESSAGE_TEXT'"
        )
        result = WebDriverWait(self, 10).until(
            expected_conditions.text_to_be_present_in_element(
                TestRailPageLocators.FOOTER_MESSAGE_TEXT, "Integration is connected."
            )
        )

        self.logger.info("Finishing method 'test_valid_creds' in 'TestRailPage' class")
        return result

    def click_save(self):
        self.logger.info("Started method 'click_save' in 'TestRailPage' class")
        self.click(TestRailPageLocators.SAVE_BUTTON)
        self.logger.info("'SAVE_BUTTON' was clicked")
        self.logger.info("Finished method 'click_save' in 'TestRailPage' class")

    def page_url_pattern(self, project_key=None) -> str:
        self.logger.info("Started method 'page_url_pattern' in 'TestRailPage' class")
        if project_key is None:
            self.logger.info(
                "Project key was not specified, comparing with regex pattern"
            )
            url = (
                    configuration.get("base_url")
                    + "projects/"
                    + ".{3,6}/"
                    + "integrations/testrail"
            )
            self.logger.info("Pattern: " + url)
            self.logger.info(
                "Finishing method 'page_url_pattern' in 'TestRailPage' class"
            )
            return url
        else:
            self.logger.info("Project key was specified as: " + project_key)
            url = (
                    configuration.get("base_url")
                    + "projects/"
                    + f"{project_key.upper()}"
                    + "/"
                    + "integrations/testrail"
            )
            self.logger.info("Url: " + url)
            self.logger.info(
                "Finishing method 'page_url_pattern' in 'TestRailPage' class"
            )
            return url
