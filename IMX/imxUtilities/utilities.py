#!/usr/bin/env python

import datetime as dt

import pandas as pd
from dateutil import parser
from datetime import timedelta
import logging
from IPython import embed


def dates_list(start_date, end_date):
    logging.debug('in utilities.dates_list')
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


def create_log(debug, gui):
    if debug:
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(levelname)s:%(name)s:%(message)s')

        fileHandler = logging.FileHandler(f'{gui}.log', 'w')
        fileHandler.setLevel(logging.DEBUG)
        fileHandler.setFormatter(formatter)
        logger.addHandler(fileHandler)

        shellHandler = logging.StreamHandler()
        shellHandler.setLevel(logging.WARNING)
        logger.addHandler(shellHandler)
        logging.debug('logging established')

def print_to_screen(data):
    columns = ['ticket_number', 'internal_id', 'company_name', 'job_site', 'date',
               'attribute_date', 'employees', 'num_of_employees', 'gross_weight',
               'tare_weight', 'net_weight', 'hours_worked', 'material_type', 'rate']
    #embed()
    data = pd.DataFrame(data=[data], columns=columns)
    print('##########')
    print(data)
    print('##########')



