#!/usr/bin/env python

import pandas as pd

def get_companies():
    data = pd.read_csv('../Data/Raw/Companies.csv')
    list_of_companies = list(data['company_name'])
    #print(list_of_companies)
    return list_of_companies

def get_paired_company_jobsite():
    jobsite_data = pd.read_csv('../Data/Raw/Jobsite.csv')
    list_of_companies = get_companies()
    jobsites = []
    for company in list_of_companies:
        jobsites_at_company = jobsite_data.loc[jobsite_data['company_name']==company]['jobsite_name']
        jobsites.append(jobsites_at_company.to_list())
        #print(jobsites_at_company.to_list())
    return (list_of_companies, jobsites)

def main():
    a = get_paired_company_jobsite()
    for row in a:
        print(row)

if __name__=='__main__':
    main()