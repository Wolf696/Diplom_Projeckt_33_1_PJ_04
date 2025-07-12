
import pytest
import time

from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from auth_page import AuthPage


@pytest.fixture(scope="function")
def auth_page(chrome_browser_instance):
    return AuthPage(chrome_browser_instance)


def test_auth_page_title(auth_page):
    auth_title = WebDriverWait(auth_page._web_driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id='page-right']/div/div[1]/h1"))
    )
    time.sleep(1)
    assert auth_title.text == "Авторизация"


def test_auth_page_all_tabs_text(auth_page):
    phone_tab_text = auth_page.btn_tab_phone.get_text()
    email_tab_text = auth_page.btn_tab_email.get_text()
    login_tab_text = auth_page.btn_tab_login.get_text()
    ls_tab_text = auth_page.btn_tab_ls.get_text()

    assert phone_tab_text == "Телефон"
    assert email_tab_text == "Почта"
    assert login_tab_text == "Логин"
    assert ls_tab_text == "Лицевой счёт"


def test_auth_page_all_fields_text(auth_page):
    # Локаторы для основных элементов формы
    LOCATORS = {
        'username_tab': "div.rt-tabs div.rt-tab:first-child",
        'username_field': "input#username",
        'password_field': "input#password",
        'login_button': "button#kc-login",
        'forgot_password_link': "a#forgot_password"
    }

    # Проверка загрузки страницы
    try:
        WebDriverWait(auth_page._web_driver, 20).until(
            lambda d: d.execute_script('return document.readyState') == 'complete'
        )
    except TimeoutException:
        auth_page._web_driver.save_screenshot('page_not_loaded.png')
        raise AssertionError("Страница не загрузилась за 20 секунд")

    # Проверка видимости основных элементов
    for element_name, locator in LOCATORS.items():
        try:
            element = WebDriverWait(auth_page._web_driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, locator))
            )
            print(f"Элемент {element_name} найден: {element.text if element.text else element.get_attribute('value')}")
        except TimeoutException:
            auth_page._web_driver.save_screenshot(f'element_not_found_{element_name}.png')
            raise AssertionError(f"Элемент {element_name} не найден на странице")

    # Дополнительная проверка текста на вкладках
    try:
        tabs = auth_page._web_driver.find_elements(By.CSS_SELECTOR, "div.rt-tabs div.rt-tab")
        assert len(tabs) >= 2, "Не найдены вкладки для выбора типа авторизации"

        tab_texts = [tab.text for tab in tabs]
        expected_texts = ['Телефон', 'Почта', 'Логин', 'Лицевой счёт']

        for expected in expected_texts:
            assert any(expected in text for text in tab_texts), f"Не найдена вкладка с текстом '{expected}'"
    except Exception as e:
        auth_page._web_driver.save_screenshot('tabs_error.png')
        raise


def test_auth_page_forgot_password_text_color(auth_page):
    forgot_password_text = auth_page.forgot_password.get_text()
    assert forgot_password_text == "Забыл пароль"
    forgot_password = auth_page._web_driver.find_element(By.XPATH, '//*[@id="forgot_password"]')
    element_color = forgot_password.value_of_css_property('color')
    assert element_color in ['rgba(255, 79, 18, 1)', 'rgb(255, 79, 18)']


def test_auth_page_enter_button_text_color(auth_page):
    enter_button_text = auth_page.btn_enter.get_text()
    assert enter_button_text == "Войти"
    enter_button = auth_page._web_driver.find_element(By.XPATH, '//button[@id="kc-login"]')
    button_color = enter_button.value_of_css_property('background-color')
    expected_color = 'rgba(255, 79, 18, 1)'
    assert button_color == expected_color


def test_auth_page_btn_register_text_color(auth_page):
    btn_register_text = auth_page.btn_register.get_text()
    auth_page.btn_register.click()
    time.sleep(1)
    reg_title = WebDriverWait(auth_page._web_driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//h1[contains(text(), 'Регистрация')]"))
    )
    assert btn_register_text == "Зарегистрироваться"
    assert reg_title.text == "Регистрация"


def test_auth_page_help_modal_text_color(auth_page):
    help_modal_text = auth_page.help_modal.get_text()
    assert help_modal_text == "Помощь"
    help_modal = auth_page._web_driver.find_element(By.XPATH, '//*[@id="faq-open"]/a')
    element_color = help_modal.value_of_css_property('color')
    expected_color = 'rgba(255, 79, 18, 1)'
    assert element_color == expected_color
    auth_page.help_modal.click()
    time.sleep(2)
    heading = WebDriverWait(auth_page._web_driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//h2[contains(text(), 'Как войти в личный кабинет?')]"))
    )
    assert heading.text == "Как войти в личный кабинет?"
