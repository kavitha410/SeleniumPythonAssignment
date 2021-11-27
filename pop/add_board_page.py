import time

from selenium.webdriver.common.by import By
from datetime import datetime

from utilities.base import Base


class AddBoardPage(Base):
    add_board_title_txt = (By.CSS_SELECTOR, "input[data-test-id='create-board-title-input']")
    visibility_dropdown_btn = (By.CSS_SELECTOR, "._2UfkIbRfqDCSix._3TTqkG5muwOzqZ._1B-RHqvgdP9uPc._1Tu9wiuW4Te8Rx")
    create_board_btn = (By.CSS_SELECTOR, "button[data-test-id='create-board-submit-button']")
    yes_make_board_public_btn = (By.XPATH, "//button[contains(text(),'make board')]")
    board_name_title_lbl = (By.CSS_SELECTOR, ".js-board-editing-target.board-header-btn-text")

    def __init__(self, driver):
        self.driver = driver

    def add_board(self, visibility):
        """
        Function to add board and handle visibility based on parameter
        :param visibility: visibility options ["Public", "Private","Workspace Visible"]
        """
        time_stamp = datetime.now().strftime("%b-%d-%Y-%H%M%S")
        self.driver.find_element(*self.add_board_title_txt).send_keys("test-board-{}".format(time_stamp))
        self.wait_for_element_present(self.visibility_dropdown_btn, 20)
        current_visibility = self.driver.find_element(*self.visibility_dropdown_btn).text
        print(current_visibility)
        print(current_visibility.strip() not in visibility)
        if current_visibility.strip() != visibility:
            self.driver.find_element(*self.visibility_dropdown_btn).click()
            if visibility == "Private":
                self.driver.find_element_by_xpath("//span[contains(@aria-label, '{}')]".format(visibility)).click()
            elif visibility == "Public":
                self.driver.find_element_by_xpath("//span[contains(@aria-label, '{}')]".format(visibility)).click()
                self.driver.find_element(*self.yes_make_board_public_btn).click()
        time.sleep(2)
        self.driver.find_element(*self.create_board_btn).click()
        return "test-board-{}".format(time_stamp)

    def get_board_name(self):
        """
        Function to get board name/title
        :return: string: return name of the board
        """
        self.wait_for_element_staleness(self.driver.find_element(*self.board_name_title_lbl), 5)
        return self.driver.find_element(*self.board_name_title_lbl).text
