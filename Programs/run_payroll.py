import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from collections import defaultdict
import pandas as pd

# TODO: a function that takes in contractor id and returns the string form of
#   id first_name last_name

def hours_worked(jobsite, contractor, start_date, end_date):
    hours_worked_data = pd.read_csv('../Data/Raw/Hours_Worked.csv')
    dates_list =


