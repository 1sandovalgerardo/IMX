from . import tickets
from . import data
from . import jobsite
from dateutil import parser
from datetime import timedelta
import datetime as dt



__all__ = ['tickets',
           'data',
           'jobsite',
           'utilities'
           ]


def dates_list(start_date, end_date):
    if start_date == end_date:
        return start_date
    # check if its dt.date() object
    if not isinstance(start_date, dt.date) or not isinstance(end_date, dt.date):
        start_date = parser.parse(start_date).date()
        end_date = parser.parse(end_date).date()
    number_of_days = int((end_date - start_date).days)
    # create list of dates
    list_of_dates = []
    for n in range(number_of_days + 1):
        date_to_add = start_date + timedelta(days=n)
        list_of_dates.append(date_to_add)
    list_of_dates = [str(date) for date in list_of_dates]
    return list_of_dates

