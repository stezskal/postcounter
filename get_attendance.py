import pandas as pd
import pymysql  # You can use the appropriate library for your database
import os 

def get_attendance_df_pickle(pkl_filename='attendance_data.pkl'):
    """ Connects to sql database and gets the attendance view dataframe.
        Writes it to a pkl file and also returns it for use.

        Must have the db_password set for paxminer read-only mode.
        This password is in the notes google doc for F3.
    """

    # Initialize MySQL connection
    # Get the database password from the environment variable
    db_password = os.environ.get('DB_PASSWORD')
    if(db_password==None):
        raise ValueError("Must set the DB_PASSWORD env variable in order to login to database!")
    db_params = {
        'host' : "f3stlouis.cac36jsyb5ss.us-east-2.rds.amazonaws.com",
        'user' : "paxminer",
        'password': db_password,  # Use the environment variable here
        'database' : "f3nwhighway"
    }


    # Establish a connection to the database
    connection = pymysql.connect(**db_params)


    # SQL query to get attendance data
    sql_query = """
        SELECT PAX, Date
        FROM attendance_view
    """

    # Read the data into a DataFrame
    df = pd.read_sql_query(sql_query, connection)

    # Save the DataFrame to a pickle file
    df.to_pickle(pkl_filename)

    return df