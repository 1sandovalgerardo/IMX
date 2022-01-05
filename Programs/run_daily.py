#!/usr/bin/env python

import tkinter as tk
from tkinter import ttk
import IMX_Utils as utils

def run_report_gui():
    master_window = tk.Tk()

    tk.Label(master_window, text=' ').grid(row=0)
    tk.Label(master_window, text='Select Company Name').grid(row=1)
    tk.Label(master_window, text='Select Job Site').grid(row=2)

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

    # Place GUI objects
    company_name_menu.grid(row=1, column=2)
    company_jobsite_menu.grid(row=2, column=2)

    company_jobsite_menu.bind('<Button-1>', callback)

    ## I need to add the buttons to triger window logic

    master_window.mainloop()

def main():
    run_report_gui()

if __name__=='__main__':
    main()









