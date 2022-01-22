#!/usr/bin/env python

import pandas as pd
import numpy as np
import datetime as dt
from datetime import timedelta
import logging
from dateutil import parser

# TODO: a function that takes in contractor id and returns the string form of
#   id first_name last_name

def create_log(debug):
    if debug:
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(levelname)s: %(name)s: %(message)s')

        file_handler = logging.FileHandler('log_imx.log', 'w')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        shell_handler = logging.StreamHandler()
        shell_handler.setLevel(logging.WARNING)
        logger.addHandler(shell_handler)
        logging.debug('logging established')
    else:
        pass


def get_companies():
    """ Returns a list of companies found in the Companies.csv file"""
    logging.info('get_companies() called')
    data = pd.read_csv('../Data/Raw/Companies.csv')
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
    jobsite_data = pd.read_csv('../Data/Raw/Jobsite.csv')
    list_of_companies = get_companies()
    jobsites = []
    for company in list_of_companies:
        jobsites_at_company = jobsite_data.loc[jobsite_data['company_name']==company]['jobsite_name']
        jobsites.append(jobsites_at_company.to_list())
        #print(jobsites_at_company.to_list())
    logging.debug('get_paired_company_jobsite() ended')
    return (list_of_companies, jobsites)



def ticket_revenue(ticket_number):
    ''' Returns the revenue generated by a specific ticket.'''
    logging.debug('ticket_revenue() called')
    ticket_number = int(ticket_number)
    ticket_data = pd.read_csv('../Data/Raw/Tickets.csv')
    # filter data for specific ticket number
    ticket_data = ticket_data.loc[ticket_data['external_id']==ticket_number]
    type_of_material = str(ticket_data['material_type'])
    material_weight = float(ticket_data['net_weight'])
    rate = float(ticket_data['rate'])
    if material_weight == 0:
        hourly_rate = float(ticket_data['hours_worked'])
        revenue = round(rate * hourly_rate, 3)
    else:
        revenue = round(material_weight * rate, 3)
    logging.debug('ticket_revenue() ended')
    return revenue

def days_tickets(company, desired_date):
    '''returns a list of tickets for a specific company and day
    args:
        company(string): company should be listed in companies.csv
        desired_date(string): make sure to pass in a string and not date object'''
    logging.debug('days_tickets() called')
    data = pd.read_csv('../Data/Raw/Tickets.csv')
    # Make date column datetime objects
    data['date'] = pd.to_datetime(data['date'],yearfirst=True, format='%Y-%m-%d').dt.date
    if isinstance(desired_date, str):
        print('in if for days_tickets')
        desired_date = list(map(int, desired_date.split(sep='-')))
        desired_date = dt.date(desired_date[0], desired_date[1], desired_date[2])
    return_data = data.loc[(data['date'] == desired_date) & (data['company_name']==company)]
    list_of_tickets = list(return_data['external_id'])
    logging.debug('days_tickets() ended')
    return list_of_tickets


def dates_list(start_date, end_date):
    if start_date == end_date:
        return start_date
    if not isinstance(start_date, dt.date) or not isinstance(end_date, dt.date):
        start_date = parser.parse(start_date).date()
        end_date = parser.parse(end_date).date()
    number_of_days = int((end_date - start_date).days)
    list_of_dates = []
    for n in range(number_of_days+1):
        date_to_add = start_date + timedelta(days=n)
        list_of_dates.append(date_to_add)
    list_of_dates = [str(date) for date in list_of_dates]
    return list_of_dates

# TODO: I am working on the logic for dates_list.  Then I will continue building the function
#   for run_payroll.py

#### Functions for run_daily ####


def multiday_revenue(company, start_date, end_date):
    """Returns the total revenue generated at a company over specified day.
    Will include revenue for end date."""
    # make start and end dates date objects
    start_date =  parser.parse(start_date)
    end_date = parser.parse(end_date)
    # determine date range
    number_of_days = start_date - end_date
    number_of_days = abs(int(number_of_days.days))
    # generate the list of desired dates
    list_of_dates = [(start_date+timedelta(days=n)).date() for n in range(number_of_days + 1)]
    revenue_for_time_period = 0
    for date in list_of_dates:
        logging.debug(f'Revenue for: {date}')
        logging.debug(days_revenue(company, date))
        revenue_for_time_period += days_revenue(company, date)
    print(revenue_for_time_period)
    return revenue_for_time_period


