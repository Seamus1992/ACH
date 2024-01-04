import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from mplsoccer.pitch import Pitch
import numpy as np
import streamlit as st
st.set_page_config(layout='wide')
df = pd.read_csv(r'C:\Users\SéamusPeareBartholdy\Documents\GitHub\AC-Horsens\xT\U19 Ligaen 23 24.csv')

hold = 'Horsens U19'
df = df[df['label'].str.contains(hold)]
df = df.sort_values(by='label')
valgtekamp = st.multiselect('Vælg kamp', df['label'].unique())
df.loc[df['player.id'] == 624663, 'player.name'] = 'Je. Beluli'
df.loc[df['pass.recipient.id'] == 624663, 'pass.recipient.name'] = 'Je. Beluli'

df1 = df.copy()
df = df[['id','matchId','label','date','matchPeriod','minute','shot.isGoal','type.primary','type.secondary','location.x','location.y','team.name','opponentTeam.name','player.id','player.name','pass.accurate','pass.endLocation.x','pass.endLocation.y','pass.recipient.id','pass.recipient.name','possession.id','possession.duration','possession.id','possession.eventsNumber','possession.eventIndex','possession.team.name','possession.attack.xg','carry.progression','carry.endLocation.x','carry.endLocation.y']]

df = df[df['label'].isin(valgtekamp)]
df = df[(df['pass.accurate'] ==True) | (df['carry.progression'] > 0)]
df = df[~df['type.primary'].str.contains('infraction')]
df = df[~df['type.primary'].str.contains('game_interruption')]
df = df[~df['type.primary'].str.contains('throw_in')]
df = df[~df['type.primary'].str.contains('free_kick')]
df = df[~df['type.primary'].str.contains('penalty')]
df = df[~df['type.primary'].str.contains('corner')]

df1 = df1[df1['label'].isin(valgtekamp)]
df1['possession.types'] = df1['possession.types'].astype(str)
df1 = df1[~df1['possession.types'].str.contains('set_piece_attack')]
df1 = df1[~df1['possession.types'].str.contains('throw_in')]
df1 = df1[~df1['possession.types'].str.contains('free_kick')]
df1 = df1[~df1['possession.types'].str.contains('corner')]


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

dfscore = pd.read_csv(r'C:\Users\SéamusPeareBartholdy\Documents\GitHub\AC-Horsens\xT\Zone scores.csv')

df = df.merge(dfscore[['Start Zone', 'Start zone score']], on='Start Zone', how='left')

# Merge 'End Zone' scores
df = df.merge(dfscore[['End Zone', 'End zone score']], on='End Zone', how='left')

df['xT'] = df['End zone score'] - df['Start zone score']
xThold = df.groupby(['team.name'])['xT'].agg('sum').reset_index()

with st.expander('Se xT model'):
    col1,col2 = st.columns(2)
    with col1:
        from PIL import Image
        image = Image.open('C:\Users\SéamusPeareBartholdy\Documents\GitHub\AC-Horsens\xT\xT zoner.png')
        st.image(image,'xT zoner')
    with col2:
        zoner = pd.read_csv(r'C:\Users\SéamusPeareBartholdy\Documents\GitHub\AC-Horsens\xT\Zone scores.csv')
        zoner = zoner[['Start Zone','Start zone score']]
        zoner = zoner.rename(columns={'Start Zone': 'Zone'})
        zoner = zoner.rename(columns={'Start zone score': 'Zone score'})

        st.dataframe(zoner,hide_index=True)
        st.write('xT udregnes som: zonen hvor pasning/dribling slutter - zone hvor pasning/dribling starter')
        st.write('Zonernes værdi er udregnet på baggrund af de seneste 8 sæsoner i 1. div og Superligaen med udgangspunkt i den gennemsnitlige værdi for en boldbesiddelse i zonen. Den er så vægtet efter hvor mange aktioner der går fra boldbesiddelsen i zonen til en afslutning. Jo flere jo lavere vægtning')

