#!/usr/bin/env python
import traceback

import numpy as np
import pandas as pd
import os
import logging
from datetime import date
import traceback
from IPython import embed


from . import data
from . import utilities


ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT_DIR, 'Data')
REPORT_TO_PROCESS = os.path.join(DATA_DIR, 'Reports_To_Process')

def jobsite_production(jobsite, start_date, end_date, to_file=False):
    """
    Returns a data frame that contains key columns for determine the production at a jobsite
    across a number of days.
    :param jobsite: str
    :param start_date: str
    :param end_date: str
    :param to_file: bool
    :return: pandas dataframe containing date, material type, net weight, hours worked, rate,
    man hours, per hours production
    """
    logging.debug('in jobsite.jobsite_production')
    total_man_hours = jobsite_man_hours(jobsite, start_date, end_date, return_dates=True)
    hours = total_man_hours.values
    dates = total_man_hours.index
    total_man_hours = pd.DataFrame({'date': dates, 'man_hours': hours})
    total_tons_cut = tons_cut(jobsite, start_date, end_date, return_dates=True)
    total_tons_cut = total_tons_cut.reset_index()
    # We use outer join since the dates on the tickets may not be the actual date that
    # material was cut. Outer join thus allows all hours worked from the date range to be
    # included
    final_df = total_tons_cut.merge(total_man_hours, how='outer', left_index=True, right_index=True)
    final_df['per_hour_production'] = round(final_df.net_weight / final_df.man_hours, 3)
    # saves output to directory Reports_To_Process
    if to_file:
        file_name = f'Production_{jobsite}_{start_date}_{end_date}.csv'
        #full_path = f'../Data/Reports_To_Process/{file_name}'
        full_path = os.path.join(DATA_DIR, 'Reports_To_Process', file_name)
        final_df.to_csv(full_path, index=False)
    return final_df


def jobsite_hours_worked(jobsite, start_date, end_date, **kwargs):
    logging.debug('in jobsite.jobsite_hours_worked')
    hours_data = data.hours_worked_data()
    list_of_dates = utilities.dates_list(start_date, end_date)
    site_data = hours_data[hours_data['jobsite'] == jobsite]
    if list_of_dates==start_date:
        list_of_dates = [str(list_of_dates)]
    #if list
    by_date = site_data[site_data['date'].isin(list_of_dates)]
    #embed()
    grouped_data = by_date.groupby(['date', 'contractor_id',
                                    'first_name', 'last_name']).sum()
    if 'to_file' in kwargs.keys():
        print('in to file')
        print(grouped_data)
        file_name = f'HoursWorked_{jobsite}_{start_date}_{end_date}.csv'
        #file_path = f'../Data/Reports_To_Process/{file_name}'
        file_path = os.path.join(DATA_DIR, 'Reports_To_Process', file_name)
        # I do not use index=False here because the index contains the date, id, and names
        # this is due to the group by
        grouped_data.to_csv(file_path, sep=',')
    grouped_data = grouped_data[['hours_worked']]
    return grouped_data



def jobsite_man_hours(jobsite, start_date, end_date, **kwargs):
    # list of contractors at site
    logging.debug('in jobsite.jobsite_man_hours')
    contractors_ids = contractors_at_site(jobsite, start_date, end_date)
    if 'return_dates' in kwargs.keys():
        list_of_dates = utilities.dates_list(start_date, end_date)
        # load csv file
        weekly_hours_data = data.hours_worked_data()
        # Filter by jobsite
        job_site_hours = weekly_hours_data[weekly_hours_data['jobsite'] == jobsite]
        # Filter by contractors
        daily_hours = job_site_hours[job_site_hours['contractor_id'].isin(contractors_ids)]
        # Filter by passed dates
        # If single date entered use ==, else use .isin()
        if list_of_dates == start_date:
            daily_hours = daily_hours[daily_hours['date'] == str(list_of_dates)]
        else:
            daily_hours = daily_hours[daily_hours['date'].isin(list_of_dates)]
        grouped_daily_hours = daily_hours.groupby('date').sum()['hours_worked']
        # returns the total hours at a jobsite worked by
        # all contractors on a specific date
        return grouped_daily_hours
    else:
        total_hours = []
        for id in contractors_ids:
            hours_worked = contractor_weekly_hours(id, jobsite, start_date, end_date)
            total_hours.append(hours_worked)
        total_hours = np.array(total_hours)
        return total_hours.sum()


