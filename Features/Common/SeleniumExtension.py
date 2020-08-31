import re
import time
from typing import List

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver
import selenium.common.exceptions  as sel_exceptions
from selenium.webdriver.common.by import By

_LOCATOR_MAP = {'css selector': By.CSS_SELECTOR,
                'id_': By.ID,
                'id': By.ID,
                'name': By.NAME,
                'xpath': By.XPATH,
                'link_text': By.LINK_TEXT,
                'partial_link_text': By.PARTIAL_LINK_TEXT,
                'tag_name': By.TAG_NAME,
                'class_name': By.CLASS_NAME,
                }


class Element:

    def __init__(self, we):
        self.parent = getattr(we, "parent", None)
        if isinstance(we, Element):
            self.we = we.we
        elif isinstance(we, WebDriver):
            self.parent = we
        else:
            try:
                self.we = we
            except AttributeError:
                pass

    def find_element(self, by_=By.ID, value=None, locator=None):
        # Used in wrapper to find Element using parent: WebDriver
        if isinstance(by_, Locator):
            locator = by_
        if locator is not None:
            by_ = locator.by
            value = locator.value
        # Wrapped WebElement using Find Element of WebDriver Classed with parameters extracted from Class
        return Element(self.we.find_element(by_, value))

    def find_elements(self, by=By.ID, value=None, locator=None):
        if isinstance(by, Locator):
            locator = by
        if locator is not None:
            by = locator.by
            value = locator.value
        elements = self.we.find_elements(by, value)
        return list(map(lambda web_element: Element(web_element), elements))

    def clear_and_send_keys(self, *value):
        try:
            self.we.clear()
            self.we.send_keys(str(*value))
        except sel_exceptions.InvalidElementStateException:
            Exception("Invalid Element State")

    def get_attribute(self, attribute):
        return self.we.get_attribute(attribute)

    def click(self, driver):
        try:
            self.we.click()
        except sel_exceptions.JavascriptException:
            driver.execute_script("arguments[0].click();", self.we)

    def send_keys(self, keys):
        self.we.send_keys(keys)

    def aria_dropdown_open(self, driver, aria_dropdown):
        Element(aria_dropdown).click(driver)
        driver.execute_script("arguments[0].setAttribute('aria-expanded', arguments[1]);",Element(aria_dropdown).we,
                              "true")

    def highlight(self, driver, element):
        original_style = element.get_attribute('style')
        highlight_style = "border: 2px solid red !important;"
        driver.execute_script("arguments[0].setAttribute('style', arguments[1]);",
                                   Element(element).we, original_style + highlight_style)
        time.sleep(2)
        driver.execute_script("arguments[0].setAttribute('style', arguments[1]);",
                              Element(element).we, original_style)


class Locator:
    def __init__(self, driver, by: str, value: str, child_of=None):
        self.driver = driver
        self._driver = driver if driver is not None else self._driver
        self._index = None
        self.by_ = by
        self._by = by
        self.value_ = value
        self.child_of = child_of

    @property
    def by(self):
        if self.value_.__contains__("{idx}") or self.value_.__contains__("|"):
            if self.by_ == By.ID:
                self._by = By.XPATH
        return self._by

    @by.setter
    def by(self, value):
        self._by = value

    @property
    def index(self):
        return self._index

    @index.setter
    def index(self, value: int):
        self._index = value

    @property
    def value(self):
        # This will format the XPATHin case path contains an id with multiple elements like "data_table_id1 = xxx "
        formatted_value = self.value_

        return formatted_value

    # To Format the element received on the LOCATOR_MAP and send it as a SEL_EXT Object to find it
    def get_element(self) -> Element:
        # If there's no index on the element I use find element
        if self.index is None:
            if self.child_of is None:
                return SeleniumExtension(self._driver).find_element(self)
            else:
                if isinstance(self.child_of, Element):
                    return self.child_of.find_element(self)
                return SeleniumExtension(self._driver).find_element(self.child_of).find_element(self)
        else:
            return self.get_elements[self.index]

    def get_elements(self) -> List[Element]:
        if self.child_of is None:
            return SeleniumExtension(self._driver).find_elements(self)
        else:
            if isinstance(self.child_of, Element):
                return self.child_of.find_elements(self)
            return SeleniumExtension(self._driver).find_element(self.child_of).find_elements(self)


class SeleniumExtension:

    def __init__(self, driver):
        self.driver = driver

    def get_element(self, by_, value_):
        try:
            # Web Element find_element Method
            element = self.driver.find_element(by_, value_)
            # Return Web Element Wrapped
            return Element(element).we
        except sel_exceptions.NoSuchElementException:
            raise
        except Exception("Element does not exist"):

            raise

    def get_elements(self, by_, value_):
        try:
            try:
                web_elements = self.driver.find_elements(by=by_, value=value_)
            except:
                web_elements = self.driver.find_elements(by=by_, value=value_)
            elements = []
            for web_element in web_elements:
                elements.append(Element(web_element).we)
            return elements
        except sel_exceptions.NoSuchElementException:
            Exception("Element is not visible")

    def find_element(self, by_=By.ID, value=None, locator: Locator = None):
        # Get Element using get element on a Element object
        if isinstance(by_, Locator):
            locator = by_
        if locator is not None:
            by_ = locator.by
            value = locator.value

        return self.get_element(by_, value)

    def find_elements(self, by=By.ID, value_=None, locator: Locator = None):
        if locator is not None:
            by = locator.by
            value_ = locator.value
        if isinstance(by, Locator):
            value_ = by.value
            by = by.by
        return self.get_elements(by, value_)

    @staticmethod
    def get_locator(kwargs):
        if not kwargs:
            raise ValueError("A parameter/Locator is Missing")

        # If the key arguments are inside a dict
        if isinstance(kwargs, dict):
            by_ = kwargs["by"]
            value = kwargs["value"]
            return by_, value

        # if they are not in a dict but it has 2 or more locators
        if len(kwargs) > 1:
            raise ValueError("Please specify only one locator")

        # If the key args are inside a Locator object
        if isinstance(kwargs, Locator):
            by_ = kwargs.by
            value = kwargs.value
            return by_, value

    def wait_for_element(self, appear_timeout=10, **kwargs):
        try:
            k, value = self.get_locator(kwargs)
            WebDriverWait(self, appear_timeout).until(EC.presence_of_element_located((_LOCATOR_MAP[k], value)))
            WebDriverWait(self, appear_timeout).until(EC.visibility_of_element_located((_LOCATOR_MAP[k], value)))
            WebDriverWait(self, appear_timeout).until(EC.element_to_be_clickable((_LOCATOR_MAP[k], value)))
            #if "preview" in value:
            #    time.sleep(5)
            return self.find_element(_LOCATOR_MAP[k], value)
        except sel_exceptions.TimeoutException:
            return f"Element not present after {appear_timeout}"

    def wait_and_click(self, driver, by, value):
        kwargs = {"by": by,
                  "value": value}
        Element(self.wait_for_element(10, **kwargs)).click(driver)

    def get_kwargs_from_locator(self,locator):
        kwargs = {"by": locator.by,
                  "value": locator.value}
        return kwargs

    # def click_and_wait_element(self, driver, element_to_click, element_to_wait):
    #     element_to_click.click(driver)
    #     kwargs = self.get_kwargs_from_locator(element_to_wait.WAIT_ELEMENT_LOCATOR)
    #     self.wait_for_element(10, **kwargs)
    #     return


