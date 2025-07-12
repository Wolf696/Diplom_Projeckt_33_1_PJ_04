from telnetlib import EC

import pytest
import os
import time

from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from pages.auth_page import AuthPage

load_dotenv()

invalid_email = os.getenv('invalid_email')
invalid_phone = os.getenv('invalid_phone')
invalid_login = os.getenv('invalid_login')

invalid_password = os.getenv('invalid_password')


@pytest.fixture(scope="function")
def auth_page(chrome_browser_instance):
    return AuthPage(chrome_browser_instance)


def test_unsuccessful_authorization_by_email(auth_page, invalid_email, invalid_password):

    auth_page.input_username.send_keys(invalid_email)
    auth_page.input_password.send_keys(invalid_password)
    auth_page.login_button.click()
    time.sleep(1)  # если требуется ввести капчу
    auth_page.btn_enter.click()

    error_message = WebDriverWait(auth_page._web_driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "span.rt-input-container__meta--error"))
    )
    assert "Неверный логин или пароль" in error_message.text

    forgot_password = auth_page._web_driver.find_element(By.XPATH, '//*[@id="forgot_password"]')
    element_color = forgot_password.value_of_css_property('color')
    assert element_color in ['rgba(255, 79, 18, 1)', 'rgb(255, 79, 18)']  # ожидаем что элемент "Забыл пароль" перекрашивается в оранжевый цвет


def test_unsuccessful_authorization_by_phone(auth_page):
    auth_page.input_username.send_keys(invalid_phone)
    auth_page.input_password.send_keys(invalid_password)
    time.sleep(1)  # если требуется ввести капчу
    auth_page.btn_enter.click()

    error_message = auth_page._web_driver.find_element(By.ID, "form-error-message")
    assert error_message.text == "Неверный логин или пароль"

    forgot_password = auth_page._web_driver.find_element(By.XPATH, '//*[@id="forgot_password"]')
    element_color = forgot_password.value_of_css_property('color')
    assert element_color in ['rgba(255, 79, 18, 1)', 'rgb(255, 79, 18)']  # ожидаем что элемент "Забыл пароль" перекрашивается в оранжевый цвет


def test_unsuccessful_authorization_by_login(auth_page):
    auth_page.input_username.send_keys(invalid_login)
    auth_page.input_password.send_keys(invalid_password)
    time.sleep(1)  # если требуется ввести капчу
    auth_page.btn_enter.click()

    error_message = auth_page._web_driver.find_element(By.ID, "form-error-message")
    assert error_message.text == "Неверный логин или пароль"

    forgot_password = auth_page._web_driver.find_element(By.XPATH, '//*[@id="forgot_password"]')
    element_color = forgot_password.value_of_css_property('color')
    assert element_color in ['rgba(255, 79, 18, 1)', 'rgb(255, 79, 18)']  # ожидаем что элемент "Забыл пароль" перекрашивается в оранжевый цвет
