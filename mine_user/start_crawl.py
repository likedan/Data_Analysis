#!/usr/bin/env python
import time
# import crawler
from multiprocessing import Process
import database

db = database.Database()
print(db.get_greatest_amoung(0,200000))
print(db.get_greatest_amoung(200000,399999))
print(db.get_greatest_amoung(400000,599999))
print(db.get_greatest_amoung(600000,799999))
print(db.get_greatest_amoung(800000,999999))

# def crawl(start, end):
#     my_crawler = crawler.Crawler()
#     info = my_crawler.check_unit_existance(start, end)
#
# for x in xrange(5):
#     p = Process(target=crawl, args=(x * 200000, (x+1)*200000))
#     p.start()
