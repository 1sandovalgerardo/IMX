import logging
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from collections import defaultdict
import pandas as pd
from csv import writer
import imxUtilities as util


def perform_checks(*args, **kwargs):
    ticket_number = args[0].get()
    gross_weight = float(args[1].get()) if len(args[1].get()) > 0 else 0
    tare_weight = float(args[2].get()) if len(args[2].get()) > 0 else 0
    net_weight = float(args[3].get()) if len(args[3].get()) > 0 else 0
    logging.debug(f'Gross: {gross_weight}\t Tare: {tare_weight}\t Net: {net_weight}')

    if util.duplicate_ticket(ticket_number):
        message = 'This is a duplicate ticket'
        messagebox.showwarning(title='DUPLICATE TICKET',
                               message=message)
    # if 0, then only net weight was provided on the ticket
    if 0 not in [gross_weight, tare_weight]:
        # checks for accurate math on ticket
        if net_weight != (gross_weight - tare_weight):
            print('weights are wrong')
            message2 = 'The weights are wrong'
            messagebox.showwarning(title='WRONG WEIGHTS',
                                   message=message2)
    return True

