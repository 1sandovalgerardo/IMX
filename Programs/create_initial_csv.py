#!/usr/bin/env python

import pandas as pd


def create_company(**kwargs):
    company_id = kwargs['company_id']
    company_name = kwargs['company_name']
    address = kwargs['address']
    city = kwargs['city']
    state = kwargs['state']
    active = kwargs['active']
    company_data = [[company_id, company_name, address, city,
                     state, active]]
    col_names = ['company_id', 'company_name', 'address', 'city',
                 'state', 'active']
    company_df = pd.DataFrame(data=company_data, columns=col_names)
    print(company_df)
    company_df.to_csv('../Data/Raw/Companies.csv', sep=',', header=True,
                      index=False, mode='a')
    return None


def company_main():
    create_company(company_id=1001,
                   company_name='Scrap Inc',
                   address='123 Main St',
                   city='Chicago',
                   state='IL',
                   active=True)
    create_company(company_id=1002,
                   company_name='Big Inc',
                   address='321 Main St',
                   city='Chicago',
                   state='IL',
                   active=True)


def create_site_rate():
    rebar_rate = input('Please enter rate for rebar: ')
    upsteel_rate = input('Please enter rate for upsteel: ')
    wire_rate = input('Please enter rate for wire: ')
    hourly_rate = input('Please enter rate for hourly: ')
    site_rate_values = {'rebar_rate': rebar_rate,
                        'upsteel_rate': upsteel_rate,
                        'wire_rate': wire_rate,
                        'hourly_rate': hourly_rate}
    return site_rate_values


def create_jobsite(**kwargs):
    company_name = kwargs['company_name']
    company_id = kwargs['company_id']
    jobsite_name = kwargs['jobsite_name']
    jobsite_id = kwargs['jobsite_id']
    site_rate = create_site_rate()
    active_site = kwargs['active_site']
    job_site_data = [[company_name, company_id, jobsite_name, jobsite_id,
                     site_rate, active_site]]
    col_names = ['company_name', 'company_id', 'jobsite_name', 'jobsite_id',
                 'site_rate', 'active_site']
    company_df = pd.DataFrame(data=job_site_data, columns=col_names)
    print(company_df)
    company_df.to_csv('../Data/Raw/Jobsite.csv', sep=',', header=False,
                      index=False, mode='a')


def job_site_main():
    create_jobsite(company_name='Scrap Inc',
                   company_id=1001,
                   jobsite_name='Site1',
                   jobsite_id=101,
                   active_site=True)
    create_jobsite(company_name='Scrap Inc',
                   company_id=1001,
                   jobsite_name='Site2',
                   jobsite_id=102,
                   active_site=True)
    create_jobsite(company_name='Scrap2 Inc',
                   company_id=1002,
                   jobsite_name='Site1',
                   jobsite_id=101,
                   active_site=True)
    create_jobsite(company_name='Big Inc',
                   company_id=1003,
                   jobsite_name='Site1',
                   jobsite_id=101,
                   active_site=True)


if __name__ == "__main__":
    job_site_main()
