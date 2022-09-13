import pytest
from selenium.webdriver.remote.webdriver import WebDriver

from service.LoginPage.LoginPage import LoginPage
from tests import configuration


@pytest.fixture(scope="function")
def driver():
    desired_capabilities = {
        "browserName": configuration.get("browserName"),
        "browserVersion": configuration.get("browserVersion"),
        "platform": configuration.get("platform"),
        "platformName": configuration.get("platformName"),
        "enableVideo": True,
        "enableLog": True,
        "enableVNC": True,
        "provider": "zebrunner",
    }

    driver = WebDriver(
        command_executor=configuration.get("hub_url"),
        desired_capabilities=desired_capabilities,
    )

    driver.set_page_load_timeout(20)
    driver.implicitly_wait(10)
    driver.maximize_window()

    driver.get(configuration.get("base_url"))
    LoginPage(driver).login_with_valid_creds(configuration.get("username"), configuration.get("password"))

    yield driver

    driver.delete_all_cookies()
    driver.quit()
