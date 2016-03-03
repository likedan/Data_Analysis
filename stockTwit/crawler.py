from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from global_variables import *
class Crawler:

    def __init__(self):
        self.driver = webdriver.Firefox()#Phantom
        self.driver.set_window_size(1500, 1500)
        self.driver.get("https://www.pinterest.com/login/?referrer=home_page")
        self.login()

    #login to Pinterest with username and password
    def login(self):
        emailField = self.driver.find_element_by_name('username_or_email')
        emailField.send_keys(LOGIN_EMAIL)
        passField = self.driver.find_element_by_name('password')
        passField.send_keys(LOGIN_PASSWORD)
        submitContainer = self.driver.find_element_by_class_name('formFooterButtons')
        submitButton = submitContainer.find_element_by_xpath('button[1]')
        submitButton.click()
        try:
            WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "tokenizedInputWrapper")))
        finally:
            print "login done"

    # get the detailed information about a pin
    def populatePinInfo(self, pinID):
        pinURL = 'https://www.pinterest.com/pin/' + pinID + '/'
        print pinURL
        pinInfoDict = {}

        self.driver.get(pinURL)
        WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "pinWrapper")))
        #get image url
        try:
            imageURL = self.driver.find_element_by_class_name('pinImage').get_attribute('src')
            pinInfoDict['imageURL'] = imageURL
        except Exception as e:
            try:
                imageURL = self.driver.find_element_by_xpath('//*[@class="pinImage rounded"]').get_attribute('src')
                pinInfoDict['imageURL'] = imageURL
            except Exception as e:
                print "No Image Error"
                pinInfoDict['imageURL'] = 'no image'
        #get the shared pin People

        pinedUser = {}
        try:
            pinedUsersButton = self.driver.find_element_by_xpath('//*[@class="Button IncrementingNavigateButton Module NavigateButton btn hasText medium primary repinLikeNavigateButton pinActionBarButton  rounded"]')
            pinedUsersButton.click()
            try:
                WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "boardLinkWrapper")))
            finally:
                print "load boards done"
                currentHeight = 0
                #terminate when no more new pin can be found
                sameLengthCount = 0
                oldLength = 0
                while sameLengthCount < 100 and len(pinedUser) < MAXIMUM_MINE_OBJECT :
                    try:
                        WebDriverWait(self.driver, 5).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "boardLinkWrapper")))
                    finally:
                        self.driver.execute_script("window.scrollTo(0, " + str(currentHeight) + ");")
                        currentHeight = currentHeight + 800
                        boards = self.driver.find_elements_by_xpath('//*[@class="Board Module boardCoverImage draggable"]')
                        if oldLength == len(boards):
                            sameLengthCount = sameLengthCount + 1
                        else:
                            sameLengthCount = 0
                            oldLength = len(boards)
                            for board in boards:
                                try:
                                    href = board.find_element_by_css_selector('a').get_attribute('href')
                                    hrefArr = href.split('/')
                                    pinedUser[hrefArr[len(hrefArr) - 3]] = True
                                except Exception as e:
                                    print "no href"
                                    break

        except Exception as e:
            print "no shared People"
        pinInfoDict['pinedUser'] = pinedUser.keys()

        #get list of people who liked
        likedUser = {}
        self.driver.get(pinURL)
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "pinWrapper")))
        try:
            pinedUsersButton = self.driver.find_element_by_xpath('//*[@class="Button IncrementingNavigateButton Module NavigateButton btn hasText medium repinLikeNavigateButton like leftRounded pinActionBarButton  rounded"]')
            pinedUsersButton.click()
            try:
                WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "userWrapper")))
            finally:
                print "load users done"
                currentHeight = 0
                #terminate when no more new pin can be found
                sameLengthCount = 0
                oldLength = 0
                while sameLengthCount < 100 and len(likedUser) < MAXIMUM_MINE_OBJECT:
                    try:
                        WebDriverWait(self.driver, 5).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "userWrapper")))
                    finally:
                        self.driver.execute_script("window.scrollTo(0, " + str(currentHeight) + ");")
                        currentHeight = currentHeight + 800
                        boards = self.driver.find_elements_by_class_name('userWrapper')
                        if oldLength == len(boards):
                            sameLengthCount = sameLengthCount + 1
                        else:
                            sameLengthCount = 0
                            oldLength = len(boards)
                            for board in boards:
                                try:
                                    href = board.get_attribute('href')
                                    hrefArr = href.split('/')
                                    likedUser[hrefArr[len(hrefArr) - 2]] = True
                                except Exception as e:
                                    print "no href"
                                    break
        except Exception as e:
            print "no shared People"

        pinInfoDict['likedUser'] = likedUser.keys()
        print pinInfoDict
        return pinInfoDict

    def populateUserInfo(self, userID):
        userURL = 'https://www.pinterest.com/' + userID + '/'
        print userURL
        userInfoDict = {}

        self.driver.get(userURL)
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "nameInner")))

        #get nickname
        nickName = self.driver.find_element_by_class_name('nameInner').text
        userInfoDict['nickName'] = nickName

        #get user metadata
        boardCount = self.driver.find_element_by_xpath('//*[@class="BoardCount Module"]')
        boardCount = boardCount.find_element_by_xpath('span[1]').text
        userInfoDict['boardCount'] = boardCount

        pinCount = self.driver.find_element_by_xpath('//*[@class="Module PinCount"]')
        pinCount = pinCount.find_element_by_xpath('span[1]').text
        userInfoDict['pinCount'] = pinCount

        likeCount = self.driver.find_element_by_xpath('//*[@class="LikeCount Module"]')
        likeCount = likeCount.find_element_by_xpath('span[1]').text
        userInfoDict['likeCount'] = likeCount

        followerCount = self.driver.find_element_by_xpath('//*[@class="FollowerCount Module"]')
        followerCount = followerCount.find_element_by_xpath('span[1]').text
        userInfoDict['followerCount'] = followerCount

        followingCount = self.driver.find_element_by_xpath('//*[@class="FollowingCount Module"]')
        followingCount = followingCount.find_element_by_xpath('span[1]').text
        userInfoDict['followingCount'] = followingCount

        boardList = []
        pinDict = {}
        #get board list
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "boardLinkWrapper")))
        except Exception as e:
            print "no board in user"
        finally:
            boardElementList = self.driver.find_elements_by_class_name('boardLinkWrapper')
            for board in boardElementList:
                try:
                    href = board.get_attribute('href')
                    hrefArr = href.split('/')
                    boardList.append(hrefArr[len(hrefArr) - 2])
                except Exception as e:
                    print "no href"

        userInfoDict['boardList'] = boardList
        #get all the pins
        pinsURL = 'https://www.pinterest.com/' + userID + '/pins/'
        pinDict = self.getPinDict(pinsURL)

        likesURL = 'https://www.pinterest.com/' + userID + '/likes/'
        likeDict = self.getPinDict(likesURL)

        userInfoDict['likeDict'] = likeDict
        userInfoDict['pinDict'] = pinDict

        return userInfoDict

    def getPinDict(self, url):
        self.driver.get(url)
        pinDict = {}
        try:
            WebDriverWait(self.driver, 8).until(EC.presence_of_element_located((By.CLASS_NAME, "pinHolder")))
        except Exception as e:
            print "no Pin"
        else:
            currentHeight = 0
            #terminate when no more new pin can be found
            sameLengthCount = 0
            oldLength = 0
            while len(pinDict) < MAXIMUM_MINE_OBJECT and sameLengthCount < 200 :
                try:
                    WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "fadeContainer")))
                finally:
                    self.driver.execute_script("window.scrollTo(0, " + str(currentHeight) + ");")
                    currentHeight = currentHeight + 1200
                    pinsElementList = self.driver.find_elements_by_xpath('//*[@class="pinImageWrapper draggable"]')
                    if oldLength == len(pinsElementList):
                        sameLengthCount = sameLengthCount + 1
                    else:
                        sameLengthCount = 0
                        oldLength = len(pinsElementList)
                        for pin in pinsElementList:
                            try:
                                href = pin.get_attribute('href')
                                hrefArr = href.split('/')
                                pinDict[hrefArr[len(hrefArr) - 2]] = True
                            except Exception as e:
                                print "no href"
                                break

        return pinDict
    def quit(self):
        self.driver.quit()
