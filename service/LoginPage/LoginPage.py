import logging

from pytest_zebrunner.zebrunner_logging import ZebrunnerHandler
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from service.TestRunsPage.TestRunsPage import TestRunsPage
from service.ZebrunnerBasePage.ZebrunnerBasePage import ZebrunnerBasePage
from tests import configuration


class LoginPageLocators:
    USER_LOGIN = (By.XPATH, "//input[@id='username']")
    USER_PASSWORD = (By.XPATH, "//input[@id='password']")
    LOGIN_BUTTON = (By.XPATH, "//button[@id='signin']")


class LoginPage(ZebrunnerBasePage):
    logger = logging.getLogger(__name__)
    logger.addHandler(ZebrunnerHandler())

    def login_with_valid_creds(self, login, password) -> TestRunsPage:
        self.logger.info("Started method 'login_with_valid_creds' in 'LoginPage' class")

        self.enter_text(LoginPageLocators.USER_LOGIN, login)
        self.logger.info(f"Login: '{login}' was sent")

        self.enter_text(LoginPageLocators.USER_PASSWORD, password)
        self.logger.info("USER_PASSWORD was sent")

        self.click(LoginPageLocators.LOGIN_BUTTON)
        self.logger.info("LOGIN_BUTTON was clicked")

        WebDriverWait(self.driver, 10).until(
            expected_conditions.url_matches(
                TestRunsPage(self.driver).page_url_pattern()
            )
        )
        self.logger.info("URL is: " + self.driver.current_url)

        self.logger.info(
            "Finishing method 'login_with_valid_creds' in 'LoginPage' class"
        )
        return TestRunsPage(self.driver)

    def page_url_pattern(self, project_key=None) -> str:
        return configuration.get("base_url") + "/signin"
