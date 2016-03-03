#!/usr/bin/env python
from twilio.rest import TwilioRestClient
import time
from random import randint
import crawler
import checker
combination = [["38319"],["38315"],["51326"],["51327"],["38297"],["38284"],["38300"],["58993"],["38285"],["51330"],["38284"],["38300"],["58993"],["58989"],["38321"]]
select = None

def send_message(message):
	account_sid = "ACd4c3fbbe5af185b06bce7e1032adcd56"
	auth_token = "4117b759bae2e5d74ea414b6290fe237"
	client = TwilioRestClient(account_sid, auth_token) 
	client.messages.create(to="+12175080347", from_="+12176864502", body=message)

# my_crawler = crawler.Crawler(select, "Kinesiology", "100")

my_checker = checker.Checker(combination)
while True:
    num = randint(3,8)
    time.sleep(float(num))
    state = my_checker.check() 
    if state == None:
    	print ""
    else:
		select = state
		break
print select
my_checker.driver.quit()

send_message(str(select))
# my_crawler = crawler.Crawler(select, "Art", "100")
# my_crawler.select()
# num = randint(250,600)
# time.sleep(float(num))
# print "got course"
