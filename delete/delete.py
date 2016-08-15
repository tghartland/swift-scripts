"""
Test deletion rate of an OpenStack container.

The "delete" method uploads a single file
to an OpenStack container and copies it
to have total_objects number of files.
All created files are then deleted, and
the deletion rate is measured.
num_threads is the number of threads
used in both the copy and delete
operations. These parameters can be
modified in settings.py. Auth details
can be given in settings.py or
found in the user environment.
"""

# Author: Thomas Hartland
# Email: t.hartland@lancaster.ac.uk



# Ignore warnings for Python 2.6 deprecation
import warnings
warnings.simplefilter("ignore", DeprecationWarning)
warnings.simplefilter("ignore", UserWarning)

import os
import urllib2
import time
import threading

from swift_connect import swift_connect
import settings

copies = 0
copy_cur_percent = 0


def delete(total_objects=settings.total_objects, num_threads=settings.num_threads, container=settings.test_container):
    print("Creating then deleting %s objects with %s threads in container '%s'" % (total_objects, num_threads, container))
    conn = swift_connect()

    # Put a single file "testfile0" in the container
    conn.put_object(container, "testfile0", os.urandom(settings.object_size*1024*1024))
    print("Uploaded testfile0")

    # Create request to copy testfile0
    opener = urllib2.build_opener(urllib2.HTTPHandler)
    req = urllib2.Request("%s/%s/testfile0" % (conn.url, container))
    req.add_header("X-Auth-Token", conn.token)
    req.get_method = lambda: "COPY"

    def copy_thread(thread_num):
        # with two threads, thread 0 will copy to testfile1, testfile3, testfile5
        # thread 1 will copy to testfile2, testfile4, testfile6, etc

        global copies, copy_cur_percent

        for i in range(1+thread_num, total_objects, num_threads):
            req.add_header("Destination", "%s/testfile%s" % (container, i))
            url = opener.open(req)

            copies += 1
            percent = int(100*(float(copies)/total_objects))
            if percent % 10 == 0 and percent > 0 and percent > copy_cur_percent:
                copy_cur_percent = percent
                print("%s%%" % percent)

    print("Starting copy operation")
    threads = []
    for thread_num in range(0, num_threads):
        t = threading.Thread(target=copy_thread, args=(thread_num,))
        threads.append(t)

    start_time = time.time()

    # start all copy threads
    [thread.start() for thread in threads]
    # wait for all copy threads to finish
    [thread.join() for thread in threads]

    time_taken = time.time()-start_time
    print("Copied testfile")
    print("Total time: %.02f s" % time_taken)
    print("Copies/s: %.02f" % (total_objects/time_taken))
    print("")



    def deletion_thread(thread_num):
        for i in range(thread_num, total_objects, num_threads):
            conn.delete_object("tgh_delete", "testfile%s" % i)

    threads = []
    for thread_num in range(0, num_threads):
        t = threading.Thread(target=deletion_thread, args=(thread_num,))
        threads.append(t)

    print("Starting deletion")
    start_time = time.time()

    # start all  delete threads
    [thread.start() for thread in threads]
    # wait for all delete threads to finish
    [thread.join() for thread in threads]


    time_taken = time.time()-start_time
    print("Deletion finished")
    print("Time taken: %.02f s" % time_taken)
    print("Deletes/s: %.02f" % (total_objects/time_taken))

if __name__ == "__main__":
     delete()
