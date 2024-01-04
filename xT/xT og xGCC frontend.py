import pandas as pd
import streamlit as st
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
import plotly.express as px

st.set_page_config(layout='wide')
df = pd.read_csv(r'C:\Users\SéamusPeareBartholdy\Desktop\xT\U17 Ligaen 23 24.csv')

df = df[['id','matchId','label','date','matchPeriod','minute','shot.isGoal','type.primary','type.secondary','location.x','location.y','team.name','opponentTeam.name','player.id','player.name','pass.accurate','pass.endLocation.x','pass.endLocation.y','pass.recipient.id','pass.recipient.name','possession.id','possession.duration','possession.id','possession.eventsNumber','possession.eventIndex','possession.team.name','possession.attack.xg','carry.progression','carry.endLocation.x','carry.endLocation.y']]
df1 = df.copy()
df = df[(df['pass.accurate'] ==True) | (df['carry.progression'] > 0)]
df = df[~df['type.primary'].str.contains('infraction')]
df = df[~df['type.primary'].str.contains('game_interruption')]
df = df[~df['type.primary'].str.contains('throw_in')]
df = df[~df['type.primary'].str.contains('free_kick')]
df = df[~df['type.primary'].str.contains('penalty')]
df = df[~df['type.primary'].str.contains('corner')]

df1 = df1[~df1['type.primary'].str.contains('infraction')]
df1 = df1[~df1['type.primary'].str.contains('game_interruption')]
df1 = df1[~df1['type.primary'].str.contains('throw_in')]
df1 = df1[~df1['type.primary'].str.contains('free_kick')]
df1 = df1[~df1['type.primary'].str.contains('penalty')]
df1 = df1[~df1['type.primary'].str.contains('corner')]

conditions = [
    (df['location.x'] <= 30) & ((df['location.y'] <= 19) | (df['location.y'] >= 81)),
    (df['location.x'] <= 30) & ((df['location.y'] >= 19) | (df['location.y'] <= 81)),
    ((df['location.x'] >= 30) & (df['location.x'] <= 50)),
    ((df['location.x'] >= 50) & (df['location.x'] <= 70)),
    ((df['location.x'] >= 70) & ((df['location.y'] <= 15) | (df['location.y'] >= 84))),
    (((df['location.x'] >= 70) & (df['location.x'] <= 84)) & ((df['location.y'] >= 15) & (df['location.y'] <= 84))),
    ((df['location.x'] >= 84) & ((df['location.y'] >= 15) & (df['location.y'] <= 37)) | ((df['location.y'] <= 84) & (df['location.y'] >= 63))),
    ((df['location.x'] >= 84) & ((df['location.y'] >= 37) & (df['location.y'] <= 63)))
]

# Define corresponding zone values
zone_values = ['Zone 1', 'Zone 2', 'Zone 3', 'Zone 4', 'Zone 5', 'Zone 6', 'Zone 7', 'Zone 8']

# Assign 'Start Zone' based on conditions
df['Start Zone'] = np.select(conditions, zone_values, default=None)

conditions_pass_end = [
    (df['pass.endLocation.x'] <= 30) & ((df['pass.endLocation.y'] <= 19) | (df['pass.endLocation.y'] >= 81)),
    (df['pass.endLocation.x'] <= 30) & ((df['pass.endLocation.y'] >= 19) | (df['pass.endLocation.y'] <= 81)),
    ((df['pass.endLocation.x'] >= 30) & (df['pass.endLocation.x'] <= 50)),
    ((df['pass.endLocation.x'] >= 50) & (df['pass.endLocation.x'] <= 70)),
    ((df['pass.endLocation.x'] >= 70) & ((df['pass.endLocation.y'] <= 15) | (df['pass.endLocation.y'] >= 84))),
    (((df['pass.endLocation.x'] >= 70) & (df['pass.endLocation.x'] <= 84)) & ((df['pass.endLocation.y'] >= 15) & (df['pass.endLocation.y'] <= 84))),
    ((df['pass.endLocation.x'] >= 84) & ((df['pass.endLocation.y'] >= 15) & (df['pass.endLocation.y'] <= 37)) | ((df['pass.endLocation.y'] <= 84) & (df['pass.endLocation.y'] >= 63))),
    ((df['pass.endLocation.x'] >= 84) & ((df['pass.endLocation.y'] >= 37) & (df['pass.endLocation.y'] <= 63)))
]

# Define conditions for zone assignment for 'carry.endLocation'
conditions_carry_end = [
    (df['carry.endLocation.x'] <= 30) & ((df['carry.endLocation.y'] <= 19) | (df['carry.endLocation.y'] >= 81)),
    (df['carry.endLocation.x'] <= 30) & ((df['carry.endLocation.y'] >= 19) | (df['carry.endLocation.y'] <= 81)),
    ((df['carry.endLocation.x'] >= 30) & (df['carry.endLocation.x'] <= 50)),
    ((df['carry.endLocation.x'] >= 50) & (df['carry.endLocation.x'] <= 70)),
    ((df['carry.endLocation.x'] >= 70) & ((df['carry.endLocation.y'] <= 15) | (df['carry.endLocation.y'] >= 84))),
    (((df['carry.endLocation.x'] >= 70) & (df['carry.endLocation.x'] <= 84)) & ((df['carry.endLocation.y'] >= 15) & (df['carry.endLocation.y'] <= 84))),
    ((df['carry.endLocation.x'] >= 84) & ((df['carry.endLocation.y'] >= 15) & (df['carry.endLocation.y'] <= 37)) | ((df['carry.endLocation.y'] <= 84) & (df['carry.endLocation.y'] >= 63))),
    ((df['carry.endLocation.x'] >= 84) & ((df['carry.endLocation.y'] >= 37) & (df['carry.endLocation.y'] <= 63)))
]

