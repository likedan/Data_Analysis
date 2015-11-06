import beanstalkc
import threading

beanstalk = beanstalkc.Connection(host='localhost', port=11300)
beanstalk.use('unit_to_update')
beanstalk.put('ZH350127')
beanstalk.watch('update_unit_ZH350127')
print "AAA"
print beanstalk.watching()
job = beanstalk.reserve()
print job.body

def addJob(id):
    beanstalk = beanstalkc.Connection(host='localhost', port=14711)
    beanstalk.use('unit_to_update')
    beanstalk.put(id)
    string = 'update_unit_' + id
    beanstalk.watch(string)
    job = beanstalk.reserve(timeout=10000)
    print job.body

for num in range(0, 10):
    p = threading.Thread(target=addJob, args=("ZH350127",))
    p.start()

for num in range(0, 13):
    p = threading.Thread(target=addJob, args=("ZH350327",))
    p.start()

for num in range(0, 13):
    p = threading.Thread(target=addJob, args=("ZH453327",))
    p.start()