xgc = df1[['id','label','team.name','player.id','player.name','possession.attack.xg','possession.id','type.primary','type.secondary']]
xgchold = xgc.drop_duplicates(subset='possession.id',keep='last')
xgchold = xgchold.rename(columns={'possession.attack.xg': 'Hold xG i åbent spil'})
xgchold = xgchold.groupby('team.name')['Hold xG i åbent spil'].agg('sum').reset_index()
xgchold = xgchold.sort_values(by='Hold xG i åbent spil',ascending=False)
xgc = xgc.merge(xgchold, on='team.name', how='left')
xThold = xThold.merge(xgchold)
if hold in xThold['team.name'].values:
    hold_xG_open_play = xThold.loc[xThold['team.name'] == hold, 'Hold xG i åbent spil'].values[0]
    hold_xT = xThold.loc[xThold['team.name'] == hold, 'xT'].values[0]

    num_teams = len(xThold['team.name'].unique())    
    if num_teams > 1:
        xThold.loc[xThold['team.name'] == hold, 'Hold xG i åbent spil'] = hold_xG_open_play / (num_teams - 1)
        xThold.loc[xThold['team.name'] == hold,'xT'] = hold_xT/(num_teams-1)
    else:
        st.write("There is only one team in the dataset. Unable to calculate.")

st.dataframe(xThold,hide_index=True)
    


xgc = xgc[xgc['team.name'] == hold]

xgcspiller = xgc.groupby(['player.id','player.name','team.name','Hold xG i åbent spil'])['possession.attack.xg'].agg('sum').reset_index()
xgcspiller = xgcspiller[['player.name','team.name','possession.attack.xg','Hold xG i åbent spil']]
xgcspiller['xGCC'] = xgcspiller['possession.attack.xg'] / xgcspiller['Hold xG i åbent spil']
xgcspiller = xgcspiller.rename(columns={'possession.attack.xg': 'xGC'})
xgcspiller = xgcspiller.sort_values(by='xGCC',ascending=False)
xgcspiller = xgcspiller[xgcspiller['team.name'] == hold]


col1,col2 = st.columns(2)
with col1:  
    xTspiller = df.groupby(['player.name','team.name'])['xT'].agg('sum').reset_index()
    xTspiller = xTspiller[xTspiller['team.name'] == hold]
    xTspiller = xTspiller.sort_values(by='xT', ascending=False)
    st.dataframe(xTspiller,hide_index=True)
samlet = xgcspiller.merge(xTspiller)
with col2:
    st.dataframe(xgcspiller,hide_index=True)
    
    
team_passes = (df1['type.primary'] == 'pass') & (df1['team.name'] == hold) & (df1['type.secondary'] != "Throw-in")
team_passes = df1.loc[team_passes, ['location.x', 'location.y', 'pass.endLocation.x', 'pass.endLocation.y', 'player.name','player.id','pass.recipient.name','pass.recipient.id','pass.accurate']]
players = team_passes[['player.id','player.name']]
players = players.drop_duplicates()
pitch = Pitch(pitch_type='wyscout',line_color='white', pitch_color='#02540b', pad_top=20)
fig, axs = pitch.grid(ncols=4, nrows=5, grid_height=0.85, title_height=0.00, axis=False, title_space=0.04, endnote_space=0.01)
plt.figure()
for name, ax in zip(players['player.name'], axs['pitch'].flat[:len(players)]):
    player_df = team_passes.loc[team_passes["player.name"] == name]
    xT_score = xTspiller.loc[xTspiller["player.name"] == name, "xT"].values[0]  # Fetch xT score for the player
    ax.text(60, -10, f"{name} ({xT_score:.3f} xT)", ha='center', va='center', fontsize=8, color='white')

    for i in player_df.index:
        x = player_df['location.x'][i]
        y = player_df['location.y'][i]
        dx = player_df['pass.endLocation.x'][i] - player_df['location.x'][i]
        dy = player_df['pass.endLocation.y'][i] - player_df['location.y'][i]
        if player_df['pass.accurate'][i]:  # Changed df to player_df here
            ax.arrow(x, y, dx, dy, color='#0dff00', length_includes_head=True, head_width=1, head_length=0.8)
            pitch.scatter(player_df['location.x'][i], player_df['location.y'][i], color='#0dff00', ax=ax)
        else:
            ax.arrow(x, y, dx, dy, color='red', length_includes_head=True, head_width=1, head_length=0.8)
            pitch.scatter(player_df['location.x'][i], player_df['location.y'][i], color='red', ax=ax)


