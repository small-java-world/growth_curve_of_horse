from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from typing import Counter, Dict, Tuple, List

class WebDriverFacade:
    driver: webdriver = None

    @staticmethod
    def init_driver() -> None:
        if WebDriverFacade.driver == None:
            WebDriverFacade.driver = webdriver.Chrome()

    @staticmethod
    def quit() -> None:
        WebDriverFacade.driver.quit()
        WebDriverFacade.driver = None

    @staticmethod
    def get(url:str) -> None:
        WebDriverFacade.init_driver()
        WebDriverFacade.driver.get(url)

    @staticmethod
    def get_text(css_selector:str) -> str:
        text = WebDriverFacade.driver.find_element_by_css_selector(css_selector)
        return text.get_attribute("textContent")

    @staticmethod
    def send_keys(css_selector:str, input_value:str) -> None:
        input_box = WebDriverFacade.driver.find_element_by_css_selector(css_selector)
        input_box.clear()
        input_box.send_keys(input_value)

    @staticmethod
    def click(css_selector:str) -> None:
        target = WebDriverFacade.driver.find_element_by_css_selector(css_selector)
        target.click()

    @staticmethod
    def click_button_js(css_selector:str) -> None:
        botton = WebDriverFacade.driver.find_element_by_css_selector(css_selector)
        WebDriverFacade.driver.execute_script('arguments[0].click();', botton)

    @staticmethod
    def click_by_link_text(link_text:str) -> None:
        link = WebDriverFacade.driver.find_element_by_link_text(link_text)
        link.click()

    @staticmethod
    def wait_until(css_selector:str, timeout:int = 10) -> None:
        WebDriverWait(WebDriverFacade.driver, timeout).until(lambda x: x.find_element_by_css_selector(css_selector))

    @staticmethod
    def get_page_source() -> str:
        return WebDriverFacade.driver.page_source.encode("utf-8")
        