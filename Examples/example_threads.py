from threading import Thread
from time import sleep


def long_task():
    sleep(2)
    print('Long Task')


print("Before long task")
t = Thread(target=long_task)
t.start()
other_thread = Thread(target=long_task)
other_thread.start()
print("After long task")
