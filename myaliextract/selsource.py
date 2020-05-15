from selenium import webdriver
import time

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('chromedriver')
driver = webdriver.Chrome(
    'C:\chromedriver_win32\chromedriver.exe', options=options)


def getSource(url):
    driver.get(url)
    time.sleep(int(10))
    return driver.page_source


def quitSession():
    driver.quit()
