import tkinter as tk
import DB_Function as db

def get_company(selected_company):
    company_value = selected_company.get()
    print(company_value)

def working_window():
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
    working_window()

if __name__=='__main__':
    main()