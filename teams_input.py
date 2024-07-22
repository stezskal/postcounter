import sheets
from gspread_dataframe import get_as_dataframe, set_with_dataframe
from tabulate import tabulate

import pandas as pd


class Teams(object):

    def __init__(self):
        self._connect_google_sheets()
        self._get_pax_teams_from_google_sheets()
        self._get_aos_from_google_sheets()
        self._get_names_from_google_sheets()
        self._get_team_names()

    def _connect_google_sheets(self):
        ## instantiate the sheets module (custom)
        ## will use authentication to google sheets
        ## make sure both google sheets have the service acct email shared
        self.sheets_connection = sheets.sheets(name='f3_challenge_input')

    def _get_pax_teams_from_google_sheets(self):
        ws=self.sheets_connection.get_sheet('teams')
        df = get_as_dataframe(ws, evaluate_formulas=True)

        #print(tabulate(df))

        self.teams = df['Team'].unique()
        print(self.teams)
        team_dict={}
        for team in self.teams:
            paxs = df[df['Team']==team]['PAX'].unique()
            team_dict[team]=paxs

        #print(tabulate(team_dict))

        l=len(team_dict.keys())
        if(l not in [8,9]):
            raise Exception(f"expected to be 8 or 9 teams but there are {l} teams: {team_dict.keys()}")

        self.team_dict = team_dict
        self.pax_df = df



    def _get_aos_from_google_sheets(self):
        ws=self.sheets_connection.get_sheet('aos')
        df = get_as_dataframe(ws, evaluate_formulas=True)
        self.aos_df = df

    def _get_names_from_google_sheets(self):
        ws=self.sheets_connection.get_sheet('names')
        df = get_as_dataframe(ws, evaluate_formulas=True)
        self.team_names_df = df

    
    def get_team_for_pax(self, pax):
        """ Use dataframe lookup for pax to see what team they are on and return it
        """
        df_match = self.pax_df[self.pax_df['PAX']==pax] ## look up that pax's information
        df_match2 = df_match.reset_index()  ## reset index to 0 for easy access otherwise it'll have the index from the original df
        team = df_match2.at[0,'Team']
        return team

    def get_home_for_pax(self, pax):
        """ Use dataframe lookup for pax to see what team they are on and return it
        """
        df_match = self.pax_df[self.pax_df['PAX']==pax] ## look up that pax's information
        df_match2 = df_match.reset_index()  ## reset index to 0 for easy access otherwise it'll have the index from the original df
        home = df_match2.at[0,'Home']
        return home
        
    def get_home_for_ao(self, ao):
        """ Use dataframe lookup for ao to see what side it is on
        """
        df_match = self.aos_df[self.aos_df['AO']==ao] ## look up that pax's information
        if df_match.shape[0]==0:
            raise Exception(f"No entry for ao {ao} in google sheet aos, need to add with east or west designation.")
        df_match2 = df_match.reset_index(drop=True)  ## reset index to 0 for easy access otherwise it'll have the index from the original df
        home = df_match2.at[0,'Home']
        return home

    def drop_downrange(self, df):
        ''' Drop any rows that have substring downrange in PAX name
        '''

        ## create a mask of all the rows that contain downrange for PAX
        mask = df['PAX'].str.contains('downrange')
        ## drop them in place for this df
        df.drop(index=df[mask].index, inplace=True)
        ## reset the indexes to account for the dropped rows
        df.reset_index(inplace=True, drop=True)

    def add_pax_homes_to_posts_df(self, df):
        df['PAXHome']=''

        ## reset index starting at 0, have to do this to use iloc below
        df.reset_index(inplace=True, drop=True)

        for index, row in df.iterrows():
            pax = row['PAX']
            ## Lookup team for that PAX
            try:
                home = self.get_home_for_pax(pax) # gets E or W for that PAX
            except:
                raise Exception(f"Could not get home for pax {pax}, are they new and do they need to be added to google sheet input?")
            ## Assign E or W for that row in Home column
            df.iloc[index, df.columns.get_loc('PAXHome')]=home

        ## reset index starting at 0
        df.reset_index(inplace=True, drop=True)

        return df

    def add_teams_to_posts_df(self, df):
        df['Team']='' ## add a column for Team to be inserted

        ## reset index starting at 0, have to do this to use iloc below
        df.reset_index(inplace=True, drop=True)

        for index, row in df.iterrows():
            pax = row['PAX']
            ## Lookup team for that PAX
            team = self.get_team_for_pax(pax) # gets team name for that PAX
            ## Assign the team for that row in Team column
            df.iloc[index, df.columns.get_loc('Team')]=team

        ## group/sort by teams
        df.sort_values(by='Team', inplace=True)
        df.sort_values(by='Date', inplace=True)

        ## reset index starting at 0
        df.reset_index(inplace=True, drop=True)

        return df

    def add_ao_home_to_posts_df(self, df):
        df['AOHome']=''
        for index, row in df.iterrows():
            post_ao=row['AO']
            ao_home = self.get_home_for_ao(post_ao)
            assert(ao_home in ['W','E', 'Away'])
            df.iloc[index, df.columns.get_loc('AOHome')]=ao_home

    def evaluate_posts(self, df):
        df['Post Points']=0
        df['Q Points']=0
        df['Total Points']=0
        df['Notes']=''
        for index, row in df.iterrows():
            q_points=0
            if row['PAX']==row['Q']:
                q_points=1
                df.iloc[index, df.columns.get_loc('Q Points')]=q_points

            if row['PAXHome']==row['AOHome']:
                post_points=1
                df.iloc[index, df.columns.get_loc('Post Points')]=post_points
            else:
                post_points=2
                df.iloc[index, df.columns.get_loc('Post Points')]=post_points

            df.iloc[index, df.columns.get_loc('Total Points')]=post_points + q_points

        self.check_runruck_q_points(df)

    def check_runruck_q_points(self,df):
        # Merge the two DataFrames on the 'AO' column
        merged_df = pd.merge(df, self.aos_df, on='AO', how='left')

        # Check if Q Points are non-zero and Beatdown is not 'y'
        condition = (merged_df['Q Points'] > 0) & (merged_df['Beatdown'] != 'y')

        # Zero out 'Q Points' and update 'Notes' column based on the condition
        df.loc[condition, 'Q Points'] = 0
        df.loc[condition, 'Total Points'] = df.loc[condition, 'Post Points']
        df.loc[condition, 'Notes'] = df.loc[condition, 'Notes'] + 'Run/Ruck no Q pts'
            

    def tally_team_points(self, df):

        d={}
        for team in self.teams:
            points = df.loc[df['Team'] == team, 'Total Points'].sum()
            d[team]=points
        
            print(f"Team:{team}  points:{points}")

        #self.team_pts_df = pd.DataFrame(d, index=[1], columns=['Points']).transpose().sort_values(by=[1], ascending=False)
        pts_df = pd.DataFrame(d, index=[0]).transpose()
        pts_df.rename(columns={0:'Points'}, inplace=True)
        pts_df.sort_values(by='Points', ascending=False, inplace=True)

        pts_df['PAX']=''
        for index, row in pts_df.iterrows():
            pts_df.loc[index, 'PAX'] = ", ".join(self.team_dict[index])



        self.replace_team_names(pts_df)

        self.pts_df = pts_df

        return self.pts_df


    def _get_team_names(self):
        self.team_names={}
        for pax_team in self.teams:
            try:
                new_team = self.team_names_df[self.team_names_df['PAX']==pax_team].iloc[0,self.team_names_df.columns.get_loc('Name')]
            except:
                raise Exception("There was an issue trying to replace team name {pax_team} from the google sheet, check that there is an entry for this pax team.")
            self.team_names[pax_team] = new_team
    
    def replace_team_names(self,df):
        for index, row in df.iterrows():
            pax_team=row.name ## index is the team name
            new_team = self.team_names[pax_team]
            df.rename(index={pax_team: new_team}, inplace=True)

    def check_for_double_taps(self, df):
        # Create a boolean mask to identify the first occurrence of each PAX on the same date
        df['is_first_occurrence'] = ~df.duplicated(subset=['PAX', 'Date'], keep='first')

        # Zero out 'Post Points' and 'Q Points' and update 'Notes' column for subsequent occurrences
        df.loc[~df['is_first_occurrence'], ['Post Points', 'Q Points', 'Total Points']] = 0
        df.loc[~df['is_first_occurrence'], 'Notes'] = df.loc[~df['is_first_occurrence'], 'Notes'] + 'Add\'l workout no points'

        # Drop the helper column
        df = df.drop(columns=['is_first_occurrence'])

        