# Define corresponding zone values
zone_values = ['Zone 1', 'Zone 2', 'Zone 3', 'Zone 4', 'Zone 5', 'Zone 6', 'Zone 7', 'Zone 8']

df['End Zone'] = None
# Assign 'End Zone' based on conditions for 'pass.endLocation' and 'carry.endLocation'
df['End Zone'] = np.select(
    [
        df['End Zone'].isnull() & np.isin(np.select(conditions_pass_end, zone_values, default=None), zone_values),
        df['End Zone'].isnull() & np.isin(np.select(conditions_carry_end, zone_values, default=None), zone_values)
    ],
    [
        np.select(conditions_pass_end, zone_values, default=None),
        np.select(conditions_carry_end, zone_values, default=None)
    ],
    default=df['End Zone']
)

dfscore = pd.read_csv(r'C:\Users\SéamusPeareBartholdy\Desktop\xT\Zone scores.csv')

df = df.merge(dfscore[['Start Zone', 'Start zone score']], on='Start Zone', how='left')

# Merge 'End Zone' scores
df = df.merge(dfscore[['End Zone', 'End zone score']], on='End Zone', how='left')

df['xT'] = df['End zone score'] - df['Start zone score']

xThold = df.groupby('team.name')['xT'].agg('sum').reset_index()
xTspiller = df.groupby(['player.id','player.name','team.name'])['xT'].agg('sum').reset_index()
xTmodtager = df.groupby(['pass.recipient.id','pass.recipient.name','team.name'])['xT'].agg('sum').reset_index()
xThold = xThold.sort_values(by='xT', ascending=False)
xThold['xT hold rank'] = xThold['xT'].rank(ascending=False).astype(int)
xTspiller = xTspiller.sort_values(by='xT', ascending=False)
xTmodtager = xTmodtager.sort_values(by='xT', ascending=False)
xTmodtager = xTmodtager.rename(columns={'pass.recipient.name': 'player.name'})
xTmodtager = xTmodtager.rename(columns={'pass.recipient.id': 'player.id'})
xT = pd.merge(xTspiller, xTmodtager, on=['player.id','player.name', 'team.name'], how='outer')
xT = xT.dropna(subset=['xT_x'])
xT['xT'] = xT['xT_x'] + xT['xT_y']
xT = xT.sort_values(by='xT',ascending=False)
xT = xT[['player.id','player.name','team.name','xT']]
xT['xT'] = xT['xT'].fillna(0)
xT['xT Rank'] = xT['xT'].rank(ascending=False).astype(int)

xgc = df1[['id','label','team.name','player.id','player.name','possession.attack.xg','possession.id','type.primary','type.secondary']]
xgchold = xgc.drop_duplicates(subset='possession.id',keep='first')
xgchold = xgchold.rename(columns={'possession.attack.xg': 'Hold xG'})
xgchold = xgchold.groupby('team.name')['Hold xG'].agg('sum').reset_index()
xgchold = xgchold.sort_values(by='Hold xG',ascending=False)
xgchold['Hold xG rank'] = xgchold['Hold xG'].rank(ascending=False).astype(int)
xgc = xgc.merge(xgchold, on='team.name', how='left')

xgcspiller = xgc.groupby(['player.id','player.name','team.name','Hold xG'])['possession.attack.xg'].agg('sum').reset_index()
xgcspiller = xgcspiller[['player.id','player.name','team.name','possession.attack.xg','Hold xG']]
xgcspiller['xGCC'] = xgcspiller['possession.attack.xg'] / xgcspiller['Hold xG']
xgcspiller = xgcspiller.rename(columns={'possession.attack.xg': 'xGC'})
xgcspiller = xgcspiller.sort_values(by='xGCC',ascending=False)
xgcspiller['xGCC Rank'] = xgcspiller['xGCC'].rank(ascending=False).astype(int)

samlet = xgcspiller.merge(xT)
samlethold = xgchold.merge(xThold)
samlet = samlet[['player.name','team.name','xGC','Hold xG','xGCC','xGCC Rank','xT','xT Rank']]

fig = px.scatter(samlet, x='xGCC', y='xT', text='player.name', hover_name='player.name', title='xGCC vs xT')
fig.update_traces(textposition='top center')
col1,col2 = st.columns([2,2])
with col1:
    st.plotly_chart(fig)

fig = px.scatter(samlethold, x='Hold xG', y='xT', text='team.name', hover_name='team.name', title='Hold xG vs xT')
fig.update_traces(textposition='top center')

with col2:
    st.plotly_chart(fig)


col1,col2 = st.columns([3,2])
with col1:
    st.dataframe(samlet,use_container_width=True,hide_index=True)

with col2:
    st.dataframe(samlethold,hide_index=True)


col1,col2,col3 = st.columns(3)
with col1:
    st.dataframe(xThold,hide_index=True)
    st.dataframe(xgchold,hide_index=True)
with col2:
    st.dataframe(xTspiller,hide_index=True)
    st.dataframe(xgcspiller,hide_index=True)
with col3:
    st.dataframe(xTmodtager,hide_index=True)
   