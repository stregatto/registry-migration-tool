import datetime
import os

class LogFile(object):


    def __init__(self):
        self.filename = os.environ.get('DT_MIGRATION_TOOL_LOG', '/tmp/registry_migration.log')
        self.__touch__(self.filename)
        with open(self.filename) as f:
            self.images_log = f.read().splitlines()

    def image_done(self, string, status='OK'):
        text = "%s %s %s" % (self.__now__(),
                             string,
                             status)
        with open(self.filename, "a") as myfile:
            myfile.write('%s\n' % text)
            print(text)
        return

    def is_image_done(self, image):
        if any(image in s for s in self.images_log):
            return True
        return False

    def __touch__(self, filename, times=None):
        with open(filename, 'a'):
            os.utime(filename, times)

    def __now__(self):
        time = datetime.datetime.now()
        nowtime = "%s-%s-%s %s:%s:%s" % (time.day,
                                         time.month,
                                         time.year,
                                         time.hour,
                                         time.minute,
                                         time.second)
        return nowtime

# logfile = LogFile()
# logfile.is_image_done('pippo')
# res = logfile.image_done('pippo')
