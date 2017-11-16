import abc
import time

class AbstractLock(metaclass=abc.ABCMeta):

    def __init__(self, lock_key):
        self.lock_key = lock_key

    def __enter__(self):
        self.acquire()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()

    @abc.abstractmethod
    def acquire(self):
        """"""

    @abc.abstractmethod
    def release(self):
        """"""


class DogPileLock(AbstractLock):
    sleep = 0.1
    timeout = 5 * 60

    def __init__(self, lock_key, client,  **kwargs):
        super(DogPileLock, self).__init__(lock_key)
        self.client = client
        self.timeout = kwargs.pop('timeout', self.timeout)

    def acquire(self):
        while True:
            if self.client.set(self.lock_key, 'value', nx=True, timeout=self.timeout):
                return True
            else:
                time.sleep(self.sleep*10)

    def release(self):
        self.client.delete(self.lock_key)


if __name__ == '__main__':
    import os, threading
    import sys

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    print(BASE_DIR)
    sys.path.extend([BASE_DIR, ])
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "example.settings")

    import django
    django.setup()
    from django.core.cache import cache

    set_key = 0

    def test():
        cache.set('test_lock', 'value')
        print('require:{}'.format(time.time()))
        global set_key
        set_key = 1
        time.sleep(5)
        cache.delete('test_lock')
        print('release:{}'.format(time.time()))


    t = threading.Thread(target=test)
    t.start()


    while not set_key: time.sleep(0.1)

    start_time = time.time()
    with DogPileLock('test_lock', cache):
        print('wait time:{}'.format(time.time()-start_time))