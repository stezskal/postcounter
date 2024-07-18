import sheets
from gspread_dataframe import get_as_dataframe, set_with_dataframe
from tabulate import tabulate

def get_teams_from_google_sheets():
    ## instantiate the sheets module (custom)
    ## will use authentication to google sheets
    ## make sure both google sheets have the service acct email shared
    sheets_input = sheets.sheets(name='f3_challenge_input')
    ws=sheets_input.get_sheet('teams')
    df = get_as_dataframe(ws, evaluate_formulas=True)

    print(tabulate(df))

    teams = df['Team'].unique()
    print(teams)
    team_dict={}
    for team in teams:
        paxs = df[df['Team']==team]['PAX'].unique()
        team_dict[team]=paxs

    print(tabulate(team_dict))

    l=len(team_dict.keys())
    if(l!=8):
        raise Exception(f"expected to be 8 teams but there are {l} teams: {team_dict.keys()}")

    return team_dict