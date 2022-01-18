#!/usr/bin/env python

import tkinter as tk
from tkinter import ttk
from dateutil import parser

import pandas as pd

import IMX_Utils as utils

def enter_time_logic(*args):
    company = args[0].get()
    jobsite = args[1].get()
    contractor_id, first_name, last_name = args[2].get().split()
    date_worked = parser.parse(args[3].get()).date()
    hours_worked = args[4].get()
    data = [[contractor_id, first_name, last_name, date_worked, hours_worked, company, jobsite]]
    df = pd.DataFrame(data, columns=['contractor_id', 'first_name', 'last_name', 'date',
                                     'hours_worked', 'company', 'jobsite'])
    df.to_csv('../Data/Raw/Hours_Worked.csv', sep=',', header=False, index=False, mode='a')

def run_time_entry():
    master_window = tk.Tk()

    tk.Label(master_window, text=' ').grid(row=0)
    tk.Label(master_window, text='Select Company').grid(row=1)
    tk.Label(master_window, text='Select Job Site').grid(row=2)
    tk.Label(master_window, text='Enter Date as YYYY-MM-DD').grid(row=3)
    tk.Label(master_window, text='Select Employee').grid(row=4)
    tk.Label(master_window, text='Hours Worked').grid(row=5)

    date_worked = tk.Entry(master_window, width=25)
    hours_worked = tk.Entry(master_window, width=25)


    ## Company Dropdown menu
    def company_show():
        tk.label.config(text=clicked.get())
    company_options = utils.get_companies()
    selected_company = tk.StringVar()
    selected_company.set('Selected Company')
    company_name = tk.OptionMenu(master_window, selected_company, *company_options)

    selected_jobsite = ttk.Combobox(master_window, width=25)

    ## Jobsite Combo Box
    company_names, jobsites = utils.get_paired_company_jobsite()
    def callback(eventObject):
        abc = eventObject.widget.get()
        company_selected = selected_company.get()
        index = company_names.index(company_selected)
        selected_jobsite.config(values=jobsites[index])

    ## Employees Drop Down
    def contractor_show():
        tk.label.config(text=clicked.get())
    # get list of contractors
    contractor_options = utils.get_contractors()
    selected_contractor = tk.StringVar()
    selected_contractor.set('Select Contractor')
    contractor_name = tk.OptionMenu(master_window, selected_contractor, *contractor_options)
    contractor_name.config(width=25)

    company_name.grid(row=1, column=2, sticky='w')
    selected_jobsite.grid(row=2, column=2, sticky='w')
    contractor_name.grid(row=4, column=2, sticky='w')
    date_worked.grid(row=3, column=2, sticky='w')
    hours_worked.grid(row=5, column=2, sticky='w')

    # Activates combobox for jobsite selections
    selected_jobsite.bind('<Button-1>', callback)


    ## Buttons for actions
    tk.Button(master_window, text='Close',
              command=master_window.quit).grid(row=6, column=0, sticky='W', pady=4)
    tk.Button(master_window, text='Submit',
              command = lambda: enter_time_logic(selected_company,
                                                 selected_jobsite,
                                                 selected_contractor,
                                                 date_worked,
                                                 hours_worked)).grid(row=6, column=3, pady=4)



    master_window.mainloop()


def main():
    run_time_entry()


if __name__=='__main__':
    main()