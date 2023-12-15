import pandas as pd
import pymysql  # You can use the appropriate library for your database
import os
import matplotlib.pyplot as plt
import get_attendance
from datetime import datetime



# Define teams and corresponding PAX
teams = {
    'Team 1': ['Scrum', 'Gazelle', 'Redick', 'EscapeRoom', 'Great Clips', 'Frank N\' Beans', 'Lulu'],
    'Team 2': ['Safety’s off', 'Captain Kirk', 'Spork', 'Big Spoon', 'Luigi', 'Majkowski', 'Lost Signal'],
    'Team 3': ['Smores', 'Gypsy', 'Connors', 'Ricky-Bobby', 'Pryor', 'Spirit', 'Guppy'],
    'Team 4': ['Soybean', 'Tuna', 'Saganaki', 'White Belt', 'Lake Forest', 'PomPom', 'Caddyshack'],
    'Team 5': ['Fanny-Pack', 'LaX', 'Speedo', 'Swoosh', 'Backseat', 'FEMA', 'Business Casual'],
    'Team 6': ['D3', 'Mule', 'Wally', 'Zebulon', 'Autopilot', 'Frosted Tips', 'McDowells'],
}
# Create a mapping between team names and the desired values for the new column
team_nicknames = {
    'Team 1': 'Team SCRUMptious(Scrum)',
    'Team 2': 'Who does #2 work for? (Safetys Off)',
    'Team 3': 'Team Threesomes (Smores)',
    'Team 4': 'Drew Barryfour (Soybean)',
    'Team 5': 'Great RESPECTations (Fanny-pack)',
    'Team 6': 'Sixitime (D3)',
    # Add other teams and corresponding values as needed
}

team_bonus = {
    'Team 1': 0,
    'Team 2': 1,
    'Team 3': 2,
    'Team 4': 0,
    'Team 5': 1,
    'Team 6': 0,
}

force_get_attendance = True
## Read the data from pickle file if it exists, if not run and get data from SQL.
file_path = 'attendance_data.pkl'
if not os.path.exists(file_path) or force_get_attendance:
    get_attendance.get_attendance_df_pickle(file_path)
df = pd.read_pickle('attendance_data.pkl')

date_str = input("Up to and including date e.g. 2023-12-01")

# Filter data for November and December 2023
filtered_df = df[
    (df['Date'] >= '2023-11-01') &
    (df['Date'] <= date_str)
]
# Filter data for November and December 2023
#df['Date'] = pd.to_datetime(df['Date'])
#filtered_df_old = df[df['Date'].dt.to_period('M').isin(['2023-11', '2023-12'])]
#filtered_df = df[(df['Date'].dt.year == 2023) & ((df['Date'].dt.month == 11) | (df['Date'].dt.month == 12))]


# Create a new column for Team based on PAX
for team, pax_list in teams.items():
    filtered_df.loc[filtered_df['PAX'].isin(pax_list), 'Team'] = team


# Results table for PAX with posts
result_pax = filtered_df.groupby(['Team', 'PAX']).size().reset_index(name='TotalPosts')

# Results table for each Team's counts
result_team = result_pax.groupby('Team')['TotalPosts'].sum().reset_index()

# Order the DataFrames in descending order of 'TotalPosts'
result_pax = result_pax.sort_values(by='TotalPosts', ascending=False)
result_team = result_team.sort_values(by='TotalPosts', ascending=False)


# Add a new column based on the team names
result_team['Name'] = result_team['Team'].map(team_nicknames)

# Add a new columns  on the team number
result_team['Bonus Points'] = result_team['Team'].map(team_bonus)
result_team['Total Points'] = result_team['TotalPosts'] + result_team['Bonus Points']

desired_order = ['Team', 'Name', 'TotalPosts', 'Bonus Points', 'Total Points']
result_team = result_team[desired_order]

# Display the results
print("Results table for PAX with posts:")
print(result_pax)



# Convert the DataFrame to an HTML table
html_table = result_team.to_html(index=False)

with open('team_results.html', 'w') as f:
    f.write(html_table)

html_pax_table = result_pax.to_html(index=False)
with open('team_pax.html', 'w') as f:
    f.write(html_pax_table)

date_object = datetime.strptime(date_str, "%Y-%m-%d")
# Get the day of the week (Monday is 0 and Sunday is 6)
day_of_week = date_object.weekday()
day_name = date_object.strftime("%A")

date_str_full = day_name+" "+date_str


latest_day_df = filtered_df[(filtered_df['Date']==date_str)]
print(f"\n\n======  #tag-team-challenge posts for {date_str_full} ======\n")
print(result_team)
for team in teams:
    team_pax = latest_day_df[(latest_day_df['Team']==team)]['PAX'].tolist()
    cnt = len(team_pax)
    if(cnt>0):
        paxstr='@'+' @'.join(team_pax)
    else:
        paxstr=''
    print(f"{team} --  +{cnt} posted:  {paxstr}")

    mo_list=[]
    for pax in teams[team]:
        if pax not in team_pax:
            mo_list.append(pax)

    cnt = len(mo_list)
    if(cnt>0):
        paxstr='@'+' @'.join(mo_list)
    else:
        paxstr=''
    print(f"(MO:  {paxstr})")
    #print(f"\n")


## experiment with auto-detecting bonus point for all posting

#for team_name in teams.keys():
#    # Specify the team you're interested in
#    #team_name = 'Team 3'
#
#    # Filter the DataFrame for the specified team
#    #team_data = df[df['Team'] == team_name]
#
#    # Get the list of all members in the specified team
#    #all_members = ['Scrum', 'Gazelle', 'Redick', 'EscapeRoom', 'Great Clips', 'Frank N\' Beans', 'Lulu']
#    all_members = teams[team_name]
#    # Add other teams as needed
#
#    # Group the data by Date and count the unique members for each date
#    #date_member_counts = team_data.groupby('Date')['PAX'].nunique()
#    date_member_counts = filtered_df.groupby('Date')['PAX'].nunique()
#
#
#    # Filter the dates where all members have an entry
#    dates_with_all_members = date_member_counts[date_member_counts == len(all_members)].index
#
#    print(f'Dates where all members of {team_name} have an entry:')
#    print(dates_with_all_members)