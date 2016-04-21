from main_page import MainPage
from Page import PageLogin
from unittest import TestCase
import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class OttripTest(TestCase):
    def setUp(self):
        """
        Предусловие:
        зайти на сайт www.onetwotrip.com
        нажать "личный кабинет"
        """
        self.driver = webdriver.Firefox()
        self.driver.maximize_window()
        page = MainPage(self.driver)
        page.open("http://www.onetwotrip.com/ru")
        page.top_panel.click_login()

    def tearDown(self):
        self.driver.quit()

    def test_forgot_password_non_existent_email(self):
        """
        Тест-кейс "Проверка вывода сообщения об ошибке при вводе несуществующего email в форме "забыли пароль""
        Шаги:
        1. Зайти на сайт "www.onetwotrip.com"
        2. Нажать "Личный кабинет"
        3. В открывшемся окне нажимаем "забыли пароль"
        4. В открывшемся окне ввести несуществующий email
        Ожидание:
        Вывод сообщения об ошибке "Пользователя с таким email не существует" в браузере.
        """
        page_auth = PageLogin(self.driver)
        page_auth.form_auth.forgot_password("lllll@mail.ru")

        error = page_auth.result_forgot_pass.message_incorrect_email()

        self.assertIn("Пользователя с таким email не существует", error.text)

    def test_forgot_password_correct_email(self):
        """
        Тест-кейс "Проверка вывода сообщения об отправке нового пароля на указанный email в форме "забыли пароль""
        Шаги:
        1.Нажать "забыли пароль"
        2.В поле "Электронная почта" ввести зарегистрированный на onetwotrip email
        3.Нажать кнопку "Получить пароль"
        Ожидание:
        Вывод сообщения об отправке нового пароля на указанный email.
        """
        page_auth = PageLogin(self.driver)
        page_auth.form_auth.forgot_password("ld040994@mail.ru")

        message = page_auth.result_forgot_pass.message_get_pass()
        self.assertTrue(message.is_displayed)

    def test_auth_incorrect_login(self):
        """
        Тест-кейс "Проверка вывода сообщения об ошибке при вводе неверного логина в форме авторизации"
        Шаги:
        1.В поле "Электронная почта" вести почту незарегистрированную на onetwotrip
        2.В поле "Пароль" ввести пароль
        3.Нажать кнопку "Войти"
        Ожидание:
        Вывод сообщения "Неправильный пароль или почта"
        """
        page_auth = PageLogin(self.driver)
        page_auth.form_auth.authorization("l040994@mail.ru","040994alex")

        error = page_auth.result_auth.message_incorret_login()

        self.assertIn("Неправильный пароль или почта", error.text)

    def test_auth_correct(self):
        """
        Тест-кейс "Проверка ввода верного логина и пароля в форме авторизации"
        Шаги:
        1.В поле "Электронная почта" вести почту зарегистрированную на onetwotrip
        2.В поле "Пароль" ввести верный пароль
        3.Нажать кнопку "Войти"
        Ожидание:
        Успешная авторизация (название кнопки личный кабинет заменяется на email адрес)
        """
        page_auth = PageLogin(self.driver)
        page_auth.form_auth.authorization("ld040994@mail.ru","040994alex")

        profile = page_auth.result_auth.user_name()
        self.assertEqual(profile.text, "ld040994@mail.ru")

    def test_auth_facebook(self):
        """
        Тест-кейс "Проверка ввода верного логина и пароля в форме авторизации"
        Шаги:
        1.Нажать на иконку Facebook
        2.В новом окне ввести логин и пароль от аккаунта Facebook
        3.Нажать кнопку "Войти"
        Ожидание:
        Успешная авторизация (название кнопки "личный кабинет" заменяется название профиля)
        """
        page_auth = PageLogin(self.driver)
        page_auth.form_auth.auth_facebook("alexld45@mail.ru","040994alex")

        profile = page_auth.result_auth.user_name()
        self.assertEqual(profile.text, "Алексей Демин")


if __name__ == '__main__':
    unittest.main()
