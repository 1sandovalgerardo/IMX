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

class Company(object):
    def __init__(self, company_id, company_name, address, city, state,
                 active):
        self.company_id = company_id
        self.company_name = company_name
        self.address = address
        self.city = city
        self.state = state
        self.active = active

class JobSite(Company):
    def __init__(self, company_name, company_id, jobsite_name, jobsite_id,
                 active_site, **kwargs):
        Company.__init__(self, company_name, company_id)
        self.jobsite_name = jobsite_name
        self.jobsite_id = jobsite_id
        self.site_rate = SiteRate(**kwargs)
        self.active_site = active_site

    def add_metal_rate(self):
        pass

class SiteRate(object):
    def __init__(self, **kwargs):
        self.rebar_rate = kwargs['rebar']
        self.upsteel_rate = kwargs['upsteel']
        self.wire_rate = kwargs['wire']
        self.hourly_rate = kwargs['hourly']

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





