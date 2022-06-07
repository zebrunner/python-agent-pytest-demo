import logging
import random
import string

import pytest
import pytest_zebrunner
from pytest_zebrunner import tcm, attach_test_screenshot
from pytest_zebrunner.zebrunner_logging import ZebrunnerHandler
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from service.AddRepoPage.AddRepoPage import AddRepoPage
from service.Api.Api import create_test_run_with_integrations
from service.DashboardsPage.DashboardsPage import DashboardsPage
from service.IntegrationsPage.IntegrationsPage import IntegrationsPage
from service.IntegrationsPage.JiraPage import JiraPage
from service.IntegrationsPage.TestRailPage import TestRailPage
from service.LaunchersPage.LaunchersPage import LaunchersPage
from service.MilestonesPage.MilestonesPage import MilestonesPage
from service.PageElements.LeftSideMenu import LeftSideMenu
from service.PageElements.TopHeader import TopHeader
from service.ProjectsPage.ProjectsPage import ProjectsPage
from service.TestRunsPage.TestRunPage.TestRunPage import TestRunPage
from service.TestRunsPage.TestRunsPage import TestRunsPage
from tests import configuration

# Logger configuring
logger = logging.getLogger(__name__)
logger.addHandler(ZebrunnerHandler())
logger.setLevel(logging.NOTSET)

# Test run configuring
pytest_zebrunner.attach_test_run_artifact_reference(
    "Zebrunner", "https://zebrunner.com/"
)
pytest_zebrunner.attach_test_run_artifact_reference(
    "PyTest", "https://docs.pytest.org/en/latest/"
)
pytest_zebrunner.attach_test_run_artifact_reference(
    "PyTest Zebrunner agent", "https://zebrunner.com/documentation/reporting/pytest/"
)

pytest_zebrunner.attach_test_run_label("framework", "PyTest")
pytest_zebrunner.attach_test_run_label("reporter", "Zebrunner")

pytest_zebrunner.attach_test_run_artifact("../artifacts/txt.txt")
pytest_zebrunner.attach_test_run_artifact("../artifacts/zeb.png")

# Test run locale
pytest_zebrunner.CurrentTestRun.set_locale("en_US")

# Test run build
pytest_zebrunner.CurrentTestRun.set_build("build-1")

# Project key generating
key = "".join(random.choices(string.ascii_letters + string.digits, k=3)).upper()


def attach_screenshot(driver):
    driver.save_screenshot("screenshot.png")
    attach_test_screenshot("screenshot.png")


# Test 0
@pytest.mark.maintainer("hpotter")
def test_clear_tenant(driver):
    logger.info("'test_clear_tenant' test was started")
    attach_screenshot(driver)
    pytest_zebrunner.attach_test_artifact_reference(
        "Zebrunner", "https://zebrunner.com/"
    )
    pytest_zebrunner.attach_test_label("Group", "Support tests")
    pytest_zebrunner.attach_test_artifact("../artifacts/txt.txt")
    pytest_zebrunner.attach_test_artifact("../artifacts/zeb.png")

    attach_screenshot(driver)
    TopHeader(driver).select_view_all_projects()
    attach_screenshot(driver)
    ProjectsPage(driver).clear_projects()
    attach_screenshot(driver)
    logger.info("'test_clear_tenant' test was finished")


# Test 1
@pytest.mark.maintainer("jhetfield")
def test_login(driver):
    logger.info("'test_login' test was started")
    attach_screenshot(driver)

    pytest_zebrunner.attach_test_artifact_reference(
        "Zebrunner", "https://zebrunner.com/"
    )
    pytest_zebrunner.attach_test_label("Group", "Login")
    pytest_zebrunner.attach_test_artifact("../artifacts/txt.txt")
    pytest_zebrunner.attach_test_artifact("../artifacts/zeb.png")
    tcm.TestRail.set_case_id("1")
    tcm.Xray.set_test_key("ZEB-51")
    tcm.Zephyr.set_test_case_key("ZEB-52")

    assert WebDriverWait(driver, 10).until(
        EC.url_matches(TestRunsPage(driver).page_url_pattern())
    )
    attach_screenshot(driver)
    logger.info("'test_login' test was finished")


