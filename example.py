import selenium as sn
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json
import time
import sys
import os

class AutomateBuy:
    def __init__(self):
        self.define_variable()
        self.setUp()

        self.login()
        time.sleep(10)

    def define_variable(self) :  
        self.config = self.get_config("phoenixnext")
        self.user_json = self.read_json(self.config["file-json"])

        self.chrome_option = Options()
        self.chrome_option.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome()

        self.name_book = "โฉมงามพูดไม่เก่งกับผองเพื่อนไม่เต็มเต็ง"
        self.books = [1, 2, 3, 4]

    def read_json(self, path) :
        with open(path, "r") as f :
            json_file = json.load(f)
        return json_file

    def get_config(self, booking) :
        config = {
            "file-json": "user-detail.json",
        }
        (
            config["username"], 
            config["password"], 
            config["base_url"], 
            config["login_url"],
            config["login_btn"]
        ) = self.get_attribute_on(booking)
        return config 

    def setUp(self) :
        self.driver.maximize_window()
        self.driver.get(self.config["base_url"])

    def login(self) :
        self.driver.get(self.config["login_url"])

        username = self.driver.find_element_by_name(self.config["username"])
        password = self.driver.find_element_by_name(self.config["password"])

        username.send_keys(self.user_json["username"])
        password.send_keys(self.user_json["password"])

        btn = self.driver.find_element_by_xpath(self.config["login_btn"])
        btn.click()

        time.sleep(2)
        self.driver.implicitly_wait(50)
        self.current_url = self.driver.current_url


    def to_name_url(self, name, books) :
        self.driver.get(f"{self.config['base_url']}s/{name}/")
        self.driver.implicitly_wait(30)
        print(self.driver.current_url)

        for i in range(len(books)) :
            print(books[i])
            self.create_tab(f"tab{i}")
            self.driver.find_element_by_partial_link_text(f"{name} {books[i]}")

    def create_tab(self, name) :
        self.driver.execute_script(f"window.open('about:blank', '{name}');")

    def switch_tab_browser(self, name) :
        self.driver.switch_to.window(name) 

    def get_attribute_on(self, web) :
        if "phoenixnext" in web :
            el_username =  "login[username]"
            el_password = "login[password]"
            base_url = "https://www.phoenixnext.com/"
            login_url = "https://www.phoenixnext.com/customer/account/login/"
            login_btn = "//button[@class='action login primary']"
        elif "mangaque" in web :
            el_username = "username"
            el_password = "password"
            base_url = "https://www.mangaqube.com/"
            login_url = f"{base_url}account/?redirect=%2F"
            login_btn = "//button[@class='ui fluid blue account__login__button submit button']"
        
        return el_username, el_password, base_url, login_url, login_btn

def main() :
    a = AutomateBuy()

if __name__ == "__main__" :
    main()