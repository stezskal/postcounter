import pandas as pd
import pymysql  # You can use the appropriate library for your database
import os
import matplotlib.pyplot as plt
import get_attendance
import argparse
from datetime import datetime
from tabulate import tabulate
from datetime import datetime, timedelta

import make_html

from teams_input import Teams


def main(start_date: str, end_date: str, get_database: bool):

    ## Read the data from pickle file if it exists, if not run and get data from SQL.
    file_path = 'attendance_data.pkl'
    if not os.path.exists(file_path) or get_database:
        get_attendance.get_attendance_df_pickle(file_path)
    df = pd.read_pickle('attendance_data.pkl')


    teams = Teams()

    print("Note must include leading zeros for the date entry below:")
    #start_date_str = input("Start date filter e.g. 2023-12-01:")
    #end_date_str = input("End date filter e.g. 2023-12-01:")
    #pax_str = input("PAX Name (hit return for all PAX):")


    #while(end_date_str!=date):
    day_df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]

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

    teams.evaluate_posts(day_df)
    teams.check_for_double_taps(day_df)

    team_results = teams.tally_team_points(day_df)
    #teams.check_q(day_df)



    with open("output.txt", 'w') as file:
        file.write(f'{start_date}\n\n')

        file.write(tabulate(team_results, headers='keys', tablefmt='pretty'))
        file.write(f'\n\n')
        file.write(tabulate(day_df, headers='keys', tablefmt='pretty'))
        file.write(f'\n\n')
        file.write(tabulate(teams.pax_df, headers='keys', tablefmt='pretty'))
        file.write(f'\n\n')


        print(f"Done")
        file.write(f"{start_date:}  \n")

        for index, row in day_df.iterrows():
            pax = row['PAX']
            q = row['Q']
            ao = row['AO']
            pts = row['Total Points']
            if(pax==q):
                q_today=True
                q_str="(+Q Point!) "
            else:
                q_today=True
                q_str=""
        
            team = row['Team']
            if team=="NoTeam":
                noteam_list.append(pax)
        
                
            #file.write(f"{start_date:<8}  For team {teams.team_names[team]:<30},  @{pax:<20} posted at {ao} and scored {pts}! {q_str}\n")
            file.write(f'@{pax} posted at #{ao} and scored {pts} points for team {teams.team_names[team]}! {q_str}\n')
    
    make_html.combine_dataframes_to_html('./challenge.htm',team_results,day_df,date=end_date,titles=["Team Standings", "Post Data"])



def increment_date_string(date_string):
    # Parse the date string into a datetime object
    date_object = datetime.strptime(date_string, "%Y-%m-%d")
    # Increment the date by 1 day
    new_date_object = date_object + timedelta(days=1)
    # Convert the datetime object back to a string
    new_date_string = new_date_object.strftime("%Y-%m-%d")
    return new_date_string

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process some dates and a database flag.")
    parser.add_argument('start_date', type=str, help='The start date')
    parser.add_argument('end_date', type=str, help='The end date')
    parser.add_argument('--get_database', action='store_true', help='Flag to get database')

    args = parser.parse_args()
    main(args.start_date, args.end_date, args.get_database)