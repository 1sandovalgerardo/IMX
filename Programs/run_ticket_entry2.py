#!/usr/bin/env python

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from collections import defaultdict
import pandas as pd
from csv import writer
import IMX_Utilities.tickets as tu
import IMX_Utils as utils


# TODO: what if no net or gross weight is provided on the ticket
#       I need to account for no value being entered into gross and tare

# TODO: add strip to contractor name input.  Ensures removal of white space

# TODO: BUG : when entering ticket information, to file does not take into account
#   if no hours worked is enterd.

# TODO: add method that allows na for tare and gross weights.  If NA entered, then
#   default value is 0 but skips the weight check.

def enter_ticket_logic(*args):
    for arg in args:
        print(arg.get())
    return None

def perform_checks(*args):
    ticket_number = args[0].get()
    gross_weight = float(args[1].get())
    tare_weight = float(args[2].get())
    net_weight = float(args[3].get())
    if tu.duplicate_ticket(ticket_number):
        message = 'This is a duplicate ticket.'
        messagebox.showwarning(title='DUPLICATE TICKET',
                               message=message)
    if 0 not in [gross_weight, tare_weight]:
        if net_weight != (gross_weight - tare_weight):
            print('weights are wrong')
            message2 = 'The weights are wrong'
            messagebox.showwarning(title='WRONG WEIGHTS',
                                   message=message2)
    return None


    # external_ticket, weights,
    #### I am rebuilding the ticket entry method.
    #### Purpose is to organize the code.
    #### Next I need to: create check_weight, checkduped ticket,
    #   check/create internal id, and other i have not thought of.

def ticket_entry_window():
    master_window = tk.Tk()
    master_window.title('IMX Ticket Entry')

    tk.Label(master_window, text='Ticket Number\n').grid(row=0)
    tk.Label(master_window, text='Company Name\n').grid(row=1)
    tk.Label(master_window, text='Job Site\n').grid(row=2)
    tk.Label(master_window, text='Date \n(yyyy-mm-dd)').grid(row=3)
    tk.Label(master_window, text='Week Cut').grid(row=3, column=2)
    tk.Label(master_window, text='Employees \n(separate with comma)').grid(row=4)
    tk.Label(master_window, text='Gross Weight\n').grid(row=5)
    tk.Label(master_window, text='Tare Weight\n').grid(row=6)
    tk.Label(master_window, text='Net Weight\n').grid(row=7)
    tk.Label(master_window, text='Hours Worked \n(if hourly project)').grid(row=8)
    tk.Label(master_window, text='Material Type\n').grid(row=9)
    tk.Label(master_window, text='Rate (Material or Hourly)\n').grid(row=10)

    # Creates companies dropdown menu
    def company_show():
        tk.label.config(text=clicked.get())
    company_options = utils.get_companies()
    selected_company = tk.StringVar()
    selected_company.set('Select Company')

    # Combobox for job sites
    # two list with a company name, job site correctly indexed
    company_names, job_sites = utils.get_paired_company_jobsite()
    def callback(eventObject):
        abc = eventObject.widget.get()
        # Gets the company that was choosen in the options menu
        company_selected = selected_company.get()
        index = company_names.index(company_selected)
        company_jobsite.config(values=job_sites[index])

    # Dropdown for material types
    metal_options = ['1_foot_heavy_torching', '2_foot', '2_foot_rail_road_crops',
                     '3_foot', '3_foot_heavy_torch', '3_foot_nitro',
                     '3_foot_rail_crops', '4_foot_cable', '4_foot_gt',
                     '4_foot_heavy_torch', '4_foot_rail_crops', '5_foo_and_less',
                     '5_foot', '5_foot_heavy_torching', '5_foot_manganese',
                     '5_foot_ship_plate', '5_foot_x_2_foot', 'cast', 'coil_torching',
                     'electric_motor', 'equiptment_plate', 'ferrous_skulls', 'heavy_melt',
                     'mill_rolls', 'rail_car', 'rail_car', 'railroad_railcar', 'rebar_wire_cable',
                     'rod_coils', 'wheel_axel',
                     'hourly', 'overtime']
    selected_metal = tk.StringVar()
    selected_metal.set('Select Material / Product')

    # Entry windows and options menus

    ticket_number     =  tk.Entry(master_window, width=37)
    company_name      =  tk.OptionMenu(master_window, selected_company, *company_options)
    company_jobsite   =  ttk.Combobox(master_window, width=37)
    date              =  tk.Entry(master_window, width=37)
    attribute_date    =  ttk.Entry(width=25)
    employees         =  tk.Entry(master_window, width=37)
    gross_weight      =  tk.Entry(master_window, width=37)
    tare_weight       =  tk.Entry(master_window, width=37)
    net_weight        =  tk.Entry(master_window, width=37)
    hours_worked      =  tk.Entry(master_window, width=37)
    material_type     =  tk.OptionMenu(master_window, selected_metal, *metal_options)
    rate              =  tk.Entry(master_window, width=37)

    ticket_number.grid( row=0,  column=1)
    company_name.grid(  row=1,  column=1, sticky='w')
    company_jobsite.grid(row=2, column=1)
    date.grid(          row=3,  column=1)
    attribute_date.grid(row=3,  column=3)
    employees.grid(     row=4,  column=1)
    gross_weight.grid(  row=5,  column=1)
    tare_weight.grid(   row=6,  column=1)
    net_weight.grid(    row=7,  column=1)
    hours_worked.grid(  row=8,  column=1)
    material_type.grid( row=9,  column=1, sticky='w')
    rate.grid(          row=10, column=1)

    # bind combobox with callback
    # button 1 refers to left click of mouse
    # 2nd arg is the function that is triggered.
    company_jobsite.bind('<Button-1>', callback)

    close_button = tk.Button(master_window,
              text='Close',
              command=master_window.quit)
    run_checks_button = tk.Button(master_window,
              text='Run Checks',
              command=lambda: perform_checks(ticket_number,
                                            gross_weight,
                                            tare_weight,
                                            net_weight))
    run_logic_button = tk.Button(master_window,
              text='Enter Data',
              command=lambda: enter_ticket_logic(ticket_number,
                                                 selected_company,
                                                 company_jobsite,
                                                 date,
                                                 attribute_date,
                                                 employees,
                                                 tare_weight,
                                                 gross_weight,
                                                 net_weight,
                                                 selected_metal,
                                                 rate))
    close_button.grid(row=11, column=0, sticky='W', pady=4)
    run_checks_button.grid(row=11, column=1, sticky='W', pady=4)
    run_logic_button.grid(row=11, column=2, sticky='W', pady=4)

    master_window.mainloop()




def main():
    ticket_entry_window()

if __name__=='__main__':
    main()