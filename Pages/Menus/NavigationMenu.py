from selenium.webdriver.common.by import By

from Features.Common.SeleniumExtension import SeleniumExtension, Locator


class NavigationMenu:

    def __init__(self, driver):
        self.sel_ext = SeleniumExtension(driver)
        self.driver = driver
        self.PAGE_LOCATOR = Locator(self.driver, By.XPATH, "//a[contains(text(),'All Rights reserved')]")
        self.NAVIGATION_BAR_ID = Locator(self.driver, By.ID, "skip-target-nav-3")
        self.COMPONENT_REFERENCE_MENU_LOCATOR = Locator(self.driver, By.XPATH, "//span[contains(text(),'Component "
                                                                          "Reference')]/..")
        self.DEVELOPER_GUIDE_MENU_LOCATOR = Locator(self.driver, By.XPATH, "//span[contains(text(),'Developer "
                                                                           "Guide')]/..")
        self.LOCKER_CONSOLE_MENU_LOCATOR = Locator(self.driver, By.XPATH,
                                                   "//span[contains(text(),'Locker Console')]/..")
        self.LOCKER_API_MENU_LOCATOR = Locator(self.driver, By.XPATH, "//span[contains(text(),'Locker API Viewer')]/..")
        self.PLAYGROUND_MENU_LOCATOR = Locator(self.driver, By.XPATH, "//span[contains(text(),'Playground')]/..")

    @property
    def page_load_locator(self):
        return self.PAGE_LOCATOR.get_element()

    @property
    def navigation_bar(self):
        return self.NAVIGATION_BAR_ID.get_element()

    @property
    def component_reference_menu(self):
        return self.COMPONENT_REFERENCE_MENU_LOCATOR.get_element()

    def click_comp_ref_menu(self):
        kwargs = self.sel_ext.get_kwargs_from_locator(self.COMPONENT_REFERENCE_MENU_LOCATOR)
        self.sel_ext.wait_and_click(**kwargs)

    @property
    def developer_guide_menu(self):
        return self.DEVELOPER_GUIDE_MENU_LOCATOR.get_element()

    def click_guide_menu(self):
        kwargs = self.sel_ext.get_kwargs_from_locator(self.DEVELOPER_GUIDE_MENU_LOCATOR)
        self.sel_ext.wait_and_click(**kwargs)

    @property
    def locker_console_menu(self):
        return self.LOCKER_CONSOLE_MENU_LOCATOR.get_element()

    def click_locker_console_menu(self):
        kwargs = self.sel_ext.get_kwargs_from_locator(self.DEVELOPER_GUIDE_MENU_LOCATOR)
        self.sel_ext.wait_and_click(**kwargs)

    @property
    def locker_api_menu(self):
        return self.LOCKER_API_MENU_LOCATOR.get_element()

    def click_locker_api_menu(self):
        kwargs = self.sel_ext.get_kwargs_from_locator(self.LOCKER_API_MENU_LOCATOR)
        self.sel_ext.wait_and_click(**kwargs)

    @property
    def playground_menu(self):
        return self.PLAYGROUND_MENU_LOCATOR.get_element()

    def click_playground_menu(self):
        kwargs = self.sel_ext.get_kwargs_from_locator(self.PLAYGROUND_MENU_LOCATOR)
        self.sel_ext.wait_and_click(**kwargs)
