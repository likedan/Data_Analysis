from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time
from random import randint

class Crawler:

    def __init__(self, combination, major, classNum):
        self.combination = combination
        self.major = major
        self.classNum = classNum
        print "init Crawler"
        # options = []
        # options.append('--load-images=false')
        # firefox_profile = webdriver.FirefoxProfile()
        # firefox_profile.set_preference("browser.download.folderList",2)
        # firefox_profile.set_preference("javascript.enabled", False)

        self.driver = webdriver.Firefox()#firefox_profile=firefox_profile)
        self.driver.set_window_size(1500, 1500)
        self.driver.get("https://eas.admin.uillinois.edu/eas/servlet/EasLogin?redirect=https://webprod.admin.uillinois.edu/ssa/servlet/SelfServiceLogin?appName=edu.uillinois.aits.SelfServiceLogin&dad=BANPROD1")

        self.login()
        self.navigate()
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
        emailField.send_keys("kedanli2")
        passField = self.driver.find_element_by_id('PASSWORD')
        passField.send_keys("Fox4ever")
        self.driver.find_element_by_class_name('idbuttons').click()

    def sleepppp(self):
        num = randint(10,30)
        time.sleep(float(num)/20)

    def navigate(self):
        self.driver.find_element_by_link_text('Registration & Records').click()
        self.sleepppp()
        self.driver.find_element_by_link_text('Registration').click()
        self.sleepppp()
        self.driver.find_element_by_link_text('Add/Drop Classes').click()
        self.sleepppp()
        self.driver.find_element_by_link_text('I Agree to the Above Statement').click()
        self.sleepppp()

    def select(self):
        el = self.driver.find_elements_by_tag_name('input')
        for i in el:
            if i.get_attribute("type") == "submit" and i.get_attribute("value") == "Submit":
                i.click()
        el = self.driver.find_elements_by_tag_name('input')
        for num in xrange(len(self.combination)):
            for i in el:
                if i.get_attribute("id") == "crn_id" + str(num+1) and i.get_attribute("name") == "CRN_IN":
                    i.send_keys(self.combination[num])
                    break
                    break
        for i in el:
            if i.get_attribute("name") == "REG_BTN" and i.get_attribute("value") == "Submit Changes":
                i.click()
                break



        # selector = self.driver.find_element_by_id('term_input_id')
        # selector.find_element_by_xpath("//select/option[@value='120161']").click()
        # self.driver.find_element_by_class_name("dataentrytable").submit()
        # self.sleepppp()
        # el = self.driver.find_element_by_id('subj_id')
        # for option in el:
        #     if option.text == self.major:
        #         option.click()
        # self.sleepppp()
        # for i in self.driver.find_elements_by_xpath("//*[@type='submit']"):
        #     if i.get_attribute("value") == "Course Search":
        #         i.click()
        #         break
        # self.sleepppp()
        # terminate = False
        # for form in self.driver.find_elements_by_tag_name('form'):
        #     should_submit = False
        #     for inpp in form.find_elements_by_tag_name('input'):
        #         if inpp.get_attribute("name") == "SEL_CRSE" and inpp.get_attribute("value") == self.classNum:
        #             should_submit = True
        #         if should_submit and inpp.get_attribute("type") == "submit":
        #             inpp.click()
        #             terminate = True
        #             break
        #     if terminate:
        #         break

    def check(self):
        available_list = {}

        for block in self.driver.find_elements_by_class_name("dddefault"):
            for choice in block.find_elements_by_tag_name('input'):
                if len(choice.get_attribute("value")) == 12:
                    available_list[choice.get_attribute("value")[:5]] = choice

        selectable = True
        for clas in self.combination:
            if clas not in available_list.keys():
                selectable = False

        if selectable:
            for clas in self.combination:
                available_list[clas].click()
            for but in self.driver.find_elements_by_tag_name('input'):
                if but.get_attribute("value") == "Register" and but.get_attribute("name") == "ADD_BTN":
                    but.click()
                    break
            return True

        print available_list
        return False
        # select() in earlier versions of webdriver

        # self.driver.find_element_by_class_name('submenulinktext2').click()
        # submitButton.click()
        # self.driver.find_element_by_id("SubmissionUpload").send_keys(os.getcwd()+"/sampleSubmission.csv")
        # self.driver.find_element_by_id('submission-form').submit()


        # try:
        #     WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "tokenizedInputWrapper")))
        # finally:
        #     print "login done"

    # get the detailed information about a pin
    # def populatePinInfo(self, pinID):
    #     pinURL = 'https://www.pinterest.com/pin/' + pinID + '/'
    #     print pinURL
    #
    #     self.driver.get(pinURL)
    #     WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "pinWrapper")))
    #     #get image url
    #     try:
    #         imageURL = self.driver.find_element_by_class_name('pinImage').get_attribute('src')
    #         pinInfoDict['imageURL'] = imageURL
    #     except Exception as e:
    #         try:
    #             imageURL = self.driver.find_element_by_xpath('//*[@class="pinImage rounded"]').get_attribute('src')
    #             pinInfoDict['imageURL'] = imageURL
    #         except Exception as e:
    #             print "No Image Error"
    #             pinInfoDict['imageURL'] = 'no image'
    #     #get the shared pin People
    #
    #     pinedUser = {}
    #     try:
    #         pinedUsersButton = self.driver.find_element_by_xpath('//*[@class="Button IncrementingNavigateButton Module NavigateButton btn hasText medium primary repinLikeNavigateButton pinActionBarButton  rounded"]')
    #         pinedUsersButton.click()
    #         try:
    #             WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "boardLinkWrapper")))
    #         finally:
    #             print "load boards done"
    #             currentHeight = 0
    #             #terminate when no more new pin can be found
    #             sameLengthCount = 0
    #             oldLength = 0
    #             while sameLengthCount < 100 and len(pinedUser) < MAXIMUM_MINE_OBJECT :
    #                 try:
    #                     WebDriverWait(self.driver, 5).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "boardLinkWrapper")))
    #                 finally:
    #                     self.driver.execute_script("window.scrollTo(0, " + str(currentHeight) + ");")
    #                     currentHeight = currentHeight + 800
    #                     boards = self.driver.find_elements_by_xpath('//*[@class="Board Module boardCoverImage draggable"]')
    #                     if oldLength == len(boards):
    #                         sameLengthCount = sameLengthCount + 1
    #                     else:
    #                         sameLengthCount = 0
    #                         oldLength = len(boards)
    #                         for board in boards:
    #                             try:
    #                                 href = board.find_element_by_css_selector('a').get_attribute('href')
    #                                 hrefArr = href.split('/')
    #                                 pinedUser[hrefArr[len(hrefArr) - 3]] = True
    #                             except Exception as e:
    #                                 print "no href"
    #                                 break
    #
    #     except Exception as e:
    #         print "no shared People"
    #     pinInfoDict['pinedUser'] = pinedUser.keys()
    #
    #     #get list of people who liked
    #     likedUser = {}
    #     self.driver.get(pinURL)
    #     WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "pinWrapper")))
    #     try:
    #         pinedUsersButton = self.driver.find_element_by_xpath('//*[@class="Button IncrementingNavigateButton Module NavigateButton btn hasText medium repinLikeNavigateButton like leftRounded pinActionBarButton  rounded"]')
    #         pinedUsersButton.click()
    #         try:
    #             WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "userWrapper")))
    #         finally:
    #             print "load users done"
    #             currentHeight = 0
    #             #terminate when no more new pin can be found
    #             sameLengthCount = 0
    #             oldLength = 0
    #             while sameLengthCount < 100 and len(likedUser) < MAXIMUM_MINE_OBJECT:
    #                 try:
    #                     WebDriverWait(self.driver, 5).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "userWrapper")))
    #                 finally:
    #                     self.driver.execute_script("window.scrollTo(0, " + str(currentHeight) + ");")
    #                     currentHeight = currentHeight + 800
    #                     boards = self.driver.find_elements_by_class_name('userWrapper')
    #                     if oldLength == len(boards):
    #                         sameLengthCount = sameLengthCount + 1
    #                     else:
    #                         sameLengthCount = 0
    #                         oldLength = len(boards)
    #                         for board in boards:
    #                             try:
    #                                 href = board.get_attribute('href')
    #                                 hrefArr = href.split('/')
    #                                 likedUser[hrefArr[len(hrefArr) - 2]] = True
    #                             except Exception as e:
    #                                 print "no href"
    #                                 break
    #     except Exception as e:
    #         print "no shared People"
    #
    #     pinInfoDict['likedUser'] = likedUser.keys()
    #     print pinInfoDict
    #     return pinInfoDict
    #
    # def populateUserInfo(self, userID):
    #     userURL = 'https://www.pinterest.com/' + userID + '/'
    #     print userURL
    #     userInfoDict = {}
    #
    #     self.driver.get(userURL)
    #     WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "nameInner")))
    #
    #     #get nickname
    #     nickName = self.driver.find_element_by_class_name('nameInner').text
    #     userInfoDict['nickName'] = nickName
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
