import pose_analyze as pa
import time
import sys

while True:
    send("hello world")
    time.sleep(1)


def send(message):
    print(message)
    sys.stdout.flush()