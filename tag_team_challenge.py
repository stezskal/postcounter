import pandas as pd
import pymysql  # You can use the appropriate library for your database
import os
import matplotlib.pyplot as plt
import get_attendance

# Define teams and corresponding PAX
teams = {
    'Team 1': ['Scrum', 'Gazelle', 'Redick', 'EscapeRoom', 'Great Clips', 'Frank N\' Beans', 'Lulu'],
    'Team 2': ['Safety’s off', 'Captain Kirk', 'Spork', 'Big Spoon', 'Luigi', 'Majkowski', 'Lost Signal'],
    'Team 3': ['Smores', 'Gypsy', 'Connors', 'Ricky-Bobby', 'Pryor', 'Spirit', 'Guppy'],
    'Team 4': ['Soybean', 'Tuna', 'Saganaki', 'White Belt', 'Lake Forest', 'PomPom', 'Caddyshack'],
    'Team 5': ['Fanny-Pack', 'LaX', 'Speedo', 'Swoosh', 'Backseat', 'FEMA', 'Business Casual'],
    'Team 6': ['D3', 'Mule', 'Wally', 'Zebulon', 'Autopilot', 'Frosted Tips', 'McDowells'],
}

## Read the data from pickle file if it exists, if not run and get data from SQL.
file_path = 'attendance_data.pkl'
if not os.path.exists(file_path):
    get_attendance.get_attendance_df_pickle(file_path)
df = pd.read_pickle('attendance_data.pkl')

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


# Plotting the team results
fig, ax = plt.subplots(figsize=(10, 6))
ax.axis('off')  # Turn off axis
table_data = [result_team.columns] + result_team.values.tolist()
ax.table(cellText=table_data, colLabels=None, cellLoc='center', loc='center')

plt.savefig('team_results.png', bbox_inches='tight')
plt.show()