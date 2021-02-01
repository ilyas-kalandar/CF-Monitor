from datetime import datetime
from calendar import monthrange


def date_to_str(date: datetime):
    """ Convert datetime obj to simple string """
    return f"{date.year}:{date.month}:{date.day}"


def is_between(moment, **kwargs):
    """ Return True if moment is between _from and to"""

    try:
        kwargs['_from']
    except KeyError:
        kwargs['_from'] = None

    try:
        kwargs['to']
    except KeyError:
        kwargs['to'] = None

    _from = kwargs['_from']
    to = kwargs['to']

    if _from and (moment.year < _from.year or
                  (moment.year == _from.year and moment.month < _from.month or (
                      _from.year == moment.year and
                      moment.month == _from.month and moment.day < _from.day))):
        return False
    if to and (moment.year > to.year or
               (moment.year == to.year and moment.month > to.month or (
                   moment.year == to.year and
                   moment.month == to.month and moment.day > to.day))):
        return False

    return True


def days_ago(date, d):
    """ Return a date with d days ago"""
    year = date.year
    month = date.month
    day = date.day - d

    if day <= 0:
        month -= 1
        if not month:
            month = 12
            year -= 1

        day += monthrange(year, month)[1]

    return datetime(year, month, day)
