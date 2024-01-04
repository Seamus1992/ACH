import gspread
import pandas as pd
import streamlit as st
import plotly.express as px


gc = gspread.service_account(r'C:\Users\SéamusPeareBartholdy\Documents\GitHub\AC-Horsens\wellness-1123-178fea106d0a.json')
sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1haWEtNQdhthKaSQjb2BRHlq2FLexicUOAHbjNFRAUAk/edit#gid=1984878556')
ws = sh.worksheet('Samlet')
df = pd.DataFrame(ws.get_all_records())

dfU13 = df[['Spillere U13','Hvilken årgang er du?']]
dfU13 = dfU13[['Spillere U13','Hvilken årgang er du?']].astype(str).value_counts().reset_index()
dfU13.columns = ['Spillernavn','Årgang','Antal besvarelser']
dfU13 = dfU13[dfU13['Spillernavn'].str.strip() != '']
dfU13 = dfU13.reset_index(drop=True)
st.title('U13')

st.dataframe(dfU13)

dfU14 = df[['Spillere U14','Hvilken årgang er du?']]
dfU14 = dfU14[['Spillere U14','Hvilken årgang er du?']].astype(str).value_counts().reset_index()
dfU14.columns = ['Spillernavn','Årgang','Antal besvarelser']
dfU14 = dfU14[dfU14['Spillernavn'].str.strip() != '']
dfU14 = dfU14.reset_index(drop=True)
st.title('U14')

st.dataframe(dfU14)

dfU15 = df[['Spillere U15','Hvilken årgang er du?']]
dfU15 = dfU15[['Spillere U15','Hvilken årgang er du?']].astype(str).value_counts().reset_index()
dfU15.columns = ['Spillernavn','Årgang','Antal besvarelser']
dfU15 = dfU15[dfU15['Spillernavn'].str.strip() != '']
dfU15 = dfU15.reset_index(drop=True)
st.title('U15')

st.dataframe(dfU15)

dfU16 = df[['Spillere U16','Hvilken årgang er du?']]
dfU16 = dfU16[['Spillere U16','Hvilken årgang er du?']].astype(str).value_counts().reset_index()
dfU16.columns = ['Spillernavn','Årgang','Antal besvarelser']
dfU16 = dfU16[dfU16['Spillernavn'].str.strip() != '']
dfU16 = dfU16.reset_index(drop=True)
st.title('U16')

st.dataframe(dfU16)

dfU17 = df[['Spillere U17','Hvilken årgang er du?']]
dfU17 = dfU17[['Spillere U17','Hvilken årgang er du?']].astype(str).value_counts().reset_index()
dfU17.columns = ['Spillernavn','Årgang','Antal besvarelser']
dfU17 = dfU17[dfU17['Spillernavn'].str.strip() != '']
dfU17 = dfU17.reset_index(drop=True)
st.title('U17')

st.dataframe(dfU17)

dfU18 = df[['Spillere U18','Hvilken årgang er du?']]
dfU18 = dfU18[['Spillere U18','Hvilken årgang er du?']].astype(str).value_counts().reset_index()
dfU18.columns = ['Spillernavn','Årgang','Antal besvarelser']
dfU18 = dfU18[dfU18['Spillernavn'].str.strip() != '']
dfU18 = dfU18.reset_index(drop=True)
st.title('U18')

st.dataframe(dfU18)

dfU19 = df[['Spillere U19','Hvilken årgang er du?']]
dfU19 = dfU19[['Spillere U19','Hvilken årgang er du?']].astype(str).value_counts().reset_index()
dfU19.columns = ['Spillernavn','Årgang','Antal besvarelser']
dfU19 = dfU19[dfU19['Spillernavn'].str.strip() != '']
dfU19 = dfU19.reset_index(drop=True)
st.title('U19')

df_U19 = pd.concat([dfU18,dfU19])
sorted(df_U19['Antal besvarelser'])
st.dataframe(df_U19)

data = {
    'Alder': ['U13', 'U14', 'U15', 'U16', 'U17', 'U18', 'U19'],
    'Besvarelser pr. spiller': [79.05, 82, 102.2, 100.3, 68.1, 44.4, 49.0]
}
df = pd.DataFrame(data)
df['Besvarelser pr. spiller'] = df['Besvarelser pr. spiller'].astype(float)

st.dataframe(df)
fig = px.bar(df, x='Alder', y='Besvarelser pr. spiller', title='Besvarelser pr. spiller per Alder')
st.plotly_chart(fig)