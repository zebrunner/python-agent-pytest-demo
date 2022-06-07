import logging

from pytest_zebrunner.zebrunner_logging import ZebrunnerHandler
from selenium.webdriver.common.by import By

from service.MilestonesPage.CreateMilestoneModal import CreateMilestoneModal
from service.ZebrunnerBasePage.ZebrunnerBasePage import ZebrunnerBasePage
from tests import configuration


class MilestonesPageLocators:
    ADD_MILESTONE_BUTTON = (
        By.XPATH,
        "//button[contains(@class, 'milestones-add-button')]",
    )


class MilestonesPage(ZebrunnerBasePage):
    logger = logging.getLogger(__name__)
    logger.addHandler(ZebrunnerHandler())

    def create_milestone(self, title=None, description=None):
        self.logger.info("Started method 'create_milestone' in 'MilestonesPage' class")
        self.click(MilestonesPageLocators.ADD_MILESTONE_BUTTON)
        self.logger.info("ADD_MILESTONE_BUTTON was clicked")
        CreateMilestoneModal(self).create_milestone(title, description)
        self.logger.info("Finished method 'create_milestone' in 'MilestonesPage' class")

    def page_url_pattern(self, project_key=None) -> str:
        self.logger.info("Started method 'page_url_pattern' in 'MilestonesPage' class")
        if project_key is None:
            self.logger.info(
                "Project key was not specified, comparing with regex pattern"
            )
            pattern = (
                    configuration.get("base_url") + "projects/" + ".{3,6}/" + "milestones"
            )
            self.logger.info("Pattern: " + pattern)
            self.logger.info(
                "Finishing method 'page_url_pattern' in 'MilestonesPage' class"
            )
            return pattern
        else:
            self.logger.info("Project key was specified as: " + project_key)
            pattern = (
                    configuration.get("base_url")
                    + "projects/"
                    + {project_key.upper()}
                    + "/"
                    + "milestones"
            )
            self.logger.info("Url: " + pattern)
            self.logger.info(
                "Finishing method 'page_url_pattern' in 'MilestonesPage' class"
            )
            return pattern
