import sheets
from gspread_dataframe import get_as_dataframe, set_with_dataframe
from tabulate import tabulate

## instantiate the sheets module (custom)
## will use authentication to google sheets
## make sure both google sheets have the service acct email shared
sheets_input = sheets.sheets(name='f3_challenge_input')
ws=sheets_input.get_sheet('teams')
df = get_as_dataframe(ws, evaluate_formulas=True)

print(tabulate(df))