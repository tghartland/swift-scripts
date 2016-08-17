"""
Interactive command line tool to display usage stats for a container.

Number of objects stored and total size for the selected container
is printed. 
""" 

# Author: Thomas Hartland
# Email: t.hartland@lancaster.ac.uk

# Ignore warnings for Python 2.6
import warnings
warnings.simplefilter("ignore", DeprecationWarning)
warnings.simplefilter("ignore", UserWarning)

import sys

from swift_connect import swift_connect


conn = swift_connect()

# Get account and print list of containers
# get_account gets a tuple ({metadata}, [list of containers])
acc = conn.get_account()
print(acc[0])
for i, container in enumerate(acc[1]):
    print("%s: %s" % (i, container["name"]))


while True:
    index = raw_input("Enter a container to get stats for (or 'exit'): ")
    if index == "exit":
        break
    if not index.isdigit():
        print("Enter a number")
        continue

    index = int(index)

    if index < 0 or index >= len(acc[1]):
        print("Index out of range")
        continue

    container_name = acc[1][index]["name"]

    print("Getting container %s" % container_name)

    # get_container gets a tuple with ({metadata}, [list of objects])
    # object list is limited to 10000 objects unless full_listing=True
    # passed to conn.get_container. Only use if you actually need
    # the entire list, otherwise it just wastes time.
    container = conn.get_container(container_name)

    metadata = container[0]
    object_count = metadata["x-container-object-count"]
    size = int(metadata["x-container-bytes-used"])
    label = "b"

    for s, l in [(1024**3, "gb"), (1024**2, "mb"), (1024, "kb")]:
        if size > s:
            size = float(size) / s
            label = l
            break

    print("Total objects: %s" % object_count)
    print("Total size: %0.2f %s" % (size, label))
