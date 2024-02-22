

from threading import Thread
from threading import Lock
from datetime import datetime
import random
import time

resource = Lock()
wrtCount = Lock()
priority = Lock()
counter = Lock()

# Shared shared_string
shared_string = "Initial String Value"

rdCount = 0
writersWaiting = 0

# Writes a timestamp, including seconds, to the string.
class WriterA(Thread):
    def run(self):
        global shared_string
        global writersWaiting

        while True:
            time.sleep(random.uniform(0, 3 / 10))

            # Only get the reader lock if it hasn't been acquired
            if priority.locked():
                priority.acquire()

            print("WriterA requests access")
            with wrtCount:
                writersWaiting += 1

            # Acquire mutex lock for writers
            with resource:

                with wrtCount:
                    writersWaiting -= 1

                # Prints out shared_string before and after
                temp = datetime.now()
                print("Shared shared_string BEFORE overwrite for %s is: %s " % (self.name, shared_string))
                shared_string = temp.strftime("%Y/%m/%d %H:%M:%S")
                print("Shared shared_string AFTER overwrite for %s is:  %s " % (self.name, shared_string))

                # Release counter
                if writersWaiting == 0:
                    print("Releasing lock for readers, no more writers waiting")
                    if priority.locked():
                        priority.release()

            print("WriterA releases lock!\n" + '-' * 68)


# Writes a reversed timestamp, including seconds, to the string.

class WriterB(Thread):
    def run(self):
        global shared_string
        global writersWaiting

        for x in range(1, 10):
            time.sleep(random.uniform(0, 3 / 10))

            print("WriterB requests access")

            with wrtCount:
                writersWaiting += 1

            with resource:
                writersWaiting -= 1

                print("WriterB locking!")
                tmp = str(writersWaiting)
                print("Atm there are " + tmp + " writers")

                temp = datetime.now()
                print("Shared shared_string BEFORE overwrite for %s is:  %s " % (self.name, shared_string))
                shared_string = temp.strftime("%S:%M:%H %d/%m/%Y")
                print("Shared shared_string AFTER overwrite for %s is:  %s " % (self.name, shared_string))

                if writersWaiting == 0:
                    print("Releasing lock for readers, no more writers waiting")
                    if priority.locked():
                        priority.release()

                # If there are writers waiting, acquire priority
                else:
                    priority.acquire()


            print("WriterB releases lock!\n" + '-' * 68)


class Reader(Thread):
    def run(self):
        global shared_string
        global rdCount

        #for x in range(1, 10):
        while True:
            time.sleep(random.uniform(0, 3 / 10))

            print("Reader wants to enter")

            priority.acquire()
            priority.release()

            # Entry section
            with counter:
                print("Reader locks!")
                rdCount += 1

                # No writers can write if there are readers in the critical section
                if rdCount == 1:
                    print(">>>Reader acquires writer lock!")
                    resource.acquire()

            # Temporary copy to print out the string equivalent of the number of rdCount
            tmp = str(rdCount)
            print("Right now there are: " + tmp + " readers")

            # Critical section
            print("Prints out shared shared_string for reader: ", shared_string)

            # Exit section
            with counter:
                rdCount -= 1

                # Releases writerMutex
                if rdCount == 0:
                    print("<<<Releasing lock for writer")
                    resource.release()

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

    t4 = WriterA()
    threads.append(t4)
    t4.start()

    #t5 = WriterA()
    #threads.append(t5)
    #t5.start()

    # t6 = Reader()
    # threads.append(t6)
    # t6.start()

    # Waits for all threads to finish executing
    for t in threads:
        t.join()

main()
