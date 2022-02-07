import time
from functools import wraps


# 1 task

def timeit(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        func(*args, **kwargs)
        print(time.time() - start)

    return wrapper


@timeit
def test():
    time.sleep(0.5)


# 2 task

def clocks(hour: int, minutes: int) -> int:
    degree_per_hour = 360 // 12
    degree_per_minute = 360 // 60

    return abs(degree_per_hour * hour - degree_per_minute * minutes)


# 3 task
def expand_list(lst_: list) -> list:
    output = []
    for item in lst_:
        if isinstance(item, list):
            output += expand_list(item)
            continue
        output.append(item)
    return output


if __name__ == '__main__':
    # 3 task
    lst = expand_list([[1], [8, 7, 1, 0], [76, [98, 6]], 38])
    max_elem = max(lst)
    avg_el = sum(lst) / len(lst)
    print(max_elem, avg_el)
