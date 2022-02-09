#!/usr/bin/env python

import pandas as pd
import os, sys

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT_DIR, 'Data')

def tickets_data():
    tickets_path = os.path.join(DATA_DIR,'Raw', 'Tickets.csv')
    data = pd.read_csv(tickets_path, index_col=False)
    return data


def main():
    print(ROOT_DIR)
    print(DATA_DIR)
    tickets_data()


if __name__=="__main__":
    main()
