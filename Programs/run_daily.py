#!/usr/bin/env python

import tkinter as tk
from tkinter import ttk
import IMX_Utils as utils

def run_report_gui():
    master_window = tk.Tk()
    tk.Label(master_window, text='Select Company Name').grid(row=1)
    tk.Label(master_window, text='Select Job Site').grid(row=2)

    # Create companies dropdown menu
    def company_show():
        tk.label.config(text=clicked.get())
    list_of_companies = utils.get_companies()
    selected_company = tk.StringVar()
    selected_company.set('CLICK FOR OPTIONS')

    # combobox for jobsites
    company_names, jobsites = get_paired_company_jobsite()



