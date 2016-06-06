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

        delay = 10
        def download_page(page):
            full_url_page_1 = DEFAULT_SITE_URL + os.path.join(stock_url, PRICE_HISTORY_SUFFIX) + TIMEFRAME_URL + page
            print full_url_page_1
            self.driver.get(full_url_page_1)
            try:
                WebDriverWait(self.driver, delay).until(lambda the_driver: the_driver.find_element_by_class_name('qm_maintext').is_displayed())
                source = lxml.html.fromstring(self.driver.page_source)

                stock_price_data = []
                def add_rows(class_key):
                    for row in source.xpath('.//table[@class="qm_history_historyContent"]//tbody//tr[@class="' + class_key + '"]'):
                        one_day_data = {}
                        one_day_data["date"] = row.xpath('.//td/text()')[0]
                        one_day_data["open"] = row.xpath('.//td/text()')[1]
                        one_day_data["high"] = row.xpath('.//td/text()')[2]
                        one_day_data["low"] = row.xpath('.//td/text()')[3]
                        one_day_data["close"] = row.xpath('.//td/text()')[4]
                        one_day_data["volume"] = row.xpath('.//td/text()')[5]
                        one_day_data["chg"] = row.xpath('.//td/text()')[6]
                        one_day_data["chg_p"] = row.xpath('.//td/text()')[7]
                        one_day_data["adj_close"] = row.xpath('.//td/text()')[8]
                        one_day_data["trade_val"] = row.xpath('.//td/text()')[9]
                        one_day_data["trades"] = row.xpath('.//td/text()')[10]
                        stock_price_data.append(one_day_data)
                add_rows("qm_cycle qm_historyData_row")
                add_rows("qm_main qm_historyData_row")
                print len(stock_price_data)

            except Exception as e:
                print "no stock data"
                print e
        download_page("1")
        download_page("2")





    def quit(self):
        self.driver.quit()