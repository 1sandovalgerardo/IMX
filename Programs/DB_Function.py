#!/usr/bin/env python

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from collections import defaultdict
import pandas as pd
from csv import writer
from IPython import embed # embed()
import Objects as db

def get_values(*args):
    """Gets values from ticket entry GUI"""
    fields = ['ticket_number', 'company_name', 'job_site', 'date', 'employees',
              'tare_weight', 'gross_weight', 'net_weight',
              'material_type', 'rate']
    data_entered = defaultdict()
    for variable, value in zip(fields, args):
        print(f'The item: {variable}.    The Value: {value.get()}')
        data_entered[variable] = value.get()
    print('values entered to dictionary')
    data_entered['internal_id'] = next_ticket_id()
    perform_checks(data_entered)
    save_ticket_data(data_entered)

def save_ticket_data(ticket_data):
    data_to_save = clean_ticket_data(ticket_data)
    with open('../Data/Raw/Tickets.csv', 'a') as ticket_file:
        writer_object = writer(ticket_file)
        writer_object.writerow(data_to_save)

#### Functions for ticket entry ####

def next_ticket_id():
    latest_internal_id = list(pd.read_csv('../Data/Raw/Tickets.csv')['internal_id'])[-1]
    new_internal_id = int(latest_internal_id) + 1
    print(latest_internal_id)
    print(new_internal_id)
    return (new_internal_id)

def clean_ticket_data(ticket_data):
    order_of_keys = ['ticket_number', 'internal_id', 'company_name', 'job_site',
                     'date', 'employees', 'num_of_employees', 'tare_weight',
                     'gross_weight', 'net_weight', 'material_type', 'rate']
    clean_list = []
    for key in order_of_keys:
        if key == 'ticket_number':
            clean_list.append(ticket_data['ticket_number'])
        elif key == 'num_of_employees':
            employees = ticket_data['employees'].split(',')
            clean_list.append(len(employees))
        else:
            clean_list.append(ticket_data[key])
    #print(clean_list)
    return clean_list


def get_companies():
    data = pd.read_csv('../Data/Raw/Companies.csv')
    list_of_companies = list(data['company_name'])
    #print(list_of_companies)
    return list_of_companies

def get_jobsite_details():
    data = pd.read_csv('../Data/Raw/Jobsite.csv')
    jobsite_data = data
    list_jobsite_ids = jobsite_data.loc[jobsite_data['company_name']==company_name]
    list_jobsite_ids = list_jobsite_ids[['company_name', 'jobsite_name', 'jobsite_id']]
    jobsite_names_ids = list_jobsite_ids[['jobsite_name', 'jobsite_id']]
    return data

def get_paired_company_jobsite():
    local_data = pd.read_csv('../Data/Raw/Jobsite.csv')
    companies = local_data['company_name'].unique()
    jobsites = []
    for value in companies:
        jobsites_at_company = local_data.loc[local_data['company_name']==value]['jobsite_name']
        jobsites.append(jobsites_at_company.to_list())
    return (companies.tolist(), jobsites)

#### Safety Checks ####
def perform_checks(data_dict):
    print('in perform_checks')
    check_weights(data_dict)
    check_internal_id(data_dict)

def check_internal_id(data_dict):
    internal_id = data_dict['internal_id']
    # internal_id = 100003
    all_internal_ids = list(pd.read_csv('../Data/Raw/Tickets.csv')['internal_id'])
    # print(internal_id)
    # print(all_internal_ids)
    if internal_id in all_internal_ids:
        # These next two lines prevent a background window from appearing
        #window = tk.Tk(how to set up a databse for small business)
        #window.wm_withdraw()
        message = 'You are creating a duplicate internal id'
        messagebox.showwarning(title='Internal ID',
                               message=message)

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
    message = 'Weights reported incorrectly.'
    messagebox.showwarning(title='Weight are wrong',
                           message=message)
    #warning_window.mainloop()

def create_ticket():
    master_window = tk.Tk()
    tk.Label(master_window, text='Ticket Number').grid(row=0)
    tk.Label(master_window, text='Company Name').grid(row=1)
    tk.Label(master_window, text='Job Site').grid(row=2)
    tk.Label(master_window, text='Date (yyyy-mm-dd)').grid(row=3)
    tk.Label(master_window, text='Employees (separate with comma)').grid(row=4)
    tk.Label(master_window, text='Tare Weight').grid(row=5)
    tk.Label(master_window, text='Gross Weight').grid(row=6)
    tk.Label(master_window, text='Net Weight').grid(row=7)
    tk.Label(master_window, text='Material Type').grid(row=8)
    tk.Label(master_window, text='Rate').grid(row=9)

    # create companies dropdown menu
    def company_show():
        tk.label.config(text=clicked.get())
    company_options = get_companies()
    selected_company = tk.StringVar()
    selected_company.set('Select Company')

    # combobox for jobsites
    company_names, jobsites = get_paired_company_jobsite()
    def callback(eventObject):
        abc = eventObject.widget.get()
        # for OptionMenu version
        company_selected = selected_company.get()
        index = company_names.index(company_selected)
        company_jobsite.config(values=jobsites[index])

    # dropdown for material types
    metal_options = ['rebar', 'upsteel', 'wire', 'hourly']
    selected_metal = tk.StringVar()
    selected_metal.set('Select Metal')

    ticket_number = tk.Entry(master_window, width=37)
    company_name = tk.OptionMenu(master_window, selected_company, *company_options)
    company_jobsite = ttk.Combobox(master_window, width=37)
    date = tk.Entry(master_window, width=37)
    employees = tk.Entry(master_window, width=37)
    tare_weight = tk.Entry(master_window, width=37)
    gross_weight = tk.Entry(master_window, width=37)
    net_weight = tk.Entry(master_window, width=37)
    material_type = tk.OptionMenu(master_window, selected_metal, *metal_options)
    rate = tk.Entry(master_window, width=37)

    ticket_number.grid(row=0, column=1)
    company_name.grid( row=1, column=1, sticky='w')
    company_jobsite.grid(row=2, column=1)
    date.grid(         row=3, column=1)
    employees.grid(    row=4, column=1)
    tare_weight.grid(  row=5, column=1)
    gross_weight.grid( row=6, column=1)
    net_weight.grid(   row=7, column=1)
    material_type.grid(row=8, column=1, sticky='w')
    rate.grid(         row=9, column=1)

    company_jobsite.bind('<Button-1>', callback)

    tk.Button(master_window,
              text='Quit',
              command=master_window.quit).grid(row=10, column=0, sticky=tk.W, pady=4)
    tk.Button(master_window,
              text='Enter Data',
              command=lambda: get_values(ticket_number,
                                         selected_company,
                                         company_jobsite,
                                         #job_site,
                                         date,
                                         employees,
                                         tare_weight,
                                         gross_weight,
                                         net_weight,
                                         selected_metal,
                                         rate)).grid(row=10, column=1, sticky=tk.W, pady=4)

    master_window.mainloop()


def main():
    create_ticket()
    #next_ticket_id()
    #check_internal_id()


if __name__=='__main__':
    main()





