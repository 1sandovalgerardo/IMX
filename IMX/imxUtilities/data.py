#!/usr/bin/env python
import traceback

import numpy as np
import pandas as pd
from csv import writer
import os, sys
import logging

from IPython import embed

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT_DIR, 'Data')
TICKETS_CSV = os.path.join(DATA_DIR, 'Raw', 'Tickets.csv')
COMPANIES_CSV = os.path.join(DATA_DIR, 'Raw', 'Companies.csv')
JOBSITE_CSV = os.path.join(DATA_DIR, 'Raw', 'Jobsite.csv')
HOURS_WORKED = os.path.join(DATA_DIR, 'Raw', 'Hours_Worked.csv')
INVOICES_CSV = os.path.join(DATA_DIR, 'Raw', 'Invoices.csv')
CONTRACTORS_CSV = os.path.join(DATA_DIR, 'Raw', 'Contractors.csv')

def clean_contractors():
    c_data = pd.read_csv(CONTRACTORS_CSV)
    c_data['first_name'] = c_data['first_name'].str.strip().str.title()
    c_data['last_name'] = c_data['last_name'].str.strip().str.title()
    c_data['nickname'] = c_data['nickname'].str.strip().str.title()
    c_data['Address'] = c_data['Address'].str.split(' ')
    c_data['address'] = [x[:-3] for x in c_data['Address']]
    c_data['city'] = [x[-3] for x in c_data['Address']]
    c_data['state'] = [x[-2] for x in c_data['Address']]
    c_data['zip_code'] = c_data['Address'].str.get(-1)
    file_name = os.path.join(DATA_DIR, 'Raw', 'Contractors2.csv')
    c_data.to_csv(file_name, index=False)

def tickets_data():
    logging.debug('Tickets.csv loaded')
    tickets_path = os.path.join(DATA_DIR,'Raw', 'Tickets.csv')
    data = pd.read_csv(tickets_path, index_col=False)
    data['date'] = pd.to_datetime(data['date'], format='mixed')
    data['date'] = data.date.dt.strftime('%Y-%m-%d')
    #embed()
    data['attribute_date'] = pd.to_datetime(data['attribute_date'])
    data['attribute_date'] = data.attribute_date.dt.strftime('%Y-%m-%d')
    return data


def hours_worked_data():
    logging.debug('Hours_Worked.csv loaded')
    data = pd.read_csv(HOURS_WORKED, index_col=False)
    data['date'] = pd.to_datetime(data['date'], format='mixed')
    data['date'] = data.date.dt.strftime('%Y-%m-%d')
    data['attribute_date'] = pd.to_datetime(data['attribute_date'])
    data['attribute_date'] = data.attribute_date.dt.strftime('%Y-%m-%d')
    return data


def jobsite_data():
    logging.debug('Jobsite.csv Loaded')
    return pd.read_csv(JOBSITE_CSV, index_col=False)


def contractors_data():
    data = pd.read_csv(CONTRACTORS_CSV, index_col=False)
    return data

def invoice_data():
    data = pd.read_csv(INVOICES_CSV, index_col=False)
    return data


def get_contractors():
    """Returns a list of contractors found in Contractors.csv"""
    # TODO: add logic to exclude contractors that are not active
    logging.info('called get_countractors()')
    cont_data = contractors_data()
    cont_data['contractor_id'] = list(map(str, cont_data['contractor_id']))
    cont_data = cont_data.loc[cont_data['active']==True]
    cont_data['nickname'] = cont_data['nickname'].fillna('')
    employee_var = cont_data[['contractor_id', 'nickname', 'first_name', 'last_name']]
    id_employee_list = [' '.join(x) for x in employee_var.values]
    return id_employee_list


def get_companies():
    """ Returns a list of companies found in the Companies.csv file"""
    logging.info('get_companies() called')
    data = pd.read_csv(COMPANIES_CSV, index_col=False)
    list_of_companies = list(data['company_name'])
    logging.debug(list_of_companies)
    logging.debug('get_companies() ended')
    return list_of_companies


def get_paired_company_jobsite():
    """ Returns a tuple of two values. Each value is a list.
        The purpose of this is to have a company and jobsite list that are at the same
        index position within their respective list.
        This is for functionality of the drop down menus within the gui."""
    logging.debug('get_paired_company_jobsite() called')
    jobsite_data = pd.read_csv(JOBSITE_CSV, index_col=False)
    list_of_companies = get_companies()
    jobsites = []
    for company in list_of_companies:
        jobsites_at_company = jobsite_data.loc[jobsite_data['company_name']==company]['jobsite_name']
        jobsites.append(jobsites_at_company.to_list())
    logging.debug('get_paired_company_jobsite() ended')
    return list_of_companies, jobsites


def get_material_rate(company, jobsite):
    jobsite_data = pd.read_csv(JOBSITE_CSV, index_col=False)
    jobsite_data = jobsite_data.loc[(jobsite_data['company_name'].str.strip() == company) &
                                    (jobsite_data['jobsite_name'].str.strip()==jobsite)]
    print(jobsite_data)




def next_ticket_id():
    '''Returns the next internal id for the ticket that is being entered'''
    last_internal_id = list(pd.read_csv(TICKETS_CSV)['internal_id'])[-1]
    new_internal_id = int(last_internal_id) + 1
    return new_internal_id


def next_invoice_num():
    """Returns the next internal invoice number."""
    logging.debug('In next_invoice_num()')
    invoice_data = pd.read_csv(INVOICES_CSV)
    latest_num = int(invoice_data['invoice_num'].max())
    return latest_num + 1


def save_ticket_data(ticket_data):
    '''Write row of data to Tickets.csv'''
    try:
        with open(TICKETS_CSV, 'a', newline='') as ticket_file:
            writer_object = writer(ticket_file)
            writer_object.writerow(ticket_data)
    except Exception as e:
        print('error in save_ticket_data')
        print(e)
        return False
    return True


def save_to_invoice(data):
    logging.debug(data)
    # If this doesn't work, use 'ab' instead of 'a'
    with open(INVOICES_CSV, 'a', newline='') as invoice_file:
        writer_object = writer(invoice_file)
        writer_object.writerow(data)


def save_hours_worked(data_df):
    logging.debug('in save_hours_worked')
    try:
        data_df.to_csv(HOURS_WORKED, sep=',', header=False,
                       index=False, mode='a')
        return True
    except Exception:
        print('error in save_hours_worked')
        print(traceback.format_exc())
        return False





def main():
    #tickets_data()
    #print(next_ticket_id())
    #print(get_companies())
    #print(get_paired_company_jobsite())
    #next_invoice_num()
    #get_material_rate('Cohen Recycling', 'Vine')
    #clean_contractors()
    get_contractors()


if __name__=="__main__":
    main()
