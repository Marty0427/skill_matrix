from tinydb import TinyDB, where
import streamlit as st

st.set_page_config(
    page_title="Remove user",
)

st.header('Remove user')


db = TinyDB('db.json', encoding = 'utf-8')
Person_table = db.table('Person')


option_name = st.selectbox(
    'Select a person to remove from database (and all his skills, certificates and languages)',
    [row['name'] for row in Person_table])

if st.button('Remove'):
    for table_str in db.tables():
        table = db.table(table_str)
        table.remove(where('name') == option_name)


    st.success(f'{option_name} has been deleted')

