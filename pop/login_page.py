import time

from selenium.webdriver.common.by import By

from utilities.base import Base


class LoginPage(Base):
    username_txt = (By.CSS_SELECTOR, "#user")
    password_txt = (By.CSS_SELECTOR, "#password")
    login_with_atlassian_btn = (By.CSS_SELECTOR, "#login")
    login_btn = (By.CSS_SELECTOR, "#login-submit")

    def __init__(self, driver):
        self.driver = driver

    def perform_login(self, username, password):
        """
        Function to handle login to the Application
        :param self: driver: browser instance
        :param username: username passed as parameter
        :param password: password passed as parameter
        """
        self.driver.find_element(*self.username_txt).send_keys(username)
        self.driver.find_element(*self.login_with_atlassian_btn).click()
        self.wait_for_element_present(self.login_btn, 30)
        self.driver.find_element(*self.password_txt).send_keys(password)
        self.driver.find_element(*self.login_btn).click()
