import duckdb
import pandas as pd
import streamlit as st

def load_data():
    tables: list[str] = ['bowler', 'ball', 'arsenal', 'house', 'practice', 'tournament', 'league', 'game']
    if any(f'{table}_data' not in st.session_state for table in tables):
        conn = duckdb.connect('bowling.duckdb')
        for table in tables:
            df: pd.DataFrame = conn.sql(f'select * from {table}').df()
            st.session_state[f'{table}_data'] = df
        st.session_state['connection'] = conn