st.title('Pasninger')
st.pyplot(fig)

team_passes = (df1['type.primary'] == 'pass') & (df1['team.name'] == hold) & (df1['type.secondary'] != "Throw-in") & (df1['pass.accurate'] == True)
team_passes = df1.loc[team_passes, ['location.x', 'location.y', 'pass.endLocation.x', 'pass.endLocation.y','player.name','player.id','pass.recipient.name','pass.recipient.id','pass.accurate']]
players = players.rename(columns={'player.id': 'pass.recipient.id', 'player.name': 'pass.recipient.name'})
players = players.drop_duplicates()
players = players.dropna()
pitch = Pitch(pitch_type='wyscout',line_color='white', pitch_color='#02540b', pad_top=20)
fig, axs = pitch.grid(ncols=4, nrows=5, grid_height=0.85, title_height=0.00, axis=False, title_space=0.04, endnote_space=0.01)
plt.figure()
for name, ax in zip(players['pass.recipient.name'], axs['pitch'].flat[:len(players)]):
    player_df = team_passes.loc[team_passes["pass.recipient.name"] == name]
    xT_score = xTspiller.loc[xTspiller["player.name"] == name, "xT"].values[0]  # Fetch xT score for the player
    ax.text(60, -10, f"{name} ({xT_score:.3f} xT)", ha='center', va='center', fontsize=8, color='white')

    for i in player_df.index:
        x = player_df['location.x'][i]
        y = player_df['location.y'][i]
        dx = player_df['pass.endLocation.x'][i] - player_df['location.x'][i]
        dy = player_df['pass.endLocation.y'][i] - player_df['location.y'][i]
        if player_df['pass.accurate'][i]:  # Changed df to player_df here
            ax.arrow(x, y, dx, dy, color='#0dff00', length_includes_head=True, head_width=1, head_length=0.8)
            pitch.scatter(player_df['pass.endLocation.x'][i], player_df['pass.endLocation.y'][i], color='#0dff00', ax=ax)
        else:
            ax.arrow(dx, dy, x, y, color='red', length_includes_head=True, head_width=1, head_length=0.8)
            pitch.scatter(player_df['pass.endLocation.x'][i], player_df['pass.endLocation.y'][i], color='red', ax=ax)

st.title('Modtagne pasninger')
st.pyplot(fig)

col1,col2,col3 = st.columns(3)
#Pasningsnetværk
    # Check for the index of the first substitution
    
