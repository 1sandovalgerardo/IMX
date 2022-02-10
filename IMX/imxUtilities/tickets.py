#!/usr/bin/env python

#import pandas as pd
#import os, sys
from collections import defaultdict
from . import data



def duplicate_ticket(ticket_number):
    ticket_data = data.tickets_data()
    dup_ticket = int(ticket_number) in list(ticket_data['ticket_number'])
    return dup_ticket

def get_ticket_values(*ticket_data):
    """
    Get ticket information that was passed into the gui.
    Returns a dictionary.
    """
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
    This also adds columns that are not collected through the gui.
    Returns:
        list: data to write to file
    """
    key_order = ['ticket_number', 'internal_ticket', 'selected_company', 'company_jobsite', 'date',
                 'attribute_date', 'employees',  'num_of_employees', 'gross_weight', 'tare_weight',
                 'net_weight', 'hours_worked', 'material_type', 'rate']
    data_to_write = []
    for key in key_order:
        if key == 'internal_ticket':
            data_to_write.append(data.next_ticket_id())
        elif key == 'num_of_employees':
            data_to_write.append(len(data_dict['employees'].split(',')))
        else:
            data_to_write.append(data_dict[key])
    return data_to_write





def main():
    print(duplicate_ticket('1025'))

if __name__=='__main__':
    main()