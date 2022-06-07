import logging

from pytest_zebrunner.zebrunner_logging import ZebrunnerHandler
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from service.PageElements.ModalWindowBase import ModalWindowBaseLocators
from service.ZebrunnerBasePage.ZebrunnerBasePage import ZebrunnerBasePage


class CreateProjectModal(ZebrunnerBasePage):
    logger = logging.getLogger(__name__)
    logger.addHandler(ZebrunnerHandler())

    def create_project(self, name, key):
        self.logger.info(
            "Started method 'create_project' in 'CreateProjectModal' class"
        )

        self.enter_text(ModalWindowBaseLocators.PROJECT_NAME_FIELD, name)
        self.logger.info(f"'{name}' was sent to 'PROJECT_NAME_FIELD'")
        self.enter_text(ModalWindowBaseLocators.PROJECT_KEY_FIELD, key)
        self.logger.info(f"'{key}' was sent to 'PROJECT_KEY_FIELD'")
        self.click(ModalWindowBaseLocators.SUBMIT_BUTTON)
        self.logger.info("'SUBMIT_BUTTON' was clicked")

        self.wait_for_focus_trap_disappear()

        from service.TestRunsPage.TestRunsPage import TestRunsPage

        WebDriverWait(self.driver, 10).until(
            expected_conditions.url_matches(
                TestRunsPage(self.driver).page_url_pattern()
            )
        )
        self.logger.info(
            "Finishing method 'create_project' in 'CreateProjectModal' class"
        )
        return TestRunsPage(self.driver)

    def page_url_pattern(self, project_key=None) -> str:
        pass
