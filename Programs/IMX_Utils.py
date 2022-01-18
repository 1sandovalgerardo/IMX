#!/usr/bin/env python

import pandas as pd
import datetime as dt
from datetime import timedelta
import logging
from dateutil import parser


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
    logging.debug('get_companies() called')
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


def get_contractors():
    """ Returns a list of companies found in Employees.csv"""
    ## I need to add logic to exclude contractors that are no longer active.
    logging.debug('get_employees() called')
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










def main():
    create_log(True)
    ## test daily revenue
    #daily_revenue = days_revenue('Scrap Inc', '2022-01-02')
    #print(daily_revenue)

    ## Test multiday_revenue
    #multiday_revenue('Total', '2022-1-1', '2022-1-5')

    ## Test get_employees
    get_employees()



if __name__=='__main__':
    main()