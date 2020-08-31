from behave import fixture
from selenium import webdriver
from selenium.common import exceptions as sel_excep

from Features.Common.Utils.Ask_Driver import AskWebDriver


def get_selected_driver(browser=None, driver_path=""):
    try:
        if "chromedriver.exe" in driver_path or "Chrome" in browser:
            if driver_path == "":
                selected_webdriver = webdriver.Chrome()
            else:
                selected_webdriver = webdriver.Chrome(executable_path=driver_path)
        elif "geckodriver.exe" in driver_path or "Firefox" in browser:
            if driver_path == "":
                selected_webdriver = webdriver.Firefox()
            else:
                selected_webdriver = webdriver.Firefox(executable_path=driver_path)
        elif "MicrosoftWebDriver.exe" in driver_path or "Edge" in browser:
            if driver_path == "":
                selected_webdriver = webdriver.Edge()
            else:
                selected_webdriver = webdriver.Edge(executable_path=driver_path)
        elif browser == "Safari":
            selected_webdriver = webdriver.Safari()
    except sel_excep.WebDriverException:
        alert_window = AskWebDriver()
        driver_path = alert_window.ask_web_driver_folder_alert()
        selected_webdriver = get_selected_driver(driver_path=driver_path, browser=browser)

    return selected_webdriver


@fixture
def select_driver_from_config(context):
    try:
        browser = context.config.userdata["browser"]
    except KeyError:
        context.config.userdata["browser"] = "Firefox"
        browser = context.config.userdata["browser"]
    context.driver = get_selected_driver(browser=browser)

    yield context.driver

    context.driver.quit()


@fixture
def open_web_page(context, page):
    yield context.driver.get(page)
