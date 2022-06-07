import calendar
import logging
import random
import string
from datetime import date
from typing import Tuple

from pytest_zebrunner.zebrunner_logging import ZebrunnerHandler
from selenium.webdriver.common.by import By

from service.PageElements.ModalWindowBase import ModalWindowBaseLocators
from service.ZebrunnerBasePage.ZebrunnerBasePage import ZebrunnerBasePage


class CreateMilestoneModalLocators(ModalWindowBaseLocators):
    TITLE_FIELD = (By.ID, "milestoneName")

    START_DATE = (By.XPATH, "//md-datepicker[@name='milestoneStartDate']")
    DUE_DATE = (By.XPATH, "//md-datepicker[@name='milestoneDueDate']")

    DESCRIPTION_FIELD = (By.ID, "milestoneDescription")

    @staticmethod
    def day(last_day_of_month=False, day_of_month=1) -> Tuple[str, str]:
        today = date.today()
        year = today.year
        month = today.month

        days_in_month = calendar.monthrange(year, month)[1]

        if last_day_of_month:
            day = today.replace(day=days_in_month).strftime("%A %B %-d %Y")
        else:
            day = today.replace(day=day_of_month).strftime("%A %B %-d %Y")
        return By.XPATH, f"//td[@aria-label='{day}']"


class CreateMilestoneModal(ZebrunnerBasePage):
    logger = logging.getLogger(__name__)
    logger.addHandler(ZebrunnerHandler())

    def create_milestone(self, title=None, description=None):
        self.logger.info(
            "Started method 'create_milestone' in 'CreateMilestoneModal' class"
        )
        if title is None:
            self.logger.info("Milestone title was not specified")
            title = "".join(random.choices(string.ascii_letters + string.digits, k=10))
            self.logger.info("Generated milestone title: " + title)
        else:
            self.logger.info("Milestone title was specified: " + title)

        self.enter_text(CreateMilestoneModalLocators.TITLE_FIELD, title)
        self.logger.info("Title was entered in TITLE_FIELD")

        self.click(CreateMilestoneModalLocators.START_DATE)
        self.logger.info("START_DATE was clicked")
        self.click(CreateMilestoneModalLocators.day())
        self.logger.info("DAY was selected")
        self.click(CreateMilestoneModalLocators.DUE_DATE)
        self.logger.info("DUE_DATE was clicked")
        self.click(CreateMilestoneModalLocators.day(last_day_of_month=True))
        self.logger.info("DAY was selected")

        if description is None:
            self.logger.info("Milestone description was not specified")
            description = "".join(
                random.choices(string.ascii_letters + string.digits, k=100)
            )
            self.logger.info("Generated milestone description: " + description)
        else:
            self.logger.info("Milestone description was specified: " + description)

        self.enter_text(CreateMilestoneModalLocators.DESCRIPTION_FIELD, description)
        self.logger.info("Description was entered in DESCRIPTION_FIELD")

        self.click(CreateMilestoneModalLocators.SUBMIT_BUTTON)
        self.logger.info("SUBMIT_BUTTON was clicked")
        self.wait_for_progress_bar_disappear()
        self.logger.info(
            "Finished method 'create_milestone' in 'CreateMilestoneModal' class"
        )

    def page_url_pattern(self, project_key=None) -> str:
        pass
