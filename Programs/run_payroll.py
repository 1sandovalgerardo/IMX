#!/usr/bin/env python

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from collections import defaultdict
import pandas as pd
import numpy as np
import IMX_Utils as utils
from dateutil import parser

# TODO: add popup window to confirm payroll ran

# TODO: continue on to invoice

# TODO: add logic to add the contractors payout rate for material

def payroll_logic(*args):
    jobsite = args[0].get()
    start_date = args[1].get()
    end_date = args[2].get()
    for arg in args:
        print(arg.get())
    utils.jobsite_production(jobsite, start_date, end_date, to_file=True)
    utils.jobsite_hours_worked(jobsite, start_date, end_date,
                                  to_file=True)


def run_payroll_gui():
    master_window = tk.Tk()
    master_window.title('IMX Payroll')

    tk.Label(master_window, text=' ').grid(row=0)
    tk.Label(master_window, text='Select Company Name').grid(row=1, column=1, sticky='E')
    tk.Label(master_window, text='Select Job Site').grid(row=2, column=1, sticky='E')
    ## Add functionality for start and end date
    tk.Label(master_window, text='Enter start date: ').grid(row=3, column=1, sticky='E')
    tk.Label(master_window, text='Enter end date: ').grid(row=3, column=3)


    # Create companies dropdown menu
    ## I commented out this function. I'm not sure if it does anything.
    #def company_show():
    #    tk.label.config(text=clicked.get())
    list_of_companies = utils.get_companies()
    selected_company = tk.StringVar()
    selected_company.set('CLICK FOR OPTIONS')

    # combobox for jobsites
    paired_list_company_names, jobsites = utils.get_paired_company_jobsite()
    def callback(eventObject):
        company_selected = selected_company.get()
        # Get index for company_selected as found in company_names
        selection_index = paired_list_company_names.index(company_selected)
        # This pairs with ttk.Combobox
        company_jobsite_menu.config(values=jobsites[selection_index])

    # Create GUI visual
    company_name_menu = tk.OptionMenu(master_window, selected_company, *list_of_companies)
    company_jobsite_menu = ttk.Combobox(master_window)
    start_date = tk.Entry(master_window, width=25)
    end_date = tk.Entry(master_window, width=25)

    # Place GUI objects
    company_name_menu.grid(row=1, column=2, sticky='w')
    company_jobsite_menu.grid(row=2, column=2, sticky='w')
    start_date.grid(row=3, column=2, sticky='w')
    end_date.grid(row=3, column=4, sticky='w')

    ## Buttons on window
    company_jobsite_menu.bind('<Button-1>', callback)
    tk.Button(master_window, text='Close', command=master_window.quit).grid(row=4, column=1, sticky=tk.W, pady=4)
    tk.Button(master_window, text='Run Payroll',
              command = lambda: payroll_logic(company_jobsite_menu,
                                              start_date,
                                              end_date)).grid(row=4, column=3, pady=4)


    master_window.mainloop()



def main():
    run_payroll_gui()



if __name__=="__main__":
    main()

