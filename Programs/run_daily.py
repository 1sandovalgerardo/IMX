#!/usr/bin/env python

import tkinter as tk
from tkinter import ttk
import IMX_Utils as utils
from dateutil import parser

#### Need ####
## Revenue by ticket
## Revenue for company by day
## Contractor pay by ticket
## Contractor pay by day

## Select Company
## Revenue by ticket
##  Revenue for day

def generate_daily(*args):
    """Expected Args: company_name, jobsite, start_date, end_date
        in respective order."""
    company_name = args[0].get()
    jobsite = args[1].get()
    start_date = args[2].get()
    end_date = args[3].get()
    if start_date == end_date:
        revenue = utils.days_revenue(company_name, start_date)
        return revenue
    else:
        pass
        ## Start logic if getting the cummulative sum of
        ## of revenue from start to end.
        ## I will need to use utils.multiday_revenue()
        ## Look at creating a function generate_daily_data() that can be used to
        ## run template excel reports


def run_report_gui():
    master_window = tk.Tk()

    tk.Label(master_window, text=' ').grid(row=0)
    tk.Label(master_window, text='Select Company Name').grid(row=1)
    tk.Label(master_window, text='Select Job Site').grid(row=2)
    ## Add functionality for start and end date
    tk.Label(master_window, text='Enter start date: ').grid(row=3)
    tk.Label(master_window, text='Enter end date: ').grid(row=3, column=3)


    # Create companies dropdown menu
    ## I commented out this function. I'm not sure if it does anything.
    #def company_show():
    #    tk.label.config(text=clicked.get())
    # company_options
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
    company_name_menu.grid(row=1, column=2)
    company_jobsite_menu.grid(row=2, column=2)
    start_date.grid(row=3, column=2)
    end_date.grid(row=3, column=4)

    ## Buttons on window
    company_jobsite_menu.bind('<Button-1>', callback)
    tk.Button(master_window, text='Close', command=master_window.quit).grid(row=4, column=1, sticky=tk.W, pady=4)
    tk.Button(master_window, text='Run Daily',
              command = lambda: generate_daily(selected_company,
                                          company_jobsite_menu,
                                          start_date,
                                          end_date)).grid(row=4, column=3, pady=4)


    master_window.mainloop()

def main():
    run_report_gui()

if __name__=='__main__':
    main()