with col1:
    passes = (
        (df['type.primary'] == 'pass') &
        (df['team.name'] == hold) &
        (df['pass.accurate'] == True) &
        (df['type.secondary'] != "Throw-in"))    
    # Select necessary columns
    pass_df = df.loc[passes, ['location.x', 'location.y', 'pass.endLocation.x', 'pass.endLocation.y', 'player.name', 'pass.recipient.name']]
    pass_df = pass_df[(pass_df['location.x'] < 33)]
    # Adjusting that only the surname of a player is presented.
    pass_df["player.name"] = pass_df["player.name"].apply(lambda x: str(x).split()[-1])
    pass_df["pass.recipient.name"] = pass_df["pass.recipient.name"].apply(lambda x: str(x).split()[-1])

    scatter_df = pd.DataFrame()
    for i, name in enumerate(pass_df["player.name"].unique()):
        pass_x = pass_df.loc[pass_df["player.name"] == name]["location.x"].to_numpy()
        rec_x = pass_df.loc[pass_df["pass.recipient.name"] == name]["pass.endLocation.x"].to_numpy()
        pass_y = pass_df.loc[pass_df["player.name"] == name]["location.y"].to_numpy()
        rec_y = pass_df.loc[pass_df["pass.recipient.name"] == name]["pass.endLocation.y"].to_numpy()
        scatter_df.at[i, "player.name"] = name
        # Make sure that x and y location for each circle representing the player is the average of passes and receptions
        scatter_df.at[i, "x"] = np.mean(np.concatenate([pass_x, rec_x]))
        scatter_df.at[i, "y"] = np.mean(np.concatenate([pass_y, rec_y]))
        # Calculate number of passes
        scatter_df.at[i, "no"] = pass_df.loc[pass_df["player.name"] == name].count().iloc[0]
        
        # Adjust the size of a circle so that the player who made more passes
    scatter_df['marker_size'] = (scatter_df["no"] / scatter_df["no"].max() * 1500)

    # Counting passes between players
    pass_df["pair_key"] = pass_df.apply(lambda x: "_".join(sorted([x["player.name"], x["pass.recipient.name"]])), axis=1)
    lines_df = pass_df.groupby(["pair_key"]).size().reset_index(name='pass_count')
    # Setting a threshold. You can try to investigate how it changes when you change it.
    lines_df = lines_df[lines_df['pass_count'] > 2]

    # Plot once again pitch and vertices
    pitch = Pitch(pitch_type='wyscout',line_color='white', pitch_color='#02540b')
    fig, ax = pitch.grid(grid_height=0.9, title_height=0.06, axis=False,
                        endnote_height=0.04, title_space=0, endnote_space=0)
    pitch.scatter(scatter_df.x, scatter_df.y, s=scatter_df.marker_size, color='yellow', edgecolors='black', linewidth=1, alpha=1, ax=ax["pitch"], zorder=3)
    for i, row in scatter_df.iterrows():
        pitch.annotate(row["player.name"], xy=(row.x, row.y), c='black', va='center', ha='center', weight="bold", size=12, ax=ax["pitch"], zorder=3)
    for i, row in lines_df.iterrows():
        player1 = row["pair_key"].split("_")[0]
        player2 = row['pair_key'].split("_")[1]

        # Check if data exists for player1 and player2
        if player1 in scatter_df['player.name'].values and player2 in scatter_df['player.name'].values:
            player1_x = scatter_df.loc[scatter_df["player.name"] == player1]['x'].iloc[0]
            player1_y = scatter_df.loc[scatter_df["player.name"] == player1]['y'].iloc[0]
            player2_x = scatter_df.loc[scatter_df["player.name"] == player2]['x'].iloc[0]
            player2_y = scatter_df.loc[scatter_df["player.name"] == player2]['y'].iloc[0]

            num_passes = row["pass_count"]
            line_width = (num_passes / lines_df['pass_count'].max() * 10)
            pitch.lines(player1_x, player1_y, player2_x, player2_y,
                        alpha=1, lw=line_width, zorder=2, color="yellow", ax=ax["pitch"])
    st.pyplot(fig)
