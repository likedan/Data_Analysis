import beanstalkc
import threading
import time

class CrawlerQueue:

    def __init__(self):
        print "init"

    def updateUnit(self, unitID, completion):
        thread = threading.Thread(target=self.updateUnitThread, args=(unitID, completion,))
        thread.start()

    def updateUnitThread(self, unitID, completion):
        beanstalk = beanstalkc.Connection(host='localhost', port=11300)
        beanstalk.use('unit_to_update')
        beanstalk.put(unitID)
        queue_to_get = 'update_unit_' + unitID
        beanstalk.watch(queue_to_get)
        finished = beanstalk.reserve()#timeout=10000)
        finished.delete()
        print finished.body
        completion()

# def addJob(id):
#     beanstalk = beanstalkc.Connection(host='localhost', port=11300)
#     beanstalk.use('unit_to_update')
#     beanstalk.put(id)
#     string = 'update_unit_' + id
#     beanstalk.watch(string)
#     job = beanstalk.reserve(timeout=10000)
#     print job.body
#
# for num in range(0, 10):
#     p = threading.Thread(target=addJob, args=("ZH350127",))
#     p.start()
#
# for num in range(0, 13):
#     p = threading.Thread(target=addJob, args=("ZH350327",))
#     p.start()
#
# for num in range(0, 13):
#     p = threading.Thread(target=addJob, args=("ZH453327",))
#     p.start()
