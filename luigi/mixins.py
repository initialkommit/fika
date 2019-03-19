import datetime

import luigi
from luigi import date_interval as luigi_date_interval


class BaseDateMixin(luigi.Task):
    """조회 일자(base_date)를 Parameter로 받는 클래스"""
    today = datetime.datetime.today()
    yesterday = today - datetime.timedelta(days=1)
    base_date = luigi.DateParameter(default=yesterday)


class DateIntervalMixin(luigi.Task):
    """조회 일자 범위를 Parameter로 받는 클래스"""
    today = datetime.datetime.now().date()
    luigi_today = luigi_date_interval.Date(today.year, today.month, today.day)
    yesterday = today - datetime.timedelta(days=1)
    luigi_yesterday = luigi_date_interval.Date(yesterday.year, yesterday.month, yesterday.day)
    date_interval = luigi.DateIntervalParameter(luigi_yesterday, luigi_today)
