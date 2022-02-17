#!/usr/bin/env python

import imxUtilities as utils
import pandas as pd
import os


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
    #logging.debug('in jobsite.jobsite_production')
    total_man_hours = utils.jobsite.jobsite_man_hours(jobsite, start_date, end_date, return_dates=True)
    hours = total_man_hours.values
    dates = total_man_hours.index
    total_man_hours = pd.DataFrame({'date': dates, 'man_hours': hours})
    total_tons_cut = utils.jobsite.tons_cut(jobsite, start_date, end_date, return_dates=True)
    total_tons_cut = total_tons_cut.reset_index()
    final_df = total_tons_cut.merge(total_man_hours, how='outer', left_index=True, right_index=True)
    final_df['per_hour_production'] = round(final_df.net_weight / final_df.man_hours, 3)
    # saves output to directory Reports_To_Process
    if to_file:
        file_name = f'Production_{jobsite}_{start_date}_{end_date}.csv'
        #full_path = f'../Data/Reports_To_Process/{file_name}'
        full_path = os.path.join(utils.data.DATA_DIR, 'Reports_To_Process', file_name)
        final_df.to_csv(full_path, index=False)
    return final_df

def main():
    result = jobsite_production('JBI', '2022-02-01', '2022-02-05')
    print(result)

if __name__=='__main__':
    main()
