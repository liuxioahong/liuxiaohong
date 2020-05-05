import logging

import yaml
from appium.webdriver import WebElement
from appium.webdriver.webdriver import WebDriver
from selenium.webdriver.common.by import By


class BasePage:
    logging.basicConfig(level=logging.INFO)

    _driver: WebElement
    _black_list = [
        (By.ID, 'tv_agree'),
        (By.XPATH, '//*[@text="确定"]'),
        (By.ID, 'image_cancel'),
        (By.XPATH, '//*[@text="下次再说"]')
    ]

    _error_max = 10
    _error_count = 0

    _params = {}

    def __init__(self, driver: WebDriver = None):
        self._driver = driver

    def find(self, locator, value:str = None):
        logging.info(locator)
        logging.info(value)

        try:
            # 寻找控件
            element = self._driver.find_element(*locator) if isinstance(locator,tuple) else self._driver.find_element(
                locator,value)
            self._error_count = 0
        except Exception as e:
            # 如果异常次数太多，就退出
            if self._error_count > self._error_max:
                raise e
            self._error_count += 1

            # 对黑名单中的弹框进行处理
            for element in self._black_list:
                logging.info(element)
                elements = self._driver.find_elements(*element)
                if len(elements) > 0:
                    elements[0].click()
                    # 继续寻找原来的正常控件
                    return self.find(locator,value)
            logging.warn("black list no one found")

            raise e

    def text(self, key):
        return By.XPATH, "//*[@text='%s']" % key

    def find_by_text(self,key):
        return self.find(self.text(key))

    # 封装step
    def step(self, path):
        with open(path) as f:
            steps: list[dict] = yaml.safe_load(f)
            element: WebElement = None

            for step in steps:
                logging.info(step)
                if "by" in step.keys():
                    element = self.find(self["by"], self["locator"])
                if "action" in step.keys():
                    action = step["action"]
                    if action == "find":
                        pass
                    elif action == "click":
                        element.click()
                    elif action == "text":
                        element.text
                    elif action == "attribute":
                        element.get_attribute(step["value"])
                    elif action in ["send", "input"]:
                        content: str = step["value"]
                        for key in self._params.keys():
                            content = content.replace("{%s}"%key, self._params[key])
                        element.send_keys(content)
