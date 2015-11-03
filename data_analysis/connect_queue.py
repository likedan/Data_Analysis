import beanstalkc
beanstalk = beanstalkc.Connection(host='localhost', port=14711)
beanstalk.use('crawler')
beanstalk.put('hey!')

print beanstalk.tubes()
beanstalk.watch('done')
job = beanstalk.reserve(timeout=100)
print job.body + " job"
crawler.watch("crawler")
job1 = crawler.reserve(timeout=10)
print job1.body
#processing
crawler.use('done')
crawler.put("result")
print job.body
