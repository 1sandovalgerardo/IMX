#!/usr/bin/env python

import pandas as pd
import numpy as np
import os, sys
from collections import defaultdict
from csv import writer
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import IMX_Utils as utils


def get_ticket_values(*ticket_data):
    key_order = ['ticket_number', 'selected_company', 'company_jobsite', 'date',
                 'attribute_date', 'employees',  'gross_weight', 'tare_weight',
                 'net_weight', 'hours_worked', 'material_type', 'rate']
    data_dict = defaultdict()
    for key, value in zip(key_order, ticket_data):
        if len(value.get()) == 0:
            data_dict[key] = 0
        else:
            data_dict[key] = value.get()
    if data_dict['attribute_date']==0:
        data_dict['attribute_date'] = data_dict['date']
    return data_dict

def clean_ticket(data_dict):
    """
    Takes in dictionary from get_ticket_values and returns a list that is to be written
    to Tickets.csv. List will be in correct order.
    """
    key_order = ['ticket_number', 'internal_ticket', 'selected_company', 'company_jobsite', 'date',
                 'attribute_date', 'employees',  'num_of_employees', 'gross_weight', 'tare_weight',
                 'net_weight', 'hours_worked', 'material_type', 'rate']
    data_to_write = []
    for key in key_order:
        if key == 'internal_ticket':
            data_to_write.append(next_ticket_id())
        elif key == 'num_of_employees':
            data_to_write.append(len(data_dict['employees'].split(',')))
        else:
            data_to_write.append(data_dict[key])
    return data_to_write


def next_ticket_id():
    latest_internal_id = list(pd.read_csv('../Data/Raw/Tickets.csv')['internal_id'])[-1]
    new_internal_id = int(latest_internal_id) + 1
    return new_internal_id


def duplicate_ticket(ticket_number):
    ticket_data = pd.read_csv('../Data/Raw/Tickets.csv')
    ticket_exists = int(ticket_number) in list(ticket_data['external_id'])
    return ticket_exists


def save_ticket_data(ticket_data):
    print(ticket_data)
    with open('../Data/Raw/Tickets.csv', 'a') as ticket_file:
        writer_object = writer(ticket_file)
        writer_object.writerow(ticket_data)
    return None

def main():
    duplicate_ticket(1021)

if __name__=='__main__':
    main()


