from selenium.webdriver.common.by import By

from test_selenium.page.base_page import BasePage
from test_selenium.page.register import Register


class Login(BasePage):
    def goto_regitstry(self):
        self.find((By.LINK_TEXT, "企业注册")).click()
        return Register(self._driver)

    def scan_qrcode(self):
        pass