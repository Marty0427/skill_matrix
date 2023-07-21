from tinydb import TinyDB
import streamlit as st
import pandas as pd

st.set_page_config(layout="centered")

header_slot = st.empty()

option_slot = st.empty()

df_slot = st.empty()

db = TinyDB('db.json')

Person_table = db.table('Person')

df = pd.DataFrame(Person_table)

st.header('Input new user')

name = st.text_input('Enter your name')
phone = st.text_input('Enter your phone number')
email = st.text_input('Enter your email')


if st.button('Save'):
    if name.lower() in [row['name'].lower() for row in Person_table]:
        st.error('{name} already exists in database')
    else:
        Person_table.insert({'name': name, 'phone': phone, 'email': email})
        st.success(f'{name} saved to the database')


#view
header_slot.header('View data')

option_names = option_slot.multiselect('Select a name',
                                       df.name.unique())


if option_names:
    df_slot.dataframe(df[df.name.isin(option_names)], hide_index=True)
else:
    df_slot.dataframe(df, hide_index=True)