import threading
import crawler_queue
import beanstalkc

def hahaha():
    print "stt"

queue = crawler_queue.CrawlerQueue()
queue.updateUnit("XXXXX", hahaha)
queue.updateUnit("XX134X", hahaha)
queue.updateUnit("XX324X", hahaha)
queue.updateUnit("XXX234X", hahaha)
queue.updateUnit("XXrX", hahaha)
queue.updateUnit("XXsdfX", hahaha)
queue.updateUnit("XXdgfX", hahaha)



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