def contractors_at_site(jobsite, start_date, end_date, **kwargs):
    """Takes in a jobsite, start date, end date.  Returns a list of
    contractor ids for those contractors that worked at the jobsite on specified dates.

    The kwargs, should be used to change what is returned.

    Args:
        jobsite(str): name of jobsite
        start_date(str): first date
        end_date(str): inclusive end date
        return_contractor(keyword): will be used to return contractor info with hours

    Returns:
        contractor_ids(set): contractor ids found at the jobsite over the dates
    """
    logging.debug('in jobsite.contractors_at_site')
    # uses Hours_Worked.csv
    site_data = data.hours_worked_data()
    # fileter for jobsite
    list_of_contractors = site_data.loc[site_data['jobsite'] == jobsite]
    # get list of desired dates
    list_of_dates = utilities.dates_list(start_date, end_date)
    contractor_ids = []
    # look through list of dates to filter for contractors at the jobsite on that date
    if list_of_dates == start_date:
        ids = list_of_contractors.loc[list_of_contractors['date'] == str(start_date)]
        contractor_ids = contractor_ids + list(ids['contractor_id'])
    else:
        for date in list_of_dates:
            ids = list_of_contractors.loc[list_of_contractors['date'] == str(date)]
            contractor_ids = contractor_ids + list(ids['contractor_id'])
    # return a set of ids
    return set(contractor_ids)


def contractor_weekly_hours(contractor, jobsite, start_date, end_date, **kwargs):
    """Calculates how many hours a contractor worked over the desired time period.
    Args:
        contractor(int): contractor_id to get information for
        jobsite(str): job site to get the data for
        start_date(str): initial day
        end_date(str): las day to return, inclusive
    kwargs:
        return_date(bool): if true returns pandas multi-index series that contains
            the date, job
    Returns:
        if no kwargs: returns int of total hours a contractor worked over the desired date range.
        else: returns dataframe
    """
    logging.debug('in jobsite.contractor_weekly_hours')
    dates_to_sum = utilities.dates_list(start_date, end_date)
    hours_worked = []
    # Used to return dates the hours where worked
    if 'return_dates' in kwargs.keys():
        weekly_hours_data = data.hours_worked_data()
        job_site_hours = weekly_hours_data[weekly_hours_data['jobsite'] == jobsite]
        daily_hours = job_site_hours[job_site_hours['contractor_id'] == contractor]
        daily_hours = daily_hours[daily_hours['date'].isin(dates_to_sum)]
        return_data = daily_hours[['contractor_id', 'date', 'jobsite',
                                   'first_name', 'last_name',
                                   'hours_worked']]
        return return_data
    else:
        for date in dates_to_sum:
            hours_worked.append(contractor_daily_hours(contractor, str(date), jobsite))
        hours_worked = np.array(hours_worked)
        return int(hours_worked.sum())

def contractor_daily_hours(contractor, a_date, jobsite):
    """
    Will return the number of hours a contractor worked on a specific date
        at a specific job site.
    Args:
        contractor(int): contractor id
        a_date(str): a string date in format YYYY-MM-DD
        jobsite(str): jobsite to evaluate
    """
    logging.debug('in jobsite.contractor_daily_hours')
    hours_worked_data = data.hours_worked_data()
    contractor_data = hours_worked_data.loc[(hours_worked_data['date'] == a_date) & (hours_worked_data['contractor_id'] == contractor)]
    contractor_data = contractor_data[contractor_data['jobsite'] == jobsite]
    hours_worked_on_date = int(contractor_data['hours_worked'].sum())
    return hours_worked_on_date