with col2:
    passes = (
        (df['type.primary'] == 'pass') &
        (df['team.name'] == hold) &
        (df['pass.accurate'] == True) &
        (df['type.secondary'] != "Throw-in"))    
    # Select necessary columns
    pass_df = df.loc[passes, ['location.x', 'location.y', 'pass.endLocation.x', 'pass.endLocation.y', 'player.name', 'pass.recipient.name']]
    pass_df = pass_df[(pass_df['location.x'] > 33) & pass_df['location.x'] < 66]
    # Adjusting that only the surname of a player is presented.
    pass_df["player.name"] = pass_df["player.name"].apply(lambda x: str(x).split()[-1])
    pass_df["pass.recipient.name"] = pass_df["pass.recipient.name"].apply(lambda x: str(x).split()[-1])

    scatter_df = pd.DataFrame()
    for i, name in enumerate(pass_df["player.name"].unique()):
        pass_x = pass_df.loc[pass_df["player.name"] == name]["location.x"].to_numpy()
        rec_x = pass_df.loc[pass_df["pass.recipient.name"] == name]["pass.endLocation.x"].to_numpy()
        pass_y = pass_df.loc[pass_df["player.name"] == name]["location.y"].to_numpy()
        rec_y = pass_df.loc[pass_df["pass.recipient.name"] == name]["pass.endLocation.y"].to_numpy()
        scatter_df.at[i, "player.name"] = name
        # Make sure that x and y location for each circle representing the player is the average of passes and receptions
        scatter_df.at[i, "x"] = np.mean(np.concatenate([pass_x, rec_x]))
        scatter_df.at[i, "y"] = np.mean(np.concatenate([pass_y, rec_y]))
        # Calculate number of passes
        scatter_df.at[i, "no"] = pass_df.loc[pass_df["player.name"] == name].count().iloc[0]
        
        # Adjust the size of a circle so that the player who made more passes
    scatter_df['marker_size'] = (scatter_df["no"] / scatter_df["no"].max() * 1500)

    # Counting passes between players
    pass_df["pair_key"] = pass_df.apply(lambda x: "_".join(sorted([x["player.name"], x["pass.recipient.name"]])), axis=1)
    lines_df = pass_df.groupby(["pair_key"]).size().reset_index(name='pass_count')
    # Setting a threshold. You can try to investigate how it changes when you change it.
    lines_df = lines_df[lines_df['pass_count'] > 2]

    # Plot once again pitch and vertices
    pitch = Pitch(pitch_type='wyscout',line_color='white', pitch_color='#02540b')
    fig, ax = pitch.grid(grid_height=0.9, title_height=0.06, axis=False,
                        endnote_height=0.04, title_space=0, endnote_space=0)
    pitch.scatter(scatter_df.x, scatter_df.y, s=scatter_df.marker_size, color='yellow', edgecolors='black', linewidth=1, alpha=1, ax=ax["pitch"], zorder=3)
    for i, row in scatter_df.iterrows():
        pitch.annotate(row["player.name"], xy=(row.x, row.y), c='black', va='center', ha='center', weight="bold", size=12, ax=ax["pitch"], zorder=3)
    for i, row in lines_df.iterrows():
        player1 = row["pair_key"].split("_")[0]
        player2 = row['pair_key'].split("_")[1]

        # Check if data exists for player1 and player2
        if player1 in scatter_df['player.name'].values and player2 in scatter_df['player.name'].values:
            player1_x = scatter_df.loc[scatter_df["player.name"] == player1]['x'].iloc[0]
            player1_y = scatter_df.loc[scatter_df["player.name"] == player1]['y'].iloc[0]
            player2_x = scatter_df.loc[scatter_df["player.name"] == player2]['x'].iloc[0]
            player2_y = scatter_df.loc[scatter_df["player.name"] == player2]['y'].iloc[0]

            num_passes = row["pass_count"]
            line_width = (num_passes / lines_df['pass_count'].max() * 10)
            pitch.lines(player1_x, player1_y, player2_x, player2_y,
                        alpha=1, lw=line_width, zorder=2, color="yellow", ax=ax["pitch"])
    st.pyplot(fig)

