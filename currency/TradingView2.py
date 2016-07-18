from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import selenium.webdriver.support.ui as ui
import lxml.html
from Database import Database
from lxml import etree
from PIL import Image

from DefaultVariables import *
import Helper
import os, sys, os
import time

class TradingView:

    def __init__(self):
        print "init Crawler"
        firefox_profile = webdriver.FirefoxProfile()
        firefox_profile.set_preference("javascript.enabled", False)
        self.driver = webdriver.Firefox(firefox_profile=firefox_profile)
        self.driver.set_window_size(BROWSER_WIDTH, BROWSER_HEIGHT)
        self.is_ready = False

        image_name = str(id(self)) + "screenshot.png"
        try:
            self.driver.get(DEFAULT_EXPERTOPTION_URL)
            self.driver.find_element_by_xpath("//a[@class='demo-link']").click()
            wait = ui.WebDriverWait(self.driver, 20)
            wait.until(lambda driver: self.driver.find_element_by_xpath("//div[@class='ngdialog-close']"))
            self.driver.find_element_by_xpath("//div[@class='ngdialog-close']").click()
            time.sleep(2)
        except Exception as e:
            print "connection failed"
            print e
            
    def trade_up(self):
        try:
            self.driver.find_element_by_xpath("//span[@class='operate-button call ng-binding']").click()
        except Exception as e:
            try:
                self.driver.find_element_by_xpath("//span[@class='new-button ng-binding']").click()
                self.driver.find_element_by_xpath("//span[@class='operate-button call ng-binding']").click()
            except Exception as e:
                print e
                return False
        return True 

    def trade_down(self):
        try:
            self.driver.find_element_by_xpath("//span[@class='operate-button put ng-binding']").click()
        except Exception as e:
            try:
                self.driver.find_element_by_xpath("//span[@class='new-button ng-binding']").click()
                self.driver.find_element_by_xpath("//span[@class='operate-button put ng-binding']").click()
            except Exception as e:
                print e
                return False
        return True 

    def trade_element(self, symbol):
        try:
            self.driver.find_element_by_xpath("//span[@class='arm']").click()
            self.driver.find_element_by_xpath("//div[@data-reactid='" + self.tradable_elements[symbol]["reactid"] + "']").click()
        except Exception as e:
            return False
        return True

    def get_all_available_trades(self):
        try:
            self.tradable_elements = {}
            self.current_trade_element = {}
            source = lxml.html.fromstring(self.driver.page_source)
            for element in source.xpath('.//div[@class="nano-content"]'):
                if "row selected" in etree.tostring(element):
                    for div in element.xpath('.//div[@class="row"]'):
                        # for d in div.xpath('.//div[@class="row"]'):
                        ele_source = etree.tostring(div)
                        reactid = ele_source.split('data-reactid="')[1].split('"')[0]
                        title = ele_source.split('title">')[1].split('<')[0]
                        profit = ele_source.split('"profit"><')[1].split('<')[0].split('>')[1]
                        self.tradable_elements[title] = {"profit":int(profit), "reactid": reactid}
                        
                    for div in element.xpath('.//div[@class="row selected"]'):
                        ele_source = etree.tostring(div)
                        reactid = ele_source.split('data-reactid="')[1].split('"')[0]
                        title = ele_source.split('title">')[1].split('<')[0]
                        profit = ele_source.split('"profit"><')[1].split('<')[0].split('>')[1]
                        self.tradable_elements[title] = {"profit":int(profit), "reactid": reactid}
                        self.current_trade_element = title
                    break
        except Exception, e:
            raise e
        return (self.current_trade_element, self.tradable_elements)

    def quit(self):
        self.driver.quit()