#!/usr/bin/env python

import tkinter as tk

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


def get_values(*args):
    fields = ['id_external', 'id_internal','job_site','date',
              'employees','num_of_employees','tare_weight','gross_weight',
              'net_weight','material_type','rate']
    print(args)
    for variable, value in zip(fields, args):
        print(f'The varialbe is: {variable}. The value is: {value.get()}')

def create_ticket():
    master_window = tk.Tk()
    tk.Label(master_window, text='Ticket Number').grid(row=0)
    tk.Label(master_window, text='Job Site').grid(row=1)
    tk.Label(master_window, text='Date (yyyy-mm-dd)').grid(row=2)
    tk.Label(master_window, text='Employees (separate with comma)').grid(row=3)
    tk.Label(master_window, text='Tare Weight').grid(row=4)
    tk.Label(master_window, text='Gross Weight').grid(row=5)
    tk.Label(master_window, text='Net Weight').grid(row=6)
    tk.Label(master_window, text='Material Type').grid(row=7)
    tk.Label(master_window, text='Rate').grid(row=8)

    ticket_number = tk.Entry(master_window).grid(row=0, column=1)
    job_site = tk.Entry(master_window).grid(row=1, column=1)
    date = tk.Entry(master_window).grid(row=2, column=1)
    employees = tk.Entry(master_window).grid(row=3, column=1)
    tare_weight = tk.Entry(master_window).grid(row=4, column=1)
    gross_weight = tk.Entry(master_window).grid(row=5, column=1)
    net_weight = tk.Entry(master_window).grid(row=6, column=1)
    material_type = tk.Entry(master_window).grid(row=7, column=1)
    rate = tk.Entry(master_window).grid(row=8, column=1)


    tk.Button(master_window,
              text='Quit',
              command=master_window.quit).grid(row=9, column=0, sticky=tk.W, pady=4)
    tk.Button(master_window,
              text='Enter Data',
              command=lambda:get_values(ticket_number,
                                        job_site,
                                        date,
                                        employees,
                                        tare_weight,
                                        gross_weight,
                                        net_weight,
                                        material_type,
                                        rate)).grid(row=9, column=1, sticky=tk.W, pady=4)

    master_window.mainloop()


def main():
    create_ticket()


if __name__=='__main__':
    main()





