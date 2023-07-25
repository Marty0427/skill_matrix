from tinydb import TinyDB
import streamlit as st
import pandas as pd

st.set_page_config(layout="centered")

header_slot = st.empty()

option_slot1 = st.empty()

option_slot2 = st.empty()

df_slot = st.empty()


db = TinyDB('db.json', encoding = 'utf-8')

Person_table = db.table('Person')
Certificate_table = db.table('Certificate')
PersonCertificate_table = db.table('PersonCertificate')

df_PersonCertificate = pd.DataFrame(PersonCertificate_table)
df_Certificate = pd.DataFrame(Certificate_table)

df = pd.merge(df_PersonCertificate, df_Certificate, on='certificate')

st.header('Input new certificate')

certificate = st.text_input('Enter certificate name')
description = st.text_input('Enter certificate description')
category = st.text_input('Enter certificate category')


if st.button('Save'):
    if certificate.lower() in [row['certificate'].lower() for row in Certificate_table]:
        st.error('Certificate already exists in database')
    elif certificate == '':
        st.error('Certificate name field is empty')
    else:
        Certificate_table.insert({'certificate': certificate, 'description': description, 'category': category})
        st.success(f'{certificate} certificate saved to the database')



# Add

st.header('Assign certificate to a person')

option_name = st.selectbox(
    'Select a person to assign a certificate',
    [row['name'] for row in Person_table])

option_certificate = st.selectbox(
    'Select a certificate to assign',
    [row['certificate'] for row in Certificate_table])


if st.button('Assign'):
    PersonCertificate_table.insert({'name': option_name, 'certificate': option_certificate})
    st.success(f'{option_certificate} certificate for {option_name} added to the database')



#view

header_slot.header('View data')

option_names = option_slot1.multiselect('Select a person',
               df.name.unique())

option_certificates = option_slot2.multiselect('Select a certificate',
               df.certificate.unique())




if option_names and option_certificates:
    df_slot.dataframe(df[(df.name.isin(option_names)) & (df.certificate.isin(option_certificates))], hide_index=True)

elif option_names and not option_certificates:
    df_slot.dataframe(df[(df.name.isin(option_names))], hide_index=True)

elif option_certificates and not option_names:
    df_slot.dataframe(df[(df.certificate.isin(option_certificates))], hide_index=True)

else:
    df_slot.dataframe(df, hide_index=True)