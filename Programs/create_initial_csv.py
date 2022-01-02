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
    company_df = pd.DataFrame(data = company_data, columns=col_names)
    print(company_df)
    company_df.to_csv('../Data/Raw/Companies.csv', sep=',', header=True,
                      index=False, mode='a')
    return None

def main():
    create_company(company_id=1001,
                   company_name='Scrap Inc',
                   address='123 Main St',
                   city = 'Chicago',
                   state = 'IL',
                   active = True)
    create_company(company_id=1002,
                   company_name='Big Inc',
                   address='321 Main St',
                   city = 'Chicago',
                   state = 'IL',
                   active = True)

if __name__ == "__main__":
    main()
