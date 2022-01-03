import tkinter as tk
from tkinter import ttk
import DB_Function as db
import pandas as pd

def get_company(selected_company):
    company_value = selected_company.get()
    print(company_value)

def get_jobsites(company_name):
    jobsite_data = pd.read_csv('../Data/Raw/Jobsite.csv')
    list_jobsite_ids = jobsite_data.loc[jobsite_data['company_name']==company_name]
    list_jobsite_ids = list_jobsite_ids[['company_name', 'jobsite_name', 'jobsite_id']]
    return list_jobsite_ids

def jobsite_for_dropdown(company_name):
    jobsite_details = get_jobsites(company_name)
    jobsite_values = jobsite_details[['jobsite_name', 'jobsite_id']]
    dropdown_values = []
    # Merge two values into one string
    for site_name, site_id in jobsite_values.values:
        dropdown_values.append(f'{site_name} {site_id}')
    return dropdown_values

def get_paired_company_jobsite():
    data = pd.read_csv('../Data/Raw/Jobsite.csv')
    companies = data['company_name'].unique()
    jobsites = []
    for value in companies:
        jobsites_at_company = data.loc[data['company_name']==value]['jobsite_name']
        jobsites.append(jobsites_at_company.to_list())
    return (companies.tolist(), jobsites)

def master_window():
    master_window = tk.Tk()
    tk.Label(master_window, text = 'Company Name').grid(row=0)

    # get list of companies in database
    company_options = db.get_companies()
    # set type for object
    selected_company = tk.StringVar()
    # initial value of dropdown menu
    selected_company.set('Select Company')
    # creates the dropdown menu
    company_name = tk.OptionMenu(master_window, selected_company, *company_options)
    company_name.grid(row=1, column=1)
    ## alternate for combobox
    #company_name = ttk.Combobox(master_window, value=(company_options))
    #company_name.grid(row=1, column=1, columnspan=2, sticky='w')
    # Create company_names(list):
    # matching index based jobsite list
    company_names, jobsites = get_paired_company_jobsite()
    def callback(eventObject):
        abc = eventObject.widget.get()
        # for OptionMenu version
        company_selected = selected_company.get()
        ## for combobox version
        #company_selected = company_name.get()
        index = company_names.index(company_selected)
        company_jobsite.config(values=jobsites[index])
    company_jobsite = ttk.Combobox(master_window, width=37)
    company_jobsite.grid(row=2, column=1, columnspan=2, sticky='w')
    company_jobsite.bind('<Button-1>', callback)


    tk.Button(master_window, text='Enter Data',
              command=lambda:get_company(selected_company)).grid(row=2, column=1, sticky=tk.W,
                                                             pady=4)
    master_window.mainloop()


def example():
    from tkinter import ttk

    root = tk.Tk()
    ''' 
    widgets are added here 
    '''
    brands = ["Bugatti","VW","Opel","Porsche"]

    models = [["Veyron","Chiron"],
              ["Golf","Passat","Polo","Caddy"],
              ["Insignia","Corsa","Astra"],
              ["Taycan","Cayenne","911"]]

    car_brand = ttk.Combobox(root, width=37, value=(brands))
    car_brand.grid(row=3, column=1, columnspan=2, padx=10, pady=2, sticky='w')

    def callback(eventObject):
        abc = eventObject.widget.get()
        car = car_brand.get()
        index=brands.index(car)
        car_model.config(values=models[index])

    car_model = ttk.Combobox(root, width=37)
    car_model.grid(row=4, column=1, columnspan=2, padx=10, pady=2, sticky='w')
    car_model.bind('<Button-1>', callback)

    root.mainloop()

def main():
    master_window()

if __name__=='__main__':
    main()