import logging

from pytest_zebrunner.zebrunner_logging import ZebrunnerHandler
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from service.PageElements.ModalWindowBase import ModalWindowBaseLocators
from service.ProjectsPage.ProjectsPage import ProjectsPage
from service.ZebrunnerBasePage.ZebrunnerBasePage import ZebrunnerBasePage


class TopHeaderLocators:
    PROJECTS_BUTTON = (By.XPATH, "//md-select[contains(@class, 'project-settings')]")
    CREATE_PROJECT_NESTED_BUTTON = (
        By.XPATH,
        ".//div[contains(@class, 'gtm-project-button')]",
    )
    VIEW_ALL_PROJECTS_NESTED_BUTTON = (
        By.XPATH,
        ".//div[@class='project-settings__button']",
    )


class TopHeader(ZebrunnerBasePage):
    logger = logging.getLogger(__name__)
    logger.addHandler(ZebrunnerHandler())

    def select_create_project(self):
        self.logger.info("Started method 'select_create_project' in 'TopHeader' class")
        self.click(TopHeaderLocators.PROJECTS_BUTTON)
        self.logger.info("'PROJECTS_BUTTON' was clicked")
        self.click(TopHeaderLocators.CREATE_PROJECT_NESTED_BUTTON)
        self.logger.info("'CREATE_PROJECT_NESTED_BUTTON' was clicked")

        self.logger.info(
            "Waiting for 'visibility_of_element_located' of 'MODAL_WINDOW_LOCATOR'"
        )
        WebDriverWait(self, 5).until(
            expected_conditions.visibility_of_element_located(
                ModalWindowBaseLocators.MODAL_WINDOW_LOCATOR
            )
        )
        self.logger.info("Finished method 'select_create_project' in 'TopHeader' class")

    def select_view_all_projects(self):
        self.logger.info(
            "Started method 'select_view_all_projects' in 'TopHeader' class"
        )

        self.click(TopHeaderLocators.PROJECTS_BUTTON)
        self.logger.info("'PROJECTS_BUTTON' was clicked")
        self.click(TopHeaderLocators.VIEW_ALL_PROJECTS_NESTED_BUTTON)
        self.logger.info("'VIEW_ALL_PROJECTS_NESTED_BUTTON' was clicked")

        self.wait_for_progress_bar_disappear()

        WebDriverWait(self, 5).until(
            expected_conditions.url_matches(ProjectsPage(self).page_url_pattern())
        )
        self.logger.info(
            "Finished method 'select_view_all_projects' in 'TopHeader' class"
        )

    def page_url_pattern(self, project_key=None) -> str:
        pass
