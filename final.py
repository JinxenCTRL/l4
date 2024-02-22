# Namn: Jens Rodin
# Datum: 22/02-2024
# Laboration 4 - Reader Writers Problem

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

# Global resource
shared_string = "Initial String Value"

rdCount = 0
writerCount = 0


# Writes a timestamp, including seconds, to the string.
class WriterA(Thread):
    def run(self):
        global shared_string
        global writerCount

        while True:
            time.sleep(random.uniform(0, 3 / 10))

            # Keeps track of writers
            with wrtCount:
                writerCount += 1

                if writerCount == 1:
                    priority.acquire()

            # Inside CS
            with resource:

                print("Entered CS for WriterA using thread: %s " % self.name)

                # Prints out shared_string before and after
                temp = datetime.now()
                print("Global resource BEFORE overwrite is: %s " % shared_string)
                shared_string = temp.strftime("%Y/%m/%d %H:%M:%S")
                print("Global resource AFTER overwrite is:  %s " % shared_string)
                print("Exiting CS for WriterA using thread: %s " % self.name + "\n" + '-' * 68)


            # Decrement counter of writer
            with wrtCount:
                writerCount -= 1

            with wrtCount:
                # If there are no writers waiting to enter CS, release priority
                if writerCount == 0:
                    priority.release()


# Writes a reversed timestamp, including seconds, to the string.

class WriterB(Thread):
    def run(self):
        global shared_string
        global writerCount

        while True:
            time.sleep(random.uniform(0, 3 / 10))

            # Keeps track of writers
            with wrtCount:
                writerCount += 1

                if writerCount == 1:
                    priority.acquire()

            # ENTER CRITICAL SECTION
            with resource:
                print("Entered CS for WriterB using thread: %s " % self.name)

                # Prints out shared_string before and after
                temp = datetime.now()
                print("Global resource BEFORE overwrite for %s is:  %s " % (self.name, shared_string))
                shared_string = temp.strftime("%S:%M:%H %d/%m/%Y")
                print("Global resource AFTER overwrite for %s is:  %s " % (self.name, shared_string))
                print("Exiting CS for WriterB using thread: %s " % self.name + "\n" + '-' * 68)

            with wrtCount:
                writerCount -= 1

            with wrtCount:
                # If there are no writers waiting to enter CS, release priority
                if writerCount == 0:
                    priority.release()


class Reader(Thread):
    def run(self):
        global shared_string
        global rdCount

        while True:
            time.sleep(random.uniform(0, 3 / 10))

            # Important for writers preference - halts reader from progressing any further
            priority.acquire()
            priority.release()


            # Entry section
            with counter:
                rdCount += 1

                # No writers can write if there are readers in the critical section
                if rdCount == 1:
                    resource.acquire()

            # Critical section
            print("Entered CS for Reader using thread: %s " % self.name)
            print("Prints out Global resource for Reader: ", shared_string)
            print("Exiting CS for Reader using thread: %s " % self.name + "\n" + '-' * 68)

            # Exit section
            with counter:
                rdCount -= 1

                # Now writers can write
                if rdCount == 0:
                    resource.release()

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

    t5 = WriterB()
    threads.append(t5)
    t5.start()

    # Waits for all threads to finish executing
    for t in threads:
        t.join()

main()