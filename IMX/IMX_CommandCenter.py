#!/usr/bin/env python

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from dateutil import parser

import imxUtilities as utils
from imxUtilities import jobsite
from imxUtilities import utilities


def payroll_logic(*args):
    jobsite = args[0].get()
    start_date = parser.parse(args[1].get()).date()
    end_date = parser.parse(args[2].get()).date()
    print(start_date, end_date)
    utils.jobsite.jobsite_production(jobsite, start_date, end_date, to_file=True)
    utils.jobsite.jobsite_hours_worked(jobsite, start_date, end_date, to_file=True)
    payroll_completed()

def payroll_completed():
    message = 'Payroll Entered'
    messagebox.showinfo(title='Payroll Entered',
                        message = message)


def invoice_logic(*args):
    company = args[0].get()
    jobsite_name = args[1].get()
    start_date = parser.parse(args[2].get()).date()
    end_date = parser.parse(args[3].get()).date()
    invoice_number = args[4].get()
    print(company, jobsite, start_date, end_date)
    invoice_result = jobsite.generate_invoice(company, jobsite_name, start_date, end_date,
                                              invoice_number)
    if not invoice_result:
        message = """Invoice generated but may not contain data.
There may not be any tickets for specified dates and jobsite."""
        messagebox.showerror(title='Invoice Status',
                             message=message)
    if invoice_result:
        messagebox.showinfo(title='Invoice Status',
                            message='Invoice Created')
    return None


def run_control_center():
    master_window = tk.Tk()
    master_window.title('IMX Command Center')

    tk.Label(master_window, text=' ').grid(row=0)
    tk.Label(master_window, text='Select Company Name').grid(row=1, column=1, sticky='E')
    tk.Label(master_window, text='Select Job Site').grid(row=2, column=1, sticky='E')
    ## Add functionality for start and end date
    tk.Label(master_window, text='Enter start date: ').grid(row=3, column=1, sticky='E')
    tk.Label(master_window, text='Enter end date: ').grid(row=3, column=3)
    tk.Label(master_window, text='Invoice Number:').grid(row=4, column=1)

    # Create companies dropdown menu
    ## I commented out this function. I'm not sure if it does anything.
    # def company_show():
    #    tk.label.config(text=clicked.get())
    list_of_companies = utils.data.get_companies()
    selected_company = tk.StringVar()
    selected_company.set('CLICK FOR OPTIONS')

    # combobox for jobsites
    paired_list_company_names, jobsites = utils.data.get_paired_company_jobsite()

    def callback(eventObject):
        company_selected = selected_company.get()
        # Get index for company_selected as found in company_names
        selection_index = paired_list_company_names.index(company_selected)
        # This pairs with ttk.Combobox
        company_jobsite_menu.config(values=jobsites[selection_index])

    # Create GUI visuals
    company_name_menu = tk.OptionMenu(master_window, selected_company, *list_of_companies)
    company_jobsite_menu = ttk.Combobox(master_window)
    start_date = tk.Entry(master_window, width=25)
    end_date = tk.Entry(master_window, width=25)
    invoice_number = tk.Entry(master_window, width=25)

    # Place GUI objects
    company_name_menu.grid(row=1, column=2, sticky='w')
    company_jobsite_menu.grid(row=2, column=2, sticky='w')
    start_date.grid(row=3, column=2, sticky='w')
    end_date.grid(row=3, column=4, sticky='w')
    invoice_number.grid(row=4, column=2)

    ## Buttons on window
    company_jobsite_menu.bind('<Button-1>', callback)
    tk.Button(master_window, text='Close', command=master_window.quit).grid(row=5, column=1, sticky=tk.W, pady=4)
    payroll_button = tk.Button(master_window,
                               text='Run Payroll',
                               command=lambda: payroll_logic(company_jobsite_menu,
                                                             start_date,
                                                             end_date))
    invoice_button = tk.Button(master_window, text='Run Invoice',
                               command=lambda: invoice_logic(selected_company,
                                                             company_jobsite_menu,
                                                             start_date,
                                                             end_date,
                                                             invoice_number
                                                             ))

    payroll_button.grid(row=5, column=3, pady=4)
    invoice_button.grid(row=5, column=4, pady=4)

    master_window.mainloop()


def main():
    #utilities.create_log(True, 'Command_Center')
    run_control_center()
    # utils.jobsite_hours_worked('Big 3', '2022-01-03', '2022-01-07', to_file=True)

if __name__=='__main__':
    main()
