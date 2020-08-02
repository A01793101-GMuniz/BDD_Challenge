import time

from selenium.webdriver.common.by import By

from Features.Common.SeleniumExtension import SeleniumExtension, Locator, Element
from selenium.webdriver.common.keys import Keys


class PlaygroundPreview:
    def __init__(self, driver):
        self.driver = driver
        self.sel_ext = SeleniumExtension(self.driver
                                         )
        self.PLAYGROUND_IFRAME_LOCATOR = Locator(self.driver, By.XPATH, "//iframe[@name='preview']")

        # This is inside first PLAYGROUND_IFRAME_LOCATOR
        self.SECOND_PREVIEW_IFRAME_LOCATOR = Locator(self.driver, By.XPATH,
                                                     "/html/body/playground-app/main/playground-split"
                                                     "-pane/div/slot/playground-preview/div/iframe["
                                                     "@name='preview']")

        self.FULLY_PLAYGROUND_IFRAME = Locator(self.driver, By.XPATH, "//componentreference-full-playground["
                                                                      "@class='dsc-visible']//iframe")

        self.PREVIEW_TABLE_LOCATOR = Locator(self.driver, By.XPATH, "/html/body/main/c-basic/div/lightning-datatable"
                                                                    "/div[2]/div/div/div/table/tbody/tr[1]")

    @property
    def playground_iframe(self):
        self.sel_ext.wait_for_element(10, **self.sel_ext.get_kwargs_from_locator(self.PLAYGROUND_IFRAME_LOCATOR))
        return self.PLAYGROUND_IFRAME_LOCATOR.get_element()

    @property
    def preview_iframe(self):
        self.sel_ext.wait_for_element(10,
                                      **self.sel_ext.get_kwargs_from_locator(self.SECOND_PREVIEW_IFRAME_LOCATOR))
        return self.SECOND_PREVIEW_IFRAME_LOCATOR.get_element()

    @property
    def preview_table(self):
        self.sel_ext.wait_for_element(10, **self.sel_ext.get_kwargs_from_locator(self.PREVIEW_TABLE_LOCATOR))
        return self.PREVIEW_TABLE_LOCATOR.get_element()


class Datatable:
    def __init__(self, driver):
        self.driver = driver
        self.sel_ext = SeleniumExtension(self.driver)
        self.EXAMPLE_DROPDOWN_LOCATOR = Locator(self.driver, By.XPATH, "//div[@class='slds-combobox__form-element "
                                                                       "slds-input-has-icon "
                                                                       "slds-input-has-icon_right']/..")

        self.EXAMPLE_DROPDOWN_INPUT_LOCATOR = Locator(self.driver, By.XPATH,
                                                      "//div[@class='slds-combobox__form-element "
                                                      "slds-input-has-icon "
                                                      "slds-input-has-icon_right']/input")

        # PlayGround PreviewSection on Datatable
        self.PLAYGROUND_BUTTON_LOCATOR = Locator(self.driver, By.XPATH, "//button[text()='Open in Playground']")

    @property
    def example_dropdown(self):
        self.sel_ext.wait_for_element(10, **self.sel_ext.get_kwargs_from_locator(self.EXAMPLE_DROPDOWN_LOCATOR))
        return self.EXAMPLE_DROPDOWN_LOCATOR.get_element()

    @property
    def example_dropdown_input(self):
        self.sel_ext.wait_for_element(10, **self.sel_ext.get_kwargs_from_locator(self.EXAMPLE_DROPDOWN_INPUT_LOCATOR))
        return self.EXAMPLE_DROPDOWN_INPUT_LOCATOR.get_element()

    @property
    def playground_button(self):
        self.sel_ext.wait_for_element(10, **self.sel_ext.get_kwargs_from_locator(self.EXAMPLE_DROPDOWN_LOCATOR))
        return self.PLAYGROUND_BUTTON_LOCATOR.get_element()

    def get_current_aria_descendant(self):
        Element(self.example_dropdown).aria_dropdown_open(self.driver, self.example_dropdown)
        current = self.example_dropdown_input.get_attribute('aria-activedescendant')
        time.sleep(2)
        return int(current.split("-")[2])

    def select_aria_descendant(self, value):
        example_options = {"Basic Data Table": 0,
                           "Data Table with Row Numbers": 1,
                           "Data Table with Row Actions": 2,
                           "Data Table with Inline Edit": 3,
                           "Data Table with Sortable Columns": 4}
        return example_options[value]

    def NavigateUp(self, movement_keys):
        Element(self.example_dropdown).aria_dropdown_open(self.driver, self.example_dropdown)
        for i in range(0, movement_keys + 1):
            self.example_dropdown_input.send_keys(Keys.UP)
        self.example_dropdown_input.send_keys(Keys.ENTER)
        time.sleep(2)

    def NavigateDown(self, movement_keys):
        Element(self.example_dropdown).aria_dropdown_open(self.driver, self.example_dropdown)
        for i in range(0, movement_keys + 1):
            self.example_dropdown_input.send_keys(Keys.DOWN)
        self.example_dropdown_input.send_keys(Keys.ENTER)
        time.sleep(2)

    def wait_for_preview_frame_to_load(self, preview_section):
        self.driver.switch_to.frame(preview_section.playground_iframe)
        kwargs = self.sel_ext.get_kwargs_from_locator(preview_section.SECOND_PREVIEW_IFRAME_LOCATOR)
        self.sel_ext.wait_for_element(60, **kwargs)
        self.driver.switch_to.frame(preview_section.preview_iframe)
        kwargs = self.sel_ext.get_kwargs_from_locator(preview_section.PREVIEW_TABLE_LOCATOR)
        self.sel_ext.wait_for_element(10, **kwargs)
        self.driver.switch_to.default_content()

    def choose_example_dropdown_value(self, value):
        # locator_id = self.example_dropdown.get_attribute('id')
        # self.driver.execute_script("arguments[0].setAttribute('aria-activedescendant', arguments[1]);",
        #                            Element(self.example_dropdown).we, f"input-214-{locator_id}-214")
        preview_section = PlaygroundPreview(self.driver)
        self.wait_for_preview_frame_to_load(preview_section)

        current_value = self.get_current_aria_descendant()
        choosen_value = self.select_aria_descendant(value)
        movement_keys = choosen_value - current_value
        if movement_keys < 0:
            self.NavigateUp(abs(movement_keys))
        elif movement_keys > 0:
            self.NavigateDown(movement_keys)

    def click_playground_button(self):
        Element(self.playground_button).click(self.driver)
