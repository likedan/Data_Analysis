import beanstalkc
beanstalk = beanstalkc.Connection(host='localhost', port=14711)
beanstalk.use('group_to_update')
beanstalk.put('ZH350127')
beanstalk.watch('ZH350127')

job = beanstalk.reserve(timeout=10000)
print job.body
#processing
