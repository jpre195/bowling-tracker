import streamlit as st

from model import load_data
from view import plot_scores_line

def main():
    st.title('Bowling Tracker')
    load_data()
    plot_scores_line()

if __name__ == '__main__':
    main()