def days_revenue(company, a_date):
    logging.debug('days_revenue() called')
    tickets_for_date = days_tickets(company, a_date)
    total_revenue = 0
    logging.debug('Tickets for desired date:')
    logging.debug(tickets_for_date)
    for ticket in tickets_for_date:
        revenue = ticket_revenue(ticket)
        #print(revenue)
        logging.debug(f'Ticket #: {ticket}')
        total_revenue += ticket_revenue(ticket)
    logging.debug('days_revenue() ended')
    return total_revenue


#### Functions for run_scrapsplit ####

# TODO: need to add a filter to exclude contractors that are not active
def get_contractors():
    """ Returns a list of companies found in Employees.csv"""
    ## I need to add logic to exclude contractors that are no longer active.
    logging.debug('get_contractors() called')
    data = pd.read_csv('../Data/Raw/Employees.csv')
    data['employee_id'] = list(map(str, data['employee_id']))
    employee_var = data[['employee_id', 'first_name', 'last_name']]
    id_employee_list = [' '.join(x) for x in employee_var.values]
    return id_employee_list


def to_file(**kwargs):
    start_date = str(kwargs['start_date'])
    end_date = str(kwargs['end_date'])
    contractor_name = kwargs['contractor_name'].split()
    file_name = f'{start_date}_{end_date}_{"_".join(contractor_name)}.csv'
    # the if to be able to use the function for other items
    if kwargs['contractor_tickets']:
        columns = ['external_id', 'date', 'contractor_name','material_type',
                   'qty', 'num_of_employees', 'qty_to_contractor' ]
        file_to_save = pd.DataFrame(kwargs['contractor_tickets'], columns=columns)
        file_name = f'../Data/Reports_To_Process/{file_name}'
        file_to_save.to_csv(file_name, sep=',', index=False)


def filter_tickets_by_date(contractor_tickets, start_date, end_date):
    select_tickets = []
    if start_date == end_date:
        for ticket in contractor_tickets:
            if str(start_date) == ticket[1]:
                select_tickets.append(ticket)
    else:
        number_of_days = start_date - end_date
        number_of_days = abs(int(number_of_days.days))
        # list of desired dates, inclusive
        desired_dates = [(start_date + timedelta(days=n)) for n in range(number_of_days + 1)]
        for date in desired_dates:
            for ticket in contractor_tickets:
                if str(date) == ticket[1]:
                    select_tickets.append(ticket)
    return select_tickets


def tickets_contractors_on(first_name, last_name):
    """Takes contractor first_name and las_name.
    Returns a list of tickets that the contractor is on."""
    data = pd.read_csv('../Data/Raw/Tickets.csv')
    first_name = first_name.title()
    last_name = last_name.title()
    contractors_tickets = []
    for index, row in data.iterrows():
        ticket_id = row['external_id']
        contractors_on_ticket = row['employees'].split(',')
        for name in contractors_on_ticket:
            if first_name.lower() in name.lower() and last_name.lower() in name.lower():
                weight_to_contractor = round(float(row['net_weight']) / float(row['num_of_employees']), 3)
                if row['material_type'] == 'hourly':
                    hours_to_contractor = round(float(row['hours_worked'])/float(row['num_of_employees']), 3)
                    contractors_tickets.append([ticket_id,
                                                row['date'],
                                                f'{first_name} {last_name}',
                                                row['material_type'],
                                                row['hours_worked'],
                                                row['num_of_employees'],
                                                hours_to_contractor])
                else:
                    contractors_tickets.append([ticket_id,
                                                row['date'],
                                                f'{first_name} {last_name}',
                                                row['material_type'],
                                                row['net_weight'],
                                                row['num_of_employees'],
                                                weight_to_contractor])
    return contractors_tickets

def full_payroll(start_date, end_date):
    contractor_list = get_contractors()
    ticket_data = pd.read_csv('../Data/Raw/Tickets.csv', delimiter=',')
    number_of_days = start_date - end_date
    number_of_days = abs(int(number_of_days.days))
    # list of desired dates, inclusive
    desired_dates = [(start_date + timedelta(days=n)) for n in range(number_of_days + 1)]
    select_tickets = []
    for date in desired_dates:
        test_rows = ticket_data[ticket_data['date'] == str(date)]
        print(f'Desired Date: {date}')
        print(test_rows)

