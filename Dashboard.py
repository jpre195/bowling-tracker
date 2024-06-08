import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sqlalchemy import create_engine
import streamlit as st

#Connect to database
# connection_string = f"mysql+mysqlconnector://{os.environ['PS_USER']}:{os.environ['PS_PASS']}@{os.environ['PS_HOST']}:3306/{os.environ['PS_DATABASE']}"
connection_string = 'sqlite:///bowling.db'
engine = create_engine(connection_string)

#Query all league scores
scores = pd.read_sql('select * from league', engine)

#Add scores and engine to session state
st.session_state['scores'] = scores
st.session_state['engine'] = engine

#Capitalize column names
scores.rename({col : col.capitalize() for col in scores.columns}, axis = 1, inplace = True)

#Cast date column to datetime
# scores['Date'] = pd.to_datetime(scores['Date'])

#Cast score column to integer
scores['Score'] = [np.nan if pd.isna(score) else int(score) for score in scores['Score']]

#Calculate min, average, and max for each day
scores_min = scores.pivot_table(values = 'Score', index = ['Date', 'Season', 'Week'], aggfunc = min)
scores_avg = scores.pivot_table(values = 'Score', index = ['Date', 'Season', 'Week'], aggfunc = np.mean)
scores_max = scores.pivot_table(values = 'Score', index = ['Date', 'Season', 'Week'], aggfunc = max)
scores_series = scores.pivot_table(values = 'Score', index = ['Date', 'Season', 'Week'], aggfunc = sum)
scores_games = scores.pivot_table(values = 'Score', index = ['Date', 'Season', 'Week'], aggfunc = 'count')

#Rename score columns in each pivot table
scores_min.rename({'Score' : 'Min Score'}, axis = 1, inplace = True)
scores_avg.rename({'Score' : 'Average Score'}, axis = 1, inplace = True)
scores_max.rename({'Score' : 'Max Score'}, axis = 1, inplace = True)

#Join tables and reset index
scores_agg = scores_min.join(scores_avg).join(scores_max)
scores_agg.reset_index(inplace = True)

#Set title of application
st.title('Bowling Tracker')

#Show high game and current average
col1, col2, col3 = st.columns(3)

col1.metric('High Game', max(scores['Score']))

col2.metric('High Series', max(scores[['Week', 'Score']].groupby('Week').sum()['Score']))

previous_scores = scores[scores.Date < max(scores.Date)]
delta = scores['Score'].mean() - previous_scores['Score'].mean()

col3.metric('Average', round(scores['Score'].mean(), 1), delta = round(delta, 1))

st.divider()

#Create a plot of scores over time
fig, ax = plt.subplots()

ax.plot(scores_agg['Week'], scores_agg['Min Score'], label = 'Low Game', color = 'blue', linestyle = 'dashed')
ax.plot(scores_agg['Week'], scores_agg['Max Score'], label = 'High Game', color = 'blue', linestyle = 'dashed')
ax.fill_between(scores_agg['Week'], scores_agg['Min Score'], scores_agg['Max Score'], alpha = 0.25)
ax.plot(scores_agg['Week'], scores_agg['Average Score'], label = 'Average', color = 'red', marker = 'o')

ax.set_xlabel('Week')
ax.set_ylabel('Scores')

ax.set_title('Scores by Week')

st.pyplot(fig, use_container_width = True)

#Create a plot of average over time
scores_series.rename({'Score' : 'Series'}, axis = 1, inplace = True)
scores_games.rename({'Score' : 'Games'}, axis = 1, inplace = True)

avg_df = scores_series.join(scores_games)
avg_df.reset_index(inplace = True)

avg_df['Total Pins'] = avg_df['Series'].expanding(1).sum()
avg_df['Total Games'] = avg_df['Games'].expanding(1).sum()

avg_df['League Average'] = avg_df['Total Pins'] / avg_df['Total Games']

fig, ax = plt.subplots()

ax.plot(avg_df['Week'], avg_df['League Average'])

ax.set_xlabel('Week')
ax.set_ylabel('Average')

ax.set_title('Average by Week')

st.pyplot(fig, use_container_width = True)

#Display scores
st.dataframe(scores, use_container_width = True)
