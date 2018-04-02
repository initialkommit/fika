import time
from multiprocessing import Value
from multiprocessing.queues import Queue, JoinableQueue


class CountableQueue(Queue):
    """A portable implementation of multiprocessing.Queue
    Counter를 이용해 Queue의 요소를 셀 수 있도록 한다.
    """

    def __init__(self, *args, **kwargs):
        import multiprocessing
        ctx = multiprocessing.get_context()
        super(CountableQueue, self).__init__(*args, **kwargs, ctx=ctx)
        self.counter = Counter(0)

    def put(self, *args, **kwargs):
        super(CountableQueue, self).put(*args, **kwargs)
        self.counter.increase()

    def get(self, *args, **kwargs):
        ret = super(CountableQueue, self).get(*args, **kwargs)
        self.counter.decrease()
        return ret

    @property
    def qsize(self):
        """Reliable implementation of multiprocessing.Queue.qsize() """
        return self.counter.value


class CountableJoinableQueue(JoinableQueue):
    """A portable implementation of multiprocessing.JoinableQueue
    Counter를 이용해 Queue의 요소를 셀 수 있도록 한다.
    """

    def __init__(self, *args, **kwargs):
        import multiprocessing
        ctx = multiprocessing.get_context()
        super(CountableJoinableQueue, self).__init__(*args, **kwargs, ctx=ctx)
        self.counter = Counter(0)

    def put(self, *args, **kwargs):
        self.counter.increase()
        super(CountableJoinableQueue, self).put(*args, **kwargs)

    def get(self, *args, **kwargs):
        self.counter.decrease()
        return super(CountableJoinableQueue, self).get(*args, **kwargs)

    @property
    def qsize(self):
        """Reliable implementation of multiprocessing.Queue.qsize() """
        return self.counter.value


class Counter(object):
    def __init__(self, initval=0):
        self.val = Value('i', initval)

    def __repr__(self):
        return str(self.val.value)

    def __add__(self, other):
        with self.val.get_lock():
            self.val.value += other
            return self

    def __sub__(self, other):
        with self.val.get_lock():
            self.val.value -= other
            return self

    def increase(self, other=1):
        with self.val.get_lock():
            self.val.value += other

    def decrease(self, other=1):
        with self.val.get_lock():
            self.val.value -= other

    def set(self, value):
        with self.val.get_lock():
            self.val.value = value

    @property
    def value(self):
        return self.val.value


if __name__ == '__main__':
    from multiprocessing import Process


    def func(counter):
        for i in range(50):
            time.sleep(0.01)
            counter += 1


    counter = Counter(0)
    procs = [Process(target=func, args=(counter,)) for i in range(10)]
    counter.set(10)

    for p in procs:
        p.start()
    for p in procs:
        p.join()

    print(counter.get())
    print(counter)
    counter -= 10
    print(counter)
