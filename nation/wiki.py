# coding: utf-8

from urllib.parse import quote
from selenium import webdriver

def get_text(name):
    driver = webdriver.PhantomJS()
    driver.get("https://ja.wikipedia.org/wiki/{}".format(quote(name)))
    text = driver.find_element_by_id("content").text
    if text.find("ウィキペディアには現在この名前の項目はありません。") != -1:
        return None
    return text
