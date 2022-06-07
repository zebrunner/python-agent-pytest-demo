import logging
import random
import string

from pytest_zebrunner.zebrunner_logging import ZebrunnerHandler
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from service.DashboardsPage.NewDasboardModal import NewDashboardModalLocators
from service.ZebrunnerBasePage.ZebrunnerBasePage import ZebrunnerBasePage
from tests import configuration


class DashboardsPageLocators:
    ADD_DASHBOARD_BUTTON = (By.XPATH, "//button[contains(@class, 'dashboard-button')]")


class DashboardsPage(ZebrunnerBasePage):
    logger = logging.getLogger(__name__)
    logger.addHandler(ZebrunnerHandler())

    def create_dashboard(self):
        self.logger.info("Started method 'create_dashboard' in 'DashboardsPage' class")

        self.click(DashboardsPageLocators.ADD_DASHBOARD_BUTTON)
        self.logger.info("'ADD_DASHBOARD_BUTTON' was clicked")

        name = "".join(random.choices(string.ascii_letters + string.digits, k=6))
        self.logger.info(f"Generated dashboard name: '{name}'")

        self.logger.info(
            "Waiting for 'visibility_of_element_located' of 'NEW_DASHBOARD_MODAL_WINDOW'"
        )
        WebDriverWait(self, 5).until(
            expected_conditions.visibility_of_element_located(
                NewDashboardModalLocators.NEW_DASHBOARD_MODAL_WINDOW
            )
        )
        self.logger.info("Waiting for 'visibility_of_element_located' of 'NAME_FIELD'")
        WebDriverWait(self, 5).until(
            expected_conditions.visibility_of_element_located(
                NewDashboardModalLocators.NAME_FIELD
            )
        )

        self.click(NewDashboardModalLocators.NAME_FIELD)
        self.logger.info("'NAME_FIELD' was clicked")
        self.enter_text(NewDashboardModalLocators.NAME_FIELD, name)
        self.logger.info(f"'{name}' was sent to 'NAME_FIELD'")
        self.click(NewDashboardModalLocators.SUBMIT_BUTTON)
        self.logger.info("'SUBMIT_BUTTON' was clicked")
        self.logger.info(
            "Waiting for 'invisibility_of_element_located' of 'NEW_DASHBOARD_MODAL_WINDOW'"
        )
        WebDriverWait(self, 5).until(
            expected_conditions.invisibility_of_element_located(
                NewDashboardModalLocators.NEW_DASHBOARD_MODAL_WINDOW
            )
        )
        self.logger.info("Finished method 'create_dashboard' in 'DashboardsPage' class")

    def page_url_pattern(self, project_key=None) -> str:
        self.logger.info("Started method 'page_url_pattern' in 'DashboardsPage' class")
        if project_key is None:
            self.logger.info(
                "Project key was not specified, comparing with regex pattern"
            )
            pattern = (
                    configuration.get("base_url") + "projects/" + ".{3,6}/" + "dashboards"
            )
            self.logger.info("Pattern: " + pattern)
            self.logger.info(
                "Finishing method 'page_url_pattern' in 'DashboardsPage' class"
            )
            return pattern
        else:
            self.logger.info("Project key was specified as: " + project_key)
            pattern = (
                    configuration.get("base_url")
                    + "projects/"
                    + f"{project_key.upper()}"
                    + "/"
                    + "dashboards"
            )
            self.logger.info("Url: " + pattern)
            self.logger.info(
                "Finishing method 'page_url_pattern' in 'DashboardsPage' class"
            )
            return pattern
