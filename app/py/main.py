import pose_analyze as pa
import time
import sys

def send(message):
    print(message)
    sys.stdout.flush()

while True:
    send("hello world")
    time.sleep(1)