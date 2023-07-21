import streamlit as st
import json

with open('db.json') as db:
    data = json.load(db)
    data = str(data).replace("'", '"')



st.download_button('Download Database', str(data), 'db.json')
