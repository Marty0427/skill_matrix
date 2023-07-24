from tinydb import TinyDB
import streamlit as st
import pandas as pd

def rating_to_star(rating):
    return '⭐' * rating

st.set_page_config(layout="centered")

header_slot = st.empty()

option_slot1 = st.empty()

option_slot2 = st.empty()

df_slot = st.empty()



db = TinyDB('db.json')

Person_table = db.table('Person')
Skill_table = db.table('Skill')
PersonSkill_table = db.table('PersonSkill')

df_PersonSkill = pd.DataFrame(PersonSkill_table)
df_Skill = pd.DataFrame(Skill_table)

df_PersonSkill.level = df_PersonSkill.level.apply(rating_to_star)

df = pd.merge(df_PersonSkill, df_Skill, on='skill')

st.header('Input new skill')

skill = st.text_input('Enter skill')
description = st.text_input('Enter skill description')
category = st.selectbox(
            'Select a skill category',
            ['Programming', 'Softskill', 'Machine learning', 'Atlassian', 'Other'])



if st.button('Save'):
    if skill.lower() in [row['skill'].lower() for row in Skill_table]:
        st.error(f'{skill} skill already exists in database')
    elif skill == '':
        st.error('Skill name field is empty')
    else:
        Skill_table.insert({'skill': skill, 'description': description, 'category': category})
        st.success(f'{skill} skill saved to the database')


# add

st.header('Assign skill to a person')

option_name = st.selectbox(
    'Select a person to assign a skill (if the person is not in options, create a new user in New user tab)',
    [row['name'] for row in Person_table])

option_skill = st.selectbox(
    'Select a skill to assign',
    [row['skill'] for row in Skill_table])

level = st.selectbox(
    'Enter a skill level (1 worst - 5 best)',
    [i for i in range(1, 6)]
    )

if st.button('Assign'):
    PersonSkill_table.insert({'name': option_name, 'skill': option_skill, 'level': level*"\u2B50"})
    st.success(f'{option_skill} skill for {option_name} added to the database')

#view

header_slot.header('View data')

option_names = option_slot1.multiselect('Select a person',
               df.name.unique())

option_skills = option_slot2.multiselect('Select a skill',
               df.skill.unique())



if option_names and option_skills:
    df_slot.dataframe(df[(df.name.isin(option_names)) & (df.skill.isin(option_skills))], hide_index=True)

elif option_names and not option_skills:
    df_slot.dataframe(df[(df.name.isin(option_names))], hide_index=True)

elif option_skills and not option_names:
    df_slot.dataframe(df[(df.skill.isin(option_skills))], hide_index=True)

else:
    df_slot.dataframe(df, hide_index=True    )

