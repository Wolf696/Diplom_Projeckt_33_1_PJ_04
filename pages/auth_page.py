
from pages.base import WebPage
from pages.elements import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base import BasePage

class AuthPage(WebPage):
    def __init__(self, web_driver, url=''):
        url = ('https://b2c.passport.rt.ru/auth/realms/b2c/protocol/openid-connect/auth?'
               'client_id=account_b2c&redirect_uri=https://b2c.passport.rt.ru/account_b2c/login&'
               'response_type=code&scope=openid&state=d012f376-66d0-4417-ae7b-c3e4fcbbce9f&'
               'theme&auth_type')
        super().__init__(web_driver, url)

    btn_tab_phone = WebElement(xpath='//*[@id="t-btn-tab-phone"]')
    btn_tab_email = WebElement(xpath='//*[@id="t-btn-tab-mail"]')
    btn_tab_login = WebElement(xpath='//*[@id="t-btn-tab-login"]')
    btn_tab_ls = WebElement(xpath='//*[@id="t-btn-tab-ls"]')
    input_username = WebElement(xpath='//*[@id="username"]')
    input_password = WebElement(xpath='//*[@id="password"]')
    forgot_password = WebElement(xpath='//*[@id="forgot_password"]')
    btn_enter = WebElement(xpath='//*[@id="kc-login"]')
    help_modal = WebElement(xpath='//*[@id="faq-open"]/a')
    btn_register = WebElement(xpath='//*[@id="kc-register"]')

class AuthPage(BasePage):
    # Локаторы
    USERNAME_INPUT = (By.ID, 'username')
    PASSWORD_INPUT = (By.ID, 'password')
    LOGIN_BUTTON = (By.ID, 'kc-login')
    TAB_BUTTON = (By.XPATH, "//div[contains(@class, 'rt-tab') and contains(text(), '{}')]")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "span.rt-input-container__meta--error")

    def select_tab(self, tab_name):
        """Выбирает вкладку по названию (Телефон, Почта, Логин, Лицевой счёт)"""
        tab_locator = (self.TAB_BUTTON[0], self.TAB_BUTTON[1].format(tab_name))
        tab = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(tab_locator)
        )
        tab.click()
        return self

    def enter_credentials(self, username, password):
        """Вводит логин и пароль"""
        self.driver.find_element(*self.USERNAME_INPUT).send_keys(username)
        self.driver.find_element(*self.PASSWORD_INPUT).send_keys(password)
        return self

    def click_login(self):
        """Нажимает кнопку входа"""
        self.driver.find_element(*self.LOGIN_BUTTON).click()
        return self

    def get_error_message(self):
        """Возвращает текст сообщения об ошибке"""
        return WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.ERROR_MESSAGE)
        ).text

class AuthPage:
    def __init__(self, browser):
        self.browser = browser
