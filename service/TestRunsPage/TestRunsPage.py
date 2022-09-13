import logging
import random
import re
import string

from pytest_zebrunner.zebrunner_logging import ZebrunnerHandler
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from service.PageElements.CreateProjectModal import CreateProjectModal
from service.PageElements.ModalWindowBase import ModalWindowBaseLocators
from service.PageElements.TopHeader import TopHeader
from service.ZebrunnerBasePage.ZebrunnerBasePage import ZebrunnerBasePage
from tests import configuration


class TestRunsPageLocators:
    # Text block
    THIS_PROJECT_HAS_NO_TEST_RUNS_BLOCK = (
        By.XPATH,
        "//div[@class='docs-section__text-wrapper']",
    )
    TEXT_BLOCK_HEADER = (By.XPATH, "./h5")

    # Launcher button block
    LAUNCHER_BUTTON = (By.XPATH, "//button[contains(@class, 'launcher-button')]")

    # Test runs block
    TEST_RUN_ITEMS = (By.XPATH, "//div[@test-run='testRun']")
    TEST_RUN_TIME_FROM_START = (By.XPATH, ".//div[@class='time']")

    # Test run statuses
    TEST_RUN_QUEUED = (By.XPATH, ".//div[@class='test-run-card__wrapper QUEUED']")
    TEST_RUN_IN_PROGRESS = (
        By.XPATH,
        ".//div[@class='test-run-card__wrapper IN_PROGRESS']",
    )
    TEST_RUN_PASSED = (By.XPATH, ".//div[@class='test-run-card__wrapper PASSED']")

    # Test run item
    TEST_RUN_OPTIONS_BUTTON = (By.XPATH, ".//button[@name='testRunSetting']")
    TEST_RUN_MILESTONE_TEXT_LABEL = (
        By.XPATH,
        ".//span[contains(@class, 'text-label')]",
    )

    # Options menu
    OPTIONS_MENU = (By.XPATH, "//body/div[contains(@id, 'menu_container')]")
    ASSIGN_TO_MILESTONE = (By.XPATH, ".//button[@name='showMilestoneDialog']")


