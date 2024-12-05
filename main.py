import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from bs4 import BeautifulSoup as bs

from config import URL, LOGIN, PASSWORD


class Browser:
    def __init__(self):
        self.browser = webdriver.Chrome()
        self.browser.maximize_window()
        self.wait = WebDriverWait(self.browser, 10)
        self.proxy_data = {}

    def open_page(self):
        self.browser.get(URL)
        self.wait.until(ec.presence_of_element_located((By.CLASS_NAME, 'icon-login')))

    def authentication(self):
        self.browser.find_element(By.CLASS_NAME, 'icon-login').click()
        self.wait.until(ec.presence_of_element_located((By.NAME, 'email')))
        self.browser.find_element(By.NAME, 'email').send_keys(LOGIN)
        self.browser.find_element(By.NAME, 'password').send_keys(PASSWORD)
        # Ввод капчи
        time.sleep(25)
        self.browser.find_element(By.XPATH, '//*[@id="form-login"]/div[7]/button').click()
        self.wait.until(ec.presence_of_element_located((By.CLASS_NAME, 'icon-user')))

    def get_proxy_data(self):
        soup = bs(self.browser.page_source, 'html.parser')
        proxy_table = soup.find('table', class_='table user_proxy_table')
        proxy_list = proxy_table.find_all('tr')[1:-2]

        for item in proxy_list:
            data = item.find_all('td')[2]
            proxy = data.find('b').text

            end_date = item.find_all('td')[3]
            date = end_date.find('div', class_='right color-success').text

            self.proxy_data[proxy] = date

    def print_proxy_data(self):
        for proxy, date in self.proxy_data.items():
            print(f'{proxy} - {date}')

    def quit(self):
        self.browser.quit()


def main():
    browser = Browser()
    browser.open_page()
    browser.authentication()
    browser.get_proxy_data()
    browser.print_proxy_data()
    browser.quit()


if __name__ == '__main__':
    main()
