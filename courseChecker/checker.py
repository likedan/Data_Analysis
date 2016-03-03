from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time
from random import randint
from pyvirtualdisplay import Display

class Checker:

    def __init__(self, combination):
        self.combination = combination

        print "init Checker"
        display = Display(visible=0, size=(1024, 768))
        display.start()
        self.driver = webdriver.Firefox()#firefox_profile=firefox_profile)
        self.driver.delete_all_cookies()

    def check(self):
        for onecomb in self.combination:
            available = True
            for crn in onecomb:
                url = "https://ui2web1.apps.uillinois.edu/BANPROD1/bwckschd.p_disp_detail_sched?term_in=120161&crn_in=" + crn
                self.driver.get(url)
                tab = self.driver.find_element_by_class_name('datadisplaytable')
                el = tab.find_element_by_xpath("//tbody[1]/tr[2]/td[3]")
                remaining = int(el.text)
                if remaining <= 0:
                    available = False
                    break
            if available:
                return onecomb
        return None
        # result = self.driver.find_element_by_id('uid1')
        # print result
        # result = result.find_element_by_class_name("text-center")
        # print result
        #
        # while True:
        #     try:
        #         result = result.find_element_by_xpath("//img[contains(@title, 'Closed')]")
        #         print "checking"
        #     except Exception as e:
        #         print "AVAILABLE!!!!!!!!"
        #     time.sleep(5)


    # #login to Pinterest with username andpassword
    def login(self):
        emailField = self.driver.find_element_by_id('ENT_ID')
        emailField.send_keys("jliu152")
        passField = self.driver.find_element_by_id('PASSWORD')
        passField.send_keys("Baby243.3!")
        self.driver.find_element_by_class_name('idbuttons').click()

    def sleepppp(self):
        num = randint(40,100)
        time.sleep(float(num)/20)

    def navigate(self):
        self.driver.find_element_by_link_text('Registration & Records').click()
        self.sleepppp()
        self.driver.find_element_by_link_text('Registration').click()
        self.sleepppp()
        self.driver.find_element_by_link_text('Look-up or Select Classes').click()
        self.sleepppp()
        self.driver.find_element_by_link_text('I Agree to the Above Statement').click()
        self.sleepppp()
        selector = self.driver.find_element_by_id('term_input_id')
        selector.find_element_by_xpath("//select/option[@value='120161']").click()
        self.driver.find_element_by_class_name("dataentrytable").submit()
        self.sleepppp()
        el = self.driver.find_element_by_id('subj_id')
        for option in el.find_elements_by_tag_name('option'):
            if option.text == self.major:
                option.click()
        self.sleepppp()
        for i in self.driver.find_elements_by_xpath("//*[@type='submit']"):
            if i.get_attribute("value") == "Course Search":
                i.click()
                break
        self.sleepppp()
        terminate = False
        for form in self.driver.find_elements_by_tag_name('form'):
            should_submit = False
            for inpp in form.find_elements_by_tag_name('input'):
                if inpp.get_attribute("name") == "SEL_CRSE" and inpp.get_attribute("value") == self.classNum:
                    should_submit = True
                if should_submit and inpp.get_attribute("type") == "submit":
                    inpp.click()
                    terminate = True
                    break
            if terminate:
                break

    
    #
    #     #get user metadata
    #     boardCount = self.driver.find_element_by_xpath('//*[@class="BoardCount Module"]')
    #     boardCount = boardCount.find_element_by_xpath('span[1]').text
    #     userInfoDict['boardCount'] = boardCount
    #
    #     pinCount = self.driver.find_element_by_xpath('//*[@class="Module PinCount"]')
    #     pinCount = pinCount.find_element_by_xpath('span[1]').text
    #     userInfoDict['pinCount'] = pinCount
    #
    #     likeCount = self.driver.find_element_by_xpath('//*[@class="LikeCount Module"]')
    #     likeCount = likeCount.find_element_by_xpath('span[1]').text
    #     userInfoDict['likeCount'] = likeCount
    #
    #     followerCount = self.driver.find_element_by_xpath('//*[@class="FollowerCount Module"]')
    #     followerCount = followerCount.find_element_by_xpath('span[1]').text
    #     userInfoDict['followerCount'] = followerCount
    #
    #     followingCount = self.driver.find_element_by_xpath('//*[@class="FollowingCount Module"]')
    #     followingCount = followingCount.find_element_by_xpath('span[1]').text
    #     userInfoDict['followingCount'] = followingCount
    #
    #     boardList = []
    #     pinDict = {}
    #     #get board list
    #     self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    #     try:
    #         WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "boardLinkWrapper")))
    #     except Exception as e:
    #         print "no board in user"
    #     finally:
    #         boardElementList = self.driver.find_elements_by_class_name('boardLinkWrapper')
    #         for board in boardElementList:
    #             try:
    #                 href = board.get_attribute('href')
    #                 hrefArr = href.split('/')
    #                 boardList.append(hrefArr[len(hrefArr) - 2])
    #             except Exception as e:
    #                 print "no href"
    #
    #     userInfoDict['boardList'] = boardList
    #     #get all the pins
    #     pinsURL = 'https://www.pinterest.com/' + userID + '/pins/'
    #     pinDict = self.getPinDict(pinsURL)
    #
    #     likesURL = 'https://www.pinterest.com/' + userID + '/likes/'
    #     likeDict = self.getPinDict(likesURL)
    #
    #     userInfoDict['likeDict'] = likeDict
    #     userInfoDict['pinDict'] = pinDict
    #
    #     return userInfoDict
    #
    # def getPinDict(self, url):
    #     self.driver.get(url)
    #     pinDict = {}
    #     try:
    #         WebDriverWait(self.driver, 8).until(EC.presence_of_element_located((By.CLASS_NAME, "pinHolder")))
    #     except Exception as e:
    #         print "no Pin"
    #     else:
    #         currentHeight = 0
    #         #terminate when no more new pin can be found
    #         sameLengthCount = 0
    #         oldLength = 0
    #         while len(pinDict) < MAXIMUM_MINE_OBJECT and sameLengthCount < 200 :
    #             try:
    #                 WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "fadeContainer")))
    #             finally:
    #                 self.driver.execute_script("window.scrollTo(0, " + str(currentHeight) + ");")
    #                 currentHeight = currentHeight + 1200
    #                 pinsElementList = self.driver.find_elements_by_xpath('//*[@class="pinImageWrapper draggable"]')
    #                 if oldLength == len(pinsElementList):
    #                     sameLengthCount = sameLengthCount + 1
    #                 else:
    #                     sameLengthCount = 0
    #                     oldLength = len(pinsElementList)
    #                     for pin in pinsElementList:
    #                         try:
    #                             href = pin.get_attribute('href')
    #                             hrefArr = href.split('/')
    #                             pinDict[hrefArr[len(hrefArr) - 2]] = True
    #                         except Exception as e:
    #                             print "no href"
    #                             break
    #
    #     return pinDict
    #
    # def quit(self):
    #     self.driver.quit()
    #
    # def getMainPinIDs(self):
    #     URL = 'https://www.pinterest.com/categories/everything/'
    #     print URL
    #     pinDict = {}
    #     self.database = database.Database()
    #
    #     self.driver.get(URL)
    #     try:
    #         WebDriverWait(self.driver, 8).until(EC.presence_of_element_located((By.CLASS_NAME, "pinHolder")))
    #     except Exception as e:
    #         print "no Pin"
    #     else:
    #         currentHeight = 0
    #         #terminate when no more new pin can be found
    #         sameLengthCount = 0
    #         oldLength = 0
    #         while sameLengthCount < 200 :
    #             try:
    #                 WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "pinHolder")))
    #             finally:
    #                 self.driver.execute_script("window.scrollTo(0, " + str(currentHeight) + ");")
    #                 currentHeight = currentHeight + 1200
    #                 pinsElementList = self.driver.find_elements_by_xpath('//*[@class="pinImageWrapper draggable"]')
    #                 print len(pinsElementList)
    #
    #                 if oldLength == len(pinsElementList):
    #                     sameLengthCount = sameLengthCount + 1
    #                 else:
    #                     sameLengthCount = 0
    #                     oldLength = len(pinsElementList)
    #                     for pin in pinsElementList:
    #                         try:
    #                             href = pin.get_attribute('href')
    #                             hrefArr = href.split('/')
    #                             if len(hrefArr[len(hrefArr) - 2]) < 20:
    #                                 print hrefArr[len(hrefArr) - 2]
    #                                 self.database.addPinID(hrefArr[len(hrefArr) - 2])
    #                                 pinDict[hrefArr[len(hrefArr) - 2]] = True
    #                         except Exception as e:
    #                             print "no href"
    #                             break
    #
    #     return pinDict
    #
    # def getPinLike(self, pinID):
    #     pinURL = 'https://www.pinterest.com/pin/' + pinID + '/'
    #     print pinURL
    #
    #     self.driver.get(pinURL)
    #     try:
    #         WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "repinLike")))
    #         try:
    #             likeBar = self.driver.find_element_by_xpath('//*[@class="Button IncrementingNavigateButton Module NavigateButton btn hasText medium repinLikeNavigateButton like leftRounded pinActionBarButton  rounded"]')
    #             return likeBar.find_element_by_class_name("buttonText").text
    #         except Exception as e:
    #             return None
    #     except Exception as e:
    #         return "Deleted"
