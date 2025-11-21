import pandas as pd
import plotly.express as px
import streamlit as st

def plot_scores_line():
    conn = st.session_state['connection']
    with open('scripts/get_scores.sql') as f:
        SQL: str = f.read()

    df = conn.sql(SQL).df()

    fig = px.line(
        data_frame = df,
        x = 'event_date',
        y = 'avg_score',
        color = 'bowlerID',
        title = 'Daily Average Score',
        labels = {
            'event_date' : 'Date',
            'avg_score' : 'Average',
            'bowlerID' : 'BowlerID'
        }
    )

    with st.container(border = True, key = 'avg_scores_line'):
        st.plotly_chart(fig)