def create_ticket_employee_table():
    '''Used to establish Ticket_Contractor_Table.csv'''
    data = pd.read_csv('../Data/Raw/Tickets.csv')
    table_rows = []
    for rows in data.values:
        ticket_num = rows[0]
        internal_id = rows[1]
        all_contractors = rows[5].split(',')
        for contractor in all_contractors:
            contractor = contractor.strip().split(' ')
            if len(contractor) == 2:
                first_name, last_name = contractor
                middle_name = ''
            else:
                first_name, middle_name, last_name = contractor
            table_rows.append([ticket_num, internal_id, first_name, middle_name, last_name]) 
    table_columns = ['external_id', 'internal_id', 'first_name','middle_name', 'last_name']
    df_to_write = pd.DataFrame(table_rows, columns=table_columns)
    df_to_write.to_csv('../Data/Raw/Ticket_Contractor_Table.csv', index=False, sep=',')


#### Functions for entering hours contractor worked ####
def enter_hrs_worked(**kwargs):
    contractor_id = kwargs['contractor_id']
    contractor_first_name = kwargs['contractor_first_name']
    contractor_last_name = kwargs['contractor_last_name']
    date_worked = kwargs['date']


#### functions for run_payroll() ####

def contractor_daily_hours(contractor, a_date, jobsite):
    """
    Will return the number of hours a contractor worked on a specific date
        at a specific job site.
    Args:
        contractor(int): contractor id
        a_date(str): a string date in format YYYY-MM-DD
        jobsite(str): jobsite to evaluate
    """
    hours_worked_data = pd.read_csv('../Data/Raw/Hours_Worked.csv')
    contractor_data = hours_worked_data.loc[(hours_worked_data['date'] == a_date) & (hours_worked_data['contractor_id'] == contractor)]
    contractor_data = contractor_data[contractor_data['jobsite'] == jobsite]
    hours_worked_on_date = int(contractor_data['hours_worked'].sum())
    return hours_worked_on_date


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
    dates_to_sum = dates_list(start_date, end_date)
    hours_worked = []
    # Used to return dates the hours where worked
    if 'return_dates' in kwargs.keys():
        weekly_hours_data = pd.read_csv('../Data/Raw/Hours_Worked.csv')
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
    site_data = pd.read_csv('../Data/Raw/Hours_Worked.csv')
    # fileter for jobsite
    list_of_contractors = site_data.loc[site_data['jobsite']==jobsite]
    # get list of desired dates
    list_of_dates = dates_list(start_date, end_date)
    contractor_ids = []
    # look through list of dates to filter for contractors at the jobsite on that date
    for date in list_of_dates:
        ids = list_of_contractors.loc[list_of_contractors['date'] == str(date)]
        contractor_ids = contractor_ids + list(ids['contractor_id'])
    # return a set of ids
    return set(contractor_ids)

def jobsite_hours_worked(jobsite, start_date, end_date, **kwargs):
    hours_data = pd.read_csv('../Data/Raw/Hours_Worked.csv')
    list_of_dates = dates_list(start_date, end_date)
    site_data = hours_data[hours_data['jobsite']==jobsite]
    by_date = site_data[site_data['date'].isin(list_of_dates)]
    grouped_data = by_date.groupby(['date', 'contractor_id',
                                    'first_name', 'last_name']).sum()
    if 'to_file' in kwargs.keys():
        print('in to file')
        print(grouped_data)
        file_name = f'HoursWorked_{jobsite}_{start_date}_{end_date}.csv'
        file_path = f'../Data/Reports_To_Process/{file_name}'
        # I do not use index=False here because the index contains the date, id, and names
        grouped_data.to_csv(file_path, sep=',')
    grouped_data = grouped_data[['hours_worked']]
    return grouped_data


