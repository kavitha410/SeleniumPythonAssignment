from selenium.webdriver.common.by import By

from utilities.base import Base


class HomePage(Base):

    def __init__(self, driver):
        self.driver = driver

    def click_board_tile(self, tile_name):
        """
        Function to add the create new board tile
        :param tile_name: title of the tile present
        """
        self.wait_for_element_present((By.XPATH, "//li//*[text()='{}']".format(tile_name)), 10)
        self.driver.find_element_by_xpath("//li//*[text()='{}']".format(tile_name)).click()
