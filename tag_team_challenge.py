import pandas as pd
import pymysql  # You can use the appropriate library for your database

# Define teams and corresponding PAX
teams = {
    'Team 1': ['Scrum', 'Gazelle', 'Redick', 'EscapeRoom', 'Great Clips', 'Frank N\' Beans', 'Lulu'],
    'Team 2': ['Safety’s off', 'Captain Kirk', 'Spork', 'Big Spoon', 'Luigi', 'Majkowski', 'Lost Signal'],
    'Team 3': ['Smores', 'Gypsy', 'Connors', 'Ricky-Bobby', 'Pryor', 'Spirit', 'Guppy'],
    'Team 4': ['Soybean', 'Tuna', 'Saganaki', 'White Belt', 'Lake Forest', 'PomPom', 'Caddyshack'],
    'Team 5': ['Fanny-Pack', 'LaX', 'Speedo', 'Swoosh', 'Backseat', 'FEMA', 'Business Casual'],
    'Team 6': ['D3', 'Mule', 'Wally', 'Zebulon', 'Autopilot', 'Frosted Tips', 'McDowells'],
}



# Initialize MySQL connection

db_params = {
    'host' : "f3stlouis.cac36jsyb5ss.us-east-2.rds.amazonaws.com",
    'user' : "paxminer",
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

# Filter data for November and December 2023
filtered_df = df[
    (df['Date'] >= '2023-11-01') &
    (df['Date'] < '2024-01-01')
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

# Display the results
print("Results table for PAX with posts:")
print(result_pax)

print("\nResults table for each Team's counts:")
print(result_team)

# Close the database connection
connection.close()