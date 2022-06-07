import logging
import time
from abc import ABC, abstractmethod

from basepage import BasePage
from pytest_zebrunner.zebrunner_logging import ZebrunnerHandler
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from tests import configuration


class ZebrunnerBasePageLocators:
    # Popup
    POPUP = (By.XPATH, "//md-toast")
    POPUP_TEXT = (By.XPATH, "//span[contains(@class, 'toast-text')]")

    # Progress bar
    TOP_PROGRESS_BAR = (By.XPATH, "//md-progress-linear")

    # Focus trap
    FOCUS_TRAP_AREA = (By.XPATH, "//div[@class='md-dialog-container ng-scope']")


class ZebrunnerBasePage(BasePage, ABC):
    logger = logging.getLogger(__name__)
    logger.addHandler(ZebrunnerHandler())

    def get_popup_message(self) -> str:
        self.logger.info(
            "Started method 'get_popup_message' in 'ZebrunnerBasePage' class"
        )
        popup: WebElement = self.get_present_element(ZebrunnerBasePageLocators.POPUP)
        popup_text = popup.find_element_by_xpath(
            ZebrunnerBasePageLocators.POPUP_TEXT[1]
        ).text
        self.logger.info("Found popup text: " + popup_text)
        self.logger.info(
            "Finishing method 'get_popup_message' in 'ZebrunnerBasePage' class"
        )
        return popup_text

    def wait_for_progress_bar_disappear(self):
        self.logger.info(
            "Started method 'wait_for_progress_bar_disappear' in 'ZebrunnerBasePage' class"
        )
        try:
            self.logger.info(
                "Waiting for 'wait_for_element_to_disappear' of 'TOP_PROGRESS_BAR'"
            )
            self.wait_for_element_to_disappear(
                ZebrunnerBasePageLocators.TOP_PROGRESS_BAR, timeout=5
            )
        except TimeoutException:
            self.logger.info("Progress bar not disappear in 5 seconds")
        finally:
            self.logger.info(
                "Finished method 'wait_for_progress_bar_disappear' in 'ZebrunnerBasePage' class"
            )

    def wait_for_focus_trap_disappear(self):
        self.logger.info(
            "Started method 'wait_for_focus_trap_disappear' in 'ZebrunnerBasePage' class"
        )

        try:
            self.logger.info(
                "Waiting for 'wait_for_element_to_disappear' of 'FOCUS_TRAP_AREA'"
            )
            self.wait_for_element_to_disappear(
                ZebrunnerBasePageLocators.FOCUS_TRAP_AREA, timeout=5
            )
        except TimeoutException:
            self.logger.info("Focus trap not disappear in 5 seconds")
        finally:
            self.logger.info(
                "Finished method 'wait_for_focus_trap_disappear' in 'ZebrunnerBasePage' class"
            )

    def scroll_to_the_center(self, element):
        self.logger.info(
            "Started method 'scroll_to_the_center' in 'ZebrunnerBasePage' class"
        )
        """
        Scrolls an element into center of view.
    
        :param element: WebElement to scroll into view
        :return: None
        """
        if isinstance(element, WebElement):
            self.execute_script(
                'arguments[0].scrollIntoView({behavior: "auto", block: "center", inline: "center"});',
                element,
            )
            time.sleep(0.5)
        self.logger.info(
            "Finished method 'scroll_to_the_center' in 'ZebrunnerBasePage' class"
        )

    @abstractmethod
    def page_url_pattern(self, project_key=None) -> str:
        self.logger.info("Started method 'page_url_pattern' in 'AbstractPage' class")
        if project_key is None:
            self.logger.info(
                "Project key was not specified, comparing with regex pattern"
            )
            pattern = configuration.get("base_url") + "projects/" + ".{3,6}/" + "..."
            self.logger.info("Pattern: " + pattern)
            self.logger.info(
                "Finishing method 'page_url_pattern' in 'AbstractPage' class"
            )
            return pattern
        else:
            self.logger.info("Project key was specified as: " + project_key)
            pattern = (
                    configuration.get("base_url")
                    + "projects/"
                    + f"{project_key.upper()}"
                    + "/"
                    + "..."
            )
            self.logger.info("Url: " + pattern)
            self.logger.info(
                "Finishing method 'page_url_pattern' in 'AbstractPage' class"
            )
            return pattern

    @staticmethod
    def get_compliant_locator(by, locator, params):
        """
        Returns a tuple of by and locator prepared with optional parameters
        :param by: Type of locator (ie. CSS, ClassName, etc)
        :param locator: element locator
        :param params: (optional) locator parameters
        :return: tuple of by and locator with optional parameters
        """
        from selenium.webdriver.common.by import By

        if params is not None and not isinstance(params, dict):
            raise TypeError(
                "<params> need to be of type <dict>, was <{}>".format(
                    params.__class__.__name__
                )
            )

        return getattr(By, str(by).upper().replace(" ", "_")), locator.format(
            **(params or {})
        )
