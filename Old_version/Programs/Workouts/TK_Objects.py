#!/usr/bin/env python

import tkinter as tk
from tkinter import ttk, messagebox
import IMX_Utils as utils

def run_report_gui():
    master_window = tk.Tk()


class MainApplication(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.config(height=300, width=300, bg='white')
        self.tk.Label(self, text='Select Employee')




