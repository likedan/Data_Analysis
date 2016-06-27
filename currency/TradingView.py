from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
        self.create_folder_if_not_exist()

        image_name = str(id(self)) + "screenshot.png"
        self.screenshot_file = os.path.join(self.screenshot_dir, image_name)
        try:
            self.driver.get(DEFAULT_IQOPTION_URL)
        except Exception as e:
            print "connection failed"
            print e

    def login(self):
        self.driver.find_element_by_xpath("//div[@class='header__btn header__btn_sign btn_transparent js-login-btn']").click()
        time.sleep(3)
        login_form = self.driver.find_element_by_id("loginFrm")
        login_form.find_element_by_name("email").send_keys("likedan5@icloud.com")
        login_form.find_element_by_name("password").send_keys("Diyici140726")
        login_form.find_element_by_xpath("//button[@class='btn-submit input-form__btn input-form__btn_green']").click()
        time.sleep(2)
        self.driver.find_element_by_xpath("//div[@class='profile__trade js-btn-trade']").click()
        time.sleep(20)
        self.is_ready = True

    def create_folder_if_not_exist(self):
        file_dir = os.path.join(Helper.get_desktop_dir(), PLOT_IMAGE_PATH)
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        file_dir = os.path.join(file_dir, "BrowserScreenShot")
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        self.screenshot_dir = file_dir

    def click_canvas_position(self, x, y):
        try:
            element = self.driver.find_element_by_id("glcanvas")
            action = webdriver.common.action_chains.ActionChains(self.driver)
            #position of down button
            action.move_to_element(element).move_by_offset(x, y).click().perform()
            return True
        except Exception, e:
            raise e
    def trade_down(self):

        self.driver.save_screenshot(self.screenshot_file)
        im = Image.open(self.screenshot_file)
        rgb_im = im.convert('RGB')
        r, g, b = rgb_im.getpixel((1120, 400))

        #click open new trade
        if (r,g,b) == NEWTRADE_BUTTON: 
            self.click_canvas_position(550, 100)
            time.wait(1)
            self.driver.save_screenshot(self.screenshot_file)
            im = Image.open(self.screenshot_file)
            rgb_im = im.convert('RGB')
            r, g, b = rgb_im.getpixel((1120, 400))

        if (r,g,b) == UP_BUTTON_COLOR and self.is_ready:
            return self.click_canvas_position(550, 240)
        else:
            return False


    def trade_up(self):
        self.driver.save_screenshot(self.screenshot_file)
        im = Image.open(self.screenshot_file)
        rgb_im = im.convert('RGB')
        r, g, b = rgb_im.getpixel((1120, 400))

        #click open new trade
        if (r,g,b) == NEWTRADE_BUTTON: 
            self.click_canvas_position(550, 100)
            time.wait(1)
            self.driver.save_screenshot(self.screenshot_file)
            im = Image.open(self.screenshot_file)
            rgb_im = im.convert('RGB')
            r, g, b = rgb_im.getpixel((1120, 400))

        if (r,g,b) == UP_BUTTON_COLOR and self.is_ready:
            return self.click_canvas_position(550, 100)
        else:
            return False

    def quit(self):
        self.driver.quit()