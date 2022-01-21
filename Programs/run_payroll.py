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




# TODO: Create a function that sums all the weight on tickets at jobsite j over
#   the specified dates.






def main():
    # Test  contractor_daily_hours
    #print(utils.contractor_daily_hours(1001, '2022-01-05', "Big 3"))

    # Test contractor_weekly_hours
    #hours_in_week = utils.contractor_weekly_hours(1001, 'Big 3', '2022-01-03', '2022-01-07')
    #print(hours_in_week)
    a = hours_in_week = utils.contractor_weekly_hours(1001, 'Big 3', '2022-01-03', '2022-01-05',
                                                  return_dates=True)
    print(a)

    # Test contractors_at_site
    #utils.contractors_at_site('Big 3', '2022-01-03', '2022-01-07')

    # Test jobsite_man_hours()
    #utils.jobsite_man_hours('Big 3', '2022-01-03', '2022-01-07')

    # Test tons_cut()
    #a = utils.tons_cut('Big 3', '2022-01-03', '2022-01-07')
    #print(type(a))
    #print(a)



if __name__=="__main__":
    main()

