#!/usr/bin/env python

import numpy as np
import pandas as pd
import os

import data
import utilities


ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT_DIR, 'Data')
print(ROOT_DIR)
print(DATA_DIR)

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
    # saves output to directory Reports_To_Process
    if to_file:
        file_name = f'Production_{jobsite}_{start_date}_{end_date}.csv'
        #full_path = f'../Data/Reports_To_Process/{file_name}'
        full_path = os.path.join(DATA_DIR, 'Reports_To_Process', file_name)
        final_df.to_csv(full_path, index=False)
    return final_df


def jobsite_man_hours(jobsite, start_date, end_date, **kwargs):
    # list of contractors at site
    contractors_ids = contractors_at_site(jobsite, start_date, end_date)
    if 'return_dates' in kwargs.keys():
        list_of_dates = utilities.dates_list(start_date, end_date)
        weekly_hours_data = data.hours_worked_data()
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
    # uses Hours_Worked.csv
    site_data = data.hours_worked_data()
    # fileter for jobsite
    list_of_contractors = site_data.loc[site_data['jobsite'] == jobsite]
    # get list of desired dates
    list_of_dates = utils.dates_list(start_date, end_date)
    contractor_ids = []
    # look through list of dates to filter for contractors at the jobsite on that date
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
    dates_to_sum = utils.dates_list(start_date, end_date)
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
    hours_worked_data = data.hours_worked_data()
    contractor_data = hours_worked_data.loc[(hours_worked_data['date'] == a_date) & (hours_worked_data['contractor_id'] == contractor)]
    contractor_data = contractor_data[contractor_data['jobsite'] == jobsite]
    hours_worked_on_date = int(contractor_data['hours_worked'].sum())
    return hours_worked_on_date


def tons_cut(jobsite, start_date, end_date, **kwargs):
    """Returns pandas series that contains how many tons where cut over the dates.
    Grouped by type of material"""
    t_data = data.tickets_data()
    list_of_dates = utilities.dates_list(start_date, end_date)
    site_data = t_data.loc[t_data['jobsite'] == jobsite]
    date_data = site_data.loc[site_data['attribute_date'].isin(list_of_dates)]
    if 'return_dates' in kwargs.keys():
        total_weights = date_data.groupby(['attribute_date', 'material_type']).sum()
        return_frame = total_weights[['net_weight', 'hours_worked', 'rate']]
        return return_frame
    else:
        total_weights = date_data.groupby(['attribute_date', 'material_type']).sum()['net_weight']
        return total_weights

