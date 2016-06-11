from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import lxml.html
from DefaultVariables import *
import os, sys
from Database import Database

class Crawler:

    def __init__(self):
        self.busy = False
        print "init Crawler"

        firefox_profile = webdriver.FirefoxProfile()
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
                    stock_url = DEFAULT_SITE_URL + stock_url + PRICE_HISTORY_SUFFIX
                    stock_symbol_dict[stock_symbol] = stock_url

            add_rows("qm_main")
            add_rows("qm_cycle")

            return stock_symbol_dict

    def download_historical_data(self, symbol, stock_url):
        self.busy = True
        page_num = 2500
        month_max = 30
        month_min = 10
        delay = 20
        status = ""

        stock_price_data = []

        def download_page(full_url):
            try:
                self.driver.get(full_url)
                WebDriverWait(self.driver, delay).until(lambda the_driver: the_driver.find_element_by_class_name('qm_maintext').is_displayed())
                source = lxml.html.fromstring(self.driver.page_source)

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

                        #get the actual percentage data
                        one_day_data["chg_p"] = one_day_data["chg_p"].split(" ")[-1]
                        stock_price_data.append(one_day_data)

                add_rows("qm_cycle qm_historyData_row")
                add_rows("qm_main qm_historyData_row")

            except Exception as e:
                print e
                print full_url
                
        download_page(stock_url + TIMEFRAME_URL + "1")
        if len(stock_price_data) >= page_num:
            download_page(stock_url + TIMEFRAME_URL + "2")
        elif len(stock_price_data) > month_min and len(stock_price_data) < month_max:

            #url is deprecated,  get the new one
            new_url = self.driver.current_url
            db = Database()
            db.update_stock_url(symbol, new_url)

            stock_price_data = []
            download_page(new_url + TIMEFRAME_URL + "1")
            if len(stock_price_data) >= page_num:
                download_page(new_url + TIMEFRAME_URL + "2")

        self.busy = False
        return stock_price_data


    def quit(self):
        self.driver.quit()