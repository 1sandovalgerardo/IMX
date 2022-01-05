#!/usr/bin/env python
import pandas as pd
from collections import defaultdict
from csv import writer

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
    print(clean_list)
    return clean_list




data1 = {'ticket_number': '1001',
        'company_name': 'Big Inc',
        'job_site': 'Big 1',
        'date': '2022-01-02',
        'employees': 'john, sam',
        'tare_weight': '100',
        'gross_weight': '200',
        'net_weight': '100',
        'material_type': 'rebar',
        'rate': '25',
        'internal_id': 100004}
data_to_save = clean_ticket_data(data1)
with open('../Data/Raw/Tickets.csv', 'a') as ticket_file:
    writer_object = writer(ticket_file)
    writer_object.writerow(data_to_save)

data2 = {'ticket_number': '1002',
         'company_name': 'Big Inc',
         'job_site': 'Big 2',
         'date': '2022-01-02',
         'employees': 'john, sam, gerardo sandoval',
         'tare_weight': '1000',
         'gross_weight': '2000',
         'net_weight': '1000',
         'material_type': 'rebar',
         'rate': '25',
         'internal_id': 100005}
data_to_save = clean_ticket_data(data2)
with open('../Data/Raw/Tickets.csv', 'a') as ticket_file:
    writer_object = writer(ticket_file)
    writer_object.writerow(data_to_save)



