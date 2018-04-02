import time
from datetime import datetime

import re


def secs2string(secs):
    secs = int(secs)
    mins, secs = divmod(secs, 60)
    hours, mins = divmod(mins, 60)
    days, hours = divmod(hours, 24)
    if days > 0:
        return '%ddays %02d:%02d:%02d' % (days, hours, mins, secs)
    else:
        return '%02d:%02d:%02d' % (hours, mins, secs)


def millisecs2string(_secs):
    secs = int(_secs)
    mili_secs = float(_secs) - secs
    mins, secs = divmod(secs, 60)
    hours, mins = divmod(mins, 60)
    days, hours = divmod(hours, 24)
    if days > 0:
        return '%ddays %02d:%02d:%02d %.4f' % (days, hours, mins, secs, mili_secs)
    else:
        return '%02d:%02d:%02d %.4f' % (hours, mins, secs, mili_secs)


def datetime2string(_datetime):
    """Convert datetime into string"""
    return '%04d-%02d-%02d %02d:%02d:%02d' % \
           (_datetime.year, _datetime.month,
            _datetime.day, _datetime.hour,
            _datetime.minute, _datetime.second)


def string2datetime(str_date, time_format='%Y-%m-%d %H:%M:%S'):
    return datetime.strptime(str_date, time_format)


def datetime2yyyymmdd(_datetime):
    return '%04d%02d%02d' % (_datetime.year, _datetime.month, _datetime.day)


def current_string_datetime(time_zero=False):
    """Return str(datetime)"""
    now = time.localtime()
    date = '%04d-%02d-%02d' % (now.tm_year, now.tm_mon, now.tm_mday)
    if time_zero:
        return '%s 00:00:00' % date
    else:
        return '%s %02d:%02d:%02d' % (date, now.tm_hour, now.tm_min, now.tm_sec)


def current_yyyymmdd():
    """Current Date: YYYY-MM-DD (Str)"""
    now = time.localtime()
    return '%04d-%02d-%02d' % (now.tm_year, now.tm_mon, now.tm_mday)


def current_yyyymm():
    now = time.localtime()
    return '%04d%02d' % (now.tm_year, now.tm_mon)


def current_yyyymmddhhmmss():
    now = time.localtime()
    return '%04d%02d%02d%02d%02d%02d' % \
           (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)


def current_hhmmss():
    now = time.localtime()
    return '%d:%d:%d' % (now.tm_hour, now.tm_min, now.tm_sec)


def current_hhmm00():
    now = time.localtime()
    return '%d:%d:00' % (now.tm_hour, now.tm_min)


def current_millisecs():
    return int(round(time.time() * 1000))


def current_microsecs():
    return int(round(time.time() * 1000000))


def now():
    return datetime.now()


def today():
    return datetime.now().date()


def is_valid_date_string(date_string):
    try:
        match = re.match(
            '^(((\d{4})(-)(0[13578]|10|11|12)(-)(0[1-9]|[12][0-9]|3[01]))|((\d{4})(-)(0[469]|11)(-)([0][1-9]|[12][0-9]|30))|((\d{4})(-)(0[2])(-)(0[1-9]|1[0-9]|2[0-8]))|(([02468][048]00)(-)(02)(-)(29))|(([13579][26]00)(-)(02)(-)(29))|(([0-9][0-9][0][48])(-)(02)(-)(29))|(([0-9][0-9][2468][048])(-)(02)(-)(29))|(([0-9][0-9][13579][26])(-)(02)(-)(29)))$',
            date_string)
        if not match:
            return False
    except ValueError:
        print('ValueError')
        return False


def is_valid_datetime_string(datetime_string):
    try:
        match = re.match(
            '^(((\d{4})(-)(0[13578]|10|11|12)(-)(0[1-9]|[12][0-9]|3[01]))|((\d{4})(-)(0[469]|11)(-)([0][1-9]|[12][0-9]|30))|((\d{4})(-)(0[2])(-)(0[1-9]|1[0-9]|2[0-8]))|(([02468][048]00)(-)(02)(-)(29))|(([13579][26]00)(-)(02)(-)(29))|(([0-9][0-9][0][48])(-)(02)(-)(29))|(([0-9][0-9][2468][048])(-)(02)(-)(29))|(([0-9][0-9][13579][26])(-)(02)(-)(29)))(\s([0-1][0-9]|2[0-4]):([0-5][0-9]):([0-5][0-9]))$',
            datetime_string)
        if not match:
            return False
    except ValueError:
        print('ValueError')
        return False
