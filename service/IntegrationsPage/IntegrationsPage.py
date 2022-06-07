import logging

from pytest_zebrunner.zebrunner_logging import ZebrunnerHandler
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from service.IntegrationsPage.JiraPage import JiraPage
from service.IntegrationsPage.TestRailPage import TestRailPage
from service.ZebrunnerBasePage.ZebrunnerBasePage import ZebrunnerBasePage
from tests import configuration


class IntegrationsPageLocators:
    TESTRAIL_CARD = (By.XPATH, "//div[text()='TestRail']//ancestor::integration-card")
    JIRA_CARD = (By.XPATH, "//div[text()='Jira']//ancestor::integration-card")


class IntegrationsPage(ZebrunnerBasePage):
    logger = logging.getLogger(__name__)
    logger.addHandler(ZebrunnerHandler())

    def click_testrail_card(self):
        self.logger.info(
            "Started method 'click_testrail_card' in 'IntegrationsPage' class"
        )
        testrail_card: WebElement = self.get_present_element(
            IntegrationsPageLocators.TESTRAIL_CARD
        )
        self.scroll_to_the_center(testrail_card)
        testrail_card.click()
        self.logger.info("'testrail_card' was clicked")

        WebDriverWait(self, 10).until(
            expected_conditions.url_matches(TestRailPage(self).page_url_pattern())
        )
        self.logger.info(
            "Finished method 'click_testrail_card' in 'IntegrationsPage' class"
        )

    def click_jira_card(self):
        self.logger.info("Started method 'click_jira_card' in 'IntegrationsPage' class")
        jira_card: WebElement = self.get_present_element(
            IntegrationsPageLocators.JIRA_CARD
        )
        self.scroll_to_the_center(jira_card)
        jira_card.click()
        self.logger.info("'jira_card' was clicked")

        WebDriverWait(self, 10).until(
            expected_conditions.url_matches(JiraPage(self).page_url_pattern())
        )
        self.logger.info(
            "Finished method 'click_jira_card' in 'IntegrationsPage' class"
        )

    def page_url_pattern(self, project_key=None) -> str:
        self.logger.info(
            "Started method 'page_url_pattern' in 'IntegrationsPage' class"
        )
        if project_key is None:
            self.logger.info(
                "Project key was not specified, comparing with regex pattern"
            )
            pattern = (
                    configuration.get("base_url") + "projects/" + ".{3,6}/" + "integrations"
            )
            self.logger.info("Pattern: " + pattern)
            self.logger.info(
                "Finishing method 'page_url_pattern' in 'IntegrationsPage' class"
            )
            return pattern
        else:
            self.logger.info("Project key was specified as: " + project_key)
            pattern = (
                    configuration.get("base_url")
                    + "projects/"
                    + f"{project_key.upper()}"
                    + "/"
                    + "integrations"
            )
            self.logger.info("Url: " + pattern)
            self.logger.info(
                "Finishing method 'page_url_pattern' in 'IntegrationsPage' class"
            )
            return pattern
