import pytest
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


@pytest.mark.usefixtures("setup")
class Base:

    def wait_for_element_present(self, locator, seconds):
        """
        Function to wait for element present
        :param locator: By: locator
        :param seconds: time in seconds
        """
        wait = WebDriverWait(self.driver, int(seconds))
        wait.until(ec.presence_of_element_located(locator))

    def wait_for_element_clickable(self, locator, seconds):
        """
        Function to wait for element present
        :param locator: By: locator
        :param seconds: time in seconds
        """
        wait = WebDriverWait(self.driver, int(seconds))
        wait.until(ec.element_to_be_clickable(locator))

    def wait_for_element_staleness(self, locator, seconds=15):
        """
        Function to wait for element present
        :param locator: By: locator
        :param seconds: time in seconds
        """
        wait = WebDriverWait(self.driver, int(seconds))
        wait.until(ec.staleness_of(locator))
