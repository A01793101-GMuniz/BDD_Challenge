from behave import fixture, use_fixture
from selenium import webdriver


class InitialConfig:

    def __init__(self, path, features, browser):
        self.feature_path = path
        self.features_to_run = features
        self.browser_to_run = browser



@fixture
def select_driver_from_config(context):
    browser = context.config.userdata["browser"]
    if browser == "Chrome":
        context.driver = webdriver.Chrome()
    elif browser == "Edge":
        context.driver = webdriver.Edge()
    elif browser == "Safari":
        context.driver = webdriver.Safari()
    else:
        context.driver = webdriver.Firefox()

    yield context.driver

    context.driver.quit()


@fixture
def open_web_page(context, page):
    yield context.driver.get(page)
