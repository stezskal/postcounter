import pandas as pd
import pymysql  # You can use the appropriate library for your database
import os
import matplotlib.pyplot as plt
import get_attendance
from datetime import datetime

force_get_attendance = True
## Read the data from pickle file if it exists, if not run and get data from SQL.
file_path = 'attendance_data.pkl'
if not os.path.exists(file_path) or force_get_attendance:
    get_attendance.get_attendance_df_pickle(file_path)
df = pd.read_pickle('attendance_data.pkl')

#date_str = input("Up to and including date e.g. 2023-12-01")

# Filter data for November and December 2023
filtered_df = df[
    (df['Date'] >= '2024-05-01') &
    (df['Date'] <= '2024-07-14')
]


counts = filtered_df['PAX'].value_counts()

counts.to_csv("post_counts.csv", index=True)
