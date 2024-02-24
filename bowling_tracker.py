import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

google_oauth_secrets = st.secrets('google_oauth')

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = "1-hV-sXs0UtHTfpA2LkF52N94HoCqtXmeObGQGu3esok"
SAMPLE_RANGE_NAME = "Sheet1!A1:E"

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

creds = None

if not creds or not creds.valid:
    
    if creds and creds.expired and creds.refresh_token:
    
        creds.refresh(Request())
    
    else:

        client_config = {'web' : {'client_id' : google_oauth_secrets['client_id'],
                                  'client_secret' : google_oauth_secrets['client_secret']}}
    
        # flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
        flow = InstalledAppFlow.from_client_config(client_config = client_config, scopes = SCOPES)
        creds = flow.run_local_server(port=0)
    
    # Save the credentials for the next run
    with open("token.json", "w") as token:
        
        token.write(creds.to_json())

    try:
        service = build("sheets", "v4", credentials=creds)
        
        # Call the Sheets API
        sheet = service.spreadsheets()

        result = (
            sheet.values()
            .get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME)
            .execute()
        )
        values = result.get("values", [])
        
        if not values:

            print("No data found.")

        scores = pd.DataFrame(values[1:], columns = values[0])

        scores['Date'] = pd.to_datetime(scores['Date'])

        print(scores)

    except HttpError as err:
    
        print(err)

scores['Date'] = pd.to_datetime(scores['Date'])
scores['Score'] = [np.nan if pd.isna(score) else int(score) for score in scores['Score']]

scores_min = scores.pivot_table(values = 'Score', index = ['Date', 'Season', 'Week'], aggfunc = min)
scores_avg = scores.pivot_table(values = 'Score', index = ['Date', 'Season', 'Week'], aggfunc = np.mean)
scores_max = scores.pivot_table(values = 'Score', index = ['Date', 'Season', 'Week'], aggfunc = max)

scores_min.rename({'Score' : 'Min Score'}, axis = 1, inplace = True)
scores_avg.rename({'Score' : 'Average Score'}, axis = 1, inplace = True)
scores_max.rename({'Score' : 'Max Score'}, axis = 1, inplace = True)

scores_agg = scores_min.join(scores_avg).join(scores_max)
scores_agg.reset_index(inplace = True)

st.title('Bowling Tracker')

st.dataframe(scores, use_container_width = True)
# st.dataframe(scores_agg, use_container_width = True)

fig, ax = plt.subplots()

ax.plot(scores_agg['Week'], scores_agg['Min Score'], label = 'Low Game', color = 'blue', linestyle = 'dashed')
ax.plot(scores_agg['Week'], scores_agg['Max Score'], label = 'High Game', color = 'blue', linestyle = 'dashed')
ax.fill_between(scores_agg['Week'], scores_agg['Min Score'], scores_agg['Max Score'], alpha = 0.25)
ax.plot(scores_agg['Week'], scores_agg['Average Score'], label = 'Average', color = 'red', marker = 'o')

ax.set_xlabel('Week')
ax.set_ylabel('Scores')

# ax.legend()

st.pyplot(fig, use_container_width = True)
