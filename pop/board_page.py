from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

from utilities.base import Base


class BoardPage(Base):
    list_headers = (By.XPATH, "//div[@class='list-header js-list-header u-clearfix is-menu-shown']//textarea")
    add_another_list_btn = (By.XPATH, "//span[text()='Add another list']")
    new_list_name_txt = (By.CSS_SELECTOR, "input[name='name']")
    add_new_list_btn = (By.CSS_SELECTOR, "input[value='Add list']")
    add_card_btn = (By.CSS_SELECTOR, "input[value='Add card']")
    add_card_close_btn = (By.CSS_SELECTOR, ".icon-lg.icon-close.dark-hover.js-cancel-edit")
    add_members_btn = (By.XPATH, "//span[text()='Members']")
    current_logged_in_members_btn = (By.CSS_SELECTOR, ".name.js-select-member")
    members_popup_close_btn = (By.CSS_SELECTOR, ".pop-over-header-close-btn.icon-sm.icon-close")
    comment_txt = (By.CSS_SELECTOR, ".comment-box-input.js-new-comment-input")
    comment_save_btn = (By.CSS_SELECTOR, "input[value=Save]")
    assigned_member_icon = (By.CSS_SELECTOR, ".list-card-members.js-list-card-members .member.js-member-on-card-menu")
    added_comment_lbl = (By.CSS_SELECTOR,
                         ".js-list-actions.mod-card-back .current-comment.js-friendly-links.js-open-card p")
    updated_list_headers = (By.XPATH, "//div[@class='list js-list-content']//h2")
    card_popup_close_btn = (By.CSS_SELECTOR, "a[class='icon-md icon-close dialog-close-button js-close-window']")
    list_add_card_close_btb = (By.CSS_SELECTOR, "a[class='icon-lg icon-close dark-hover js-cancel']")

    def __init__(self, driver):
        self.driver = driver

    def add_list_to_board(self, list_name):
        """
        Function to add list to board
        :param list_name: contain list names as string
        """
        list_names = list_name.split(",")
        loc_list = self.driver.find_elements(*self.list_headers)
        for index in range(len(list_names)):
            if len(loc_list) == 0 or index > 2:
                if not self.driver.find_element(*self.new_list_name_txt).is_displayed():
                    self.driver.find_element(*self.add_another_list_btn).click()
                self.driver.find_element(*self.new_list_name_txt).clear()
                self.driver.find_element(*self.new_list_name_txt).send_keys(list_names[index])
                self.driver.find_element(*self.add_new_list_btn).click()
            else:
                self.driver.find_element_by_xpath("//div[@class='list-header-target js-editing-target'][{index}]".format(index=index+1)).click()
                loc_list[index].clear()
                loc_list[index].send_keys(list_names[index])
        self.driver.find_element(*self.add_card_close_btn).click()

    def add_card_to_list(self, card_name, list_name):
        """
        Function to add cards to list
        :param card_name: Card name to Add in list
        :param list_name: on which list name need to add card
        """
        add_card_btn_ele = self.driver. \
            find_element_by_xpath(
                "//h2[text()='{}']//ancestor::div[@class='list js-list-content']"
                "//span[text()='Add a card']".format(
                    list_name))
        if add_card_btn_ele.is_displayed():
            add_card_btn_ele.click()
        card_names = card_name.split(",")
        for card_name in card_names:
            self.driver. \
                find_element_by_xpath(
                    "//h2[text()='{}']//ancestor::div[@class='list js-list-content']"
                    "//div[@class='list-card-details u-clearfix']//textarea"
                    .format(list_name)).send_keys(card_name)
            self.driver.find_element(*self.add_card_btn).click()
        self.driver.find_element(*self.list_add_card_close_btb).click()

    def move_card_to_list(self, card_name, from_list, to_list):
        """
        Function to move Card from one list to another list
        :param card_name: name of the card want to move
        :param from_list: from which list need to move
        :param to_list: to which list need to move
        """
        source_card = self \
            .driver \
            .find_element_by_xpath("//div[contains(@class,'js-list-header')]//h2[text()='{from_list}']//..//"
                                   "..//span[@class='list-card-title js-card-name' and contains(text(),'{card}')]"
                                   .format(from_list=from_list, card=card_name))
        destination_card = self.driver \
            .find_element_by_xpath("//h2[@class='list-header-name-assist js-list-name-assist' and text()='{}']/.."
                                   .format(to_list))
        action = ActionChains(self.driver)
        action.drag_and_drop(source_card, destination_card).perform()

    def open_card_from_list(self, card_name):
        """
        Function to open card from specified list
        :param card_name: name of the card to open
        """
        self.driver.find_element_by_xpath("//span[contains(@class,'list-card-title') and text()='{card}']".format(card=card_name)).click()

    def assign_member_to_card(self, comment):
        """
        Function to assign member to card
        :param comment: Message string
        """
        self.wait_for_element_present(self.add_members_btn, 15)
        self.driver.find_element(*self.add_members_btn).click()
        self.wait_for_element_present(self.current_logged_in_members_btn, 15)
        self.driver.find_element(*self.current_logged_in_members_btn).click()
        self.driver.find_element(*self.members_popup_close_btn).click()
        self.driver.find_element(*self.comment_txt).send_keys(comment)
        self.driver.find_element(*self.comment_save_btn).click()

    def is_member_icon_added(self):
        """
        Function to check is member icon is displayed after assigned
        :return: boolean
        """
        return self.driver.find_element(*self.assigned_member_icon).is_displayed()

    def get_added_comment(self):
        """
        Function to get added comment as text
        :return: string: return inner HTML string
        """
        output = self.driver.find_element(*self.added_comment_lbl).text
        self.driver.find_element(*self.card_popup_close_btn).click()
        return output

    def get_list_name(self):
        """
        Function to get list name
        :return: string[]: array of list name
        """
        Base.wait_for_element_present(self, self.updated_list_headers, 10)
        loc_list = self.driver.find_elements(*self.updated_list_headers)

        list_title = []
        for loc in loc_list:
            list_title.append(self.driver.execute_script("return arguments[0].innerText", loc))
        return list_title

    def verify_added_list(self, list_name):
        """
        Function to validate the added list and the list from application present
        :param list_name: lists which is added
        """
        expected_list = list_name.split(",")
        actual_list = self.get_list_name()
        assert actual_list == expected_list

    def verify_member_comment_added(self, comment):
        """
        Function to validate the comment given
        :param comment: comment which is given
        """
        is_icon_displayed = self.is_member_icon_added()
        assert is_icon_displayed
        added_comment_text = self.get_added_comment()
        assert added_comment_text == comment, "Added Comment {} is not matched with {} comment in UI" \
            .format(comment, added_comment_text)

