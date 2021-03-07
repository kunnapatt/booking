import requests
import json
from bs4 import BeautifulSoup
import re

def main() :
    dict_item = {}
    for i in range(1, 73) :
        url = f"https://www.phoenixnext.com/book-series.html?p={i}"
        r = requests.get(url)
        print(r)

        soup = BeautifulSoup(r.content, "html.parser")
        # print(soup.find_all('a'))
        # print(soup.find_all('a', class_="product-item-link"))
        for el in soup.find_all('a', class_="product-item-link") :
            title = el.get("title")
            link = el.get("href")

            type_item, book = title.split(" ", 1)
            name, num_book = book.split(" เล่ม ")
            print(type_item, name, num_book)
            if type_item not in dict_item :
                dict_item[type_item] = {}
            if name not in dict_item[type_item] :
                dict_item[type_item][name] = {}
            if book not in dict_item[type_item][name] :
                dict_item[type_item][name] = {num_book: link}

    pass

if __name__ == "__main__" :
    main()