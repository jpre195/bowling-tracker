from datetime import datetime
import os

import pandas as pd
from sqlalchemy import create_engine
import streamlit as st

#Connect to database
connection_string = f"mysql+mysqlconnector://{os.environ['PS_USER']}:{os.environ['PS_PASS']}@{os.environ['PS_HOST']}:3306/{os.environ['PS_DATABASE']}"
engine = create_engine(connection_string)

st.title('Upload Scores')

with st.form('scores_form'):

    suggested_season = datetime.today().year - 1 if datetime.today().month < 6 else datetime.today().year

    scores_date = st.date_input('Date')
    season = st.number_input('Season', value = suggested_season)
    week = st.number_input('Week', min_value = 1, value = max(st.session_state['scores']['Week']) + 1)
    game = st.number_input('Game', min_value = 1, value = 1)
    score = st.number_input('Score', min_value = 0, max_value = 300)

    submitted = st.form_submit_button('Submit')

    if submitted:

        curr_scores = pd.DataFrame({'date' : [scores_date],
                                    'season' : [season],
                                    'week' : [week],
                                    'game' : [game],
                                    'score' : [score]})
        
        curr_scores['date'] = pd.to_datetime(curr_scores['date'])

        curr_scores.to_sql('league', con = engine, if_exists = 'append', index = False)

        st.warning('Score uploaded to database')
