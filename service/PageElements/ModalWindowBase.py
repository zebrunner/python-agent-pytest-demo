from selenium.webdriver.common.by import By


class ModalWindowBaseLocators:
    MODAL_WINDOW_LOCATOR = (By.XPATH, "//md-dialog[contains(@class, 'modal')]")

    CANCEL_BUTTON = (
        By.XPATH,
        "//button[contains(@class, 'md-raised md-button md-ink-ripple')]",
    )
    SUBMIT_BUTTON = (By.XPATH, "//button[contains(@class, 'md-raised md-primary')]")
    CLOSE_BUTTON = (By.ID, "close")
    DELETE_BUTTON = (By.XPATH, "//span[text()='delete']//parent::button")

    PROJECT_NAME_FIELD = (By.ID, "projectName")
    PROJECT_KEY_FIELD = (By.ID, "projectKey")

    RADIO_BUTTONS_GROUP = (By.XPATH, "//md-radio-group")
    RADIO_BUTTON_ITEM = (By.XPATH, "//md-radio-button")
