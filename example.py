import selenium as sn
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json
import time
import sys
import os

class AutomateBuy:
    def __init__(self):
        web = "phoenixnext"
        self.define_variable(web)
        self.setUp()

        self.login()
        
        self.to_book_link(self.list_link_buy)
        # time.sleep(10)
        self.driver.switch_to.window(self.driver.window_handles[0])
        self.driver.get(self.config["cart_url"])
        while True :
            pass
        

    def define_variable(self, web) :  
        self.config = self.get_config(web)
        self.user_json = self.read_json(self.config["file-json"])

        self.chrome_option = Options()
        self.chrome_option.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome()

        if web.startswith("phoenix") :
            self.data_link = self.read_json("data.json")
        # print(self.data_link)

        self.name_book = ["ขอต้อนรับ", "อุตส่าห์มีคนมาชอบ"]
        self.type_book = "LN"
        self.books = [[1, 2, 3, 4], [1, 2, 3]]
        self.list_link_buy = []
        for i in range(len(self.name_book)) :
            for k, v in self.data_link[self.type_book].items() :
                if k.startswith(self.name_book[i]) :
                    for nb in self.books[i] :
                        try :
                            link_book = v[str(nb)]
                            self.list_link_buy.append(link_book)
                        except KeyError :
                            print(f"Doesn't exists book {k} {nb} in categorical {self.type_book}")
                    ### case search name book match with name book in data
                    if self.name_book is k :
                        break

        print(self.list_link_buy)

    def read_json(self, path) :
        with open(path, "r", encoding="utf-8") as f :
            json_file = json.load(f)
        return json_file

    def get_config(self, booking) :
        config = {
            "file-json": "user-detail.json",
            **self.get_attribute_on(booking)
        }
        return config 

    def setUp(self) :
        self.driver.maximize_window()
        self.driver.get(self.config["base_url"])

    def login(self) :
        self.driver.get(self.config["login_url"])

        username = self.driver.find_element_by_name(self.config["el_username"])
        password = self.driver.find_element_by_name(self.config["el_password"])

        username.send_keys(self.user_json["username"])
        password.send_keys(self.user_json["password"])

        btn = self.driver.find_element_by_xpath(self.config["login_btn"])
        btn.click()

        self.driver.implicitly_wait(50)
        self.current_url = self.driver.current_url

    def to_book_link(self, l_book_buy) :
        for i in range(len(l_book_buy)) :
            self.create_tab(i)
            self.switch_tab_browser(i)
            self.driver.get(l_book_buy[i])
            self.add_to_cart()
            print(f"link {l_book_buy[i]} add to cart success.")

    def to_name_url(self, name, books) :
        # mangaqube
        # self.driver.get(f"{self.config['base_url']}s/{name}/")
        # self.driver.implicitly_wait(30)
        print(self.driver.current_url)

        for i in range(len(books)) :
            print(books[i])
            self.create_tab(f"tab{i}")
            self.driver.find_element_by_partial_link_text(f"{name} {books[i]}")

    def create_tab(self, name) :
        self.driver.execute_script(f"window.open('about:blank', '{name}');")

    def switch_tab_browser(self, name) :
        self.driver.switch_to.window(str(name)) 

    def get_attribute_on(self, web) :
        attributes = {}
        if "phoenixnext" in web :
            attributes["el_username"] =  "login[username]"
            attributes["el_password"] = "login[password]"
            attributes["base_url"] = "https://www.phoenixnext.com/"
            attributes["login_url"] = f"{attributes['base_url']}customer/account/login/"
            attributes["login_btn"] = "//button[@class='action login primary']"
            attributes["parent_cart_btn"] = "//div[@class='attr-info']"
            attributes["add_to_cart_btn"] = "//button[@class='action primary tocart addcart-link']"
            attributes["cart_url"] = "https://www.phoenixnext.com/checkout/cart/"
        elif "mangaque" in web :
            attributes["el_username"] = "username"
            attributes["el_password"] = "password"
            attributes["base_url"] = "https://www.mangaqube.com/"
            attributes["login_url"] = f"{attributes['base_url']}account/?redirect=%2F"
            attributes["login_btn"] = "//button[@class='ui fluid blue account__login__button submit button']"
        
        return attributes

    def add_to_cart(self) :
        btn = self.driver.find_element_by_xpath(self.config["add_to_cart_btn"])
        btn.click()
        self.driver.implicitly_wait(50)
        # time.sleep(3)

def main() :
    a = AutomateBuy()

if __name__ == "__main__" :
    main()