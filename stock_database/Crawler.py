from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import lxml.html
from DefaultVariables import *

class Crawler:

    def __init__(self):
        print "init Crawler"

        firefox_profile = webdriver.FirefoxProfile()
        firefox_profile.set_preference("browser.download.folderList",2)
        firefox_profile.set_preference("javascript.enabled", False)
        self.driver = webdriver.Firefox(firefox_profile=firefox_profile)
        # options = []
        # options.append('--load-images=false')        
        # self.driver = webdriver.PhantomJS(service_args=options)

        self.driver.set_window_size(1500, 1500)
        try:
            self.driver.get(DEFAULT_SITE_URL)
        except Exception as e:
            print "connection failed"
            print e

    def get_stock_list_with_url(self, url):
        stock_symbol_dict = {}
        self.driver.get(url)
        # container = self.driver.find_element_by_css_selector('.qm_data.qm_maintext')
        source = lxml.html.fromstring(self.driver.page_source)

        def add_rows(class_key):
            for row in source.xpath('.//table[@class="qm_data qm_maintext"]//tbody//tr[@class="'+ class_key +'"]'):
                stock_symbol = row.xpath('.//td/text()')[0]
                if stock_symbol.isalpha():
                    stock_url = row.xpath('.//a[@class="qm"]')[0].attrib['href']
                    stock_symbol_dict[stock_symbol] = stock_url

        add_rows("qm_main")
        add_rows("qm_cycle")

        return stock_symbol_dict

    def quit(self):
        self.driver.quit()