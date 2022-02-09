#!/usr/bin/env python

import pandas as pd
import os, sys
import data


def duplicate_ticket(ticket_number):
    ticket_data = data.tickets_data()
    print(type(ticket_data))
    dup_ticket = int(ticket_number) in list(ticket_data['ticket_number'])
    return dup_ticket

def main():
    duplicate_ticket(None)

if __name__=='__main__':
    main()