
import pandas as pd
import streamlit as st
from tinydb import TinyDB

db = TinyDB('db.json')

df_Person = pd.DataFrame(db.table('Person'))
df_PersonSkill = pd.DataFrame(db.table('PersonSkill'))
df_Skill = pd.DataFrame(db.table('Skill'))
df_PersonSkill = pd.merge(df_PersonSkill, df_Skill, on='skill')
df = pd.merge(df_Person, df_PersonSkill, on='name')


df_matrix = df.pivot_table(index='name', columns='skill', values='level')

st.write(df_matrix)