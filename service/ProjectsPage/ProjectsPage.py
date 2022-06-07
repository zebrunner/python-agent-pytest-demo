import logging
import time

from pytest_zebrunner.zebrunner_logging import ZebrunnerHandler
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from service.PageElements.ModalWindowBase import ModalWindowBaseLocators
from service.ZebrunnerBasePage.ZebrunnerBasePage import ZebrunnerBasePage
from tests import configuration


class ProjectsPageLocators:
    # Projects block
    ALL_PROJECTS = (By.XPATH, "//div[contains(@class, 'projects-table ng-scope')]")
    PROJECT_ITEM = (By.XPATH, ".//div[contains(@class, 'row ng-scope')]")

    # Project item
    PROJECT_NAME = (By.XPATH, ".//a[@name]")
    EDIT_PROJECT_BUTTON = (By.XPATH, ".//md-icon[@aria-label='edit']")


class ProjectsPage(ZebrunnerBasePage):
    logger = logging.getLogger(__name__)
    logger.addHandler(ZebrunnerHandler())

    def clear_projects(self):
        self.logger.info("Started method 'clear_projects' in 'ProjectsPage' class")
        projects_block: WebElement = self.get_present_element(
            ProjectsPageLocators.ALL_PROJECTS
        )
        projects_list: list = projects_block.find_elements(
            ProjectsPageLocators.PROJECT_ITEM[0], ProjectsPageLocators.PROJECT_ITEM[1]
        )

        while len(projects_list) != 1:
            self.logger.info(f"Length of projects list: {len(projects_list)}")
            for project in projects_list:
                project: WebElement

                if (
                        project.find_element(
                            ProjectsPageLocators.PROJECT_NAME[0],
                            ProjectsPageLocators.PROJECT_NAME[1],
                        ).text
                        != "Default"
                ):
                    self.logger.info("PROJECT_NAME != 'Default'")
                    edit_button: WebElement = project.find_element(
                        ProjectsPageLocators.EDIT_PROJECT_BUTTON[0],
                        ProjectsPageLocators.EDIT_PROJECT_BUTTON[1],
                    )

                    edit_button.click()
                    self.logger.info("'edit_button' was clicked")

                    self.click(ModalWindowBaseLocators.DELETE_BUTTON)
                    self.logger.info("'DELETE_BUTTON' was clicked")
                    self.click(ModalWindowBaseLocators.DELETE_BUTTON)
                    self.logger.info("'DELETE_BUTTON' was clicked")
                    self.wait_for_progress_bar_disappear()
                    time.sleep(1)
                    projects_list = projects_block.find_elements(
                        ProjectsPageLocators.PROJECT_ITEM[0],
                        ProjectsPageLocators.PROJECT_ITEM[1],
                    )
                    break

        self.logger.info("Finished method 'clear_projects' in 'ProjectsPage' class")

    def page_url_pattern(self, project_key=None) -> str:
        self.logger.info("Started method 'page_url_pattern' in 'ProjectsPage' class")
        if project_key is None:
            self.logger.info(
                "Project key was not specified, comparing with regex pattern"
            )
            pattern = configuration.get("base_url") + "projects"
            self.logger.info("Pattern: " + pattern)
            self.logger.info(
                "Finishing method 'page_url_pattern' in 'ProjectsPage' class"
            )
            return pattern
        else:
            self.logger.info("Project key was specified as: " + project_key)
            pattern = configuration.get("base_url") + "projects"
            self.logger.info("Url: " + pattern)
            self.logger.info(
                "Finishing method 'page_url_pattern' in 'ProjectsPage' class"
            )
            return pattern
