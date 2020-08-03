from behave import fixture, use_fixture
from selenium import webdriver


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
