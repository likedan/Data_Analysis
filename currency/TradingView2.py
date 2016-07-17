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
        except Exception as e:
            print "connection failed"
            print e


    def click_canvas_position(self, x, y):
        try:
            element = self.driver.find_element_by_id("glcanvas")
            action = webdriver.common.action_chains.ActionChains(self.driver)
            #position of down button
            action.move_to_element(element).move_by_offset(x, y).click().perform()
            return True
        except Exception, e:
            raise e

    def clean_new_trade(self):
        self.driver.save_screenshot(self.screenshot_file)
        im = Image.open(self.screenshot_file)
        rgb_im = im.convert('RGB')
        r, g, b = rgb_im.getpixel((1120, 400))
        #click open new trade
        if Helper.similar_color((r,g,b), NEWTRADE_BUTTON): 
            self.click_canvas_position(550, 100)
            time.sleep(0.2)

    def trade_down(self):

        self.driver.save_screenshot(self.screenshot_file)
        im = Image.open(self.screenshot_file)
        rgb_im = im.convert('RGB')
        r, g, b = rgb_im.getpixel((1120, 400))
        #click open new trade
        if Helper.similar_color((r,g,b), NEWTRADE_BUTTON): 
            self.click_canvas_position(550, 100)
            time.sleep(0.5)
            self.driver.save_screenshot(self.screenshot_file)
            im = Image.open(self.screenshot_file)
            rgb_im = im.convert('RGB')
            r, g, b = rgb_im.getpixel((1120, 400))
        
        print (r,g,b)
        if (Helper.similar_color((r,g,b), UP_BUTTON_COLOR) or Helper.similar_color((r,g,b), UP_BUTTON_COLOR2)) and self.is_ready:
            return self.click_canvas_position(550, 240)
        else:
            return False


    def trade_up(self):
        self.driver.save_screenshot(self.screenshot_file)
        im = Image.open(self.screenshot_file)
        rgb_im = im.convert('RGB')
        r, g, b = rgb_im.getpixel((1120, 400))

        #click open new trade
        if Helper.similar_color((r,g,b), NEWTRADE_BUTTON): 
            self.click_canvas_position(550, 100)
            time.sleep(0.5)
            self.driver.save_screenshot(self.screenshot_file)
            im = Image.open(self.screenshot_file)
            rgb_im = im.convert('RGB')
            r, g, b = rgb_im.getpixel((1120, 400))
        print (r,g,b)
        if (Helper.similar_color((r,g,b), UP_BUTTON_COLOR) or  Helper.similar_color((r,g,b), UP_BUTTON_COLOR2)) and self.is_ready:
            return self.click_canvas_position(550, 100)
        else:
            return False

    def quit(self):
        self.driver.quit()