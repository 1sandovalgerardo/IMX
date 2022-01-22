#!/usr/bin/env python

import pandas as pd
import numpy as np
import os, sys
from collections import defaultdict
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import IMX_Utils as utils


def get_ticket_values(*ticket_data):
    key_order = ['ticket_number', 'selected_company', 'company_jobsite', 'date',
                 'attribute_date', 'employees', 'tare_weight', 'gross_weight',
                 'net_weight', 'selected_metal', 'rate']
    data_dict = defaultdict()
    for key, value in zip(key_order, ticket_data):
        data_dict[key] = value.get()
    return data_dict


def duplicate_ticket(ticket_number):
    ticket_data = pd.read_csv('../Data/Raw/Tickets.csv')
    ticket_exists = ticket_number in list(ticket_data['external_id'])
    return ticket_exists


def main():
    duplicate_ticket(1021)

if __name__=='__main__':
    main()


