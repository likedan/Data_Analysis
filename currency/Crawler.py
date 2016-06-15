from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import lxml.html
from Database import Database

from DefaultVariables import *
import Helper
import os, sys, os
import time
class Crawler:

    def __init__(self, db):
        print "init Crawler"
        self.db = db

        firefox_profile = webdriver.FirefoxProfile()
        firefox_profile.set_preference("javascript.enabled", False)
        self.driver = webdriver.Firefox(firefox_profile=firefox_profile)
        # self.driver.set_window_size(1500, 1500)

        try:
            self.driver.get(DEFAULT_SITE_URL)
        except Exception as e:
            print "connection failed"
            print e


    def get_currency_list_with_url(self, url):
        currency_list = []
        self.driver.get(url)
        source = lxml.html.fromstring(self.driver.page_source)
        for row in source.xpath('.//div[@class="page-content"]//table//tbody//tr'):
            for element in row.xpath('.//td//a'):
                currency_list.append(element.attrib['href'][-6:])

        return currency_list

    def get_time_fragment_list_with_url(self, url):
        time_fragment_list = []
        self.driver.get(url)
        source = lxml.html.fromstring(self.driver.page_source)
        for element in (source.xpath('.//div[@class="page-content"]//p')[3]).findall('.//a'):
            time_fragment_list.append(element.attrib['href'])
        return time_fragment_list

    def download_historical_data(self, symbol, folder):
        self.quit()

        directory = os.path.join(folder, symbol)
        if not os.path.exists(directory):
            os.makedirs(directory)

        firefox_profile = webdriver.FirefoxProfile()
        firefox_profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream;application/csv;text/csv;application/vnd.ms-excel;") 
        firefox_profile.set_preference("browser.helperApps.alwaysAsk.force", False)
        firefox_profile.set_preference("browser.download.folderList", 2)
        firefox_profile.set_preference("browser.download.manager.showWhenStarting", False)
        firefox_profile.set_preference("browser.download.dir", directory)
        self.driver = webdriver.Firefox(firefox_profile=firefox_profile)

        def download_monthly_data(year, month):

            full_url = DEFAULT_SITE_URL + CURRENCYLIST_URL + os.path.join(symbol, str(year), str(month)) 
            self.driver.get(full_url)
            button = self.driver.find_element_by_id('a_file')
            button.click()
            time.sleep(DOWNLOAD_WAIT_SECOND)

            if year < CRAWLING_START_YEAR:
                return False

            return True

        Helper.run_every_month_until(download_monthly_data)


        # for year in reversed(range(2000,2016))
        # full_url = DEFAULT_SITE_URL + url
        #     self.driver.get(full_url)
    #     delay = 8
    #     status = ""

    #     stock_price_data = []

    #     def download_page(full_url):
            
    #         try:
    #             self.driver.get(full_url)
    #             WebDriverWait(self.driver, delay).until(lambda the_driver: the_driver.find_element_by_class_name('qm_maintext').is_displayed())
    #             source = lxml.html.fromstring(self.driver.page_source)
    #             def add_rows(class_key):
    #                 for row in source.xpath('.//table[@class="qm_history_historyContent"]//tbody//tr[@class="' + class_key + '"]'):
    #                     one_day_data = {}
    #                     one_day_data["date"] = row.xpath('.//td/text()')[0]
    #                     one_day_data["open"] = row.xpath('.//td/text()')[1]
    #                     one_day_data["high"] = row.xpath('.//td/text()')[2]
    #                     one_day_data["low"] = row.xpath('.//td/text()')[3]
    #                     one_day_data["close"] = row.xpath('.//td/text()')[4]
    #                     one_day_data["volume"] = row.xpath('.//td/text()')[5]
    #                     one_day_data["chg"] = row.xpath('.//td/text()')[6]
    #                     one_day_data["chg_p"] = row.xpath('.//td/text()')[7]
    #                     one_day_data["adj_close"] = row.xpath('.//td/text()')[8]
    #                     one_day_data["trade_val"] = row.xpath('.//td/text()')[9]
    #                     one_day_data["trades"] = row.xpath('.//td/text()')[10]

    #                     #get the actual percentage data
    #                     one_day_data["chg_p"] = one_day_data["chg_p"].split(" ")[-1]
    #                     stock_price_data.append(one_day_data)

    #             add_rows("qm_cycle qm_historyData_row")
    #             add_rows("qm_main qm_historyData_row")

    #         except Exception as e:
    #             print str(e)
    #             print full_url
                
    #     download_page(stock_url + TIMEFRAME_URL + "1")
    #     if len(stock_price_data) >= page_num:
    #         download_page(stock_url + TIMEFRAME_URL + "2")
    #     elif len(stock_price_data) > month_min and len(stock_price_data) < month_max:

    #         #url is deprecated,  get the new one
    #         new_url = self.driver.current_url
            
    #         self.db.update_stock_url(symbol, new_url)

    #         stock_price_data = []
    #         download_page(new_url + TIMEFRAME_URL + "1")
    #         if len(stock_price_data) >= page_num:
    #             download_page(new_url + TIMEFRAME_URL + "2")

    #     return stock_price_data


    def quit(self):
        self.driver.quit()