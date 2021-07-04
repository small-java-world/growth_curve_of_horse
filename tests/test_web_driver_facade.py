import pytest
import time
from getmodule.web_driver_facade import WebDriverFacade
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException

def test_init_driver(mocker):
    webdriver_mock = mocker.Mock()
    init_driver_mock = mocker.patch.object(webdriver, 'Chrome')
    init_driver_mock.return_value = webdriver_mock
   
    WebDriverFacade.init_driver()
    assert WebDriverFacade.driver == webdriver_mock
    assert init_driver_mock.call_count == 1

def test_quit(mocker):
    webdriver_mock = mocker.Mock()
    WebDriverFacade.driver = webdriver_mock

    quit_mock = mocker.patch.object(webdriver_mock, 'quit')
   
    WebDriverFacade.quit()
    
    assert quit_mock.call_count == 1

def test_get(mocker):
    webdriver_mock = mocker.Mock()
    WebDriverFacade.driver = webdriver_mock

    get_mock = mocker.patch.object(webdriver_mock, 'get')
    get_mock.return_value = True
   
    dummy_url = 'dummy_url'
    WebDriverFacade.get(dummy_url)

    get_mock.assert_called_once_with(dummy_url)

def test_get_text(mocker):
    webdriver_mock = mocker.Mock()
    WebDriverFacade.driver = webdriver_mock

    text_mock = mocker.Mock()
    
    find_element_by_css_selector_mock = mocker.patch.object(webdriver_mock, 'find_element_by_css_selector')
    find_element_by_css_selector_mock.return_value = text_mock

    dummy_css_selector = 'dummy_css_selector'
    dummy_text = 'dummy_text'

    get_attribute_mock = mocker.patch.object(text_mock, 'get_attribute')
    get_attribute_mock.return_value = dummy_text

    assert WebDriverFacade.get_text(dummy_css_selector) == dummy_text

    find_element_by_css_selector_mock.assert_called_once_with(dummy_css_selector)
    get_attribute_mock.assert_called_once_with('textContent')

def test_send_keys(mocker):
    webdriver_mock = mocker.Mock()
    WebDriverFacade.driver = webdriver_mock

    input_box = mocker.Mock()

    find_element_by_css_selector_mock = mocker.patch.object(webdriver_mock, 'find_element_by_css_selector')
    find_element_by_css_selector_mock.return_value = input_box
   
    clear_mock = mocker.patch.object(input_box, 'clear')
    send_keys_mock = mocker.patch.object(input_box, 'send_keys')

    dummy_css_selector = 'dummy_css_selector'
    dummy_input_value = 'dummy_input_value'

    WebDriverFacade.send_keys(dummy_css_selector, dummy_input_value)

    find_element_by_css_selector_mock.assert_called_once_with(dummy_css_selector)
    clear_mock.assert_called_once_with()
    send_keys_mock.assert_called_once_with('dummy_input_value')

def test_click(mocker):
    webdriver_mock = mocker.Mock()
    WebDriverFacade.driver = webdriver_mock

    target = mocker.Mock()

    find_element_by_css_selector_mock = mocker.patch.object(webdriver_mock, 'find_element_by_css_selector')
    find_element_by_css_selector_mock.return_value = target
   
    click_mock = mocker.patch.object(target, 'click')

    dummy_css_selector = 'dummy_css_selector'
    
    WebDriverFacade.click(dummy_css_selector)

    find_element_by_css_selector_mock.assert_called_once_with(dummy_css_selector)
    click_mock.assert_called_once()
    
def test_click_button_js(mocker):
    webdriver_mock = mocker.Mock()
    WebDriverFacade.driver = webdriver_mock

    button = mocker.Mock()

    find_element_by_css_selector_mock = mocker.patch.object(webdriver_mock, 'find_element_by_css_selector')
    find_element_by_css_selector_mock.return_value = button
   
    execute_script_mock = mocker.patch.object(webdriver_mock, 'execute_script')
    
    dummy_css_selector = 'dummy_css_selector'
    
    WebDriverFacade.click_button_js(dummy_css_selector)

    find_element_by_css_selector_mock.assert_called_once_with(dummy_css_selector)
    execute_script_mock.assert_called_once_with('arguments[0].click();', button)

def test_click_by_link_text(mocker):
    webdriver_mock = mocker.Mock()
    WebDriverFacade.driver = webdriver_mock

    link = mocker.Mock()

    dumy_link_text = 'dumy_link_text'
    
    find_element_by_link_text_mock = mocker.patch.object(webdriver_mock, 'find_element_by_link_text')
    find_element_by_link_text_mock.return_value = link
   
    click_mock = mocker.patch.object(link, 'click')
    
    WebDriverFacade.click_by_link_text(dumy_link_text)

    find_element_by_link_text_mock.assert_called_once_with(dumy_link_text)
    assert click_mock.call_count == 1

def test_wait_until(mocker):
    webdriver_mock = mocker.Mock()
    WebDriverFacade.driver = webdriver_mock

    dummy_element = mocker.Mock()

    dummy_css_selector = 'dummy_css_selector'
    
    # 初回はNoSuchElementExceptionがスロー、2回目dummy_elementが返却されるように振る舞いをセット
    find_element_by_css_selector_mock = mocker.patch.object(webdriver_mock, 'find_element_by_css_selector', side_effect=[NoSuchElementException,dummy_element])
    find_element_by_css_selector_mock.return_value = dummy_element
    
    WebDriverFacade.wait_until(dummy_css_selector)

    # 呼び出し回数は2であること   
    assert find_element_by_css_selector_mock.call_count == 2

def test_wait_until_fail(mocker):
    webdriver_mock = mocker.Mock()
    WebDriverFacade.driver = webdriver_mock

    dummy_css_selector = 'dummy_css_selector'
    
    # NoSuchElementExceptionがスローされるように振る舞いをセット
    find_element_by_css_selector_mock = mocker.patch.object(webdriver_mock, 'find_element_by_css_selector', side_effect=NoSuchElementException)
    
    timeout = 3
    POLL_FREQUENCY = 0.5

    # TimeoutExceptionが発生すること
    with pytest.raises(TimeoutException):
        WebDriverFacade.wait_until(dummy_css_selector, timeout)

    # 呼び出し回数はtimeout / POLL_FREQUENCY = 6であること    
    assert find_element_by_css_selector_mock.call_count == timeout / POLL_FREQUENCY