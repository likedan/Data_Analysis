import threading
import beanstalkc
import time
beanstalk = beanstalkc.Connection(host='localhost', port=11300)
beanstalk.watch('unit_to_update')

while True:
    job = beanstalk.reserve()
    print job.body
    queue_to_send = 'update_unit_' + job.body
    job.delete()
    beanstalk.use(queue_to_send)
    beanstalk.put(queue_to_send)

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
