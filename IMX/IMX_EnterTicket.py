#!/usr/bin/env python

import logging
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import imxUtilities as utils
import sys


#for item in sys.path:
#    print(item)



def perform_checks(*args, **kwargs):
    # Eventually this logic can be replaced with
    # utils.tickets.get_ticket_values()
    ticket_number = int(args[0].get()) if len(args[0].get()) > 0 else 0
    gross_weight = float(args[1].get()) if len(args[1].get()) > 0 else 0
    tare_weight = float(args[2].get()) if len(args[2].get()) > 0 else 0
    net_weight = float(args[3].get()) if len(args[3].get()) > 0 else 0
    company_name = args[4].get()
    logging.debug(f'Gross: {gross_weight}\t Tare: {tare_weight}\t Net: {net_weight}')
    # Run weight calculator
    if utils.tickets.should_run_weight_calculator(gross_weight, tare_weight, net_weight):
        missing_value = utils.tickets.weight_calculator(gross_weight, tare_weight, net_weight)
        message = f'The missing value is: {missing_value}'
        messagebox.showinfo(title='Missing Value Calculator',
                            message = message)
        return False
    # check for a duplicate ticket
    if utils.tickets.duplicate_ticket(ticket_number, company_name) and (ticket_number != 0):
        message = 'This is a duplicate ticket'
        messagebox.showwarning(title='DUPLICATE TICKET',
                               message=message)
        return False
    # Check for incorrect net weight
    # if 0, then only net weight was provided on the ticket
    if 0 not in [gross_weight, tare_weight]:
        # checks for accurate math on ticket
        if net_weight != (gross_weight - tare_weight):
            print('weights are wrong')
            message2 = 'The weights are wrong'
            messagebox.showwarning(title='WRONG WEIGHTS',
                                   message=message2)
            return False
    message = 'Checks complete. \n No issues found'
    messagebox.showinfo(title='Ticket Check',
                        message = message)
    return True


def enter_ticket(*args):
    """Primary gui logic"""
    ticket_data = utils.tickets.get_ticket_values(*args)
    data_to_write = utils.tickets.clean_ticket(ticket_data)
    if not perform_checks(args[0], args[6], args[7], args[8], args[1]):
        messagebox.showerror('Ticket Not Entered',
                             message="Data Not Entered")
        return False
    # run save_ticket_data, if it returns False, an error occurred
    if utils.data.save_ticket_data(data_to_write):
        utils.utilities.print_to_screen(data_to_write)
        messagebox.showinfo('Ticket Entered',
                            message='Ticket Entered Successfully')
    else:
        messagebox.showerror('Ticket Not Entered',
                             message='Data Not Entered')


def ticket_entry_window():
    master_window = tk.Tk()
    master_window.title('IMX Ticket Entry')

    tk.Label(master_window, text='Ticket Number').grid(row=0, sticky='se')
    tk.Label(master_window, text='Company Name').grid(row=1, sticky='se')
    tk.Label(master_window, text='Job Site').grid(row=2, sticky='se')
    tk.Label(master_window, text='Date (yyyy-mm-dd)').grid(row=3, sticky='se')
    tk.Label(master_window, text='Week Cut').grid(row=3, column=2, sticky='se')
    tk.Label(master_window, text='Contractors (separate with comma)').grid(row=4, sticky='se')
    tk.Label(master_window, text='Gross Weight').grid(row=5, sticky='se')
    tk.Label(master_window, text='Tare Weight').grid(row=6, sticky='se')
    tk.Label(master_window, text='Net Weight').grid(row=7, sticky='se')
    tk.Label(master_window, text='Hours Worked (if hourly project)').grid(row=8, sticky='se')
    tk.Label(master_window, text='Material Type').grid(row=9, sticky='se')
    tk.Label(master_window, text='Rate (Material or Hourly)').grid(row=10, sticky='se')

    # Creates companies dropdown menu
    def company_show():
        tk.label.config(text=clicked.get())
    company_options = utils.data.get_companies()
    selected_company = tk.StringVar()
    selected_company.set('Select Company')

    # Combobox for job sites
    # two list with a company name, job site correctly indexed
    company_names, job_sites = utils.data.get_paired_company_jobsite()
    def callback(eventObject):
        abc = eventObject.widget.get()
        # Gets the company that was choosen in the options menu
        company_selected = selected_company.get()
        logging.debug(f'Company Selected: {company_selected}')
        index = company_names.index(company_selected)
        logging.debug(f'List of jobsites: {job_sites[index]}')
        company_jobsite.config(values=job_sites[index])

    # for material combobox
    def callback2(eventObject):
        #abc = eventObject.widget.get()
        jobsite_selected = company_jobsite.get()
        logging.debug(f'Material Jobsite Selected: {jobsite_selected}')
        # get dictionary of materials(keys) and rates(values)
        material_rates = utils.tickets.get_jobsite_rates(jobsite_selected)
        logging.debug(f'Dictionary : {material_rates}')
        list_material_rates = utils.tickets.jobsite_rate_to_list(material_rates)
        material_type.config(values=list_material_rates)

    # Entry windows and options menus

    ticket_number     =  tk.Entry(master_window, width=20)
    company_name      =  tk.OptionMenu(master_window, selected_company, *company_options)
    company_jobsite   =  ttk.Combobox(master_window, width=20)
    date              =  tk.Entry(master_window, width=20)
    attribute_date    =  ttk.Entry(width=20)
    contractor         =  tk.Entry(master_window, width=37)
    gross_weight      =  tk.Entry(master_window, width=20)
    tare_weight       =  tk.Entry(master_window, width=20)
    net_weight        =  tk.Entry(master_window, width=20)
    hours_worked      =  tk.Entry(master_window, width=20)
    material_type     =  ttk.Combobox(master_window)
    rate              =  tk.Entry(master_window, width=20)

    ticket_number.grid( row=0,  column=1, sticky='w')
    company_name.grid(  row=1,  column=1, sticky='w')
    company_jobsite.grid(row=2, column=1, sticky='w')
    date.grid(          row=3,  column=1, sticky='w')
    attribute_date.grid(row=3,  column=3, sticky='w')
    contractor.grid(     row=4,  column=1, sticky='w')
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

    # Combobox for material type
    material_type.bind('<Button-1>', callback2)

    # BUTTONS
    close_button = tk.Button(master_window,
                             text='Close',
                             command=master_window.quit)
    run_checks_button = tk.Button(master_window,
                                  text='Run Checks',
                                  command=lambda: perform_checks(ticket_number,
                                                                 gross_weight,
                                                                 tare_weight,
                                                                 net_weight,
                                                                 selected_company))
    run_logic_button = tk.Button(master_window,
                                 text='Enter Data',
                                 command=lambda: enter_ticket(ticket_number,
                                                              selected_company,
                                                              company_jobsite,
                                                              date,
                                                              attribute_date,
                                                              contractor,
                                                              gross_weight,
                                                              tare_weight,
                                                              net_weight,
                                                              hours_worked,
                                                              #selected_metal,
                                                              material_type,
                                                              rate))
    # SET BUTTONS
    close_button.grid(row=11, column=0, pady=4)
    run_checks_button.grid(row=11, column=1, pady=4)
    run_logic_button.grid(row=11, column=2, pady=4)

    master_window.mainloop()


def main():
    #utils.utilities.create_log(True, 'IMX_EnterTicket')
    ticket_entry_window()


if __name__=='__main__':
    main()

