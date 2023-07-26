from tinydb import TinyDB, Query
import streamlit as st
import pandas as pd

st.set_page_config(layout="centered")


header_slot = st.empty()

option_slot1 = st.empty()

option_slot2 = st.empty()

df_slot = st.empty()

User = Query()
db = TinyDB('db.json')

Person_table = db.table('Person')
Language_table = db.table('Language')
PersonLanguage_table = db.table('PersonLanguage')

df = pd.DataFrame(PersonLanguage_table)


st.header('Input new language')

language = st.text_input('Enter language name')


if st.button('Save'):
    if language.lower() in [row['language'].lower() for row in Language_table]:
        st.error('Language already exists in database')
    elif language == '':
        st.error('Language name field is empty')
    else:
        Language_table.insert({'language': language})
        st.success(f'{language} language saved to the database')


# Add

st.header('Assign language to a person')

option_name = st.selectbox(
    'Select a person to assign a language',
    [row['name'] for row in Person_table])

option_language = st.selectbox(
    'Select a language to assign',
    [row['language'] for row in Language_table])

level = st.selectbox(
    'Select a language level',
    ['A1', 'A2', 'B1', 'B2', 'C1', 'C2'])


if st.button('Assign'):
    record_exists = PersonLanguage_table.search((User.name == option_name) & (User.language == option_language))
    if record_exists:
        PersonLanguage_table.update({'level': level}, (User.name == option_name) & (User.language == option_language))
        st.success(f'{option_language} level updated for {option_name}')

    else:
        PersonLanguage_table.insert({'name': option_name, 'language': option_language, 'level': level})
        st.success(f'{option_language} assigned to {option_name}')


#view

header_slot.header('View data')

option_names = option_slot1.multiselect('Select a person',
               df.name.unique())

option_languages = option_slot2.multiselect('Select a language',
               df.language.unique())



if option_names and option_languages:
    df_slot.dataframe(df[(df.name.isin(option_names)) & (df.language.isin(option_languages))], hide_index=True)

elif option_names and not option_languages:
    df_slot.dataframe(df[(df.name.isin(option_names))], hide_index=True)

elif option_languages and not option_names:
    df_slot.dataframe(df[(df.language.isin(option_languages))], hide_index=True)

else:
    df_slot.dataframe(df, hide_index=True)
