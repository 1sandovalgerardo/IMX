#!/usr/bin/env python

import pandas as pd
from csv import writer
import os, sys
import logging

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT_DIR, 'Data')
TICKETS_CSV = os.path.join(DATA_DIR, 'Raw', 'Tickets.csv')
COMPANIES_CSV = os.path.join(DATA_DIR, 'Raw', 'Companies.csv')
JOBSITE_CSV = os.path.join(DATA_DIR, 'Raw', 'Jobsite.csv')
HOURS_WORKED = os.path.join(DATA_DIR, 'Raw', 'Hours_Worked.csv')


def tickets_data():
    tickets_path = os.path.join(DATA_DIR,'Raw', 'Tickets.csv')
    data = pd.read_csv(tickets_path, index_col=False)
    return data


def hours_worked_data():
    data = pd.read_csv(HOURS_WORKED, index_col=False)
    return data


def get_companies():
    """ Returns a list of companies found in the Companies.csv file"""
    logging.info('get_companies() called')
    data = pd.read_csv(COMPANIES_CSV, index_col=False)
    list_of_companies = list(data['company_name'])
    logging.debug(list_of_companies)
    logging.debug('get_companies() ended')
    return list_of_companies


def next_ticket_id():
    '''Returns the next internal id for the ticket that is being entered'''
    last_internal_id = list(pd.read_csv(TICKETS_CSV)['internal_id'])[-1]
    new_internal_id = int(last_internal_id) + 1
    return new_internal_id


def save_ticket_data(ticket_data):
    '''Write row of data to Tickets.csv'''
    try:
        with open(TICKETS_CSV, 'a') as ticket_file:
            writer_object = writer(ticket_file)
            writer_object.writerow(ticket_data)
    except Exception as e:
        print('error in save_ticket_data')
        print(e)
    return True



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



def main():
    print(ROOT_DIR)
    print(DATA_DIR)
    #tickets_data()
    #print(next_ticket_id())
    #print(get_companies())
    print(get_paired_company_jobsite())


if __name__=="__main__":
    main()
