#!/usr/bin/env python
import time
import crawler
from multiprocessing import Process

def crawl(start, end):
    my_crawler = crawler.Crawler()
    info = my_crawler.check_unit_existance(start, end)

for x in xrange(5):
    p = Process(target=crawl, args=(x * 200000, (x+1)*200000))
    p.start()