with col3:
    passes = (
        (df['type.primary'] == 'pass') &
        (df['team.name'] == hold) &
        (df['pass.accurate'] == True) &
        (df['type.secondary'] != "Throw-in"))    
    # Select necessary columns
    pass_df = df.loc[passes, ['location.x', 'location.y', 'pass.endLocation.x', 'pass.endLocation.y', 'player.name', 'pass.recipient.name']]
    pass_df = pass_df[pass_df['location.x'] > 66]
    # Adjusting that only the surname of a player is presented.
    pass_df["player.name"] = pass_df["player.name"].apply(lambda x: str(x).split()[-1])
    pass_df["pass.recipient.name"] = pass_df["pass.recipient.name"].apply(lambda x: str(x).split()[-1])

    scatter_df = pd.DataFrame()
    for i, name in enumerate(pass_df["player.name"].unique()):
        pass_x = pass_df.loc[pass_df["player.name"] == name]["location.x"].to_numpy()
        rec_x = pass_df.loc[pass_df["pass.recipient.name"] == name]["pass.endLocation.x"].to_numpy()
        pass_y = pass_df.loc[pass_df["player.name"] == name]["location.y"].to_numpy()
        rec_y = pass_df.loc[pass_df["pass.recipient.name"] == name]["pass.endLocation.y"].to_numpy()
        scatter_df.at[i, "player.name"] = name
        # Make sure that x and y location for each circle representing the player is the average of passes and receptions
        scatter_df.at[i, "x"] = np.mean(np.concatenate([pass_x, rec_x]))
        scatter_df.at[i, "y"] = np.mean(np.concatenate([pass_y, rec_y]))
        # Calculate number of passes
        scatter_df.at[i, "no"] = pass_df.loc[pass_df["player.name"] == name].count().iloc[0]
        
        # Adjust the size of a circle so that the player who made more passes
    scatter_df['marker_size'] = (scatter_df["no"] / scatter_df["no"].max() * 1500)

    # Counting passes between players
    pass_df["pair_key"] = pass_df.apply(lambda x: "_".join(sorted([x["player.name"], x["pass.recipient.name"]])), axis=1)
    lines_df = pass_df.groupby(["pair_key"]).size().reset_index(name='pass_count')
    # Setting a threshold. You can try to investigate how it changes when you change it.
    lines_df = lines_df[lines_df['pass_count'] > 2]

    # Plot once again pitch and vertices
    pitch = Pitch(pitch_type='wyscout',line_color='white', pitch_color='#02540b')
    fig, ax = pitch.grid(grid_height=0.9, title_height=0.06, axis=False,
                        endnote_height=0.04, title_space=0, endnote_space=0)
    pitch.scatter(scatter_df.x, scatter_df.y, s=scatter_df.marker_size, color='yellow', edgecolors='black', linewidth=1, alpha=1, ax=ax["pitch"], zorder=3)
    for i, row in scatter_df.iterrows():
        pitch.annotate(row["player.name"], xy=(row.x, row.y), c='black', va='center', ha='center', weight="bold", size=12, ax=ax["pitch"], zorder=3)
    for i, row in lines_df.iterrows():
        player1 = row["pair_key"].split("_")[0]
        player2 = row['pair_key'].split("_")[1]

        # Check if data exists for player1 and player2
        if player1 in scatter_df['player.name'].values and player2 in scatter_df['player.name'].values:
            player1_x = scatter_df.loc[scatter_df["player.name"] == player1]['x'].iloc[0]
            player1_y = scatter_df.loc[scatter_df["player.name"] == player1]['y'].iloc[0]
            player2_x = scatter_df.loc[scatter_df["player.name"] == player2]['x'].iloc[0]
            player2_y = scatter_df.loc[scatter_df["player.name"] == player2]['y'].iloc[0]

            num_passes = row["pass_count"]
            line_width = (num_passes / lines_df['pass_count'].max() * 10)
            pitch.lines(player1_x, player1_y, player2_x, player2_y,
                        alpha=1, lw=line_width, zorder=2, color="yellow", ax=ax["pitch"])
    st.pyplot(fig)
    
