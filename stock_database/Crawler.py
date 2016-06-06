from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import lxml.html
from DefaultVariables import *
import os, sys

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
        delay = 5
        self.driver.get(url)

        try:
            WebDriverWait(self.driver, delay).until(lambda the_driver: the_driver.find_element_by_class_name('qm_cycle').is_displayed())
        finally:
            source = lxml.html.fromstring(self.driver.page_source)

            def add_rows(class_key):
                for row in source.xpath('.//table[@class="qm_data qm_maintext"]//tbody//tr[@class="'+ class_key +'"]'):
                    stock_symbol = row.xpath('.//td/text()')[0]
                    stock_url = row.xpath('.//a[@class="qm"]')[0].attrib['href']
                    stock_symbol_dict[stock_symbol] = stock_url

            add_rows("qm_main")
            add_rows("qm_cycle")

            return stock_symbol_dict

    def download_historical_data(self, stock_url):

        delay = 5
        full_url = DEFAULT_SITE_URL + os.path.join(stock_url, PRICE_HISTORY_SUFFIX)
        print full_url
        self.driver.get(full_url)
        try:
            WebDriverWait(self.driver, delay).until(lambda the_driver: the_driver.find_element_by_class_name('qm_history_startMonth').is_displayed())
            
            day_input = self.driver.find_element_by_class_name('qm_history_startDay')
            day_input.clear()
            day_input.send_keys("1")

            year_input = self.driver.find_element_by_class_name('qm_history_startYear')
            year_input.clear()
            year_input.send_keys("2000")
            self.driver.find_element_by_class_name('qm_history_startMonth').send_keys("Jan")
            # self.driver.find_element_by_class_name('qm_historyTab_GoButton').click()
        except Exception as e:
            print "no stock data"
        

    def quit(self):
        self.driver.quit()