import logging

from pytest_zebrunner.zebrunner_logging import ZebrunnerHandler
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from service.ZebrunnerBasePage.ZebrunnerBasePage import ZebrunnerBasePage


class TestRunPageLocators:
    TEST_CARDS = (By.XPATH, "//article[@class]")
    TEST_ITEM = (By.XPATH, "//test-card")

    TESTRAIL_LABEL = (By.XPATH, ".//a[@name='testRailLink']")
    XRAY_LABEL = (By.XPATH, ".//a[@name='xRayLink']")
    ZEPHYR_LABEL = (By.XPATH, ".//a[@name='zephyrLink']")

    TESTRAIL_PREVIEW_WINDOW = (
        By.XPATH,
        "//test-case-preview-dialog[contains(@test-url, 'TESTRAIL_URL')]/ancestor::div",
    )
    XRAY_PREVIEW_WINDOW = (
        By.XPATH,
        "//test-case-preview-dialog[contains(@test-url, 'XRAY_URL')]/ancestor::div",
    )
    ZEPHYR_PREVIEW_WINDOW = (
        By.XPATH,
        "//test-case-preview-dialog[contains(@test-url, 'ZEPHYR_URL')]/ancestor::div",
    )

    PREVIEW_WINDOW_TITLE = (By.XPATH, "//div[@class='label-modal__title']")
    PREVIEW_WINDOW_STEPS = (By.XPATH, "//div[contains(@class, 'item-steps')]")


class TestRunPage(ZebrunnerBasePage):
    logger = logging.getLogger(__name__)
    logger.addHandler(ZebrunnerHandler())

    def select_latest_test(self):
        self.logger.info("Started method 'select_latest_test' in 'TestRunPage' class")
        test_list: list = self.get_present_elements(
            TestRunPageLocators.TEST_ITEM, timeout=5
        )
        self.logger.info("Finishing method 'select_latest_test' in 'TestRunPage' class")
        return test_list[0]

    def is_testrail_preview_correct(self):
        self.logger.info(
            "Started method 'is_testrail_preview_correct' in 'TestRunPage' class"
        )

        test: WebElement = self.select_latest_test()
        self.logger.info(
            "Waiting for 'presence_of_element_located' of 'TESTRAIL_LABEL'"
        )
        WebDriverWait(self, 10).until(
            expected_conditions.presence_of_element_located(
                TestRunPageLocators.TESTRAIL_LABEL
            )
        )

        label: WebElement = test.find_element(
            TestRunPageLocators.TESTRAIL_LABEL[0], TestRunPageLocators.TESTRAIL_LABEL[1]
        )
        label.click()
        self.logger.info("'label' was clicked")

        testrail_preview: WebElement = self.get_present_element(
            TestRunPageLocators.TESTRAIL_PREVIEW_WINDOW, timeout=10
        )
        self.wait_for_progress_bar_disappear()
        self.get_visible_child(
            testrail_preview, TestRunPageLocators.PREVIEW_WINDOW_TITLE, timeout=10
        )

        if testrail_preview.find_element(
                TestRunPageLocators.PREVIEW_WINDOW_TITLE[0],
                TestRunPageLocators.PREVIEW_WINDOW_TITLE[1],
        ):
            self.logger.info("'PREVIEW_WINDOW_TITLE' was found")
            if testrail_preview.find_element(
                    TestRunPageLocators.PREVIEW_WINDOW_STEPS[0],
                    TestRunPageLocators.PREVIEW_WINDOW_STEPS[1],
            ):
                self.logger.info("'PREVIEW_WINDOW_STEPS' was found")
                self.logger.info(
                    "Finishing method 'is_testrail_preview_correct' in 'TestRunPage' class"
                )
                return True

        self.logger.info(
            "Finishing method 'is_testrail_preview_correct' in 'TestRunPage' class"
        )
        return False

    def is_xray_preview_correct(self):
        self.logger.info(
            "Started method 'is_xray_preview_correct' in 'TestRunPage' class"
        )

        test: WebElement = self.select_latest_test()
        self.logger.info("Waiting for 'presence_of_element_located' of 'XRAY_LABEL'")
        WebDriverWait(self, 10).until(
            expected_conditions.presence_of_element_located(
                TestRunPageLocators.XRAY_LABEL
            )
        )
        label: WebElement = test.find_element(
            TestRunPageLocators.XRAY_LABEL[0], TestRunPageLocators.XRAY_LABEL[1]
        )

        label.click()
        self.logger.info("'label' was clicked")

        xray_preview: WebElement = self.get_present_element(
            TestRunPageLocators.XRAY_PREVIEW_WINDOW, timeout=10
        )
        self.wait_for_progress_bar_disappear()
        self.get_visible_child(
            xray_preview, TestRunPageLocators.PREVIEW_WINDOW_TITLE, timeout=10
        )

        if xray_preview.find_element(
                TestRunPageLocators.PREVIEW_WINDOW_TITLE[0],
                TestRunPageLocators.PREVIEW_WINDOW_TITLE[1],
        ):
            self.logger.info("'PREVIEW_WINDOW_TITLE' was found")
            if xray_preview.find_element(
                    TestRunPageLocators.PREVIEW_WINDOW_STEPS[0],
                    TestRunPageLocators.PREVIEW_WINDOW_STEPS[1],
            ):
                self.logger.info("'PREVIEW_WINDOW_STEPS' was found")
                self.logger.info(
                    "Finishing method 'is_xray_preview_correct' in 'TestRunPage' class"
                )
                return True

        self.logger.info(
            "Finishing method 'is_xray_preview_correct' in 'TestRunPage' class"
        )
        return False

    def is_zephyr_squad_preview_correct(self):
        self.logger.info(
            "Started method 'is_zephyr_squad_preview_correct' in 'TestRunPage' class"
        )

        test: WebElement = self.select_latest_test()
        self.logger.info("Waiting for 'presence_of_element_located' of 'ZEPHYR_LABEL'")
        WebDriverWait(self, 10).until(
            expected_conditions.presence_of_element_located(
                TestRunPageLocators.ZEPHYR_LABEL
            )
        )

        label: WebElement = test.find_element(
            TestRunPageLocators.ZEPHYR_LABEL[0], TestRunPageLocators.ZEPHYR_LABEL[1]
        )

        label.click()
        self.logger.info("'label' was clicked")

        zephyr_squad_preview: WebElement = self.get_present_element(
            TestRunPageLocators.ZEPHYR_PREVIEW_WINDOW, timeout=10
        )
        self.wait_for_progress_bar_disappear()
        self.get_visible_child(
            zephyr_squad_preview, TestRunPageLocators.PREVIEW_WINDOW_TITLE, timeout=10
        )

        if zephyr_squad_preview.find_element(
                TestRunPageLocators.PREVIEW_WINDOW_TITLE[0],
                TestRunPageLocators.PREVIEW_WINDOW_TITLE[1],
        ):
            self.logger.info("'PREVIEW_WINDOW_TITLE' was found")
            if zephyr_squad_preview.find_element(
                    TestRunPageLocators.PREVIEW_WINDOW_STEPS[0],
                    TestRunPageLocators.PREVIEW_WINDOW_STEPS[1],
            ):
                self.logger.info("'PREVIEW_WINDOW_STEPS' was found")
                self.logger.info(
                    "Finishing method 'is_zephyr_squad_preview_correct' in 'TestRunPage' class"
                )
                return True

        self.logger.info(
            "Finishing method 'is_zephyr_squad_preview_correct' in 'TestRunPage' class"
        )
        return False

    def page_url_pattern(self, project_key=None) -> str:
        pass