passes = (
    (df['type.primary'] == 'pass') &
    (df['team.name'] == hold) &
    (df['pass.accurate'] == True) &
    (df['type.secondary'] != "Throw-in"))    
    # Select necessary columns
pass_df = df.loc[passes, ['location.x', 'location.y', 'pass.endLocation.x', 'pass.endLocation.y', 'player.name', 'pass.recipient.name']]
    # Adjusting that only the surname of a player is presented.
pass_df["player.name"] = pass_df["player.name"].apply(lambda x: str(x).split()[-1])
pass_df["pass.recipient.name"] = pass_df["pass.recipient.name"].apply(lambda x: str(x).split()[-1])

scatter_df = pd.DataFrame()
for i, name in enumerate(pass_df["player.name"].unique()):
    pass_x = pass_df.loc[pass_df["player.name"] == name]["location.x"].to_numpy()
    rec_x = pass_df.loc[pass_df["pass.recipient.name"] == name]["pass.endLocation.x"].to_numpy()
    pass_y = pass_df.loc[pass_df["player.name"] == name]["location.y"].to_numpy()
    rec_y = pass_df.loc[pass_df["pass.recipient.name"] == name]["pass.endLocation.y"].to_numpy()
    scatter_df.at[i, "player.name"] = name
    # Make sure that x and y location for each circle representing the player is the average of passes and receptions
    scatter_df.at[i, "x"] = np.mean(np.concatenate([pass_x, rec_x]))
    scatter_df.at[i, "y"] = np.mean(np.concatenate([pass_y, rec_y]))
    # Calculate number of passes
    scatter_df.at[i, "no"] = pass_df.loc[pass_df["player.name"] == name].count().iloc[0]
        
    # Adjust the size of a circle so that the player who made more passes
scatter_df['marker_size'] = (scatter_df["no"] / scatter_df["no"].max() * 1500)

    # Counting passes between players
pass_df["pair_key"] = pass_df.apply(lambda x: "_".join(sorted([x["player.name"], x["pass.recipient.name"]])), axis=1)
lines_df = pass_df.groupby(["pair_key"]).size().reset_index(name='pass_count')
# Setting a threshold. You can try to investigate how it changes when you change it.
lines_df = lines_df[lines_df['pass_count'] > 2]

    # Plot once again pitch and vertices
pitch = Pitch(pitch_type='wyscout',line_color='white', pitch_color='#02540b')
fig, ax = pitch.grid(grid_height=0.9, title_height=0.06, axis=False,
                    endnote_height=0.04, title_space=0, endnote_space=0)
pitch.scatter(scatter_df.x, scatter_df.y, s=scatter_df.marker_size, color='yellow', edgecolors='black', linewidth=1, alpha=1, ax=ax["pitch"], zorder=3)
for i, row in scatter_df.iterrows():
    pitch.annotate(row["player.name"], xy=(row.x, row.y), c='black', va='center', ha='center', weight="bold", size=12, ax=ax["pitch"], zorder=3)
for i, row in lines_df.iterrows():
    player1 = row["pair_key"].split("_")[0]
    player2 = row['pair_key'].split("_")[1]

    # Check if data exists for player1 and player2
    if player1 in scatter_df['player.name'].values and player2 in scatter_df['player.name'].values:
        player1_x = scatter_df.loc[scatter_df["player.name"] == player1]['x'].iloc[0]
        player1_y = scatter_df.loc[scatter_df["player.name"] == player1]['y'].iloc[0]
        player2_x = scatter_df.loc[scatter_df["player.name"] == player2]['x'].iloc[0]
        player2_y = scatter_df.loc[scatter_df["player.name"] == player2]['y'].iloc[0]
        num_passes = row["pass_count"]
        line_width = (num_passes / lines_df['pass_count'].max() * 10)
        pitch.lines(player1_x, player1_y, player2_x, player2_y,
                    alpha=1, lw=line_width, zorder=2, color="yellow", ax=ax["pitch"])
st.pyplot(fig)