# Test 2
@pytest.mark.maintainer("mpoppins")
def test_create_project(driver):
    logger.info("'test_create_project' test was started")
    pytest_zebrunner.attach_test_artifact_reference(
        "Zebrunner", "https://zebrunner.com/"
    )
    pytest_zebrunner.attach_test_label("Group", "Project")
    pytest_zebrunner.attach_test_artifact("../artifacts/txt.txt")
    pytest_zebrunner.attach_test_artifact("../artifacts/zeb.png")
    tcm.TestRail.set_case_id("2")
    tcm.Xray.set_test_key("ZEB-24")
    tcm.Zephyr.set_test_case_key("ZEB-53")

    project_data = TestRunsPage(driver).create_new_project(key=key)

    assert (
            TestRunsPage(driver).get_popup_message()
            == f"Project {project_data.get('name')} was successfully created"
    )
    assert (
            TestRunsPage(driver).no_test_runs_text_header()
            == "This project has no test runs"
    )

    attach_screenshot(driver)
    logger.info("'test_create_project' test was finished")


# Test 3
@pytest.mark.maintainer("rhood")
def test_add_repo(driver):
    logger.info("'test_add_repo' test was started")
    pytest_zebrunner.attach_test_artifact_reference(
        "Zebrunner", "https://zebrunner.com/"
    )
    pytest_zebrunner.attach_test_label("Group", "VCS")
    pytest_zebrunner.attach_test_artifact("../artifacts/txt.txt")
    pytest_zebrunner.attach_test_artifact("../artifacts/zeb.png")
    tcm.TestRail.set_case_id("3")
    tcm.Xray.set_test_key("ZEB-18")
    tcm.Zephyr.set_test_case_key("ZEB-54")

    TestRunsPage(driver).click_launcher_button()
    url = "https://github.com/zebrunner/carina-demo"
    AddRepoPage(driver).add_repo(url)
    attach_screenshot(driver)

    assert LaunchersPage(driver).is_repo_added(
        url, "Repo is connected."
    ), "Repo was not added to the launcher"
    attach_screenshot(driver)
    logger.info("'test_add_repo' test was finished")


# Test 4
@pytest.mark.maintainer("sholmes")
def test_create_launcher(driver):
    logger.info("'test_create_launcher' test was started")
    pytest_zebrunner.attach_test_artifact_reference(
        "Zebrunner", "https://zebrunner.com/"
    )
    pytest_zebrunner.attach_test_label("Group", "VCS")
    pytest_zebrunner.attach_test_label("Group", "Launcher")
    pytest_zebrunner.attach_test_artifact("../artifacts/txt.txt")
    pytest_zebrunner.attach_test_artifact("../artifacts/zeb.png")
    tcm.TestRail.set_case_id("4")
    tcm.Xray.set_test_key("ZEB-17")
    tcm.Zephyr.set_test_case_key("ZEB-55")

    TestRunsPage(driver).click_launcher_button()
    name = "Carina Api"
    branch = "master"
    docker_image = "maven:3.8-openjdk-11"
    launch_command = "mvn clean test -Dsuite=${SUITE}"
    variables = [["SUITE", "string", "api"]]
    LaunchersPage(driver).add_new_launcher(
        name, branch, docker_image, launch_command, variables
    )

    assert LaunchersPage(driver).is_launcher_added(name)
    attach_screenshot(driver)
    LaunchersPage(driver).launch_added_launcher()
    assert TestRunsPage(driver).waiting_for_latest_test_run_passed(180)
    attach_screenshot(driver)
    logger.info("'test_create_launcher' test was finished")


# Test 5
@pytest.mark.maintainer("hpotter")
def test_create_milestone(driver):
    logger.info("'test_create_milestone' test was started")
    pytest_zebrunner.attach_test_artifact_reference(
        "Zebrunner", "https://zebrunner.com/"
    )
    pytest_zebrunner.attach_test_label("Group", "Milestones")
    pytest_zebrunner.attach_test_artifact("../artifacts/txt.txt")
    pytest_zebrunner.attach_test_artifact("../artifacts/zeb.png")
    tcm.TestRail.set_case_id("5")
    tcm.Xray.set_test_key("ZEB-63")
    tcm.Zephyr.set_test_case_key("ZEB-56")

    LeftSideMenu(driver).click_milestones_button()
    MilestonesPage(driver).create_milestone()

    assert (
            MilestonesPage(driver).get_popup_message()
            == "Milestone was successfully created"
    )
    attach_screenshot(driver)
    logger.info("'test_create_milestone' test was finished")


