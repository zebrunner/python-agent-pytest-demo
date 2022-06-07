import logging
import re

from pytest_zebrunner.zebrunner_logging import ZebrunnerHandler
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from service.TestRunsPage.TestRunsPage import TestRunsPage
from service.ZebrunnerBasePage.ZebrunnerBasePage import ZebrunnerBasePage
from tests import configuration


class LaunchersPageLocators:
    # Sidebar
    LAUNCHER_TREE = (By.XPATH, "//launcher-tree")
    LAUNCHER_ITEM = (By.XPATH, "//div[contains(@class, 'item-launcher-name')]")
    ADD_NEW_LAUNCHER_BUTTON = (By.XPATH, "//button[contains(@class, 'new-launcher')]")

    # Main workspace
    HEADER_LINK = (By.XPATH, "//a[contains(@class, 'selected-repo')]")
    CONNECTION_STATUS_STRING = (
        By.XPATH,
        "//span[contains(@class, 'connection-status')]",
    )

    # Adding launcher
    LAUNCHER_NAME_FIELD = (By.XPATH, "//input[@name='launcherName']")
    BRANCH_SELECTOR_DROPDOWN = (By.XPATH, "//div[@name='repoBranch']")
    DROPDOWN_BRANCH_ITEM = (By.ID, "ui-select-choices-row-0-")
    DOCKER_IMAGE_DROPDOWN = (By.XPATH, "//input[@name='dockerImage']")
    DROPDOWN_DOCKER_ITEM = (By.XPATH, "//li[@role='option']")
    LAUNCH_COMMAND_FIELD = (By.XPATH, "//input[@name='launchCommand']")

    ADD_VARIABLE_BUTTON = (By.XPATH, "//span[text()='Add variable']//parent::button")
    VARIABLE_NAME = (By.XPATH, ".//input[@name='variableName']")
    VARIABLE_TYPE_DROPDOWN = (
        By.XPATH,
        ".//div[contains(@ng-model, 'capabilityItem.type')]",
    )
    DROPDOWN_VARIABLE_ITEM = (By.XPATH, ".//div[contains(@id, 'ui-select-choices')]")
    VARIABLE_DEFAULT_VALUE = (By.XPATH, ".//input[@name='defaultStringValue']")

    ALL_VARIABLES_BLOCK = (By.XPATH, "//custom-vars-add[contains(@class, 'env-vars')]")
    VARIABLE_BLOCK = (By.XPATH, ".//div[@ng-form]")

    ADD_BUTTON = (By.XPATH, "//button[text()='ADD']")

    LAUNCH_BUTTON = (By.XPATH, "//button[text()='Launch']")


