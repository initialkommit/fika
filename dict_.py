import collections


def sort_by_key(di, reverse=False):
    """when reverse=False, ASC sort"""
    return collections.OrderedDict(
        sorted(di.items(), reverse=reverse))


def sort_by_value(di, reverse=False):
    """when reverse=False, ASC sort"""
    return collections.OrderedDict(
        sorted(di.items(), key=lambda t: t[1], reverse=reverse))


def strip_values(di):
    for k, v in di.items():
        di[k] = str(v).strip()
    return di


def get_key_by_value(search_value: str, d: dict):
    for key, value in d.items():
        if value == search_value:
            return key
    return None


if __name__ == '__main__':
    d = {'2': 'b', '1': '  c  ', '3': 'a'}
    print([v for v in sort_by_key(d).values()])
    # print(sort_by_key(d).keys())
    # print(sort_by_value(d))
    # print(sort_by_value(d).values())
    # print(d)
    # print(strip_values(d))
