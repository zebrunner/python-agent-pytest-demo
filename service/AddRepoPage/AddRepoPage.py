import logging

from pytest_zebrunner.zebrunner_logging import ZebrunnerHandler
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from service.LaunchersPage.LaunchersPage import LaunchersPage
from service.ZebrunnerBasePage.ZebrunnerBasePage import ZebrunnerBasePage
from tests import configuration


class AddRepoPageLocators:
    SELECT_GITHUB_BUTTON = (By.XPATH, "//span[normalize-space(text()) = 'Github']/parent::button")
    URL_INPUT_FIELD = (By.XPATH, "//input[@name='addRepoUrl']")
    ADD_REPO_BUTTON = (By.XPATH, "//button[contains(@class, 'add-repo-form')]")


class AddRepoPage(ZebrunnerBasePage):
    logger = logging.getLogger(__name__)
    logger.addHandler(ZebrunnerHandler())

    def add_repo(self, url):
        self.logger.info("Started method 'add_repo' in 'AddRepoPage' class")

        self.enter_text(AddRepoPageLocators.URL_INPUT_FIELD, url)
        self.logger.info(f"'{url}' was sent to 'URL_INPUT_FIELD'")

        add_button: WebElement = self.get_present_element(
            AddRepoPageLocators.ADD_REPO_BUTTON
        )

        self.scroll_to_the_center(add_button)

        self.logger.info("Waiting for 'element_to_be_clickable' of 'ADD_REPO_BUTTON'")
        WebDriverWait(self, 10).until(
            expected_conditions.element_to_be_clickable(
                AddRepoPageLocators.ADD_REPO_BUTTON
            )
        )
        add_button.click()
        self.logger.info("'ADD_REPO_BUTTON' was clicked")

        WebDriverWait(self, 10).until(
            expected_conditions.url_matches(LaunchersPage(self).page_url_pattern())
        )

        self.logger.info("Finishing method 'add_repo' in 'AddRepoPage' class")
        return LaunchersPage(self.driver)

    def page_url_pattern(self, project_key=None) -> str:
        self.logger.info("Started method 'page_url_pattern' in 'AddRepoPage' class")
        if project_key is None:
            self.logger.info(
                "Project key was not specified, comparing with regex pattern"
            )
            pattern = (
                    configuration.get("base_url") + ".{3,6}/launchers/add-repo?provider=.+"
            )
            self.logger.info("Pattern: " + pattern)
            self.logger.info(
                "Finishing method 'page_url_pattern' in 'AddRepoPage' class"
            )
            return pattern
        else:
            self.logger.info("Project key was specified as: " + project_key)
            pattern = (
                    configuration.get("base_url")
                    + f"{project_key.upper()}"
                    + "/"
                    + "launchers/add-repo?provider=.+"
            )
            self.logger.info("Url: " + pattern)
            self.logger.info(
                "Finishing method 'page_url_pattern' in 'AddRepoPage' class"
            )
            return pattern
