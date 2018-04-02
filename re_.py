import re

REGEXS = {
    'mobile': r'^\d{3}-\d{3,4}-\d{4}$',
    'email': r'^[0-9a-zA-Z]([-_\.]?[0-9a-zA-Z])*@[0-9a-zA-Z]([-_\.]?[0-9a-zA-Z])*\.[a-zA-Z]{2,3}$',
    'full_url': r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
    'yyyy_mm_dd': r'\d{4}[\.-/]\d{2}[\.-/]\d{2}',  # ex) 2016-09-23, 2016/09/23,

}


def remove_first_chars(s, ch):
    return re.sub(r'^' + ch + '*', '', s)


def remove_last_chars(s, ch):
    return re.sub(r'' + ch + r'.*$', '', s)


def is_correct_by_regex(string, elem='mobile') -> bool:
    regex = None
    try:
        regex = REGEXS[elem]
    except KeyError:
        print('Not Found %s' % elem)

    pattern = re.compile(regex)
    if re.match(pattern, string):
        return True
    return False


def get_match(string, elem='mobile'):
    """정규표현식에 맞는 문자열 가져오기"""
    match = re.search(REGEXS(elem), string)
    if match:
        return match.group(0)
    else:
        return None


if __name__ == '__main__':
    print(remove_first_chars(',,,a,b,c', ','))
    print(remove_last_chars('a,b,c,,,,', ','))

    numbers = ["010-7324-7942", "017-123-4567", "00-00-0000", "abc-1111-1111"]
    for number in numbers:
        print("%s -> %s" % (number, is_correct_by_regex(number, elem='mobile')))
