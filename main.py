# Problem 1 - Mutual exclusion
# Only one writer can write at a time
# No writer can write while a reader is reading
# Writers have priority

import threading
from threading import Thread
from threading import Lock
from threading import Semaphore
from datetime import datetime
import random
import time

# Mutex lock for Writers
lock = Lock()

readLock = Lock()

# Semaphore for Readers, up to 3 active readers can read concurrently
#rd = Semaphore(3)

# Shared resource
resource = "Initial String Value"

# Keeps track of readers
readers = 0

writers = 0

# Writes a timestamp, including seconds, to the string.
class WriterA(Thread):
    def run(self):
        global resource
        global readers
        #global writers

        for x in range(1, 10):

            time.sleep(random.uniform(0, 3/10))

            print("WriterA requests access")

            # Acquire mutex lock for writers
            lock.acquire()

            # Writers priority
            #if ()

            temp = datetime.now()

            print("WriterA locking!")
            t = time.localtime()
            print("Shared resource BEFORE overwrite for %s is: %s " % (self.name, resource))
            resource = temp.strftime("%Y/%m/%m %H:%M:%S")
            print("Shared resource AFTER overwrite for %s is:  %s " % (self.name, temp))

            lock.release()
            print("WriterA releases lock!\n" + '-' * 68)

# Writes a reversed timestamp, including seconds, to the string.
class WriterB(Thread):
    def run(self):
        global resource
        #global readers
        global writers

        for x in range(1, 10):

            time.sleep(random.uniform(0,3/10))

            print("WriterB requests access")

            # Fetch lock
            lock.acquire()
            temp = datetime.now()

            print("WriterB locks!")

            print("Shared resource BEFORE overwrite for %s is:  %s " % (self.name, resource))
            resource = temp.strftime("%Y/%m/%m %H:%M:%S")
            # %S%M%H %m %m %Y

            resource = temp.strftime("%S:%M:%H %d%m%Y")

            print("Shared resource AFTER overwrite for %s is:  %s " % (self.name, resource))

            # Release lock
            lock.release()
            print("WriterB releases lock!\n" + '-' * 68)

class Reader(Thread):
    def run(self):
        global resource
        global readers

        for x in range(1, 10):

            time.sleep(random.uniform(0, 3/10))

            # Only one reader can modify readers at the time
            readLock.acquire()

            print("Reader locks!")

            # Entry section

            # Keeps track of the number of readers
            readers += 1

            if readers == 1:
                lock.acquire()
                print("Aquiring lock so no Writers can write!")

            # Releasing lock for entry
            readLock.release()

            # Temporary copy to print out the string equivalent of the number of readers
            tmp = str(readers)
            print("Right now there are: " + tmp + " number of readers")

            # Critical section
            print("Prints out shared resource for reader: ", resource)

            # Getting lock for exit section, prevents data race
            readLock.acquire()

            # Exit section
            readers -= 1

            # If there are no readers reading, return the lock
            if readers == 0:
                lock.release()
                print("Releasing lock so writers can write")

            # Release after exit
            readLock.release()

            print("Releases lock for Reader!\n", '-' * 68)


def main():
    threads = []

    t1 = Reader()
    threads.append(t1)
    t1.start()

    t2 = Reader()
    threads.append(t2)
    t2.start()

    t3 = WriterA()
    threads.append(t3)
    t3.start()

    t4 = WriterB()
    threads.append(t4)
    t4.start()

    #t5 = WriterB()
    #threads.append(t5)
    #t5.start()

    #t6 = Reader()
    #threads.append(t6)
    #t6.start()

    # Waits for all threads to finish executing
    for t in threads:
        t.join()

main()
