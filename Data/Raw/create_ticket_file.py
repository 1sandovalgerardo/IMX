import pandas as pd
import datetime as dt

today_date = dt.date(2021, 12, 31)

data = {'external_id': 1001,
        'internal_id': 100001,
        'job_site': 'name',
        'date': today_date,
        'employees': ['Gerardo Sandoval', 'Fred Barker'],
        'num_of_employees': 2,
        'tare_weight': 100,
        'gross_weight': 200,
        'net_weight': 100,
        'material_type': 'metal',
        'rate': 60}

df = pd.DataFrame(data)
print(df)

df.to_csv('Tickets.csv', sep=',', header=True)

