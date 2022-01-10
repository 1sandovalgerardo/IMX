#!/usr/bin/env python

import tkinter as tk
from tkinter import ttk, messagebox
import IMX_Utils as utils

def run_report_gui():
    master_window = tk.Tk()
    tk.Label(master_window, text='').grid(row=0)
    tk.Label(master_window, text='Select Company Name').grid(row=1)
    tk.Label(master_window, text='Select Job Site').grid(row=2)
    ## Add functionality for start and end date
    tk.Label(master_window, text='Enter start date: ').grid(row=3)
    tk.Label(master_window, text='Enter end date: ').grid(row=3, column=3)