# Test 6
@pytest.mark.maintainer("jhetfield")
def test_assign_milestone(driver):
    logger.info("'test_assign_milestone' test was started")
    pytest_zebrunner.attach_test_artifact_reference(
        "Zebrunner", "https://zebrunner.com/"
    )
    pytest_zebrunner.attach_test_label("Group", "Milestones")
    pytest_zebrunner.attach_test_artifact("../artifacts/txt.txt")
    pytest_zebrunner.attach_test_artifact("../artifacts/zeb.png")
    tcm.TestRail.set_case_id("6")
    tcm.Xray.set_test_key("ZEB-65")
    tcm.Zephyr.set_test_case_key("ZEB-57")

    milestone_name = TestRunsPage(driver).assign_milestone_to_latest_test_run()

    assert TestRunsPage(driver).get_test_run_milestone_label() == milestone_name
    attach_screenshot(driver)
    logger.info("'test_assign_milestone' test was finished")


# Test 7
@pytest.mark.maintainer("mpoppins")
def test_create_dashboard(driver):
    logger.info("'test_create_dashboard' test was started")
    pytest_zebrunner.attach_test_artifact_reference(
        "Zebrunner", "https://zebrunner.com/"
    )
    pytest_zebrunner.attach_test_label("Group", "Dashboards")
    pytest_zebrunner.attach_test_artifact("../artifacts/txt.txt")
    pytest_zebrunner.attach_test_artifact("../artifacts/zeb.png")
    tcm.TestRail.set_case_id("7")
    tcm.Xray.set_test_key("ZEB-19")
    tcm.Zephyr.set_test_case_key("ZEB-58")

    LeftSideMenu(driver).click_dashboards_button()
    attach_screenshot(driver)
    DashboardsPage(driver).create_dashboard()
    attach_screenshot(driver)

    assert WebDriverWait(driver, 10).until(
        EC.url_matches(DashboardsPage(driver).page_url_pattern(key) + "/\\d{1,4}")
    )
    attach_screenshot(driver)
    logger.info("'test_create_dashboard' test was finished")


# Test 8
@pytest.mark.maintainer("rhood")
def test_integrations(driver):
    logger.info("'test_integrations' test was started")
    pytest_zebrunner.attach_test_artifact_reference(
        "Zebrunner", "https://zebrunner.com/"
    )
    pytest_zebrunner.attach_test_label("Group", "TCM")
    pytest_zebrunner.attach_test_artifact("../artifacts/txt.txt")
    pytest_zebrunner.attach_test_artifact("../artifacts/zeb.png")
    tcm.TestRail.set_case_id("8")
    tcm.Xray.set_test_key("ZEB-20")
    tcm.Zephyr.set_test_case_key("ZEB-59")

    LeftSideMenu(driver).click_integrations_button()
    IntegrationsPage(driver).click_testrail_card()

    assert TestRailPage(driver).test_valid_creds(
        url=configuration.get("testrail_url"),
        username=configuration.get("testrail_username"),
        password=configuration.get("testrail_password"),
    )
    attach_screenshot(driver)

    driver.back()

    IntegrationsPage(driver).click_jira_card()
    assert JiraPage(driver).test_valid_creds(
        host=configuration.get("jira_host"),
        username=configuration.get("jira_username"),
        token=configuration.get("jira_token"),
    )
    attach_screenshot(driver)

    assert JiraPage(driver).test_valid_creds_xray(
        xray_host=configuration.get("xray_host"),
        xray_id=configuration.get("xray_id"),
        xray_secret_id=configuration.get("xray_secret_id"),
    )
    attach_screenshot(driver)

    driver.back()

    IntegrationsPage(driver).click_jira_card()
    assert JiraPage(driver).test_valid_creds(
        host=configuration.get("jira_host"),
        username=configuration.get("jira_username"),
        token=configuration.get("jira_token"),
    )
    attach_screenshot(driver)

    assert JiraPage(driver).test_valid_creds_zephyr_squad(
        zephyr_squad_account_id=configuration.get("zephyr_squad_account_id"),
        zephyr_squad_access_key=configuration.get("zephyr_squad_access_key"),
        zephyr_squad_secret_key=configuration.get("zephyr_squad_secret_key"),
    )
    attach_screenshot(driver)
    logger.info("'test_integrations' test was finished")


