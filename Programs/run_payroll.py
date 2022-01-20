#!/usr/bin/env python

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from collections import defaultdict
import pandas as pd
import numpy as np
import IMX_Utils as utils
from dateutil import parser

# TODO: a function that takes in contractor id and returns the string form of
#   id first_name last_name

# To be used in a different function
#dates_list = utils.dates_list(start_date, end_date)


def daily_hours(contractor, a_date, jobsite):
    """
    Will return the number of hours a contractor worked on a specific date
        at a specific job site.
    Args:
        contractor(int): contractor id
        a_date(str): a string date in format YYYY-MM-DD
        jobsite(str): jobsite to evaluate
    """
    hours_worked_data = pd.read_csv('../Data/Raw/Hours_Worked.csv')
    contractor_data = hours_worked_data.loc[(hours_worked_data['date'] == a_date) & (hours_worked_data['contractor_id'] == contractor)]
    contractor_data = contractor_data[contractor_data['jobsite'] == jobsite]
    hours_worked_on_date = int(contractor_data['hours_worked'].sum())
    return hours_worked_on_date


def weekly_hours(contractor, jobsite, start_date, end_date):
    dates_to_sum = utils.dates_list(start_date, end_date)
    hours_worked = []
    for date in dates_to_sum:
        hours_worked.append(daily_hours(contractor, str(date), jobsite))
    hours_worked = np.array(hours_worked)
    return hours_worked.sum()


def main():
    # Test  contractor_hours_worked
    #print(daily_hours(1001, '2022-01-05', "Big 3"))

    # Test weekly_hours
    weekly_hours(1001, 'Big 3', '2022-01-03', '2022-01-07')


if __name__=="__main__":
    main()

