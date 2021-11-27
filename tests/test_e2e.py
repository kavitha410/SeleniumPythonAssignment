from selenium import webdriver

from pop.add_board_page import AddBoardPage
from pop.board_page import BoardPage
from pop.home_page import HomePage
from pop.login_page import LoginPage
from utilities.base import Base


class TestScenario(Base):
    def test_e2e(self):
        loginPage = LoginPage(self.driver)
        loginPage.perform_login("kavipv11@gmail.com", "Welcome123!@")

        homePage = HomePage(self.driver)
        homePage.click_board_tile("Create new board")

        add_board_page = AddBoardPage(self.driver)
        add_board_page.add_board("Public")

        boardPage = BoardPage(self.driver)
        lists = "Not Started,In Progress,QA,Done"
        boardPage.add_list_to_board(lists)

        boardPage.verify_added_list(lists)

        boardPage.add_card_to_list("Card 1,Card 2,Card 3,Card 4", "Not Started")
        boardPage.move_card_to_list("Card 2", "Not Started", "In Progress")

        boardPage.move_card_to_list("Card ", "Not Started", "QA")
        boardPage.move_card_to_list("Card 2", "In Progress", "QA")
        boardPage.open_card_from_list("Card 1")
        boardPage.assign_member_to_card("I am done")

        boardPage.verify_member_comment_added("I am done")




