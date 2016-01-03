#!/usr/bin/env python
import time
import database
import crawler
from multiprocessing import Process

my_crawler = crawler.Crawler()
my_crawler.check_unit_existance()

# p = Process(target=mineUser, args=(userID, database))
# p.start()
#
# p1 = Process(target=minePin, args=(pinID, database))
# p1.start()
