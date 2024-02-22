from threading import Thread
from threading import Lock
from datetime import datetime
import random
import time

# Mutex locks for writers
resource = Lock()
wrtCount = Lock()
counter = Lock()
priority = Lock()

# Global variable
shared_string = "Initial String Value"

# Counters
rdCount = 0
writersWaiting = 0

# Writes a timestamp, including seconds, to the string.
class WriterA(Thread):
    def run(self):
        global shared_string
        global writersWaiting

        while True:
            time.sleep(random.uniform(0, 3 / 10))
            with wrtCount:
                writersWaiting += 1

            # Acquire mutex lock for writers
            with resource:
                print("Entered CS for WriterA using thread: %s " % (self.name))

                # Only retrieve priority if locked was released or it's the first writer in a sequence of writers
                if not priority.locked():
                    priority.acquire()

                with wrtCount:
                    writersWaiting -= 1

                # Prints out shared_string before and after
                temp = datetime.now()
                print("Shared shared_string BEFORE overwrite for %s is: %s " % (self.name, shared_string))
                shared_string = temp.strftime("%Y/%m/%d %H:%M:%S")
                print("Shared shared_string AFTER overwrite for %s is:  %s " % (self.name, shared_string))

                with wrtCount:
                    # Release counter
                    if writersWaiting == 0:
                        # Release priority if we have no writers waiting to enter CS
                        if priority.locked():
                            priority.release()

            print("Exit CS for WriterA using thread: %s " % (self.name) + "\n" + '-' * 68)


# Writes a reversed timestamp, including seconds, to the string.

class WriterB(Thread):
    def run(self):
        global shared_string
        global writersWaiting

        while True:

            time.sleep(random.uniform(0, 3 / 10))

            print("WriterB requests access to entry section")

            with wrtCount:
                writersWaiting += 1

            # ENTER CRITICAL SECTION
            with resource:
                print("Entered CS [WriterB]")
                with wrtCount:
                    print("decrementing writer count of writerB")
                    writersWaiting -= 1


                    # Acquire priority for writers if there are writers waiting
                    #if writersWaiting > 0:
                    print("trying to acquire writer priority in writerB")
                    priority.acquire()
                    print("ACQUIRED writer priority in writerB")

                # Prints out shared_string before and after
                temp = datetime.now()
                print("Shared shared_string BEFORE overwrite for %s is:  %s " % (self.name, shared_string))
                shared_string = temp.strftime("%S:%M:%H %d/%m/%Y")
                print("Shared shared_string AFTER overwrite for %s is:  %s " % (self.name, shared_string))
            with wrtCount:
                if writersWaiting == 0:
                    print("Releasing lock for readers, no more writers waiting")
                    # Release priority
                    priority.release()
                    #counter.release()

                    # Make sure readers can read
                    #if counter.locked():
                        #counter.release()

                    # EXITING CRITICAL SECTION
            print("WriterB releases lock!\n" + '-' * 68)


class Reader(Thread):
    def run(self):
        global shared_string
        global rdCount

        while True:
            time.sleep(random.uniform(0, 3 / 10))

            # Priority
            print("Trying to get priority [reader]")
            priority.acquire()
            print("Retrieved priority [reader]")
            #if priority.locked():
            priority.release()
            print("Releasing priority [reader]")

            print("Reader want to enter entry section")

            # Entry section
            with counter:
                print("Reader retrieves counter [entry section]")
                rdCount += 1

                # No writers can write if there are readers in the critical section
                if rdCount == 1:
                    print(">>>Reader acquires writer lock!")
                    resource.acquire()
                print("Reader exits entry section")

            # Critical section
            print("Prints out shared shared_string for reader: ", shared_string)

            # Exit section
            with counter:
                print("Reader retrieves counter [exit section]")
                rdCount -= 1

                # Releases writerMutex
                if rdCount == 0:
                    print("<<<Releasing lock for writer")
                    resource.release()
                print("Reader exits [exit section]")

            print("Releases lock for Reader!\n", '-' * 68)

def main():
    threads = []

    t1 = WriterA()
    threads.append(t1)
    t1.start()

    t2 = Reader()
    threads.append(t2)
    t2.start()

    t3 = Reader()
    threads.append(t3)
    t3.start()

    t4 = Reader()
    threads.append(t4)
    t4.start()

    t5 = WriterA()
    threads.append(t5)
    t5.start()

    # Waits for all threads to finish executing
    for t in threads:
        t.join()

main()

