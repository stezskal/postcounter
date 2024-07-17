import pandas as pd
import pymysql  # You can use the appropriate library for your database
import os
import matplotlib.pyplot as plt
import get_attendance
from datetime import datetime
from tabulate import tabulate

force_str = input("Force new download from database(y/n)?")
if('y' in force_str):
    force_get_attendance = True
else:
    force_get_attendance = False
## Read the data from pickle file if it exists, if not run and get data from SQL.
file_path = 'attendance_data.pkl'
if not os.path.exists(file_path) or force_get_attendance:
    get_attendance.get_attendance_df_pickle(file_path)
df = pd.read_pickle('attendance_data.pkl')

print("Note must include leading zeros for the date entry below:")
start_date_str = input("Start date filter e.g. 2023-12-01:")
end_date_str = input("End date filter e.g. 2023-12-01:")
pax_str = input("PAX Name (hit return for all PAX):")


## Filter by PAX
if(pax_str==''):
    filtered_pax_df = df
else:
    filtered_pax_df = df[df['PAX']==pax_str]

posts=filtered_pax_df.shape[0]
print(f"{pax_str} returned {posts} all time.")
if(posts==0):
    raise Exception("0 posts returned")

## Filter by date
filtered_pax_date_df = filtered_pax_df[
    (filtered_pax_df['Date'] >= start_date_str) &
    (filtered_pax_df['Date'] <= end_date_str)
]
posts_date_filt = filtered_pax_date_df.shape[0]
print(f"{pax_str} returned {posts_date_filt} between {start_date_str} and {end_date_str}.")

print(tabulate(filtered_pax_date_df, headers='keys', tablefmt='psql'))