class TestRunsPage(ZebrunnerBasePage):
    logger = logging.getLogger(__name__)
    logger.addHandler(ZebrunnerHandler())

    def page_url_pattern(self, project_key=None) -> str:
        self.logger.info("Started method 'page_url_pattern' in 'TestRunsPage' class")
        if project_key is None:
            self.logger.info(
                "Project key was not specified, comparing with regex pattern"
            )
            pattern = (
                    configuration.get("base_url") + "projects/" + ".{3,6}/" + "automation-launches"
            )
            self.logger.info(
                "Finishing method 'page_url_pattern' in 'TestRunsPage' class"
            )
            return pattern
        else:
            pattern = (
                    configuration.get("base_url")
                    + "projects/"
                    + f"{project_key.upper()}"
                    + "/"
                    + "automation-launches"
            )
            self.logger.info("Project key was specified as: " + project_key)
            self.logger.info(
                "Finishing method 'page_url_pattern' in 'TestRunsPage' class"
            )
            return pattern

    def no_test_runs_text_header(self) -> str:
        self.logger.info(
            "Started method 'no_test_runs_text_header' in 'TestRunsPage' class"
        )
        full_text: WebElement = self.get_present_element(
            TestRunsPageLocators.THIS_PROJECT_HAS_NO_TEST_RUNS_BLOCK
        )
        header = full_text.find_element_by_xpath(
            TestRunsPageLocators.TEXT_BLOCK_HEADER[1]
        ).text
        self.logger.info("Founded text header: " + header)
        self.logger.info(
            "Finishing method 'no_test_runs_text_header' in 'TestRunsPage' class"
        )
        return header

    def create_new_project(self, name=None, key=None):
        """
        :param name: Project name (optional)
        :param key: Project key (optional)
        :return: {"name": name, "key": key}
        """
        self.logger.info("Started method 'create_new_project' in 'TestRunsPage' class")
        if name is None:
            self.logger.info("Project name was not specified")
            name = "".join(random.choices(string.ascii_letters + string.digits, k=6))
            self.logger.info("Generated project name: " + name)
        if key is None:
            self.logger.info("Project key was not specified")
            key = "".join(random.choices(string.ascii_letters + string.digits, k=3))
            self.logger.info("Generated project key: " + key)

        TopHeader(self).select_create_project()

        CreateProjectModal(self).create_project(name, key)

        self.logger.info(
            "Finishing method 'create_new_project' in 'TestRunsPage' class"
        )
        return {"name": name, "key": key}

    def waiting_for_latest_test_run_passed(self, seconds_for_step) -> bool:
        self.logger.info(
            "Started method 'waiting_for_latest_test_run_passed' in 'TestRunsPage' class"
        )
        test_run_items: list = self.get_present_elements(
            TestRunsPageLocators.TEST_RUN_ITEMS
        )
        self.logger.info("Found " + str(len(test_run_items)) + " test runs")
        latest_test_run: WebElement = test_run_items[0]
        self.logger.info("Selected latest test run")

        self.logger.info(
            "====== waiting period is " + str(seconds_for_step) + " seconds ====== "
        )
        self.logger.info("Starting to wait for 'QUEUED' status")
        try:
            self.logger.info("Starting to wait for 'IN_PROGRESS' status")
            WebDriverWait(latest_test_run, seconds_for_step).until(
                lambda x: x.find_element(
                    TestRunsPageLocators.TEST_RUN_IN_PROGRESS[0],
                    TestRunsPageLocators.TEST_RUN_IN_PROGRESS[1],
                )
            )
            self.logger.info("Finishing to wait for 'IN_PROGRESS' status")

            self.logger.info("Starting to wait for 'PASSED' status")
            WebDriverWait(latest_test_run, seconds_for_step).until(
                lambda x: x.find_element(
                    TestRunsPageLocators.TEST_RUN_PASSED[0],
                    TestRunsPageLocators.TEST_RUN_PASSED[1],
                )
            )
            self.logger.info("Finishing to wait for 'PASSED' status")
        except TimeoutException:
            self.logger.info(
                "Finishing method 'waiting_for_latest_test_run_passed' in 'TestRunsPage' class"
            )
            return False
        else:
            self.logger.info(
                "Finishing method 'waiting_for_latest_test_run_passed' in 'TestRunsPage' class"
            )
            return True

    def click_launcher_button(self):
        self.logger.info(
            "Started method 'click_launcher_button' in 'TestRunsPage' class"
        )

        self.logger.info("Waiting for 'element_to_be_clickable' of 'LAUNCHER_BUTTON'")
        WebDriverWait(self, 5).until(
            expected_conditions.element_to_be_clickable(
                TestRunsPageLocators.LAUNCHER_BUTTON
            )
        )
        self.click(TestRunsPageLocators.LAUNCHER_BUTTON)
        self.logger.info("'LAUNCHER_BUTTON' was clicked")
        self.logger.info(
            "Finished method 'click_launcher_button' in 'TestRunsPage' class"
        )

    def assign_milestone_to_latest_test_run(self) -> str:
        self.logger.info(
            "Started method 'assign_milestone_to_latest_test_run' in 'TestRunsPage' class"
        )
        test_run_items: list[WebElement] = self.get_present_elements(
            TestRunsPageLocators.TEST_RUN_ITEMS
        )
        self.logger.info(f"Found {str(len(test_run_items))} automation-launches")
        options = test_run_items[0].find_element(
            TestRunsPageLocators.TEST_RUN_OPTIONS_BUTTON[0],
            TestRunsPageLocators.TEST_RUN_OPTIONS_BUTTON[1],
        )

        options.click()
        self.logger.info("'options' was clicked")

        options_menu: WebElement = self.get_present_element(
            TestRunsPageLocators.OPTIONS_MENU
        )

        assign_to_milestone = options_menu.find_element(
            TestRunsPageLocators.ASSIGN_TO_MILESTONE[0],
            TestRunsPageLocators.ASSIGN_TO_MILESTONE[1],
        )

        assign_to_milestone.click()
        self.logger.info("'assign_to_milestone' was clicked")

        milestones: list[WebElement] = self.get_present_elements(
            ModalWindowBaseLocators.RADIO_BUTTON_ITEM
        )
        self.logger.info(f"Found {str(len(milestones))} milestones radio buttons")

        milestone_name = milestones[1].text

        self.logger.info(f"Milestone name: '{milestone_name}'")

        milestones[1].click()
        self.logger.info("First after 'None' milestone radio button was clicked")

        self.click(ModalWindowBaseLocators.SUBMIT_BUTTON)
        self.logger.info("'SUBMIT_BUTTON' was clicked")

        self.logger.info(
            "Finishing method 'assign_milestone_to_latest_test_run' in 'TestRunsPage' class"
        )
        return milestone_name

    def get_test_run_milestone_label(self) -> str:
        self.logger.info(
            "Started method 'get_test_run_milestone_label' in 'TestRunsPage' class"
        )
        test_run_items: list[WebElement] = self.get_present_elements(
            TestRunsPageLocators.TEST_RUN_ITEMS
        )
        self.logger.info("Found " + str(len(test_run_items)) + " testruns")

        self.logger.info(
            "Waiting for 'presence_of_element_located' of 'TEST_RUN_MILESTONE_TEXT_LABEL'"
        )
        WebDriverWait(self, 5).until(
            expected_conditions.presence_of_element_located(
                TestRunsPageLocators.TEST_RUN_MILESTONE_TEXT_LABEL
            )
        )

        label: WebElement = test_run_items[0].find_element(
            TestRunsPageLocators.TEST_RUN_MILESTONE_TEXT_LABEL[0],
            TestRunsPageLocators.TEST_RUN_MILESTONE_TEXT_LABEL[1],
        )

        label_text = label.text
        self.logger.info(f"Found text: '{label_text}'")
        self.logger.info(
            "Finishing method 'get_test_run_milestone_label' in 'TestRunsPage' class"
        )
        return label_text

    def open_latest_test_run(self):
        self.logger.info(
            "Started method 'open_latest_test_run' in 'TestRunsPage' class"
        )
        test_run_items: list[WebElement] = self.get_present_elements(
            TestRunsPageLocators.TEST_RUN_ITEMS
        )
        self.logger.info(f"Found {str(len(test_run_items))} automation-launches")
        test_run_items[0].click()
        self.logger.info("First element of 'test_run_items' was clicked")
        self.logger.info(
            "Finished method 'open_latest_test_run' in 'TestRunsPage' class"
        )

    def get_current_project_key(self) -> str:
        self.logger.info(
            "Started method 'get_current_project_key' in 'TestRunsPage' class"
        )

        WebDriverWait(self, 10).until(
            expected_conditions.url_matches(self.page_url_pattern())
        )
        url = str(self.driver.current_url)
        key = re.search("projects/(d*[a-zA-Z][a-zA-Z\\d]*)", url)[1]
        self.logger.info(
            "Finishing method 'get_current_project_key' in 'TestRunsPage' class"
        )
        return key
