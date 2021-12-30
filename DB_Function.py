#!/usr/bin/env python

import tkinter as tk
from tkinter import messagebox
from collections import defaultdict
import DB_Objects as db

def get_values(*args):
    fields = ['ticket_number', 'job_site', 'date', 'employees',
              'tare_weight', 'gross_weight', 'net_weight',
              'material_type', 'rate']
    data_entered = defaultdict()
    for variable, value in zip(fields, args):
        print(f'The item: {variable}.    The Value: {value.get()}')
        data_entered[variable] = value.get()
    print('values entered to dictionary')
    perform_checks(data_entered)

def perform_checks(data_dict):
    print('in perform_checks')
    check_weights(data_dict)

def check_weights(data_dict):
    tare_weight = data_dict['tare_weight']
    gross_weight = data_dict['gross_weight']
    print(f'Gross Weight: {gross_weight}, Tare Weight: {tare_weight}')
    actual_material_weight = float(gross_weight) - float(tare_weight)
    report_net_weight = float(data_dict['net_weight'])
    if actual_material_weight != report_net_weight:
        weight_warning_box()

def weight_warning_box():
    print('in weight_warning_box')
    #warning_window = tk.Tk()
    message = 'Weights reported incorrectly.'
    messagebox.showwarning(title='Weight are wrong',
                           message=message)
    #warning_window.mainloop()


def create_ticket():
    master_window = tk.Tk()
    tk.Label(master_window, text='Ticket Number').grid(row=0)
    tk.Label(master_window, text='Job Site').grid(row=1)
    tk.Label(master_window, text='Date (yyyy-mm-dd)').grid(row=2)
    tk.Label(master_window, text='Employees (separate with comma)').grid(row=3)
    tk.Label(master_window, text='Tare Weight').grid(row=4)
    tk.Label(master_window, text='Gross Weight').grid(row=5)
    tk.Label(master_window, text='Net Weight').grid(row=6)
    tk.Label(master_window, text='Material Type').grid(row=7)
    tk.Label(master_window, text='Rate').grid(row=8)

    ticket_number = tk.Entry(master_window)
    job_site = tk.Entry(master_window)
    date = tk.Entry(master_window)
    employees = tk.Entry(master_window)
    tare_weight = tk.Entry(master_window)
    gross_weight = tk.Entry(master_window)
    net_weight = tk.Entry(master_window)
    material_type = tk.Entry(master_window)
    rate = tk.Entry(master_window)

    ticket_number.grid(row=0, column=1)
    job_site.grid(     row=1, column=1)
    date.grid(         row=2, column=1)
    employees.grid(    row=3, column=1)
    tare_weight.grid(  row=4, column=1)
    gross_weight.grid( row=5, column=1)
    net_weight.grid(   row=6, column=1)
    material_type.grid(row=7, column=1)
    rate.grid(         row=8, column=1)


    tk.Button(master_window,
              text='Quit',
              command=master_window.quit).grid(row=9, column=0, sticky=tk.W, pady=4)
    tk.Button(master_window,
              text='Enter Data',
              command=lambda: get_values(ticket_number,
                                         job_site,
                                         date,
                                         employees,
                                         tare_weight,
                                         gross_weight,
                                         net_weight,
                                         material_type,
                                         rate)).grid(row=9, column=1, sticky=tk.W, pady=4)

    master_window.mainloop()


def main():
    create_ticket()


if __name__=='__main__':
    main()





