import streamlit as st
from tinydb import TinyDB
import pandas as pd


st.set_page_config(layout="wide")


db = TinyDB('db.json', encoding = 'utf-8')

df_Person = pd.DataFrame(db.table('Person'))
df_PersonSkill = pd.DataFrame(db.table('PersonSkill'))
df_Skill = pd.DataFrame(db.table('Skill'))
df_PersonCertificate = pd.DataFrame(db.table('PersonCertificate'))
df_Certificate = pd.DataFrame(db.table('Certificate'))
df_PersonLanguage = pd.DataFrame(db.table('PersonLanguage'))
df_Language = pd.DataFrame(db.table('Language'))

df_overview = pd.concat([df_PersonSkill.rename(columns = {'name': 'name_skill'}),
                         df_PersonLanguage.rename(columns = {'name': 'name_language'}),
                         df_PersonCertificate.rename(columns = {'name': 'name_certificate'})])


df_PersonSkill.level = df_PersonSkill.level.apply(lambda x: int(x)*'⭐')
df_PersonSkill = pd.merge(df_PersonSkill, df_Skill, on='skill')
df_PersonCertificate = pd.merge(df_PersonCertificate, df_Certificate, on='certificate')
df_PersonLanguage = pd.merge(df_PersonLanguage, df_Language, on='language')

st.header('Overview')

col11, col12 = st.columns([1, 1])
col21, col22, col23 = st.columns([5, 2, 5])

with col11:
    option_names = st.multiselect('Select a person',
                            df_Person.name.unique())
    
    option_certificates = st.multiselect('Select a certificate',
                                df_Certificate.certificate.unique())
    

with col12:
    option_languages = st.multiselect('Select a language',
                            df_Language.language.unique())

    option_skills = st.multiselect('Select a skill',
                            df_Skill.skill.unique())
    

valid_names = []

if option_names:
    option_names_filter = option_names.copy()
    valid_names.append(option_names)
else:
    option_names_filter = df_Person.name.unique()


if option_certificates:
    option_certificates_filter = option_certificates.copy()
    certificate_names = df_PersonCertificate[df_PersonCertificate.certificate.isin(option_certificates)].name
    valid_names.append(list(certificate_names))
else:
    option_certificates_filter = df_Certificate.certificate.unique()


if option_languages:
    option_languages_filter = option_languages.copy()
    language_names = df_PersonLanguage[df_PersonLanguage.language.isin(option_languages)].name
    valid_names.append(list(language_names))

else:
    option_languages_filter = df_Language.language.unique()


if option_skills:
    option_skills_filter = option_skills.copy()
    skill_names = df_PersonSkill[df_PersonSkill.skill.isin(option_skills)].name
    valid_names.append(list(skill_names))

else:
    option_skills_filter = df_Skill.skill.unique()

if valid_names:
    valid_names = sum(valid_names, [])
else:
    valid_names = df_Person.name


option_certificates_bool = df_overview.certificate.isin(option_certificates_filter)
option_languages_bool = df_overview.language.isin(option_languages_filter)
option_skills_bool = df_overview.skill.isin(option_skills_filter)

df_visible = df_overview[(option_certificates_bool | option_languages_bool | option_skills_bool)]

names_intersection = set(df_visible.name_skill).intersection(df_visible.name_language).intersection(df_visible.name_certificate)


with col21:
    st.subheader('Certificates')
    st.dataframe(df_PersonCertificate[df_PersonCertificate.certificate.isin(df_visible.certificate) & df_PersonCertificate.name.isin(valid_names)], use_container_width=True, hide_index=True)

with col22:
    st.subheader('Languages')
    st.dataframe(df_PersonLanguage[df_PersonLanguage.language.isin(df_visible.language) & df_PersonLanguage.name.isin(valid_names)], use_container_width=True, hide_index=True)

with col23:
    st.subheader('Skills')
    st.dataframe(df_PersonSkill[df_PersonSkill.skill.isin(df_visible.skill) & df_PersonSkill.name.isin(valid_names)], use_container_width=True, hide_index=True)


