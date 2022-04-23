from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.chrome.options import Options

from proxy_handler import ProxyHandler, Proxy
from selenium.webdriver.common.proxy import Proxy, ProxyType


def config():
    options = Options()
    options.headless = False
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-infobars')
    options.add_argument('--disable-dev-shm-usage')
    options.add_experimental_option("excludeSwitches", ['enable-automation','enable-logging',"ignore-certificate-errors"])
    options.add_experimental_option('useAutomationExtension', False)
    driver = None

def spawn():
    
    