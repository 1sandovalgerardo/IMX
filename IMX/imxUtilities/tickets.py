#!/usr/bin/env python
import logging

import pandas as pd
#import os, sys
from collections import defaultdict
from dateutil import parser
from tkinter import messagebox

from IPython import embed
from . import data

# TODO: what to do if ticket numbers start to include letters.


def duplicate_ticket(ticket_number, company):
    """Returns True if duplicate ticket. Returns False if not."""
    ticket_data = data.tickets_data()
    dup_ticket = int(ticket_number) in list(ticket_data['ticket_number'])
    if not dup_ticket:
        return False
    else:
        ticket_df = ticket_data[ticket_data['ticket_number'] == int(ticket_number)]
        if company in list(ticket_df['company_name']):
            return True
        else:
            return False

def get_ticket_values(*ticket_data):
    """
    Get ticket information that was passed into the gui.
    Returns a dictionary.
    """
    logging.debug('in tickets.get_ticket_values()')
    key_order = ['ticket_number', 'selected_company', 'company_jobsite', 'date',
                 'attribute_date', 'contractors',  'gross_weight', 'tare_weight',
                 'net_weight', 'hours_worked', 'material_type', 'rate']
    data_dict = defaultdict()
    for key, value in zip(key_order, ticket_data):
        # Checks for entered value, if nothing is entered then its length is zero
        if len(value.get()) == 0:
            data_dict[key] = 0
        else:
            data_dict[key] = value.get()
    data_dict['date'] = parser.parse(data_dict['date']).date()
    if data_dict['attribute_date']==0:
        data_dict['attribute_date'] = data_dict['date']
    # check for unkown contractor/s
    if data_dict['contractors'] == 0:
        data_dict['contractors'] = 'unknown'
    return data_dict

def clean_ticket(data_dict):
    """
    Takes in dictionary from get_ticket_values and returns a list that is to be written
    to Tickets.csv. List will be in correct order.
    This also adds columns that are not collected through the gui.
    Returns:
        list: data to write to file
    """
    logging.debug('in tickets.clean_ticket')
    key_order = ['ticket_number', 'internal_ticket', 'selected_company', 'company_jobsite', 'date',
                 'attribute_date', 'contractors',  'num_of_contractors', 'gross_weight', 'tare_weight',
                 'net_weight', 'hours_worked', 'material_type', 'rate']
    data_to_write = []
    #embed()
    for key in key_order:
        if key == 'internal_ticket':
            data_to_write.append(data.next_ticket_id())
        elif key == 'num_of_contractors':
            # what to do if single name is entered?
            try:
                data_to_write.append(len(data_dict['contractors'].split(',')))
            except Exception as e:
                data_to_write.append(1)
        else:
            data_to_write.append(data_dict[key])
        #embed()
    material_type, rate = data_to_write[-2].split(':')
    data_to_write[-2] = material_type
    if data_to_write[-1] == 0:
        data_to_write[-1] = rate
    if data_to_write[0] == 0:
        data_to_write[0] = data_to_write[1]
    logging.info('Data that will be saved:')
    logging.info(data_to_write)
    return data_to_write


def get_jobsite_rates(jobsite):
    """Will return the materials that are cut at a specific jobsite and
    the rate that IMX is charging for them.
    Args:
        jobsite(str): the jobsite that you want the data for
    Returns:
        list(tuples): a list of tuple pairs in the following form (material, rate)
    """
    logging.debug('in tickets.get_jobsite_rates')
    site_data = data.jobsite_data()
    site_data = site_data[site_data['jobsite_name']==jobsite]
    #print(f'Site Data: {site_data}')
    if site_data.shape[0] != 1:
        messagebox.showerror(title='Duplicate Job Sites',
                             message='There are duplicate jobsites in Jobsite.csv')
        site_data = site_data.iloc[0]
    void_columns = ['company_name', 'company_id', 'jobsite_name', 'jobsite_id', 'active_site',
                    'Address', 'City', 'State']
    material_rates = defaultdict()
    for col in site_data.columns:
        if (col not in void_columns) and (not pd.isna(site_data[col].iloc[0])):
            material_rates[col] = site_data[col].iloc[0]
    return material_rates


def jobsite_rate_to_list(jobsite_rates_dict):
    '''Expects to receive output from get_jobsite_rates.
    Will return a list of values to use in the combobox dropdown'''
    logging.debug('in tickets.jobsite_rate_to_list')
    output_list = []
    for key, value in jobsite_rates_dict.items():
        output_list.append(': '.join((key, str(value))))
    return output_list

def should_run_weight_calculator(gross, tare, net):
    if len(set([gross, tare, net])) == 3 and (0 in [gross, tare, net]):
        return True
    return False

def weight_calculator(gross, tare, net):
    """Excpects weights to be passed in. Checks for number of missing values.
    If 1 value missing, provides what the difference is."""
    gross = int(gross)
    tare = int(tare)
    net = int(net)
    if gross == 0:
        return  tare + net
    if tare == 0:
        return gross - net
    if net == 0:
        return gross - tare




def main():
    print(duplicate_ticket('1025'))

if __name__=='__main__':
    main()