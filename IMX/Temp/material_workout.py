#!/usr/bin/env python

import pandas as pd
import os
#import sys
from collections import defaultdict
from tkinter import messagebox


ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT_DIR, 'Data')
RAW_DIR = os.path.join(DATA_DIR, 'Raw')


JOBSITE_DATA_PATH = os.path.join(RAW_DIR, 'Jobsite.csv')
jobsite_data = pd.read_csv(JOBSITE_DATA_PATH)

def jobsite_data():
    return pd.read_csv(JOBSITE_DATA_PATH, index_col=False)

def get_jobsite_rates(jobsite):
    """Will return the materials that are cut at a specific jobsite and
    the rate that IMX is charging for them.
    Args:
        jobsite(str): the jobsite that you want the data for
    Returns:
        list(tuples): a list of tuple pairs in the following form (material, rate)
    """
    site_data = jobsite_data()
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

def main():
    data = get_jobsite_rates('JBI')
    print(data)
    data = get_jobsite_rates('Detroit Yard')

    print(data)

if __name__=='__main__':
    main()

