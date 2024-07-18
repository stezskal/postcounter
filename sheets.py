""" 
Connect to GooleSheets using gspread and Google service account

https://gspread.readthedocs.io/en/latest/oauth2.html
    Followed directions for service account.  
    Created service account with permissions.
    GoogleCloud > Service Accounts > lilcor_financials > Keys > Add Key 
    Downloaded json.  Placed in ~/.config/gspread/service_account.json
    You can only download the json one time when you add a key.
    Then took the email address in json and shared the spreadsheet with that email address. 
    Note have to share any spreadsheet used with the service account email.
    lilcor-financials@lilcor-financial-1610802827505.iam.gserviceaccount.com

    Added a 2nd key for christle under the same service account, using same directions.

"""
import gspread
#import gspread-fomatting as fmt
from gspread_formatting import *
import os

import logging as log

class sheets(object):

    def __init__(self, name, folder_id=None):

        user = os.getlogin()

        log.info(f"Opening sheet {name} with folder id {folder_id}")

        if(user.lower()=="root"): #Christle's computer user is mac but runs under root for some reason..
            json_path = "/Users/mac/.google_auth/service_account.json"
            self.user = "Christle"
        elif(user.lower()=="alex"):
            json_path = '/home/alex/.google_auth/service_account.json'
            self.user = "Alex"
        elif(user.lower()=="smores"):
            json_path = '/home/smores/.google_auth/service_account.json'
            self.user = "Alex"
        else:
            raise Exception(f"Unkown user name received from os.getlogin()={user} not sure who is running this and where their google auth json file is.")
        gc = gspread.service_account(
            filename=json_path)

        ## Try to open the spreadsheet, if it failes try to create it.
        try:
            self.sh = gc.open(name, folder_id=folder_id)
        except:
            log.warning("Sheet {sheet} with folder id {folder_id} does not exist!! So we have to create it.  Is this expected?")
            self.sh = gc.create(name, folder_id=folder_id)
            self.sh.share('alex.stezskal@gmail.com', perm_type='user', role='writer')
            self.sh.share('christle.stezskal@gmail.com', perm_type='user', role='writer')

    def create_sheet(self, name):
        log.info("Creating sheet "+str(name))
        ## try to delete and add the sheet
        try:
            self.sh.del_worksheet(self.sh.worksheet(name))
        except:
            log.debug('tried to delete the sheet, but is does not exist')

        ## add the sheet
        self.sh.add_worksheet(title=name, rows="1000", cols="20")

        ## delete default Sheet1 if it exists
        try:
            self.sh.del_worksheet(self.sh.worksheet('Sheet1'))
        except:
            pass

        ## return the worksheet object so it can be manipulated
        return self.sh.worksheet(name)

    def get_sheet(self, name):
        return self.sh.worksheet(name)

    def get_all(self):
        return self.sh.openall()




        return worksheet
    
if __name__=="__main__":
    ss = sheets(name='test_mco', folder_id='1xHM4tt0p6f3X_0Wlu2TWSmokRSRcDPWJ')
