import logging

from pytest_zebrunner.zebrunner_logging import ZebrunnerHandler
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from service.DashboardsPage.DashboardsPage import DashboardsPage
from service.IntegrationsPage.IntegrationsPage import IntegrationsPage
from service.MilestonesPage.MilestonesPage import MilestonesPage
from service.ZebrunnerBasePage.ZebrunnerBasePage import ZebrunnerBasePage


class LeftSideMenuLocators:
    SIDE_MENU_LOCATOR = (By.XPATH, "//aside")

    MILESTONES_BUTTON = (By.XPATH, "//li[contains(@class, 'milestones')]")
    DASHBOARDS_BUTTON = (By.XPATH, "//li[contains(@class, 'dashboards')]")
    INTEGRATIONS_BUTTON = (By.XPATH, "//li[contains(@class, 'integrations')]")


class LeftSideMenu(ZebrunnerBasePage):
    logger = logging.getLogger(__name__)
    logger.addHandler(ZebrunnerHandler())

    def click_milestones_button(self):
        self.logger.info(
            "Started method 'click_milestones_button' in 'LeftSideMenu' class"
        )
        self.click(LeftSideMenuLocators.MILESTONES_BUTTON)
        self.logger.info("'MILESTONES_BUTTON' was clicked")

        WebDriverWait(self, 5).until(
            expected_conditions.url_matches(MilestonesPage(self).page_url_pattern())
        )
        self.logger.info(
            "Finishing method 'click_milestones_button' in 'LeftSideMenu' class"
        )
        return MilestonesPage(self)

    def click_dashboards_button(self):
        self.logger.info(
            "Started method 'click_dashboards_button' in 'LeftSideMenu' class"
        )

        self.click(LeftSideMenuLocators.DASHBOARDS_BUTTON)
        self.logger.info("'DASHBOARDS_BUTTON' was clicked")

        WebDriverWait(self, 5).until(
            expected_conditions.url_matches(DashboardsPage(self).page_url_pattern())
        )
        self.logger.info(
            "Finishing method 'click_dashboards_button' in 'LeftSideMenu' class"
        )
        return DashboardsPage(self)

    def click_integrations_button(self):
        self.logger.info(
            "Started method 'click_integrations_button' in 'LeftSideMenu' class"
        )
        self.click(LeftSideMenuLocators.INTEGRATIONS_BUTTON)
        self.logger.info("'INTEGRATIONS_BUTTON' was clicked")

        WebDriverWait(self, 5).until(
            expected_conditions.url_matches(IntegrationsPage(self).page_url_pattern())
        )
        self.logger.info(
            "Finishing method 'click_integrations_button' in 'LeftSideMenu' class"
        )
        return IntegrationsPage(self)

    def page_url_pattern(self, project_key=None) -> str:
        pass
