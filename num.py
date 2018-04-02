import re
from decimal import Decimal
import math


def int2digit(n, base=10):  # base: 진수
    res = ''
    while n > 0:
        n, r = divmod(n, base)
        res = str(r) + res
    return res


def comma_str(n, decimal_spaces=0):
    """
    :param n: 수치 (문자열 또는 수치형)
    :param decimal_spaces: 소수점 자리수
    """
    try:
        if n is None:
            return None
        if decimal_spaces > 0:
            n = float(n)
        else:
            n = int(float(n))

        if isinstance(n, int):
            return r'{:,d}'.format(n)
        elif isinstance(n, float):
            rule = r'{:,.%df}' % decimal_spaces
            return rule.format(n)
        else:
            return n
    except Exception:  # @UnusedVariable
        return n


def remove_comma(line):
    return re.sub(r'''(\d),(\d{1})''', r'''\1\2''', line)


def to_readable(n):
    try:
        if (0 < math.fabs(n) < 0.001) or (1000 < math.fabs(n)):
            return "{:.1e}".format(Decimal(n))
        else:
            return n
    except:
        return n


def is_float(string):
    try:
        temp = float(string)
        return True
    except ValueError:
        return False


def str_num2init(str_num):
    """string으로 된 숫자의 처음 0 값을 삭제하고 int로 return"""
    if not str_num:
        return

    str_num = str(str_num)
    while str_num.startswith('0'):
        if str_num.startswith('0'):
            str_num = str_num[1:]

    return int(str_num)


def num2valid_digit_str(num, valid_digit=3):
    """valid_digit: 유효한 자리수
    ex) 2 -> 002
    """
    if not num:
        return

    num = str(num)
    for digit in range(valid_digit):
        if len(num) == valid_digit:
            return num
        else:
            num = '%s%s' % ('0', num)


if __name__ == '__main__':
    print(num2valid_digit_str(202, valid_digit=5))
