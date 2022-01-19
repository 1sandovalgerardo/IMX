import pandas as pd
from collections import defaultdict

file = '2022-01-01_2022-01-03_1001_Gerardo_Sandoval.csv'
data = pd.read_csv(file)
ideal = defaultdict(list)
for key, value in data.iterrows():
ideal = pd.DataFrame(ideal)
print(ideal)