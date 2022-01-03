import tkinter as tk
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
    for site_name, site_id in jobsite_values.values:
        dropdown_values.append(f'{site_name} {site_id}')
    return dropdown_values

def company_window():
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

    # job site code
    list_jobsites = get_jobsites()

    tk.Button(master_window, text='Enter Data',
              command=lambda:get_company(selected_company)).grid(row=2, column=1, sticky=tk.W,
                                                             pady=4)
    master_window.mainloop()

def master_window():
    master_window = tk.Tk()
    tk.Label(master_window, text = 'Company Name').grid(row=0)

    company_options = db.get_companies()
    selected_company = tk.StringVar()
    selected_company.set('Select Company')
    company_name = tk.OptionMenu(master_window, selected_company, *company_options)
    company_name.grid(row=1, column=1)

    tk.Button(master_window, text='Enter Data',
              command=lambda:get_company(selected_company)).grid(row=2, column=1, sticky=tk.W,
                                                                 pady=4)
    master_window.mainloop()

def main():
    jobsite_for_dropdown('Scrap Inc')

if __name__=='__main__':
    main()