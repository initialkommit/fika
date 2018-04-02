import time
from functools import wraps


def retry(func, max_retries=1):
    @wraps(func)
    def wrapper(*args, **kwargs):
        exception = None
        for i in range(max_retries):
            try:
                return func(*args, **kwargs)
            except Exception as ex:
                exception = ex
                wait = 1 + int(i)
                print('Retry in %s seconds - %s/%s' %
                      (wait, i + 1, max_retries))
                time.sleep(wait)
        raise exception

    return wrapper


def try_except(func):
    def decorator(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            raise e

    return decorator


def elapsed(decimal_place=6):
    def __print_elapsed(func):
        def decorator(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            time_format = 'elapsed time: %%.%df secs' % decimal_place
            print(time_format % (end_time - start_time), 'in %s()' %
                  func.__name__)
            return result

        return decorator

    return __print_elapsed


@elapsed(decimal_place=3)
def __sample():
    total = 0
    for i in range(0, 100000):
        total += i
    return total
