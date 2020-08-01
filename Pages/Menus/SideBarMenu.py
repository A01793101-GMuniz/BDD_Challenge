from selenium.webdriver.common.by import By

from Features.Common.SeleniumExtension import SeleniumExtension, Locator, Element


class SideBarMenu:
    def __init__(self, driver):
        self.driver = driver
        self.sel_ext = SeleniumExtension(self.driver)
        self.SIDEBAR_MENU_SECTION_LOCATOR = Locator(self.driver, By.XPATH, "//section[@class='slds-grid "
                                                                           "slds-grid_vertical sidebar-content']")
        self.QUICK_SEARCH_LOCATOR = Locator(self.driver, By.XPATH, "//input[@placeholder='Quick Find']")
        self.LIGHTNING_QS_RESULTS_LOCATOR = Locator(self.driver, By.XPATH, "//h4[contains(@id,"
                                                                           "'treeheading')]/..//div[1]")

    @property
    def side_bar_menu_locator(self):
        return self.SIDEBAR_MENU_SECTION_LOCATOR.get_element()

    @property
    def quick_search_menu(self):
        return self.QUICK_SEARCH_LOCATOR.get_element()

    @quick_search_menu.setter
    def quick_search_menu(self, value):
        self.sel_ext.wait_for_element(10, **self.sel_ext.get_kwargs_from_locator(self.QUICK_SEARCH_LOCATOR))
        if value is not None:
            Element(self.quick_search_menu).clear_and_send_keys(value)

    @property
    def lighting_component_quick_search_results(self):
        return self.LIGHTNING_QS_RESULTS_LOCATOR.get_elements()[0].find_elements(By.XPATH,
                                                                                 "following-sibling::div"
                                                                                 "//componentreference-tree-item")

    def click_lighting_component(self, value):
        try:
            self.driver.implicitly_wait(2)
            for element in self.lighting_component_quick_search_results:
                if value == element.text:
                    element.click()
        except:
            Exception(f"Quick Search got no results for {value}")
