import time
import threading

# Set an new interval.

def set_interval(func, interval, params=None):
    def wrapper():
        while True:
            if params:
                func(params)
            else:
                func()
            time.sleep(interval)

    thread = threading.Thread(target=wrapper)
    thread.daemon = True
    thread.start()

    return thread

# Set an new timeout.

def set_timeout(func, timeout, params=None):
    def wrapper():
        time.sleep(timeout)

        if params:
            func(params)
        else:
            func()

    thread = threading.Thread(target=wrapper)
    thread.daemon = True
    thread.start()

    return thread