def jobsite_man_hours(jobsite, start_date, end_date, **kwargs):
    # list of contractors at site
    contractors_ids = contractors_at_site(jobsite, start_date, end_date)
    if 'return_dates' in kwargs.keys():
        list_of_dates = dates_list(start_date, end_date)
        weekly_hours_data = pd.read_csv('../Data/Raw/Hours_Worked.csv')
        job_site_hours = weekly_hours_data[weekly_hours_data['jobsite'] == jobsite]
        daily_hours = job_site_hours[job_site_hours['contractor_id'].isin(contractors_ids)]
        daily_hours = daily_hours[daily_hours['date'].isin(list_of_dates)]
        grouped_daily_hours = daily_hours.groupby('date').sum()['hours_worked']
        return grouped_daily_hours
    else:
        total_hours = []
        for id in contractors_ids:
            hours_worked = contractor_weekly_hours(id, jobsite, start_date, end_date)
            total_hours.append(hours_worked)
        total_hours = np.array(total_hours)
        return total_hours.sum()

    # hours the contractor worked at the site
    # sum of all hours

def tons_cut(jobsite, start_date, end_date, **kwargs):
    """Returns pandas series that contains how many tons where cut over the dates.
    Grouped by type of material"""
    data = pd.read_csv('../Data/Raw/Tickets.csv')
    list_of_dates = dates_list(start_date, end_date)
    site_data = data.loc[data['jobsite'] == jobsite]
    date_data = site_data.loc[site_data['date'].isin(list_of_dates)]
    if 'return_dates' in kwargs.keys():
        total_weights = date_data.groupby(['date', 'material_type']).sum()
        return_frame = total_weights[['net_weight', 'hours_worked', 'rate']]
        return return_frame
    else:
        total_weights = date_data.groupby(['date', 'material_type']).sum()['net_weight']
        return total_weights


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
    total_man_hours = jobsite_man_hours(jobsite, start_date, end_date, return_dates=True)
    hours = total_man_hours.values
    dates = total_man_hours.index
    total_man_hours = pd.DataFrame({'date': dates, 'man_hours':hours})
    total_tons_cut = tons_cut(jobsite, start_date, end_date, return_dates=True)
    total_tons_cut = total_tons_cut.reset_index()
    final_df = total_tons_cut.merge(total_man_hours)
    final_df['per_hour_production'] = round(final_df.net_weight / final_df.man_hours, 3)
    if to_file:
        file_name = f'Production_{jobsite}_{start_date}_{end_date}.csv'
        full_path = f'../Data/Reports_To_Process/{file_name}'
        final_df.to_csv(full_path, index=False)
    return final_df


#### Invoice Functions ####
def generate_invoice(company, jobsite, start_date, end_date):
    try:
        list_of_date = dates_list(start_date, end_date)
        ticket_data = pd.read_csv('../Data/Raw/Tickets.csv')
        jobsite_data = ticket_data.loc[(ticket_data['company_name'] == company) & (ticket_data['jobsite']==jobsite)]
        by_date = jobsite_data.loc[jobsite_data['date'].isin(list_of_date)]
        invoice_df = by_date[['external_id', 'jobsite', 'date', 'tare_weight', 'gross_weight',
                              'net_weight', 'material_type', 'rate']]
        invoice_df['Total'] = invoice_df['rate'] * invoice_df['net_weight']
        new_col_names = ['Ticket Num', 'Job Site', 'Date', 'Tare Weight', 'Gross Weight',
                         'Net Weight', 'Material Type', 'Rate', 'Total']
        file_name = f'Invoice_{company}_{jobsite}_{start_date}_{end_date}.csv'
        file_path = f'../Data/Reports_To_Process/{file_name}'
        invoice_df.columns = new_col_names
        invoice_df.to_csv(file_path, index=False)
        return True
    except Exception as error:
        print(error)
        return False


def mark_ticket_billed():
    # Create a method of marking that a ticket was billed
    pass

def ticket_paid():
    # anotate that an invoice was paid
    pass


def main():
    create_log(True)
    ## test daily revenue
    #daily_revenue = days_revenue('Scrap Inc', '2022-01-02')
    #print(daily_revenue)

    ## Test multiday_revenue
    #multiday_revenue('Total', '2022-1-1', '2022-1-5')

    ## Test get_contractors
    get_contractors()

    ## Test dates_list()
    dates_list('1', '4')



if __name__=='__main__':
    main()