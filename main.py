# Problem 1 - Mutual exclusion
# Only one writer can write at a time
# No writer can write while a reader is reading
# Writers have priority

from threading import Thread
from threading import Lock
from datetime import datetime
import random
import time

# Mutex locks for writers
writerLock = Lock()
wrtCountLock = Lock()

readLock = Lock()

# Shared resource
resource = "Initial String Value"

rdCount = 0
writers = 0
writersWaiting = 0


# Writes a timestamp, including seconds, to the string.
class WriterA(Thread):
    def run(self):
        global resource
        global writersWaiting

        for x in range(1, 10):
            time.sleep(random.uniform(0, 3 / 10))

            print("WriterA requests access")
            with wrtCountLock:
                writersWaiting += 1

            # Acquire mutex lock for writers
            with writerLock:
                writersWaiting -= 1

                print("WriterA locking!")
                tmp = str(writersWaiting)
                print("Atm there are " + tmp + " writers waiting to enter CS")

                # Prints out resource before and after
                temp = datetime.now()
                print("Shared resource BEFORE overwrite for %s is: %s " % (self.name, resource))
                resource = temp.strftime("%Y/%m/%d %H:%M:%S")
                print("Shared resource AFTER overwrite for %s is:  %s " % (self.name, resource))

                if writersWaiting == 0:
                    print("Releasing lock for readers, no more writers waiting")
                    # If the readLock is locked
                    if readLock.locked():
                        #readLock.release()

                else:
                    print("More writers want to write")
                    readLock.acquire()

            print("WriterA releases lock!\n" + '-' * 68)


# Writes a reversed timestamp, including seconds, to the string.

class WriterB(Thread):
    def run(self):
        global resource
        global writersWaiting

        for x in range(1, 10):
            time.sleep(random.uniform(0, 3 / 10))

            print("WriterB requests access")

            with wrtCountLock:
                writersWaiting += 1

            with writerLock:
                writersWaiting -= 1

                # Get lock for readers
                readLock.acquire()

                print("WriterB locking!")
                tmp = str(writersWaiting)
                print("Atm there are " + tmp + " writers")

                temp = datetime.now()
                print("Shared resource BEFORE overwrite for %s is:  %s " % (self.name, resource))
                resource = temp.strftime("%S:%M:%H %d/%m/%Y")
                print("Shared resource AFTER overwrite for %s is:  %s " % (self.name, resource))

                if writersWaiting == 0:
                    print("Releasing lock for readers, no more writers waiting")
                    readLock.release()

            print("WriterB releases lock!\n" + '-' * 68)


class Reader(Thread):
    def run(self):
        global resource
        global rdCount

        for x in range(1, 10):
            time.sleep(random.uniform(0, 3 / 10))

            print("Reader wants to enter")

            # Entry section
            with readLock:
                print("Reader locks!")
                rdCount += 1

                # No writers can write if there are readers in the critical section
                if rdCount == 1:
                    writerLock.acquire()

            # Temporary copy to print out the string equivalent of the number of rdCount
            tmp = str(rdCount)
            print("Right now there are: " + tmp + " readers")

            # Critical section
            print("Prints out shared resource for reader: ", resource)

            # Exit section
            with readLock:
                rdCount -= 1

                # Releases writerMutex
                if rdCount == 0:
                    print("Releasing lock for writer")
                    writerLock.release()

            print("Releases lock for Reader!\n", '-' * 68)


def main():
    threads = []

    t1 = Reader()
    threads.append(t1)
    t1.start()

    #t2 = Reader()
    #threads.append(t2)
    #t2.start()

    t3 = WriterA()
    threads.append(t3)
    t3.start()

    t4 = WriterA()
    threads.append(t4)
    t4.start()

    t5 = WriterA()
    threads.append(t5)
    t5.start()

    # t6 = Reader()
    # threads.append(t6)
    # t6.start()

    # Waits for all threads to finish executing
    for t in threads:
        t.join()


main()