class LaunchersPage(ZebrunnerBasePage):
    logger = logging.getLogger(__name__)
    logger.addHandler(ZebrunnerHandler())

    def is_repo_added(self, url, expected_text) -> bool:
        self.logger.info("Started method 'is_repo_added' in 'LaunchersPage' class")
        header_text: str = self.get_text(LaunchersPageLocators.HEADER_LINK)
        self.logger.info("Header text is: " + header_text)
        self.logger.info("Expected text is: " + url)
        url_match = re.match("https://.+?..+?/(.+)", url).group(
            1
        ) == header_text.rstrip("launch")

        repo_is_connected_text = self.get_text(
            LaunchersPageLocators.CONNECTION_STATUS_STRING
        )
        self.logger.info("'repo_is_connected_text' text is: " + repo_is_connected_text)
        self.logger.info("'expected_text' text is: " + expected_text)

        if (repo_is_connected_text == expected_text) & url_match:
            self.logger.info("Repo is added")
            self.logger.info(
                "Finishing method 'is_repo_added' in 'LaunchersPage' class"
            )
            return True
        else:
            self.logger.info("Repo is not added. Method finished.")
            self.logger.info(
                "Finishing method 'is_repo_added' in 'LaunchersPage' class"
            )
            return False

    def is_launcher_added(self, name) -> bool:
        self.logger.info("Started method 'is_launcher_added' in 'LaunchersPage' class")
        self.logger.info(
            "Waiting for 'visibility_of_element_located' of 'LAUNCHER_TREE'"
        )
        WebDriverWait(self, 5).until(
            expected_conditions.visibility_of_element_located(
                LaunchersPageLocators.LAUNCHER_TREE
            )
        )
        self.logger.info("Searching for launcher with name: " + name)
        if self.is_element_with_text_present(LaunchersPageLocators.LAUNCHER_ITEM, name):
            self.logger.info("Launcher was added")
            self.logger.info(
                "Finishing method 'is_launcher_added' in 'LaunchersPage' class"
            )
            return True
        else:
            self.logger.info("Launcher is not added")
            self.logger.info(
                "Finishing method 'is_launcher_added' in 'LaunchersPage' class"
            )
            return False

    def add_new_launcher(
            self, name, branch, docker_image, launch_command, variables=None, launch=False
    ):
        """
        Add launcher with parameters.

        :param name: name of launcher ("Carina Api")
        :param branch: remote branch name ("master")
        :param docker_image: ("maven:3.8-openjdk-11")
        :param launch_command: ("mvn clean test -Dsuite=${SUITE}")
        :param variables: list[list[str, str, str] variables types ("string", "boolean", "choice", "integer")
        :param launch: launch launcher after adding
        """
        self.logger.info("Started method 'add_new_launcher' in 'LaunchersPage' class")

        self.click(LaunchersPageLocators.ADD_NEW_LAUNCHER_BUTTON)
        self.logger.info("'ADD_NEW_LAUNCHER_BUTTON' was clicked")
        self.enter_text(LaunchersPageLocators.LAUNCHER_NAME_FIELD, name)
        self.logger.info(f"'{name}' was sent to 'LAUNCHER_NAME_FIELD'")
        self.select_from_drop_down_by_text(
            LaunchersPageLocators.BRANCH_SELECTOR_DROPDOWN,
            LaunchersPageLocators.DROPDOWN_BRANCH_ITEM,
            branch,
        )
        self.logger.info(
            f"'DROPDOWN_BRANCH_ITEM' was selected from 'BRANCH_SELECTOR_DROPDOWN' by text: '{branch}'"
        )
        self.select_from_drop_down_by_text(
            LaunchersPageLocators.DOCKER_IMAGE_DROPDOWN,
            LaunchersPageLocators.DROPDOWN_DOCKER_ITEM,
            docker_image,
        )
        self.logger.info(
            f"'DROPDOWN_DOCKER_ITEM' was selected from 'DOCKER_IMAGE_DROPDOWN' by text: '{docker_image}'"
        )

        self.enter_text(
            LaunchersPageLocators.LAUNCH_COMMAND_FIELD, launch_command, with_clear=True
        )
        self.logger.info(f"'{launch_command}' was sent to 'LAUNCH_COMMAND_FIELD'")

        # Add variable button
        for x in range(0, len(variables)):
            button = self.get_present_element(LaunchersPageLocators.ADD_VARIABLE_BUTTON)
            self.scroll_to_the_center(button)

            self.logger.info("Waiting 'until_not' for 'staleness_of' of 'button'")
            WebDriverWait(self, 10).until_not(expected_conditions.staleness_of(button))
            button.click()
            self.logger.info("'button' was clicked")

        variables_block: WebElement = self.get_present_element(
            LaunchersPageLocators.ALL_VARIABLES_BLOCK
        )
        variable_lines: list = variables_block.find_elements(
            by=LaunchersPageLocators.VARIABLE_BLOCK[0],
            value=LaunchersPageLocators.VARIABLE_BLOCK[1],
        )

        for x in range(0, len(variables)):
            self.scroll_to_the_center(variable_lines[x])
            # Variable name
            name: WebElement = variable_lines[x].find_element(
                by=LaunchersPageLocators.VARIABLE_NAME[0],
                value=LaunchersPageLocators.VARIABLE_NAME[1],
            )
            name.send_keys(variables[x][0])
            self.logger.info(f"'{variables[x][0]}' was sent to 'name'")

            # Variable type
            type_block: WebElement = variable_lines[x].find_element(
                by=LaunchersPageLocators.VARIABLE_TYPE_DROPDOWN[0],
                value=LaunchersPageLocators.VARIABLE_TYPE_DROPDOWN[1],
            )

            self.logger.info("Waiting 'until_not' for 'staleness_of' of 'type_block'")
            WebDriverWait(self, 5).until_not(
                expected_conditions.staleness_of(type_block)
            )
            type_block.click()
            self.logger.info("'type_block' was clicked")

            type_items: list = type_block.find_elements(
                by=LaunchersPageLocators.DROPDOWN_VARIABLE_ITEM[0],
                value=LaunchersPageLocators.DROPDOWN_VARIABLE_ITEM[1],
            )

            for item in type_items:
                self.logger.info("Waiting 'until_not' for 'staleness_of' of 'item'")
                WebDriverWait(self, 5).until_not(expected_conditions.staleness_of(item))
                if item.text == variables[x][1]:
                    self.logger.info(f"'item' == {variables[x][1]}")
                    item.click()
                    self.logger.info("'item' was clicked")

            # Variable default value
            default_value: WebElement = variable_lines[x].find_element(
                by=LaunchersPageLocators.VARIABLE_DEFAULT_VALUE[0],
                value=LaunchersPageLocators.VARIABLE_DEFAULT_VALUE[1],
            )
            default_value.send_keys(variables[x][2])
            self.logger.info(f"'{variables[x][2]}' was sent to 'default_value'")

        # Add button
        add_button: WebElement = self.get_present_element(
            LaunchersPageLocators.ADD_BUTTON
        )
        self.scroll_to_the_center(add_button)
        self.logger.info("Waiting for 'element_to_be_clickable' of 'ADD_BUTTON'")
        WebDriverWait(self, 5).until(
            expected_conditions.element_to_be_clickable(
                LaunchersPageLocators.ADD_BUTTON
            )
        )
        add_button.click()
        self.logger.info("'add_button' was clicked")
        self.wait_for_progress_bar_disappear()

        self.logger.info("Finishing method 'add_new_launcher' in 'LaunchersPage' class")
        if not launch:
            return self
        else:
            self.launch_added_launcher()

    def launch_added_launcher(self):
        self.logger.info("Started method 'launch_added_launcher' in '' class")
        # Launch button
        self.logger.info("Waiting for 'presence_of_element_located' of 'LAUNCH_BUTTON'")
        WebDriverWait(self, 10).until(
            expected_conditions.presence_of_element_located(
                LaunchersPageLocators.LAUNCH_BUTTON
            )
        )
        launch_button: WebElement = self.get_present_element(
            LaunchersPageLocators.LAUNCH_BUTTON
        )
        self.scroll_to_the_center(launch_button)
        self.logger.info("Waiting for 'element_to_be_clickable' of 'LAUNCH_BUTTON'")
        WebDriverWait(self, 5).until(
            expected_conditions.element_to_be_clickable(
                LaunchersPageLocators.LAUNCH_BUTTON
            )
        )
        launch_button.click()

        WebDriverWait(self, 10).until(
            expected_conditions.url_matches(TestRunsPage(self).page_url_pattern())
        )
        self.wait_for_progress_bar_disappear()
        self.logger.info("Finishing method 'launch_added_launcher'")
        return TestRunsPage(self)

    def page_url_pattern(self, project_key=None) -> str:
        self.logger.info("Started method 'page_url_pattern' in 'LaunchersPage' class")
        if project_key is None:
            self.logger.info(
                "Project key was not specified, comparing with regex pattern"
            )
            pattern = (
                    configuration.get("base_url")
                    + "projects/"
                    + ".{3,6}"
                    + "/"
                    + "launchers/"
                    + "\\d{1,4}"
            )
            self.logger.info("Pattern: " + pattern)
            self.logger.info(
                "Finishing method 'page_url_pattern' in 'LaunchersPage' class"
            )
            return pattern
        else:
            self.logger.info("Project key was specified as: " + project_key)
            pattern = (
                    configuration.get("base_url")
                    + "projects/"
                    + f"{project_key.upper()}"
                    + "/"
                    + "launchers/"
                    + "\\d{1,4}"
            )
            self.logger.info("Url: " + pattern)
            self.logger.info(
                "Finishing method 'page_url_pattern' in 'LaunchersPage' class"
            )
            return pattern