def tons_cut(jobsite, start_date, end_date, **kwargs):
    """Returns pandas series that contains how many tons where cut over the dates.
    Grouped by type of material"""
    logging.debug('in jobsite.tons_cut')
    t_data = data.tickets_data()
    list_of_dates = utilities.dates_list(start_date, end_date)
    site_data = t_data.loc[t_data['jobsite'] == jobsite]
    if list_of_dates == start_date:
        date_data = site_data.loc[site_data['attribute_date'] == str(list_of_dates)]
    else:
        date_data = site_data.loc[site_data['attribute_date'].isin(list_of_dates)]
    if 'return_dates' in kwargs.keys():
        total_weights = date_data.groupby(['attribute_date', 'material_type']).sum()
        return_frame = total_weights[['net_weight', 'hours_worked', 'rate']]
        return return_frame
    else:
        total_weights = date_data.groupby(['attribute_date', 'material_type']).sum()['net_weight']
        return total_weights



def generate_invoice(company, jobsite, start_date, end_date):
    logging.debug('in jobsite.generate_invoice')
    try:
        logging.debug('In generate_invoice')
        list_of_dates = utilities.dates_list(start_date, end_date)
        ticket_data = data.tickets_data()
        jobsite_data = ticket_data.loc[
            (ticket_data['company_name'] == company) &
            (ticket_data['jobsite'] == jobsite)]
        # this allows to generate an invoice for 1 specific day
        #embed()
        if start_date == end_date:
            by_date = jobsite_data.loc[jobsite_data['date']==str(start_date)]
        else:
            by_date = jobsite_data.loc[jobsite_data['date'].isin(list_of_dates)]
        invoice_df = by_date[['ticket_number', 'jobsite', 'date', 'tare_weight', 'gross_weight',
                              'net_weight', 'material_type', 'rate']]
        invoice_df['Total'] = invoice_df['rate'] * invoice_df['net_weight']
        new_col_names = ['Ticket Num', 'Job Site', 'Date', 'Tare Weight', 'Gross Weight',
                         'Net Weight', 'Material Type', 'Rate', 'Total']
        # new invoice is here as the invoice is not yet added to the table.
        # Hence, the table entry will generate the same invoice number
        new_invoice_num = data.next_invoice_num()
        file_name = f'Invoice_{new_invoice_num}_{company}_{jobsite}_{start_date}_{end_date}.csv'
        file_path = os.path.join(REPORT_TO_PROCESS, file_name)
        logging.info(f'invoice file name: {file_path}')
        invoice_df.columns = new_col_names
        # Save invoice data for IMX formatting
        invoice_df.to_csv(file_path, index=False, mode='w')
        # Save invoice data to invoice table
        logging.debug(f'invoice data: \n {invoice_df}')
        if not invoice_to_table(invoice_df, new_invoice_num, company):
            print('####')
            print('No data exists for selected jobsite.')
            print('Therefore no tickets entered for jobiste and selected dates.')
            print('####')
            return False
        return True
    except Exception as error:
        print(error)
        print(traceback.format_exc())
        return False


def invoice_to_table(invoice_data, invoice_num, company_name):
    logging.debug('in jobsite.invoice_to_table')
    logging.debug('In invoice_to_table')
    total_weight = invoice_data['Net Weight'].sum()
    total_revenue = invoice_data['Total'].sum()
    #embed()
    if invoice_data['Job Site'].unique().shape[0] == 0:
        return False
    job_site = invoice_data['Job Site'].unique()[0]
    sent_status = True
    sent_date = date.today()
    paid_status = False
    data_to_save = [invoice_num, company_name, job_site,
                    total_weight, total_revenue, sent_status, sent_date, paid_status]
    data.save_to_invoice(data_to_save)

