#!/usr/bin/env python

import tkinter as tk
from tkinter import messagebox
from collections import defaultdict

class Employee(object):
    def __init__(self, id, first_name, last_name, tax_id,
                 address, city, state, start_date, active):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.tax_id = tax_id
        self.address = address
        self.city = city
        self.state = state
        self.start_date = start_date
        self.active = active

class JobSite(object):
    def __init__(self, id, company_name, address, city, state,
                 active):
        self.id = id
        self.company_name = company_name
        self.address = address
        self.city = city
        self.state = state
        self.active = active

class SiteRate(JobSite):
    def __init__(self, rebar_rate=None, upsteel_rate=None, wire_rate=None, hourly_rate=None):
        self.rebar_rate = rebar_rate
        self.upsteel_rate = upsteel_rate
        self.wire_rate = wire_rate
        self.hourly_rate = hourly_rate

class Ticket(object):
    def __init__(self, id_external, id_internal, job_site,
                 date, employees, num_employees, tare_weight,
                 gross_weight, net_weight, material_type,
                 rate, rate_per_employee):
        self.id_external = id_external
        self.id_internal = id_internal
        self.job_site = job_site
        self.date = date
        self.employees = employees
        self.num_employees = num_employees
        self.tare_weight = tare_weight
        self.gross_weight = gross_weight
        self.net_weight = net_weight
        self.material_type = material_type
        self.rate = rate
        self.rate_per_employee = rate_per_employee



def main():
    print('In DB Objects')


if __name__=='__main__':
    main()





