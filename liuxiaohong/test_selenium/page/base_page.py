from time import sleep

from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver


class BasePage:
    _base_url = ""
    _driver = None

    def __init__(self,driver: WebDriver = None,reuse=False):
        if driver is None:
            if reuse:
                options = webdriver.ChromeOptions()
                options.debugger_address = "127.0.0.1:9222"
                self._driver = webdriver.chrome(options=options)
            else:
                self._driver = webdriver.Chrome()
            self._driver.implicitly_wait(3)
        else:
            self._driver = driver
        self._driver.maximize_window()

        if self._base_url !="":
            self._driver.get(self._base_url)

    def find(self, by, locator=""):
        if isinstance(by, tuple):
            return self._driver.find_element(*by)
        else:
            return self._driver.find_element(by, locator)

    def close(self):
        sleep(20)
        self._driver.quit()