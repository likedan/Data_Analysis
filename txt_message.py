from twilio.rest import TwilioRestClient
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time
from random import randint
from pyvirtualdisplay import Display

def send_message(message):
	# Find these values at https://twilio.com/user/account
	account_sid = "ACd4c3fbbe5af185b06bce7e1032adcd56"
	auth_token = "4117b759bae2e5d74ea414b6290fe237"
	client = TwilioRestClient(account_sid, auth_token) 
	client.messages.create(to="+12175080347", from_="+12176864502", body=message)


def get_update_message():
	display = Display(visible=0, size=(1024, 768))
	display.start()
    driver = webdriver.Firefox()
    driver.set_window_size(1000, 1000)
    driver.get("http://stocktwits.com/flourish")
    updates = driver.find_elements_by_class_name("messageli")
    messages_T = []
    for m in updates:
        body = m.find_element_by_class_name("message-body")
    	messages_T.append(body.text)
    driver.close()
    display.stop()
    print "got message"
    return messages_T

Messages = get_update_message()

while True:
	try:
	    num = randint(50,100)
	    time.sleep(float(num))
	    new_messages = get_update_message()
	    for m in new_messages:
	    	if not m in Messages:
	    		print "new message"
	    		send_message(m)
	    Messages = new_messages
	except Exception as e:
   		send_message("server down: " + str(e))