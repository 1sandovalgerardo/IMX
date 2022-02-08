#!/usr/bin/env python
import logging
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from collections import defaultdict
import pandas as pd
from csv import writer
import IMX_Utilities.tickets as tu
import IMX_Utils as utils

# TODO: add strip to contractor name input.  Ensures removal of white space


def perform_checks(*args, **kwargs):
    '''
    Used to check values that are entered and avoid entering incorrect information or
    information that will cause errors elsewhere. If any errors are found, this will trigger
    pop-up windows with the appropriate warning.
    :return: Bool
    '''
    ticket_number = args[0].get()
    gross_weight = float(args[1].get()) if len(args[1].get())>0 else 0
    tare_weight = float(args[2].get()) if len(args[2].get())>0 else 0
    net_weight = float(args[3].get()) if len(args[3].get())>0 else 0
    logging.debug(f'Gross: {gross_weight}\t Tare: {tare_weight}\t Net: {net_weight}')
    final_check = 0
    if tu.duplicate_ticket(ticket_number):
        message = 'This is a duplicate ticket.'
        messagebox.showwarning(title='DUPLICATE TICKET',
                               message=message)
        if 'stop_entry' in kwargs.keys():
            final_check += 1
    if 0 not in [gross_weight, tare_weight]:
        if net_weight != (gross_weight - tare_weight):
            print('weights are wrong')
            message2 = 'The weights are wrong'
            messagebox.showwarning(title='WRONG WEIGHTS',
                                   message=message2)
            if 'stop_entry' in kwargs.keys():
                final_check += 1
    # Run a check to compare rate entered vs what is in the rate key.
    # This is to be used as a final check after clicking on submit data.
    if final_check != 0:
        return False
    return True

def enter_ticket(*args):
    """Primary Logic of GUI"""
    ticket_data = tu.get_ticket_values(*args)
    data_to_write = tu.clean_ticket(ticket_data)
    tu.save_ticket_data(data_to_write)
    messagebox.showinfo('Ticket Entered',
                        message='Ticket Entered Successfully')
    return None


def ticket_entry_window():
    master_window = tk.Tk()
    master_window.title('IMX Ticket Entry')

    tk.Label(master_window, text='Ticket Number').grid(row=0, sticky='se')
    tk.Label(master_window, text='Company Name').grid(row=1, sticky='se')
    tk.Label(master_window, text='Job Site').grid(row=2, sticky='se')
    tk.Label(master_window, text='Date (yyyy-mm-dd)').grid(row=3, sticky='se')
    tk.Label(master_window, text='Week Cut').grid(row=3, column=2, sticky='se')
    tk.Label(master_window, text='Employees (separate with comma)').grid(row=4, sticky='se')
    tk.Label(master_window, text='Gross Weight').grid(row=5, sticky='se')
    tk.Label(master_window, text='Tare Weight').grid(row=6, sticky='se')
    tk.Label(master_window, text='Net Weight').grid(row=7, sticky='se')
    tk.Label(master_window, text='Hours Worked (if hourly project)').grid(row=8, sticky='se')
    tk.Label(master_window, text='Material Type').grid(row=9, sticky='se')
    tk.Label(master_window, text='Rate (Material or Hourly)').grid(row=10, sticky='se')

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

    ticket_number     =  tk.Entry(master_window, width=20)
    company_name      =  tk.OptionMenu(master_window, selected_company, *company_options)
    company_jobsite   =  ttk.Combobox(master_window, width=20)
    date              =  tk.Entry(master_window, width=20)
    attribute_date    =  ttk.Entry(width=20)
    employees         =  tk.Entry(master_window, width=37)
    gross_weight      =  tk.Entry(master_window, width=20)
    tare_weight       =  tk.Entry(master_window, width=20)
    net_weight        =  tk.Entry(master_window, width=20)
    hours_worked      =  tk.Entry(master_window, width=20)
    material_type     =  tk.OptionMenu(master_window, selected_metal, *metal_options)
    rate              =  tk.Entry(master_window, width=20)

    ticket_number.grid( row=0,  column=1, sticky='w')
    company_name.grid(  row=1,  column=1, sticky='w')
    company_jobsite.grid(row=2, column=1, sticky='w')
    date.grid(          row=3,  column=1, sticky='w')
    attribute_date.grid(row=3,  column=3, sticky='w')
    employees.grid(     row=4,  column=1, sticky='w')
    gross_weight.grid(  row=5,  column=1, sticky='w')
    tare_weight.grid(   row=6,  column=1, sticky='w')
    net_weight.grid(    row=7,  column=1, sticky='w')
    hours_worked.grid(  row=8,  column=1, sticky='w')
    material_type.grid( row=9,  column=1, sticky='w')
    rate.grid(          row=10, column=1, sticky='w')

    # bind combobox with callback
    # button 1 refers to left click of mouse
    # 2nd arg is the function that is triggered.
    company_jobsite.bind('<Button-1>', callback)

    # BUTTONS
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
              command=lambda: enter_ticket(ticket_number,
                                             selected_company,
                                             company_jobsite,
                                             date,
                                             attribute_date,
                                             employees,
                                             gross_weight,
                                             tare_weight,
                                             net_weight,
                                             hours_worked,
                                             selected_metal,
                                             rate))
    # SET BUTTONS
    close_button.grid(row=11, column=0, pady=4)
    run_checks_button.grid(row=11, column=1, pady=4)
    run_logic_button.grid(row=11, column=2, pady=4)

    master_window.mainloop()




def main():
    ticket_entry_window()
    #enter_ticket(1030, 'Big Inc', 'Big 3', '2022-01-10', '2022-01-10',
    #             'Gerardo Sandoval, John Bain', '200', '100', '100', 'metal_1',
    #             '50')

if __name__=='__main__':
    main()