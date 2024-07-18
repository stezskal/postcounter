import pandas as pd
import pymysql  # You can use the appropriate library for your database
import os
import matplotlib.pyplot as plt
import get_attendance
from datetime import datetime
from tabulate import tabulate
from datetime import datetime, timedelta


from teams_input import Teams


#force_str = input("Force new download from database(y/n)?")
force_str='n'
if('y' in force_str):
    force_get_attendance = True
else:
    force_get_attendance = False
## Read the data from pickle file if it exists, if not run and get data from SQL.
file_path = 'attendance_data.pkl'
if not os.path.exists(file_path) or force_get_attendance:
    get_attendance.get_attendance_df_pickle(file_path)
df = pd.read_pickle('attendance_data.pkl')


teams = Teams()

print("Note must include leading zeros for the date entry below:")
#start_date_str = input("Start date filter e.g. 2023-12-01:")
#end_date_str = input("End date filter e.g. 2023-12-01:")
#pax_str = input("PAX Name (hit return for all PAX):")

#date=start_date_str
date='2024-07-17'

#while(end_date_str!=date):
day_df = df[(df['Date'] == date)]

## inplace changes the index of day_df and drop restarts index at 0 instead of the index from db which is like 37000
#day_df.reset_index(inplace=True, drop=True)
#
#day_df.sort_values(by='Team', inplace=True)
print(tabulate(day_df))

noteam_list = []

## add teams column to dataframe from today and sort by team
teams.drop_downrange(day_df)
teams.add_pax_homes_to_posts_df(day_df)
teams.add_teams_to_posts_df(day_df)
teams.add_ao_home_to_posts_df(day_df)

#teams.evaluate_posts(day_df)
#teams.check_q(day_df)

print(tabulate(day_df))

for index, row in day_df.iterrows():
    pax = row['PAX']
    q = row['Q']
    ao = row['AO']
    if(pax==q):
        q_today=True
        q_str="+Q Point!"
    else:
        q_today=True
        q_str=""

    team = row['Team']
    if team=="NoTeam":
        noteam_list.append(pax)

        
        print(f"{date}  Team {team}  {pax} scored post at {ao}! {q_str}")


print(f"NoTeam PAX: {noteam_list}")
print(f"Done")




def increment_date_string(date_string):
    # Parse the date string into a datetime object
    date_object = datetime.strptime(date_string, "%Y-%m-%d")
    # Increment the date by 1 day
    new_date_object = date_object + timedelta(days=1)
    # Convert the datetime object back to a string
    new_date_string = new_date_object.strftime("%Y-%m-%d")
    return new_date_string