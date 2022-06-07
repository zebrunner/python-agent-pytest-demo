from selenium.webdriver.common.by import By

from service.PageElements.ModalWindowBase import ModalWindowBaseLocators


class NewDashboardModalLocators(ModalWindowBaseLocators):
    NEW_DASHBOARD_MODAL_WINDOW = (By.XPATH, "//md-dialog[@aria-label='Dashboard settings']")
    NAME_FIELD = (By.XPATH, "//input[@name='title']")
