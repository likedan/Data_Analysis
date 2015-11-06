import beanstalkc
import threading

beanstalk = beanstalkc.Connection(host='localhost', port=11300)
beanstalk.use('unit_to_update')
beanstalk.put('ZH350127')
beanstalk.watch('update_unit_ZH350127')
job = beanstalk.reserve(timeout=10000)
print job.body

# def addJob(id):
#     beanstalk = beanstalkc.Connection(host='localhost', port=14711)
#     beanstalk.use('unit_to_update')
#     beanstalk.put(id)
#     string = 'update_unit_' + id
#     beanstalk.watch(string)
#     job = beanstalk.reserve(timeout=10000)
#     print job.body
#
# for num in range(0, 6):
#     p = threading.Thread(target=addJob, args=("ZH350127",))
#     p.start()
