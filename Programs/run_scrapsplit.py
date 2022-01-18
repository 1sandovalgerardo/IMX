#!/usr/bin/env python

import tkinter as tk
from tkinter import ttk, messagebox
import IMX_Utils as utils
from dateutil import parser

# TODO: I need to implament a method of collecting the hours each employee worked
#   This will then be used to calculate the amount of weight cut in a week to him.

# TODO: Create employe_pay_rate table. Sets the pay per ton to the employee

def scrap_split_logic(*args):
    selected_contractor, start_date, end_date = args
    start_date = parser.parse(start_date.get()).date()
    end_date = parser.parse(end_date.get()).date() if end_date.get() != "" else start_date
    if selected_contractor.get() == 'All':
        # List of all active employees
        # data for all tickets by date that our contractors have
        utils.full_payroll(start_date, end_date)
    else:
        contractor_id, first_name, last_name = selected_contractor.get().split()
        # filter by ticket and contractor
        tickets_for_contractor = utils.tickets_contractors_on(first_name, last_name)
        # filter by date -- can be merged later
        tickets_for_contractor = utils.filter_tickets_by_date(tickets_for_contractor, start_date, end_date)
        # write to file
        utils.to_file(contractor_name=selected_contractor.get(),
                      contractor_tickets=tickets_for_contractor,
                      start_date = start_date,
                      end_date = end_date)



def run_report_gui():
    master_window = tk.Tk()

    # Create and Place Labels
    tk.Label(master_window, text='').grid(row=0)
    tk.Label(master_window, text='Select contractor Name').grid(row=1)
    tk.Label(master_window, text='').grid(row=2)
    ## Add functionality for start and end date
    tk.Label(master_window, text='Enter start date (YYYY-MM-DD): ').grid(row=3)
    tk.Label(master_window, text='Enter end date (YYYY-MM-DD): ').grid(row=3, column=4)

    ## Create entry Window

    # Employees drop down
    def contractor_show():
        tk.label.config(text=clicked.get())
    contractor_options = utils.get_contractors()
    # Create All option for drop down
    contractor_options.insert(0, 'All')
    selected_contractor = tk.StringVar()
    selected_contractor.set('Select contractor')
    contractor_name = tk.OptionMenu(master_window, selected_contractor, *contractor_options)
    contractor_name.grid(row=1, column=2)

    # Start and End dates
    start_date = tk.Entry(master_window, width=25)
    end_date = tk.Entry(master_window, width=25)

    start_date.grid(row=3, column=2)
    end_date.grid(row=3, column=5)

    # Buttons for submission
    tk.Button(master_window, text='Close',
              command=master_window.quit).grid(row=4, column=0, sticky='W', pady=4)
    tk.Button(master_window, text='Submit',
              command = lambda: scrap_split_logic(selected_contractor,
                                                  start_date,
                                                  end_date)).grid(row=4, column=3, pady=4)

    master_window.mainloop()


def main():
    run_report_gui()

if __name__ == "__main__":
    main()







