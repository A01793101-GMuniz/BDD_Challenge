import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common import exceptions as sel_exc

from Features.Common.SeleniumExtension import SeleniumExtension, Locator, Element


class Playground:

    def __init__(self, driver):
        self.driver = driver
        self.sel_ext = SeleniumExtension(self.driver)
        self.FULL_PLAYGROUND_MAIN_IFRAME_LOCATOR = \
            Locator(self.driver, By.XPATH, "//componentreference-full-playground[@class='dsc-visible']//iframe")

        self.FULL_PLAYGROUND_PREVIEW_TABLE_IFRAME_LOCATOR = \
            Locator(self.driver, By.XPATH, "/html/body/playground-app/playground-header/div/div["
                                           "2]/slot/main/playground-splitter/div{idx}/slot/playground-split-pane/div["
                                           "3]/slot/playground-preview/div[2]/iframe")

        self.FULL_PLAYGROUND_DATA_TABLE = Locator(self.driver, By.XPATH, "/html/body/main/c-withinlineedit/div"
                                                                         "/lightning-datatable/div["
                                                                         "2]/div/div/div/table/tbody/tr")

        self.FULL_PLAYGROUND_ON_EDIT_INPUT_LOCATOR = \
            Locator(self.driver, By.XPATH, "/html/body/main/c-withinlineedit/div/lightning-datatable/div["
                                           "2]/lightning-primitive-datatable-iedit-panel/section"
                                           "/div/form/lightning-primitive-datatable-iedit-input-wrapper"
                                           "/slot/lightning-primitive-datatable-iedit-type-factory"
                                           "/lightning-input/div/input")

        self.DATE_PICKER_LOCATOR = \
            Locator(self.driver, By.XPATH, "/html/body/main/c-withinlineedit/div/lightning-datatable/div["
                                           "2]/lightning-primitive-datatable-iedit-panel/section/div["
                                           "1]/form/lightning-primitive-datatable-iedit-input-wrapper//input")

        self.TIME_PICKER_LOCATOR = \
            Locator(self.driver, By.XPATH, "/html/body/main/c-withinlineedit/div/lightning-datatable/div["
                                           "2]/lightning-primitive-datatable-iedit-panel/section/div["
                                           "1]/form/lightning-primitive-datatable-iedit-input-wrapper//lightning"
                                           "-timepicker//input")


    @property
    def full_playground_iframe(self):
        self.sel_ext.wait_for_element \
            (10, **self.sel_ext.get_kwargs_from_locator(self.FULL_PLAYGROUND_MAIN_IFRAME_LOCATOR))
        return self.FULL_PLAYGROUND_MAIN_IFRAME_LOCATOR.get_element()

    @property
    def full_playground_preview_table_iframe(self):
        self.sel_ext.wait_for_element \
            (40, **self.sel_ext.get_kwargs_from_locator(self.FULL_PLAYGROUND_PREVIEW_TABLE_IFRAME_LOCATOR))
        return self.FULL_PLAYGROUND_PREVIEW_TABLE_IFRAME_LOCATOR.get_element()

    @property
    def full_playground_data_table(self):
        self.sel_ext.wait_for_element \
            (10, **self.sel_ext.get_kwargs_from_locator(self.FULL_PLAYGROUND_DATA_TABLE))
        return self.FULL_PLAYGROUND_DATA_TABLE.get_elements()

    @property
    def full_playground_on_edit_input(self):
        self.sel_ext.wait_for_element \
            (10, **self.sel_ext.get_kwargs_from_locator(self.FULL_PLAYGROUND_ON_EDIT_INPUT_LOCATOR))
        return self.FULL_PLAYGROUND_ON_EDIT_INPUT_LOCATOR.get_element()

    @full_playground_on_edit_input.setter
    def full_playground_on_edit_input(self, value):
        if value is not None:
            Element(self.full_playground_on_edit_input).clear_and_send_keys(value)

    @property
    def date_picker_input(self):
        self.sel_ext.wait_for_element \
            (10, **self.sel_ext.get_kwargs_from_locator(self.DATE_PICKER_LOCATOR))
        return self.DATE_PICKER_LOCATOR.get_element()

    @date_picker_input.setter
    def date_picker_input(self, value):
        if value is not None:
            Element(self.date_picker_input).clear_and_send_keys(value)

    @property
    def time_value_input(self):
        self.sel_ext.wait_for_element \
            (10, **self.sel_ext.get_kwargs_from_locator(self.TIME_PICKER_LOCATOR))
        return self.TIME_PICKER_LOCATOR.get_element()

    @time_value_input.setter
    def time_value_input(self, value):
        if value is not None:
            Element(self.time_value_input).clear_and_send_keys(value)

    @property
    def browser(self):
        return self.driver.capabilities["browserName"].capitalize()

    def edit_row(self, new_row_data):
        self.driver.switch_to.frame(self.full_playground_iframe)
        kwargs = self.sel_ext.get_kwargs_from_locator(self.FULL_PLAYGROUND_PREVIEW_TABLE_IFRAME_LOCATOR)
        self.sel_ext.wait_for_element(60, **kwargs)
        self.driver.switch_to.frame(self.full_playground_preview_table_iframe)
        if new_row_data["id"] > 9:
            for i in range (9, new_row_data["id"] - 2):
                self.full_playground_data_table[i].send_keys(Keys.DOWN)
        row_element = Element(self.full_playground_data_table[new_row_data["id"]]).we
        dict_of_td_editable_columns = {2: "Label",
                                       3: "Website",
                                       4: "Phone",
                                       5: "CloseAt",
                                       6: "Balance"}
        i = 0
        after_edit_data_values = {}
        before_edit_data_values = {}
        for element in row_element.find_elements(By.XPATH, "th | td"):
            if element.tag_name == "th" and "Label" in new_row_data.keys():
                before_edit_data_values.update({"Label": element.text.split("\n")[0]})
                value_to_edit = new_row_data["Label"]
                element_edited_validator = self.edit_table_column_values(element, value_to_edit)
                if element_edited_validator:
                    after_edit_data_values.update({"Label": value_to_edit})

            elif element.tag_name == "td" and "Edit" in element.text:

                if dict_of_td_editable_columns[i] in new_row_data.keys():
                    before_edit_data_values.update({dict_of_td_editable_columns[i]: element.text.split("\n")[0]})
                    if i == 5:
                        date_value = new_row_data[dict_of_td_editable_columns[i]].split("-")[0]
                        time_value = new_row_data[dict_of_td_editable_columns[i]].split("-")[1]
                        element_edited_validator = self.edit_table_column_values(element, date_value, time_value, i)
                        value_to_edit = date_value + "-" + time_value
                    else:
                        before_edit_data_values.update({dict_of_td_editable_columns[i]: element.text.split("\n")[0]})
                        value_to_edit = new_row_data[dict_of_td_editable_columns[i]]
                        element_edited_validator = self.edit_table_column_values(element, value_to_edit)

                    if element_edited_validator:
                        after_edit_data_values.update({dict_of_td_editable_columns[i]: value_to_edit})
            i += 1

        return before_edit_data_values, after_edit_data_values

    def edit_table_column_values(self, element, value_to_edit, time_value=None, i=None):
        self.lightning_primitive_cell_factory = \
            element.find_element(By.XPATH, "lightning-primitive-cell-factory")
        self.element_edit_button = \
            element.find_element(By.XPATH, "lightning-primitive-cell-factory/span/button")
        Element(self.element_edit_button).click(self.driver)
        self.driver.execute_script("arguments[0].setAttribute('aria-selected', arguments[1]);",
                                   Element(self.lightning_primitive_cell_factory).we, "true")

        if self.lightning_primitive_cell_factory.get_attribute('aria-selected') == "true":
            if i != 5:
                self.full_playground_on_edit_input = value_to_edit
                self.full_playground_on_edit_input.send_keys(Keys.TAB)
            else:
                self.date_picker_input = value_to_edit
                self.time_value_input = time_value
                self.time_value_input.send_keys(Keys.TAB)
                if self.driver.capabilities["browserName"].capitalize() == "Firefox":
                    try:
                        self.time_value_input.send_keys(Keys.TAB)
                    except sel_exc.NoSuchElementException:
                            pass
            time.sleep(2)

            return True


