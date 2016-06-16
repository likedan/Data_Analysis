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


    def quit(self):
        self.driver.quit()