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

# TODO: Create a function that calculates the total man hours at job site j
#   from a start date to an end date.
#   It will need to get a list of contractors c at jobsite j over the dates

def total_man_hours(jobsite, start_date, end_date):
    # calculates contractors at that job site on those dates
    # returns total hours at the jobsite
    pass


# TODO: Create a function that sums all the weight on tickets at jobsite j over
#   the specified dates.






def main():
    # Test  contractor_daily_hours
    #print(utils.contractor_daily_hours(1001, '2022-01-05', "Big 3"))

    # Test contractor_weekly_hours
    #hours_in_week = utils.contractor_weekly_hours(1001, 'Big 3', '2022-01-03', '2022-01-07')
    #print(hours_in_week)

    # Test contractors_at_site
    utils.contractors_at_site('Big 3', '2022-01-03', '2022-01-07')



if __name__=="__main__":
    main()