# Test 9
@pytest.mark.maintainer("sholmes")
def test_xray_connection(driver):
    logger.info("'test_xray_connection' test was started")
    pytest_zebrunner.attach_test_artifact_reference(
        "Zebrunner", "https://zebrunner.com/"
    )
    pytest_zebrunner.attach_test_label("Group", "TCM")
    pytest_zebrunner.attach_test_label("TCM", "Xray")
    pytest_zebrunner.attach_test_artifact("../artifacts/txt.txt")
    pytest_zebrunner.attach_test_artifact("../artifacts/zeb.png")
    tcm.TestRail.set_case_id("9")
    tcm.Xray.set_test_key("ZEB-22")
    tcm.Zephyr.set_test_case_key("ZEB-60")

    create_test_run_with_integrations(key, "4", "ZEB-17", "ZEB-55")
    LeftSideMenu(driver).click_integrations_button()

    IntegrationsPage(driver).click_jira_card()
    assert JiraPage(driver).test_valid_creds(
        host=configuration.get("jira_host"),
        username=configuration.get("jira_username"),
        token=configuration.get("jira_token"),
    )
    attach_screenshot(driver)

    assert JiraPage(driver).test_valid_creds_xray(
        xray_host=configuration.get("xray_host"),
        xray_id=configuration.get("xray_id"),
        xray_secret_id=configuration.get("xray_secret_id"),
    )
    attach_screenshot(driver)

    JiraPage(driver).click_save()

    driver.back()
    driver.back()

    TestRunsPage(driver).open_latest_test_run()
    assert TestRunPage(driver).is_xray_preview_correct()
    attach_screenshot(driver)
    logger.info("'test_xray_connection' test was finished")


# Test 10
@pytest.mark.maintainer("hpotter")
def test_zephyr_squad_connection(driver):
    logger.info("'test_zephyr_squad_connection' test was started")
    pytest_zebrunner.attach_test_artifact_reference(
        "Zebrunner", "https://zebrunner.com/"
    )
    pytest_zebrunner.attach_test_label("Group", "TCM")
    pytest_zebrunner.attach_test_label("TCM", "Zephyr")
    pytest_zebrunner.attach_test_artifact("../artifacts/txt.txt")
    pytest_zebrunner.attach_test_artifact("../artifacts/zeb.png")
    tcm.TestRail.set_case_id("10")
    tcm.Xray.set_test_key("ZEB-23")
    tcm.Zephyr.set_test_case_key("ZEB-61")

    create_test_run_with_integrations(key, "4", "ZEB-17", "ZEB-55")
    LeftSideMenu(driver).click_integrations_button()

    IntegrationsPage(driver).click_jira_card()
    assert JiraPage(driver).test_valid_creds(
        host=configuration.get("jira_host"),
        username=configuration.get("jira_username"),
        token=configuration.get("jira_token"),
    )
    attach_screenshot(driver)

    assert JiraPage(driver).test_valid_creds_zephyr_squad(
        zephyr_squad_account_id=configuration.get("zephyr_squad_account_id"),
        zephyr_squad_access_key=configuration.get("zephyr_squad_access_key"),
        zephyr_squad_secret_key=configuration.get("zephyr_squad_secret_key"),
    )
    attach_screenshot(driver)

    JiraPage(driver).click_save()

    driver.back()
    driver.back()

    TestRunsPage(driver).open_latest_test_run()
    assert TestRunPage(driver).is_zephyr_squad_preview_correct()
    attach_screenshot(driver)
    logger.info("'test_zephyr_squad_connection' test was finished")


# Test 11
@pytest.mark.maintainer("jhetfield")
def test_testrail_connection(driver):
    logger.info("'test_testrail_connection' test was started")
    pytest_zebrunner.attach_test_artifact_reference(
        "Zebrunner", "https://zebrunner.com/"
    )
    pytest_zebrunner.attach_test_label("Group", "TCM")
    pytest_zebrunner.attach_test_label("TCM", "TestRail")
    pytest_zebrunner.attach_test_artifact("../artifacts/txt.txt")
    pytest_zebrunner.attach_test_artifact("../artifacts/zeb.png")
    tcm.TestRail.set_case_id("11")
    tcm.Xray.set_test_key("ZEB-21")
    tcm.Zephyr.set_test_case_key("ZEB-62")

    create_test_run_with_integrations(key, "4", "ZEB-17", "ZEB-55")
    LeftSideMenu(driver).click_integrations_button()
    IntegrationsPage(driver).click_testrail_card()

    assert TestRailPage(driver).test_valid_creds(
        url=configuration.get("testrail_url"),
        username=configuration.get("testrail_username"),
        password=configuration.get("testrail_password"),
    )
    attach_screenshot(driver)

    TestRailPage(driver).click_save()

    driver.back()
    driver.back()

    TestRunsPage(driver).open_latest_test_run()
    assert TestRunPage(driver).is_testrail_preview_correct()
    attach_screenshot(driver)
    logger.info("'test_testrail_connection' test was finished")
