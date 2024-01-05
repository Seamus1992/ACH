import pandas as pd
import streamlit as st
import json
from pandas import json_normalize
import ast
import numpy as np
from dateutil import parser
import plotly.express as px
st.set_page_config(layout = 'wide')

def U15_liga ():
    col1,col2 = st.columns(2)
    with col1:
        samlettid = st.number_input('Minutter i sæsonen')
    with col2:    
        tidprkamp = st.number_input('Minutter pr. kamp')
    df = pd.read_csv(r'Individuelt dashboard/Individuelt dashboard U15.csv')
    df.rename(columns={'playerId': 'Player id'}, inplace=True)
    df = df.astype(str)
    dfevents = pd.read_csv('U15 eventdata alle.csv',low_memory=False)
    dfevents = dfevents[['Player id','Player name','team_name','label','date','matchId']]
    dfspillernavn = df[['Player id','matchId','positions','average','percent','total']]
    dfspillernavn = dfspillernavn.astype(str)
    dfevents['Player id'] = dfevents['Player id'].astype(str)
    dfevents['matchId'] = dfevents['matchId'].astype(str)
    df = dfspillernavn.merge(dfevents)

    df['Player&matchId'] = df['Player id'] + df['matchId']
    df['Player&matchId'] = df['Player&matchId'].drop_duplicates(keep='first')
    df = df.dropna()
    df = df[['Player id','Player name','team_name','matchId','label','date','positions','average','percent','total']]

    #df = df.set_index('Player id')

    data = df['positions']
    df1 = pd.DataFrame(data)
    # Funktion, der ekstraherer navne og koder fra strengdata og opretter en ny kolonne med disse værdier
    def extract_positions(data):
        positions_list = ast.literal_eval(data) # Konverterer strengen til en liste af ordbøger
        names = [pos['position']['name'] for pos in positions_list]
        codes = [pos['position']['code'] for pos in positions_list]
        return pd.Series({'position_names': names, 'position_codes': codes})

    # Anvender funktionen på kolonnen og tilføjer resultaterne som nye kolonner til dataframe
    df1[['position_names', 'position_codes']] = df1['positions'].apply(extract_positions)

    df = pd.merge(df,df1,left_index=True, right_index=True)
    df = df.set_index('Player id')
    df = df.drop(columns=['positions_x'])
    df = df.drop(columns=['positions_y'])
    df = df[['Player name','team_name','matchId','label','date','position_names','position_codes','average','percent','total']]
    df = df.rename(columns={'team_name':'Team name'})
    df['percent'] = df['percent'].apply(lambda x: ast.literal_eval(x))

    # Create a new dataframe with the columns as the dictionary keys and the values as a list
    new_df = pd.DataFrame(df['percent'].to_list(), index=df.index).add_prefix('percent_')

    # Concatenate the new dataframe with the original dataframe
    df = pd.concat([df, new_df], axis=1)

    # Drop the original 'percent' column
    df = df.drop('percent', axis=1)

    df['total'] = df['total'].apply(lambda x: ast.literal_eval(x))

    # Create a new dataframe with the columns as the dictionary keys and the values as a list
    new_df = pd.DataFrame(df['total'].to_list(), index=df.index).add_prefix('total_')

    # Concatenate the new dataframe with the original dataframe
    df = pd.concat([df, new_df], axis=1)

    # Drop the original 'percent' column
    df = df.drop('total', axis=1)

    df['average'] = df['average'].apply(lambda x: ast.literal_eval(x))

    # Create a new dataframe with the columns as the dictionary keys and the values as a list
    new_df = pd.DataFrame(df['average'].to_list(), index=df.index).add_prefix('average_')

    # Concatenate the new dataframe with the original dataframe
    df = pd.concat([df, new_df], axis=1)


    # Drop the original 'percent' column
    df = df.drop('average', axis=1)
    df['position_codes'] = df['position_codes'].astype(str)
    #df['date'] = df['date'].astype(str)
    #df['date'] = df['date'].apply(lambda x: parser.parse(x))

    # Sort the dataframe by the 'date' column
    #df = df.sort_values(by='date',ascending=False)

    # Format the 'date' column to day-month-year format
    #df['date'] = df['date'].apply(lambda x: x.strftime('%d-%m-%Y'))
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date',ascending=False)

    df_backs = df[df['position_codes'].str.contains('|'.join(['lb', 'rb']))]
    df_backs = df_backs[df_backs['total_minutesOnField'] >= tidprkamp]
    df_backsminutter = df_backs[['Player name','Team name','total_minutesOnField']]
    df_backsminutter = df_backsminutter.groupby(['Player id']).sum(numeric_only=True)
    df_backsminutter = df_backsminutter[df_backsminutter['total_minutesOnField'] >= samlettid]

    df_Stoppere = df[df['position_codes'].str.contains('|'.join(['cb']))]
    df_Stoppere = df_Stoppere[df_Stoppere['total_minutesOnField'] >= tidprkamp]
    df_stoppereminutter = df_Stoppere[['Player name','Team name','total_minutesOnField']]
    df_stoppereminutter = df_stoppereminutter.groupby(['Player id']).sum(numeric_only=True)
    df_stoppereminutter = df_stoppereminutter[df_stoppereminutter['total_minutesOnField'] >= samlettid]

    df_Centrale_midt = df[df['position_codes'].str.contains('|'.join(['cm','amf','dmf']))]
    df_Centrale_midt = df_Centrale_midt[df_Centrale_midt['total_minutesOnField'] >= tidprkamp]
    df_centraleminutter = df_Centrale_midt[['Player name','Team name','total_minutesOnField']]
    df_centraleminutter = df_centraleminutter.groupby(['Player id']).sum(numeric_only=True)
    df_centraleminutter = df_centraleminutter[df_centraleminutter['total_minutesOnField'] >= samlettid]

    df_Kanter = df[df['position_codes'].str.contains('|'.join(['rw','lw','ramf','lamf']))]
    df_Kanter = df_Kanter[df_Kanter['total_minutesOnField'] >=tidprkamp]
    df_kanterminutter = df_Kanter[['Player name','Team name','total_minutesOnField']]
    df_kanterminutter = df_kanterminutter.groupby(['Player id']).sum(numeric_only=True)
    df_kanterminutter = df_kanterminutter[df_kanterminutter['total_minutesOnField'] >=samlettid]


    df_Angribere = df[df['position_codes'].str.contains('|'.join(['cf','ss']))]
    df_Angribere = df_Angribere[df_Angribere['total_minutesOnField'] >= tidprkamp]
    df_angribereminutter = df_Angribere[['Player name','Team name','total_minutesOnField']]
    df_angribereminutter = df_angribereminutter.groupby(['Player id']).sum(numeric_only=True)
    df_angribereminutter = df_angribereminutter[df_angribereminutter['total_minutesOnField'] >= samlettid]


    df_backs = pd.merge(df_backsminutter,df_backs,on=('Player id'))
    df_backs = df_backs[df_backs['total_minutesOnField_y'] >=tidprkamp]

    df_backs['Accurate crosses score'] = pd.qcut(df_backs['percent_successfulCrosses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_backs['Number of crosses score'] = pd.qcut(df_backs['average_crosses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_backs['XA score'] = pd.qcut(df_backs['average_xgAssist'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_backs['Passes to final third score'] = pd.qcut(df_backs['average_successfulPassesToFinalThird'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_backs['Successful dribbles score'] = pd.qcut(df_backs['percent_newSuccessfulDribbles'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_backs['Defensive duels won score'] = pd.qcut(df_backs['percent_newDefensiveDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_backs['Progressive runs score'] = pd.qcut(df_backs['average_progressiveRun'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_backs['Offensive duels won score'] = pd.qcut(df_backs['percent_newOffensiveDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_backs['Accelerations score'] = pd.qcut(df_backs['average_accelerations'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_backs['Duels won score'] = pd.qcut(df_backs['percent_newDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_backs['Interceptions score'] = pd.qcut(df_backs['average_interceptions'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_backs['Successful defensive actions score'] = pd.qcut(df_backs['average_successfulDefensiveAction'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_backssæsonen = df_backs[['label','Player name','Team name','total_minutesOnField_x','total_minutesOnField_y','Number of crosses score','Accurate crosses score','XA score','Passes to final third score','Successful dribbles score','Defensive duels won score','Progressive runs score','Offensive duels won score','Accelerations score','Duels won score','Interceptions score','Successful defensive actions score']]
    df_backssæsonen.rename(columns={'total_minutesOnField_x':'Total minutes'},inplace=True)
    df_backssæsonen = df_backssæsonen.groupby(['Player name','Team name','Total minutes','label']).mean(numeric_only=True)

    df_backssæsonen['Indlægsstærk'] = (df_backssæsonen['Number of crosses score'] + df_backssæsonen['Accurate crosses score'] + df_backssæsonen['XA score'] + df_backssæsonen['Passes to final third score'])/4
    df_backssæsonen['1v1 færdigheder'] = (df_backssæsonen['Successful dribbles score'] + df_backssæsonen['Defensive duels won score'] + df_backssæsonen['Progressive runs score'] + df_backssæsonen['Offensive duels won score'] + df_backssæsonen['Accelerations score'] + df_backssæsonen['Duels won score'])/6
    df_backssæsonen['Spilintelligens defensivt'] = (df_backssæsonen['Interceptions score'] + df_backssæsonen['Successful defensive actions score'] + df_backssæsonen['Duels won score'] + df_backssæsonen['Defensive duels won score'])/4
    df_backssæsonen['Fart'] = (df_backssæsonen['Successful dribbles score'] + df_backssæsonen['Progressive runs score'] + df_backssæsonen['Offensive duels won score'] + df_backssæsonen['Accelerations score'])/4
    df_backssæsonen ['Samlet'] = (df_backssæsonen['Indlægsstærk'] + df_backssæsonen['1v1 færdigheder'] + df_backssæsonen['Spilintelligens defensivt'] + df_backssæsonen['Fart'])/4

    df_backssæsonen = df_backssæsonen[['Indlægsstærk','1v1 færdigheder','Spilintelligens defensivt','Fart','Samlet']]
    df_backssæsonen = df_backssæsonen.round(3).astype(float)
    df_backssæsonen = df_backssæsonen.sort_values(by='Samlet',ascending=False)
    
    with st.expander('Backs kamp for kamp'):
        st.write(df_backssæsonen)
    df_backssæsonen = df_backssæsonen.reset_index()
    df_backssæsonen = df_backssæsonen.drop('label',axis=1)
    df_backssæsonen = df_backssæsonen.groupby(['Player name','Team name','Total minutes']).mean(numeric_only=True)
    df_backssæsonen = df_backssæsonen.sort_values(by='Samlet',ascending=False)
    with st.expander('Backs'):
        st.dataframe(df_backssæsonen)
       
    df_Stoppere = pd.merge(df_stoppereminutter,df_Stoppere,on=('Player id'))
    df_Stoppere = df_Stoppere[df_Stoppere['total_minutesOnField_y'] >=tidprkamp]
    
    df_Stoppere['Accurate passes score'] = pd.qcut(df_Stoppere['percent_successfulPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Accurate long passes score'] = pd.qcut(df_Stoppere['percent_successfulLongPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Forward passes score'] = pd.qcut(df_Stoppere['average_successfulForwardPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Accurate forward passes score'] = pd.qcut(df_Stoppere['percent_successfulForwardPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Accurate progressive passes score'] = pd.qcut(df_Stoppere['percent_successfulProgressivePasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Accurate vertical passes score'] = pd.qcut(df_Stoppere['percent_successfulVerticalPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Interceptions score'] = pd.qcut(df_Stoppere['average_interceptions'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Succesful defensive actions score'] = pd.qcut(df_Stoppere['average_successfulDefensiveAction'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Shots blocked score'] = pd.qcut(df_Stoppere['average_shotsBlocked'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Defensive duels won score'] = pd.qcut(df_Stoppere['average_newDefensiveDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Defensive duels won % score'] = pd.qcut(df_Stoppere['percent_newDefensiveDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Accurate passes to final third'] = pd.qcut(df_Stoppere['percent_successfulPassesToFinalThird'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Accurate through passes'] = pd.qcut(df_Stoppere['percent_successfulThroughPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Vertical passes'] = pd.qcut(df_Stoppere['average_successfulVerticalPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Through passes'] = pd.qcut(df_Stoppere['average_successfulThroughPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Passes to final third'] = pd.qcut(df_Stoppere['average_successfulPassesToFinalThird'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Progressive runs'] = pd.qcut(df_Stoppere['average_progressiveRun'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Offensive duels won %'] = pd.qcut(df_Stoppere['percent_newOffensiveDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Successful dribbles %'] = pd.qcut(df_Stoppere['percent_newSuccessfulDribbles'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Progressive passes score'] = pd.qcut(df_Stoppere['average_successfulProgressivePasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Aerial duels won score'] = pd.qcut(df_Stoppere['average_fieldAerialDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Aerial duels won % score'] = pd.qcut(df_Stoppere['percent_aerialDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)

    df_Stopperesæsonen = df_Stoppere[['label','Player name','Team name','total_minutesOnField_x','total_minutesOnField_y','Accurate passes score','Accurate long passes score','Forward passes score','Accurate forward passes score','Accurate progressive passes score','Accurate vertical passes score','Interceptions score','Succesful defensive actions score','Shots blocked score','Defensive duels won score','Defensive duels won % score','Accurate passes to final third','Accurate through passes','Vertical passes','Through passes','Passes to final third','Progressive passes score','Aerial duels won score','Aerial duels won % score','Progressive runs','Offensive duels won %','Successful dribbles %']]
    df_Stopperesæsonen.rename(columns={'total_minutesOnField_x':'Total minutes'},inplace=True)
    df_Stopperesæsonen = df_Stopperesæsonen.groupby(['Player name','Team name','Total minutes','label']).mean(numeric_only=True)
    df_Stopperesæsonen['Pasningssikker'] = (df_Stopperesæsonen['Accurate passes score'] + df_Stopperesæsonen['Accurate long passes score'] + df_Stopperesæsonen['Forward passes score'] + df_Stopperesæsonen['Accurate forward passes score'] + df_Stopperesæsonen['Accurate progressive passes score'] + df_Stopperesæsonen['Accurate vertical passes score'])/6
    df_Stopperesæsonen['Spilintelligens defensivt'] = (df_Stopperesæsonen['Interceptions score'] + df_Stopperesæsonen['Succesful defensive actions score'] + df_Stopperesæsonen['Shots blocked score'] + df_Stopperesæsonen['Succesful defensive actions score'] + df_Stopperesæsonen['Defensive duels won % score']) /5
    df_Stopperesæsonen['Spilintelligens offensivt'] = (df_Stopperesæsonen['Forward passes score'] + df_Stopperesæsonen['Accurate forward passes score'] + df_Stopperesæsonen['Accurate passes to final third'] + df_Stopperesæsonen['Passes to final third'] + df_Stopperesæsonen['Accurate progressive passes score'] + df_Stopperesæsonen['Progressive passes score'] + df_Stopperesæsonen['Through passes'] + df_Stopperesæsonen['Accurate through passes']+ df_Stopperesæsonen['Progressive runs'] + df_Stopperesæsonen['Offensive duels won %'] + df_Stopperesæsonen['Successful dribbles %'])/11
    df_Stopperesæsonen['Nærkamps- og duelstærk'] = (df_Stopperesæsonen['Defensive duels won % score'] + df_Stopperesæsonen['Aerial duels won % score'] + df_Stopperesæsonen['Defensive duels won % score'])/3
    df_Stopperesæsonen['Samlet'] = (df_Stopperesæsonen['Pasningssikker'] + df_Stopperesæsonen['Spilintelligens defensivt'] + df_Stopperesæsonen['Spilintelligens offensivt'] + df_Stopperesæsonen['Nærkamps- og duelstærk'])/4

    df_Stopperesæsonen = df_Stopperesæsonen[['Pasningssikker','Spilintelligens defensivt','Spilintelligens offensivt','Nærkamps- og duelstærk','Samlet']]
    df_Stopperesæsonen = df_Stopperesæsonen.sort_values(by='Samlet',ascending=False)

    with st.expander('Stoppere kamp for kamp'):
        st.write(df_Stopperesæsonen)
    df_Stopperesæsonen = df_Stopperesæsonen.reset_index()
    df_Stopperesæsonen = df_Stopperesæsonen.drop('label',axis=1)
    df_Stopperesæsonen = df_Stopperesæsonen.groupby(['Player name','Team name','Total minutes']).mean(numeric_only=True)
    df_Stopperesæsonen = df_Stopperesæsonen.sort_values(by='Samlet',ascending=False)
    
    with st.expander('Stoppere sæson'):
        st.dataframe(df_Stopperesæsonen)

    df_Centrale_midt = pd.merge(df_centraleminutter,df_Centrale_midt,on=('Player id'))
    df_Centrale_midt = df_Centrale_midt[df_Centrale_midt['total_minutesOnField_y'] >=tidprkamp]

    df_Centrale_midt['Passes %'] = pd.qcut(df_Centrale_midt['percent_successfulPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Passes #'] = pd.qcut(df_Centrale_midt['average_successfulPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Forward Passes %'] = pd.qcut(df_Centrale_midt['percent_successfulForwardPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Forward Passes #'] = pd.qcut(df_Centrale_midt['average_successfulForwardPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Long Passes %'] = pd.qcut(df_Centrale_midt['percent_successfulLongPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Long Passes #'] = pd.qcut(df_Centrale_midt['average_successfulLongPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Smart passes %'] = pd.qcut(df_Centrale_midt['percent_successfulSmartPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Smart passes #'] = pd.qcut(df_Centrale_midt['average_successfulSmartPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Key passes %'] = pd.qcut(df_Centrale_midt['percent_successfulKeyPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Key passes #'] = pd.qcut(df_Centrale_midt['average_successfulKeyPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Passes to final third %'] = pd.qcut(df_Centrale_midt['percent_successfulPassesToFinalThird'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Passes to final third #'] = pd.qcut(df_Centrale_midt['average_successfulPassesToFinalThird'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Vertical passes %'] = pd.qcut(df_Centrale_midt['percent_successfulVerticalPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Vertical passes #'] = pd.qcut(df_Centrale_midt['average_successfulVerticalPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Through passes %'] = pd.qcut(df_Centrale_midt['percent_successfulThroughPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Through passes #'] = pd.qcut(df_Centrale_midt['average_successfulThroughPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Progressive passes %'] = pd.qcut(df_Centrale_midt['percent_successfulProgressivePasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Progressive passes #'] = pd.qcut(df_Centrale_midt['average_successfulProgressivePasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Offensive duels %'] = pd.qcut(df_Centrale_midt['percent_newOffensiveDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Received passes'] = pd.qcut(df_Centrale_midt['average_receivedPass'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Succesful dribbles %'] = pd.qcut(df_Centrale_midt['percent_newSuccessfulDribbles'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Succesful dribbles #'] = pd.qcut(df_Centrale_midt['average_newSuccessfulDribbles'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Duels won %'] = pd.qcut(df_Centrale_midt['percent_newDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Duels won #'] = pd.qcut(df_Centrale_midt['average_newDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Interceptions'] = pd.qcut(df_Centrale_midt['average_interceptions'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Counterpressing recoveries #'] = pd.qcut(df_Centrale_midt['average_counterpressingRecoveries'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Defensive duels won #'] = pd.qcut(df_Centrale_midt['average_newDefensiveDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Defensive duels won %'] = pd.qcut(df_Centrale_midt['percent_newDefensiveDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)

    df_Centrale_midtsæsonen = df_Centrale_midt.rename(columns={'total_minutesOnField_x':'Total minutes'},inplace=True)
    df_Centrale_midtsæsonen = df_Centrale_midt.groupby(['Player name','Team name','Total minutes','label']).mean(numeric_only=True)
    df_Centrale_midtsæsonen['Pasningssikker/Spilvendinger'] = (df_Centrale_midtsæsonen['Passes %'] + df_Centrale_midtsæsonen['Passes #'] + df_Centrale_midtsæsonen['Forward Passes %'] + df_Centrale_midtsæsonen['Forward Passes #'] + df_Centrale_midtsæsonen['Long Passes %'] + df_Centrale_midtsæsonen['Long Passes #']+ df_Centrale_midtsæsonen['Smart passes %'] + df_Centrale_midtsæsonen['Smart passes #'] + + df_Centrale_midtsæsonen['Key passes %'] + df_Centrale_midtsæsonen['Key passes #'] + df_Centrale_midtsæsonen['Passes to final third %'] + df_Centrale_midtsæsonen['Passes to final third #']+ df_Centrale_midtsæsonen['Vertical passes %'] + df_Centrale_midtsæsonen['Vertical passes #']+ df_Centrale_midtsæsonen['Through passes %'] + df_Centrale_midtsæsonen['Through passes #']+ df_Centrale_midtsæsonen['Progressive passes %'] + df_Centrale_midtsæsonen['Progressive passes #'])/18
    df_Centrale_midtsæsonen['Boldfast'] = (df_Centrale_midtsæsonen['Passes %'] + df_Centrale_midtsæsonen['Passes #']+ df_Centrale_midtsæsonen['Offensive duels %'] + df_Centrale_midtsæsonen['Received passes'] + df_Centrale_midtsæsonen['Succesful dribbles %'] + df_Centrale_midtsæsonen['Succesful dribbles #'])/6
    df_Centrale_midtsæsonen['Spilintelligens defensivt'] = (df_Centrale_midtsæsonen['Duels won %'] + df_Centrale_midtsæsonen['Duels won #'] +df_Centrale_midtsæsonen['Interceptions'] + df_Centrale_midtsæsonen['Counterpressing recoveries #'] + df_Centrale_midtsæsonen['Defensive duels won %'] + df_Centrale_midtsæsonen['Defensive duels won #'])/6
    df_Centrale_midtsæsonen['Samlet'] = (df_Centrale_midtsæsonen['Pasningssikker/Spilvendinger'] + df_Centrale_midtsæsonen['Boldfast'] + df_Centrale_midtsæsonen['Spilintelligens defensivt'])/3

    df_Centrale_midtsæsonen = df_Centrale_midtsæsonen[['Pasningssikker/Spilvendinger','Boldfast','Spilintelligens defensivt','Samlet']]
    df_Centrale_midtsæsonen = df_Centrale_midtsæsonen.sort_values(by='Samlet',ascending=False)
    with st.expander('Centrale midt kamp for kamp'):
        st.write(df_Centrale_midtsæsonen)

    df_Centrale_midtsæsonen = df_Centrale_midtsæsonen.reset_index()
    df_Centrale_midtsæsonen = df_Centrale_midtsæsonen.drop('label',axis=1)
    df_Centrale_midtsæsonen = df_Centrale_midtsæsonen.groupby(['Player name','Team name','Total minutes']).mean(numeric_only=True)
    df_Centrale_midtsæsonen = df_Centrale_midtsæsonen.sort_values(by='Samlet',ascending=False)
    with st.expander('Centrale midt sæson'):
        st.write(df_Centrale_midtsæsonen)

    df_Kanter = pd.merge(df_kanterminutter,df_Kanter,on=('Player id'))
    df_Kanter = df_Kanter[df_Kanter['total_minutesOnField_y'] >=tidprkamp]

    df_Kanter['Shots on target %'] = pd.qcut(df_Kanter['percent_shotsOnTarget'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Shots on target #'] = pd.qcut(df_Kanter['average_shotsOnTarget'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['XG'] = pd.qcut(df_Kanter['average_xgShot'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Successful dribbles #'] = pd.qcut(df_Kanter['average_newSuccessfulDribbles'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Successful dribbles %'] = pd.qcut(df_Kanter['percent_newSuccessfulDribbles'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Offensive duels %'] = pd.qcut(df_Kanter['percent_newOffensiveDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Offensive duels #'] = pd.qcut(df_Kanter['average_newOffensiveDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Passes %'] = pd.qcut(df_Kanter['percent_successfulPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Passes #'] = pd.qcut(df_Kanter['average_successfulPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Forward Passes %'] = pd.qcut(df_Kanter['percent_successfulForwardPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Forward Passes #'] = pd.qcut(df_Kanter['average_successfulForwardPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Smart passes %'] = pd.qcut(df_Kanter['percent_successfulSmartPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Smart passes #'] = pd.qcut(df_Kanter['average_successfulSmartPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Key passes %'] = pd.qcut(df_Kanter['percent_successfulKeyPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Key passes #'] = pd.qcut(df_Kanter['average_successfulKeyPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Passes to final third %'] = pd.qcut(df_Kanter['percent_successfulPassesToFinalThird'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Passes to final third #'] = pd.qcut(df_Kanter['average_successfulPassesToFinalThird'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Vertical passes %'] = pd.qcut(df_Kanter['percent_successfulVerticalPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Vertical passes #'] = pd.qcut(df_Kanter['average_successfulVerticalPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Through passes %'] = pd.qcut(df_Kanter['percent_successfulThroughPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Through passes #'] = pd.qcut(df_Kanter['average_successfulThroughPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Progressive passes %'] = pd.qcut(df_Kanter['percent_successfulProgressivePasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Progressive passes #'] = pd.qcut(df_Kanter['average_successfulProgressivePasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Goal conversion %'] = pd.qcut(df_Kanter['percent_goalConversion'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['XG per 90'] = pd.qcut(df_Kanter['average_xgShot'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['XA per 90'] = pd.qcut(df_Kanter['average_xgAssist'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Successful attacking actions'] = pd.qcut(df_Kanter['average_successfulAttackingActions'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Progressive runs'] = pd.qcut(df_Kanter['average_progressiveRun'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Accelerations score'] = pd.qcut(df_Kanter['average_accelerations'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)

    df_Kantersæsonen = df_Kanter.rename(columns={'total_minutesOnField_x':'Total minutes'},inplace=True)
    df_Kantersæsonen = df_Kanter.groupby(['Player name','Team name','Total minutes','label']).mean(numeric_only=True)

    df_Kantersæsonen['Sparkefærdigheder'] = (df_Kantersæsonen['Shots on target %'] + df_Kantersæsonen['Shots on target #'] + df_Kantersæsonen['XG'] + df_Kantersæsonen['Passes to final third %'] + df_Kantersæsonen['Forward Passes %'] + df_Kantersæsonen['Vertical passes %'])/6
    df_Kantersæsonen['Kombinationsstærk'] = (df_Kantersæsonen['Passes %'] + df_Kantersæsonen['Passes #'] + df_Kantersæsonen['Forward Passes %'] + df_Kantersæsonen['Forward Passes #'] + df_Kantersæsonen['Passes to final third %'] + df_Kantersæsonen['Passes to final third #'] + df_Kantersæsonen['Through passes %'] + df_Kantersæsonen['Through passes #'] + df_Kantersæsonen['Progressive passes %'] + df_Kantersæsonen['Progressive passes #'] + df_Kantersæsonen['Successful attacking actions'])/11
    df_Kantersæsonen['Spilintelligens offensivt/indlægsstærk'] = (df_Kantersæsonen['XA per 90'] + df_Kantersæsonen['XG per 90'] + df_Kantersæsonen['Through passes %'] + df_Kantersæsonen['Through passes #'] + df_Kantersæsonen['Smart passes %'] + df_Kantersæsonen['Smart passes #'] + df_Kantersæsonen['Progressive passes %'] + df_Kantersæsonen['Progressive passes #'] + df_Kantersæsonen['Key passes %'] + df_Kantersæsonen['Key passes #'] + df_Kantersæsonen['Successful attacking actions'])/11
    df_Kantersæsonen['1v1 offensivt'] = (df_Kantersæsonen['Successful dribbles #'] + df_Kantersæsonen['Successful dribbles %'] + df_Kantersæsonen['Offensive duels #'] + df_Kantersæsonen['Offensive duels %'] + df_Kantersæsonen['Progressive runs'])/5
    df_Kantersæsonen['Fart'] = (df_Kantersæsonen['Progressive runs'] + df_Kantersæsonen['Successful dribbles #'] + df_Kantersæsonen['Successful dribbles %'] + df_Kantersæsonen['Accelerations score'])/4
    df_Kantersæsonen['Samlet'] = (df_Kantersæsonen['Sparkefærdigheder'] + df_Kantersæsonen['Kombinationsstærk'] + df_Kantersæsonen['Spilintelligens offensivt/indlægsstærk'] + df_Kantersæsonen['1v1 offensivt'] + df_Kantersæsonen['Fart'])/5
    df_Kantersæsonen = df_Kantersæsonen[['Sparkefærdigheder','Kombinationsstærk','Spilintelligens offensivt/indlægsstærk','1v1 offensivt','Fart','Samlet']]
    df_Kantersæsonen = df_Kantersæsonen.sort_values(by='Samlet',ascending=False)

    with st.expander('Kanter kamp for kamp'):
        st.write(df_Kantersæsonen)

    df_Kantersæsonen = df_Kantersæsonen.reset_index()
    df_Kantersæsonen = df_Kantersæsonen.drop('label',axis=1)
    df_Kantersæsonen = df_Kantersæsonen.groupby(['Player name','Team name','Total minutes']).mean(numeric_only=True)
    df_Kantersæsonen = df_Kantersæsonen.sort_values(by='Samlet',ascending=False)
    with st.expander('Kanter sæson'):
        st.write(df_Kantersæsonen)

    df_Angribere = pd.merge(df_angribereminutter,df_Angribere,on=('Player id'))
    df_Angribere = df_Angribere[df_Angribere['total_minutesOnField_y'] >=tidprkamp]

    df_Angribere['Målfarlighed udregning'] = df_Angribere['average_goals'] - df_Angribere['average_xgShot']
    df_Angribere['Målfarlighed score'] =  pd.qcut(df_Angribere['Målfarlighed udregning'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Angribere['xG per 90 score'] = pd.qcut(df_Angribere['average_xgShot'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Angribere['Goals per 90 score'] = pd.qcut(df_Angribere['average_goals'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)  
    df_Angribere['Shots on target, % score'] = pd.qcut(df_Angribere['percent_shotsOnTarget'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)   
    df_Angribere['Offensive duels won, % score'] = pd.qcut(df_Angribere['percent_newOffensiveDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Angribere['Duels won, % score'] = pd.qcut(df_Angribere['percent_newDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Angribere['Accurate passes, % score'] = pd.qcut(df_Angribere['percent_successfulPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Angribere['Successful dribbles, % score'] = pd.qcut(df_Angribere['percent_newSuccessfulDribbles'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Angribere['xA per 90 score'] = pd.qcut(df_Angribere['average_xgAssist'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Angribere['Touches in box per 90 score'] = pd.qcut(df_Angribere['average_touchInBox'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Angribere['Progressive runs'] = pd.qcut(df_Angribere['average_progressiveRun'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Angribere['Accelerations score'] = pd.qcut(df_Angribere['average_accelerations'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Angribere['Progressive passes per 90 score'] = pd.qcut(df_Angribere['average_successfulProgressivePasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Angribere['Successful attacking actions per 90 score'] = pd.qcut(df_Angribere['average_successfulAttackingActions'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Angribere['Successful dribbles #'] = pd.qcut(df_Angribere['average_newSuccessfulDribbles'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)

    df_Angriberesæsonen = df_Angribere.rename(columns={'total_minutesOnField_x':'Total minutes'},inplace=True)
    df_Angriberesæsonen = df_Angribere.groupby(['Player name','Team name','Total minutes','label']).mean(numeric_only=True)

    df_Angriberesæsonen['Sparkefærdigheder'] = (df_Angriberesæsonen['xG per 90 score'] + df_Angriberesæsonen['xG per 90 score'] + df_Angriberesæsonen['Goals per 90 score'] + df_Angriberesæsonen['Shots on target, % score'])/4
    df_Angriberesæsonen['Boldfast'] = (df_Angriberesæsonen['Offensive duels won, % score'] + df_Angriberesæsonen['Offensive duels won, % score'] + df_Angriberesæsonen['Duels won, % score'] + df_Angriberesæsonen['Accurate passes, % score'] + df_Angriberesæsonen['Successful dribbles, % score'])/5
    df_Angriberesæsonen['Spilintelligens offensivt'] = (df_Angriberesæsonen['xA per 90 score'] + df_Angriberesæsonen['xG per 90 score'] + df_Angriberesæsonen['Touches in box per 90 score'] + df_Angriberesæsonen['Progressive passes per 90 score'] + df_Angriberesæsonen['Successful attacking actions per 90 score'] + df_Angriberesæsonen['Touches in box per 90 score'] + df_Angriberesæsonen['xG per 90 score'])/7
    df_Angriberesæsonen['Målfarlighed'] = (df_Angriberesæsonen['xG per 90 score']+df_Angriberesæsonen['Goals per 90 score']+df_Angriberesæsonen['xG per 90 score'] + df_Angriberesæsonen['Målfarlighed score'])/4
    df_Angriberesæsonen['Fart'] = (df_Angriberesæsonen['Progressive runs'] + + df_Angriberesæsonen['Progressive runs'] + df_Angriberesæsonen['Progressive runs'] + df_Angriberesæsonen['Successful dribbles #'] + df_Angriberesæsonen['Successful dribbles, % score'] + df_Angriberesæsonen['Accelerations score'] + df_Angriberesæsonen['Offensive duels won, % score'])/7
    df_Angriberesæsonen = df_Angriberesæsonen[['Sparkefærdigheder','Boldfast','Spilintelligens offensivt','Målfarlighed','Fart']]
    df_Angriberesæsonen['Samlet'] = (df_Angriberesæsonen['Sparkefærdigheder']+df_Angriberesæsonen['Boldfast']+df_Angriberesæsonen['Spilintelligens offensivt']+df_Angriberesæsonen['Målfarlighed']+df_Angriberesæsonen['Målfarlighed']+df_Angriberesæsonen['Målfarlighed']+df_Angriberesæsonen['Fart'])/7
    df_Angriberesæsonen = df_Angriberesæsonen.sort_values(by='Samlet',ascending=False)

    with st.expander('Angribere kamp for kamp'):
        st.write(df_Angriberesæsonen)

    df_Angriberesæsonen = df_Angriberesæsonen.reset_index()
    df_Angriberesæsonen = df_Angriberesæsonen.drop('label',axis=1)
    df_Angriberesæsonen = df_Angriberesæsonen.groupby(['Player name','Team name','Total minutes']).mean(numeric_only=True)
    df_Angriberesæsonen = df_Angriberesæsonen.sort_values(by='Samlet',ascending=False)
    with st.expander('Angribere sæson'):
        st.write(df_Angriberesæsonen)

    df = pd.read_csv(r'xT/U15 Ligaen 23 24.csv')

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


    dfscore = pd.read_csv(r'xT/Zone scores.csv')

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

    xgc = df1
    xgchold = xgc.rename(columns={'shot.xg': 'Hold xG'})
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

def U17_liga ():
    col1,col2 = st.columns(2)
    with col1:
        samlettid = st.number_input('Minutter i sæsonen')
    with col2:    
        tidprkamp = st.number_input('Minutter pr. kamp')
        
    df = pd.read_csv(r'Individuelt dashboard/Individuelt dashboard U17.csv')
    df.rename(columns={'playerId': 'Player id'}, inplace=True)
    df = df.astype(str)
    dfevents = pd.read_csv('U17 eventdata alle.csv',low_memory=False)
    dfevents = dfevents[['Player id','Player name','team_name','label','date','matchId']]
    dfspillernavn = df[['Player id','matchId','positions','average','percent','total']]
    dfspillernavn = dfspillernavn.astype(str)
    dfevents['Player id'] = dfevents['Player id'].astype(str)
    dfevents['matchId'] = dfevents['matchId'].astype(str)
    df = dfspillernavn.merge(dfevents)

    df['Player&matchId'] = df['Player id'] + df['matchId']
    df['Player&matchId'] = df['Player&matchId'].drop_duplicates(keep='first')
    df = df.dropna()
    df = df[['Player id','Player name','team_name','matchId','label','date','positions','average','percent','total']]

    #df = df.set_index('Player id')

    data = df['positions']
    df1 = pd.DataFrame(data)
    # Funktion, der ekstraherer navne og koder fra strengdata og opretter en ny kolonne med disse værdier
    def extract_positions(data):
        positions_list = ast.literal_eval(data) # Konverterer strengen til en liste af ordbøger
        names = [pos['position']['name'] for pos in positions_list]
        codes = [pos['position']['code'] for pos in positions_list]
        return pd.Series({'position_names': names, 'position_codes': codes})

    # Anvender funktionen på kolonnen og tilføjer resultaterne som nye kolonner til dataframe
    df1[['position_names', 'position_codes']] = df1['positions'].apply(extract_positions)

    df = pd.merge(df,df1,left_index=True, right_index=True)
    df = df.set_index('Player id')
    df = df.drop(columns=['positions_x'])
    df = df.drop(columns=['positions_y'])
    df = df[['Player name','team_name','matchId','label','date','position_names','position_codes','average','percent','total']]
    df = df.rename(columns={'team_name':'Team name'})
    df['percent'] = df['percent'].apply(lambda x: ast.literal_eval(x))

    # Create a new dataframe with the columns as the dictionary keys and the values as a list
    new_df = pd.DataFrame(df['percent'].to_list(), index=df.index).add_prefix('percent_')

    # Concatenate the new dataframe with the original dataframe
    df = pd.concat([df, new_df], axis=1)

    # Drop the original 'percent' column
    df = df.drop('percent', axis=1)

    df['total'] = df['total'].apply(lambda x: ast.literal_eval(x))

    # Create a new dataframe with the columns as the dictionary keys and the values as a list
    new_df = pd.DataFrame(df['total'].to_list(), index=df.index).add_prefix('total_')

    # Concatenate the new dataframe with the original dataframe
    df = pd.concat([df, new_df], axis=1)

    # Drop the original 'percent' column
    df = df.drop('total', axis=1)

    df['average'] = df['average'].apply(lambda x: ast.literal_eval(x))

    # Create a new dataframe with the columns as the dictionary keys and the values as a list
    new_df = pd.DataFrame(df['average'].to_list(), index=df.index).add_prefix('average_')

    # Concatenate the new dataframe with the original dataframe
    df = pd.concat([df, new_df], axis=1)


    # Drop the original 'percent' column
    df = df.drop('average', axis=1)
    df['position_codes'] = df['position_codes'].astype(str)
    #df['date'] = df['date'].astype(str)
    #df['date'] = df['date'].apply(lambda x: parser.parse(x))

    # Sort the dataframe by the 'date' column
    #df = df.sort_values(by='date',ascending=False)

    # Format the 'date' column to day-month-year format
    #df['date'] = df['date'].apply(lambda x: x.strftime('%d-%m-%Y'))
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date',ascending=False)

    df_backs = df[df['position_codes'].str.contains('|'.join(['lb', 'rb']))]
    df_backs = df_backs[df_backs['total_minutesOnField'] >= tidprkamp]
    df_backsminutter = df_backs[['Player name','Team name','total_minutesOnField']]
    df_backsminutter = df_backsminutter.groupby(['Player id']).sum(numeric_only=True)
    df_backsminutter = df_backsminutter[df_backsminutter['total_minutesOnField'] >= samlettid]

    df_Stoppere = df[df['position_codes'].str.contains('|'.join(['cb']))]
    df_Stoppere = df_Stoppere[df_Stoppere['total_minutesOnField'] >= tidprkamp]
    df_stoppereminutter = df_Stoppere[['Player name','Team name','total_minutesOnField']]
    df_stoppereminutter = df_stoppereminutter.groupby(['Player id']).sum(numeric_only=True)
    df_stoppereminutter = df_stoppereminutter[df_stoppereminutter['total_minutesOnField'] >= samlettid]

    df_Centrale_midt = df[df['position_codes'].str.contains('|'.join(['cm','amf','dmf']))]
    df_Centrale_midt = df_Centrale_midt[df_Centrale_midt['total_minutesOnField'] >= tidprkamp]
    df_centraleminutter = df_Centrale_midt[['Player name','Team name','total_minutesOnField']]
    df_centraleminutter = df_centraleminutter.groupby(['Player id']).sum(numeric_only=True)
    df_centraleminutter = df_centraleminutter[df_centraleminutter['total_minutesOnField'] >= samlettid]

    df_Kanter = df[df['position_codes'].str.contains('|'.join(['rw','lw','ramf','lamf']))]
    df_Kanter = df_Kanter[df_Kanter['total_minutesOnField'] >=tidprkamp]
    df_kanterminutter = df_Kanter[['Player name','Team name','total_minutesOnField']]
    df_kanterminutter = df_kanterminutter.groupby(['Player id']).sum(numeric_only=True)
    df_kanterminutter = df_kanterminutter[df_kanterminutter['total_minutesOnField'] >=samlettid]


    df_Angribere = df[df['position_codes'].str.contains('|'.join(['cf','ss']))]
    df_Angribere = df_Angribere[df_Angribere['total_minutesOnField'] >= tidprkamp]
    df_angribereminutter = df_Angribere[['Player name','Team name','total_minutesOnField']]
    df_angribereminutter = df_angribereminutter.groupby(['Player id']).sum(numeric_only=True)
    df_angribereminutter = df_angribereminutter[df_angribereminutter['total_minutesOnField'] >= samlettid]


    df_backs = pd.merge(df_backsminutter,df_backs,on=('Player id'))
    df_backs = df_backs[df_backs['total_minutesOnField_y'] >=tidprkamp]

    df_backs['Accurate crosses score'] = pd.qcut(df_backs['percent_successfulCrosses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_backs['Number of crosses score'] = pd.qcut(df_backs['average_crosses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_backs['XA score'] = pd.qcut(df_backs['average_xgAssist'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_backs['Passes to final third score'] = pd.qcut(df_backs['average_successfulPassesToFinalThird'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_backs['Successful dribbles score'] = pd.qcut(df_backs['percent_newSuccessfulDribbles'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_backs['Defensive duels won score'] = pd.qcut(df_backs['percent_newDefensiveDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_backs['Progressive runs score'] = pd.qcut(df_backs['average_progressiveRun'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_backs['Offensive duels won score'] = pd.qcut(df_backs['percent_newOffensiveDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_backs['Accelerations score'] = pd.qcut(df_backs['average_accelerations'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_backs['Duels won score'] = pd.qcut(df_backs['percent_newDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_backs['Interceptions score'] = pd.qcut(df_backs['average_interceptions'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_backs['Successful defensive actions score'] = pd.qcut(df_backs['average_successfulDefensiveAction'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_backssæsonen = df_backs[['label','Player name','Team name','total_minutesOnField_x','total_minutesOnField_y','Number of crosses score','Accurate crosses score','XA score','Passes to final third score','Successful dribbles score','Defensive duels won score','Progressive runs score','Offensive duels won score','Accelerations score','Duels won score','Interceptions score','Successful defensive actions score']]
    df_backssæsonen.rename(columns={'total_minutesOnField_x':'Total minutes'},inplace=True)
    df_backssæsonen = df_backssæsonen.groupby(['Player name','Team name','Total minutes','label']).mean(numeric_only=True)

    df_backssæsonen['Indlægsstærk'] = (df_backssæsonen['Number of crosses score'] + df_backssæsonen['Accurate crosses score'] + df_backssæsonen['XA score'] + df_backssæsonen['Passes to final third score'])/4
    df_backssæsonen['1v1 færdigheder'] = (df_backssæsonen['Successful dribbles score'] + df_backssæsonen['Defensive duels won score'] + df_backssæsonen['Progressive runs score'] + df_backssæsonen['Offensive duels won score'] + df_backssæsonen['Accelerations score'] + df_backssæsonen['Duels won score'])/6
    df_backssæsonen['Spilintelligens defensivt'] = (df_backssæsonen['Interceptions score'] + df_backssæsonen['Successful defensive actions score'] + df_backssæsonen['Duels won score'] + df_backssæsonen['Defensive duels won score'])/4
    df_backssæsonen['Fart'] = (df_backssæsonen['Successful dribbles score'] + df_backssæsonen['Progressive runs score'] + df_backssæsonen['Offensive duels won score'] + df_backssæsonen['Accelerations score'])/4
    df_backssæsonen ['Samlet'] = (df_backssæsonen['Indlægsstærk'] + df_backssæsonen['1v1 færdigheder'] + df_backssæsonen['Spilintelligens defensivt'] + df_backssæsonen['Fart'])/4

    df_backssæsonen = df_backssæsonen[['Indlægsstærk','1v1 færdigheder','Spilintelligens defensivt','Fart','Samlet']]
    df_backssæsonen = df_backssæsonen.round(3).astype(float)
    df_backssæsonen = df_backssæsonen.sort_values(by='Samlet',ascending=False)
    with st.expander('Backs kamp for kamp'):
        st.write(df_backssæsonen)
    df_backssæsonen = df_backssæsonen.reset_index()
    df_backssæsonen = df_backssæsonen.drop('label',axis=1)
    df_backssæsonen = df_backssæsonen.groupby(['Player name','Team name','Total minutes']).mean(numeric_only=True)
    df_backssæsonen = df_backssæsonen.sort_values(by='Samlet',ascending=False)
    with st.expander('Backs'):
        st.dataframe(df_backssæsonen)
       
    df_Stoppere = pd.merge(df_stoppereminutter,df_Stoppere,on=('Player id'))
    df_Stoppere = df_Stoppere[df_Stoppere['total_minutesOnField_y'] >=tidprkamp]
    
    df_Stoppere['Accurate passes score'] = pd.qcut(df_Stoppere['percent_successfulPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Accurate long passes score'] = pd.qcut(df_Stoppere['percent_successfulLongPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Forward passes score'] = pd.qcut(df_Stoppere['average_successfulForwardPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Accurate forward passes score'] = pd.qcut(df_Stoppere['percent_successfulForwardPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Accurate progressive passes score'] = pd.qcut(df_Stoppere['percent_successfulProgressivePasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Accurate vertical passes score'] = pd.qcut(df_Stoppere['percent_successfulVerticalPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Interceptions score'] = pd.qcut(df_Stoppere['average_interceptions'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Succesful defensive actions score'] = pd.qcut(df_Stoppere['average_successfulDefensiveAction'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Shots blocked score'] = pd.qcut(df_Stoppere['average_shotsBlocked'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Defensive duels won score'] = pd.qcut(df_Stoppere['average_newDefensiveDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Defensive duels won % score'] = pd.qcut(df_Stoppere['percent_newDefensiveDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Accurate passes to final third'] = pd.qcut(df_Stoppere['percent_successfulPassesToFinalThird'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Accurate through passes'] = pd.qcut(df_Stoppere['percent_successfulThroughPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Vertical passes'] = pd.qcut(df_Stoppere['average_successfulVerticalPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Through passes'] = pd.qcut(df_Stoppere['average_successfulThroughPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Passes to final third'] = pd.qcut(df_Stoppere['average_successfulPassesToFinalThird'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Progressive runs'] = pd.qcut(df_Stoppere['average_progressiveRun'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Offensive duels won %'] = pd.qcut(df_Stoppere['percent_newOffensiveDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Successful dribbles %'] = pd.qcut(df_Stoppere['percent_newSuccessfulDribbles'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Progressive passes score'] = pd.qcut(df_Stoppere['average_successfulProgressivePasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Aerial duels won score'] = pd.qcut(df_Stoppere['average_fieldAerialDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Aerial duels won % score'] = pd.qcut(df_Stoppere['percent_aerialDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)

    df_Stopperesæsonen = df_Stoppere[['label','Player name','Team name','total_minutesOnField_x','total_minutesOnField_y','Accurate passes score','Accurate long passes score','Forward passes score','Accurate forward passes score','Accurate progressive passes score','Accurate vertical passes score','Interceptions score','Succesful defensive actions score','Shots blocked score','Defensive duels won score','Defensive duels won % score','Accurate passes to final third','Accurate through passes','Vertical passes','Through passes','Passes to final third','Progressive passes score','Aerial duels won score','Aerial duels won % score','Progressive runs','Offensive duels won %','Successful dribbles %']]
    df_Stopperesæsonen.rename(columns={'total_minutesOnField_x':'Total minutes'},inplace=True)
    df_Stopperesæsonen = df_Stopperesæsonen.groupby(['Player name','Team name','Total minutes','label']).mean(numeric_only=True)
    df_Stopperesæsonen['Pasningssikker'] = (df_Stopperesæsonen['Accurate passes score'] + df_Stopperesæsonen['Accurate long passes score'] + df_Stopperesæsonen['Forward passes score'] + df_Stopperesæsonen['Accurate forward passes score'] + df_Stopperesæsonen['Accurate progressive passes score'] + df_Stopperesæsonen['Accurate vertical passes score'])/6
    df_Stopperesæsonen['Spilintelligens defensivt'] = (df_Stopperesæsonen['Interceptions score'] + df_Stopperesæsonen['Succesful defensive actions score'] + df_Stopperesæsonen['Shots blocked score'] + df_Stopperesæsonen['Succesful defensive actions score'] + df_Stopperesæsonen['Defensive duels won % score']) /5
    df_Stopperesæsonen['Spilintelligens offensivt'] = (df_Stopperesæsonen['Forward passes score'] + df_Stopperesæsonen['Accurate forward passes score'] + df_Stopperesæsonen['Accurate passes to final third'] + df_Stopperesæsonen['Passes to final third'] + df_Stopperesæsonen['Accurate progressive passes score'] + df_Stopperesæsonen['Progressive passes score'] + df_Stopperesæsonen['Through passes'] + df_Stopperesæsonen['Accurate through passes']+ df_Stopperesæsonen['Progressive runs'] + df_Stopperesæsonen['Offensive duels won %'] + df_Stopperesæsonen['Successful dribbles %'])/11
    df_Stopperesæsonen['Nærkamps- og duelstærk'] = (df_Stopperesæsonen['Defensive duels won % score'] + df_Stopperesæsonen['Aerial duels won % score'] + df_Stopperesæsonen['Defensive duels won % score'])/3
    df_Stopperesæsonen['Samlet'] = (df_Stopperesæsonen['Pasningssikker'] + df_Stopperesæsonen['Spilintelligens defensivt'] + df_Stopperesæsonen['Spilintelligens offensivt'] + df_Stopperesæsonen['Nærkamps- og duelstærk'])/4

    df_Stopperesæsonen = df_Stopperesæsonen[['Pasningssikker','Spilintelligens defensivt','Spilintelligens offensivt','Nærkamps- og duelstærk','Samlet']]
    df_Stopperesæsonen = df_Stopperesæsonen.sort_values(by='Samlet',ascending=False)

    with st.expander('Stoppere kamp for kamp'):
        st.write(df_Stopperesæsonen)
    df_Stopperesæsonen = df_Stopperesæsonen.reset_index()
    df_Stopperesæsonen = df_Stopperesæsonen.drop('label',axis=1)
    df_Stopperesæsonen = df_Stopperesæsonen.groupby(['Player name','Team name','Total minutes']).mean(numeric_only=True)
    df_Stopperesæsonen = df_Stopperesæsonen.sort_values(by='Samlet',ascending=False)
    
    with st.expander('Stoppere sæson'):
        st.dataframe(df_Stopperesæsonen)

    df_Centrale_midt = pd.merge(df_centraleminutter,df_Centrale_midt,on=('Player id'))
    df_Centrale_midt = df_Centrale_midt[df_Centrale_midt['total_minutesOnField_y'] >=tidprkamp]

    df_Centrale_midt['Passes %'] = pd.qcut(df_Centrale_midt['percent_successfulPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Passes #'] = pd.qcut(df_Centrale_midt['average_successfulPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Forward Passes %'] = pd.qcut(df_Centrale_midt['percent_successfulForwardPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Forward Passes #'] = pd.qcut(df_Centrale_midt['average_successfulForwardPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Long Passes %'] = pd.qcut(df_Centrale_midt['percent_successfulLongPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Long Passes #'] = pd.qcut(df_Centrale_midt['average_successfulLongPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Smart passes %'] = pd.qcut(df_Centrale_midt['percent_successfulSmartPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Smart passes #'] = pd.qcut(df_Centrale_midt['average_successfulSmartPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Key passes %'] = pd.qcut(df_Centrale_midt['percent_successfulKeyPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Key passes #'] = pd.qcut(df_Centrale_midt['average_successfulKeyPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Passes to final third %'] = pd.qcut(df_Centrale_midt['percent_successfulPassesToFinalThird'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Passes to final third #'] = pd.qcut(df_Centrale_midt['average_successfulPassesToFinalThird'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Vertical passes %'] = pd.qcut(df_Centrale_midt['percent_successfulVerticalPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Vertical passes #'] = pd.qcut(df_Centrale_midt['average_successfulVerticalPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Through passes %'] = pd.qcut(df_Centrale_midt['percent_successfulThroughPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Through passes #'] = pd.qcut(df_Centrale_midt['average_successfulThroughPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Progressive passes %'] = pd.qcut(df_Centrale_midt['percent_successfulProgressivePasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Progressive passes #'] = pd.qcut(df_Centrale_midt['average_successfulProgressivePasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Offensive duels %'] = pd.qcut(df_Centrale_midt['percent_newOffensiveDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Received passes'] = pd.qcut(df_Centrale_midt['average_receivedPass'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Succesful dribbles %'] = pd.qcut(df_Centrale_midt['percent_newSuccessfulDribbles'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Succesful dribbles #'] = pd.qcut(df_Centrale_midt['average_newSuccessfulDribbles'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Duels won %'] = pd.qcut(df_Centrale_midt['percent_newDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Duels won #'] = pd.qcut(df_Centrale_midt['average_newDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Interceptions'] = pd.qcut(df_Centrale_midt['average_interceptions'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Counterpressing recoveries #'] = pd.qcut(df_Centrale_midt['average_counterpressingRecoveries'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Defensive duels won #'] = pd.qcut(df_Centrale_midt['average_newDefensiveDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Defensive duels won %'] = pd.qcut(df_Centrale_midt['percent_newDefensiveDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)

    df_Centrale_midtsæsonen = df_Centrale_midt.rename(columns={'total_minutesOnField_x':'Total minutes'},inplace=True)
    df_Centrale_midtsæsonen = df_Centrale_midt.groupby(['Player name','Team name','Total minutes','label']).mean(numeric_only=True)
    df_Centrale_midtsæsonen['Pasningssikker/Spilvendinger'] = (df_Centrale_midtsæsonen['Passes %'] + df_Centrale_midtsæsonen['Passes #'] + df_Centrale_midtsæsonen['Forward Passes %'] + df_Centrale_midtsæsonen['Forward Passes #'] + df_Centrale_midtsæsonen['Long Passes %'] + df_Centrale_midtsæsonen['Long Passes #']+ df_Centrale_midtsæsonen['Smart passes %'] + df_Centrale_midtsæsonen['Smart passes #'] + + df_Centrale_midtsæsonen['Key passes %'] + df_Centrale_midtsæsonen['Key passes #'] + df_Centrale_midtsæsonen['Passes to final third %'] + df_Centrale_midtsæsonen['Passes to final third #']+ df_Centrale_midtsæsonen['Vertical passes %'] + df_Centrale_midtsæsonen['Vertical passes #']+ df_Centrale_midtsæsonen['Through passes %'] + df_Centrale_midtsæsonen['Through passes #']+ df_Centrale_midtsæsonen['Progressive passes %'] + df_Centrale_midtsæsonen['Progressive passes #'])/18
    df_Centrale_midtsæsonen['Boldfast'] = (df_Centrale_midtsæsonen['Passes %'] + df_Centrale_midtsæsonen['Passes #']+ df_Centrale_midtsæsonen['Offensive duels %'] + df_Centrale_midtsæsonen['Received passes'] + df_Centrale_midtsæsonen['Succesful dribbles %'] + df_Centrale_midtsæsonen['Succesful dribbles #'])/6
    df_Centrale_midtsæsonen['Spilintelligens defensivt'] = (df_Centrale_midtsæsonen['Duels won %'] + df_Centrale_midtsæsonen['Duels won #'] +df_Centrale_midtsæsonen['Interceptions'] + df_Centrale_midtsæsonen['Counterpressing recoveries #'] + df_Centrale_midtsæsonen['Defensive duels won %'] + df_Centrale_midtsæsonen['Defensive duels won #'])/6
    df_Centrale_midtsæsonen['Samlet'] = (df_Centrale_midtsæsonen['Pasningssikker/Spilvendinger'] + df_Centrale_midtsæsonen['Boldfast'] + df_Centrale_midtsæsonen['Spilintelligens defensivt'])/3

    df_Centrale_midtsæsonen = df_Centrale_midtsæsonen[['Pasningssikker/Spilvendinger','Boldfast','Spilintelligens defensivt','Samlet']]
    df_Centrale_midtsæsonen = df_Centrale_midtsæsonen.sort_values(by='Samlet',ascending=False)
    with st.expander('Centrale midt kamp for kamp'):
        st.write(df_Centrale_midtsæsonen)

    df_Centrale_midtsæsonen = df_Centrale_midtsæsonen.reset_index()
    df_Centrale_midtsæsonen = df_Centrale_midtsæsonen.drop('label',axis=1)
    df_Centrale_midtsæsonen = df_Centrale_midtsæsonen.groupby(['Player name','Team name','Total minutes']).mean(numeric_only=True)
    df_Centrale_midtsæsonen = df_Centrale_midtsæsonen.sort_values(by='Samlet',ascending=False)
    with st.expander('Centrale midt sæson'):
        st.write(df_Centrale_midtsæsonen)


    df_Kanter = pd.merge(df_kanterminutter,df_Kanter,on=('Player id'))
    df_Kanter = df_Kanter[df_Kanter['total_minutesOnField_y'] >=tidprkamp]

    df_Kanter['Shots on target %'] = pd.qcut(df_Kanter['percent_shotsOnTarget'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Shots on target #'] = pd.qcut(df_Kanter['average_shotsOnTarget'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['XG'] = pd.qcut(df_Kanter['average_xgShot'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Successful dribbles #'] = pd.qcut(df_Kanter['average_newSuccessfulDribbles'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Successful dribbles %'] = pd.qcut(df_Kanter['percent_newSuccessfulDribbles'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Offensive duels %'] = pd.qcut(df_Kanter['percent_newOffensiveDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Offensive duels #'] = pd.qcut(df_Kanter['average_newOffensiveDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Passes %'] = pd.qcut(df_Kanter['percent_successfulPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Passes #'] = pd.qcut(df_Kanter['average_successfulPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Forward Passes %'] = pd.qcut(df_Kanter['percent_successfulForwardPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Forward Passes #'] = pd.qcut(df_Kanter['average_successfulForwardPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Smart passes %'] = pd.qcut(df_Kanter['percent_successfulSmartPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Smart passes #'] = pd.qcut(df_Kanter['average_successfulSmartPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Key passes %'] = pd.qcut(df_Kanter['percent_successfulKeyPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Key passes #'] = pd.qcut(df_Kanter['average_successfulKeyPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Passes to final third %'] = pd.qcut(df_Kanter['percent_successfulPassesToFinalThird'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Passes to final third #'] = pd.qcut(df_Kanter['average_successfulPassesToFinalThird'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Vertical passes %'] = pd.qcut(df_Kanter['percent_successfulVerticalPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Vertical passes #'] = pd.qcut(df_Kanter['average_successfulVerticalPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Through passes %'] = pd.qcut(df_Kanter['percent_successfulThroughPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Through passes #'] = pd.qcut(df_Kanter['average_successfulThroughPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Progressive passes %'] = pd.qcut(df_Kanter['percent_successfulProgressivePasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Progressive passes #'] = pd.qcut(df_Kanter['average_successfulProgressivePasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Goal conversion %'] = pd.qcut(df_Kanter['percent_goalConversion'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['XG per 90'] = pd.qcut(df_Kanter['average_xgShot'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['XA per 90'] = pd.qcut(df_Kanter['average_xgAssist'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Successful attacking actions'] = pd.qcut(df_Kanter['average_successfulAttackingActions'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Progressive runs'] = pd.qcut(df_Kanter['average_progressiveRun'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Accelerations score'] = pd.qcut(df_Kanter['average_accelerations'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)

    df_Kantersæsonen = df_Kanter.rename(columns={'total_minutesOnField_x':'Total minutes'},inplace=True)
    df_Kantersæsonen = df_Kanter.groupby(['Player name','Team name','Total minutes','label']).mean(numeric_only=True)

    df_Kantersæsonen['Sparkefærdigheder'] = (df_Kantersæsonen['Shots on target %'] + df_Kantersæsonen['Shots on target #'] + df_Kantersæsonen['XG'] + df_Kantersæsonen['Passes to final third %'] + df_Kantersæsonen['Forward Passes %'] + df_Kantersæsonen['Vertical passes %'])/6
    df_Kantersæsonen['Kombinationsstærk'] = (df_Kantersæsonen['Passes %'] + df_Kantersæsonen['Passes #'] + df_Kantersæsonen['Forward Passes %'] + df_Kantersæsonen['Forward Passes #'] + df_Kantersæsonen['Passes to final third %'] + df_Kantersæsonen['Passes to final third #'] + df_Kantersæsonen['Through passes %'] + df_Kantersæsonen['Through passes #'] + df_Kantersæsonen['Progressive passes %'] + df_Kantersæsonen['Progressive passes #'] + df_Kantersæsonen['Successful attacking actions'])/11
    df_Kantersæsonen['Spilintelligens offensivt/indlægsstærk'] = (df_Kantersæsonen['XA per 90'] + df_Kantersæsonen['XG per 90'] + df_Kantersæsonen['Through passes %'] + df_Kantersæsonen['Through passes #'] + df_Kantersæsonen['Smart passes %'] + df_Kantersæsonen['Smart passes #'] + df_Kantersæsonen['Progressive passes %'] + df_Kantersæsonen['Progressive passes #'] + df_Kantersæsonen['Key passes %'] + df_Kantersæsonen['Key passes #'] + df_Kantersæsonen['Successful attacking actions'])/11
    df_Kantersæsonen['1v1 offensivt'] = (df_Kantersæsonen['Successful dribbles #'] + df_Kantersæsonen['Successful dribbles %'] + df_Kantersæsonen['Offensive duels #'] + df_Kantersæsonen['Offensive duels %'] + df_Kantersæsonen['Progressive runs'])/5
    df_Kantersæsonen['Fart'] = (df_Kantersæsonen['Progressive runs'] + df_Kantersæsonen['Successful dribbles #'] + df_Kantersæsonen['Successful dribbles %'] + df_Kantersæsonen['Accelerations score'])/4
    df_Kantersæsonen['Samlet'] = (df_Kantersæsonen['Sparkefærdigheder'] + df_Kantersæsonen['Kombinationsstærk'] + df_Kantersæsonen['Spilintelligens offensivt/indlægsstærk'] + df_Kantersæsonen['1v1 offensivt'] + df_Kantersæsonen['Fart'])/5
    df_Kantersæsonen = df_Kantersæsonen[['Sparkefærdigheder','Kombinationsstærk','Spilintelligens offensivt/indlægsstærk','1v1 offensivt','Fart','Samlet']]
    df_Kantersæsonen = df_Kantersæsonen.sort_values(by='Samlet',ascending=False)

    with st.expander('Kanter kamp for kamp'):
        st.write(df_Kantersæsonen)

    df_Kantersæsonen = df_Kantersæsonen.reset_index()
    df_Kantersæsonen = df_Kantersæsonen.drop('label',axis=1)
    df_Kantersæsonen = df_Kantersæsonen.groupby(['Player name','Team name','Total minutes']).mean(numeric_only=True)
    df_Kantersæsonen = df_Kantersæsonen.sort_values(by='Samlet',ascending=False)
    with st.expander('Kanter sæson'):
        st.write(df_Kantersæsonen)


    df_Angribere = pd.merge(df_angribereminutter,df_Angribere,on=('Player id'))
    df_Angribere = df_Angribere[df_Angribere['total_minutesOnField_y'] >=tidprkamp]

    df_Angribere['Målfarlighed udregning'] = df_Angribere['average_goals'] - df_Angribere['average_xgShot']
    df_Angribere['Målfarlighed score'] =  pd.qcut(df_Angribere['Målfarlighed udregning'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Angribere['xG per 90 score'] = pd.qcut(df_Angribere['average_xgShot'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Angribere['Goals per 90 score'] = pd.qcut(df_Angribere['average_goals'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)  
    df_Angribere['Shots on target, % score'] = pd.qcut(df_Angribere['percent_shotsOnTarget'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)   
    df_Angribere['Offensive duels won, % score'] = pd.qcut(df_Angribere['percent_newOffensiveDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Angribere['Duels won, % score'] = pd.qcut(df_Angribere['percent_newDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Angribere['Accurate passes, % score'] = pd.qcut(df_Angribere['percent_successfulPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Angribere['Successful dribbles, % score'] = pd.qcut(df_Angribere['percent_newSuccessfulDribbles'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Angribere['xA per 90 score'] = pd.qcut(df_Angribere['average_xgAssist'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Angribere['Touches in box per 90 score'] = pd.qcut(df_Angribere['average_touchInBox'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Angribere['Progressive runs'] = pd.qcut(df_Angribere['average_progressiveRun'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Angribere['Accelerations score'] = pd.qcut(df_Angribere['average_accelerations'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Angribere['Progressive passes per 90 score'] = pd.qcut(df_Angribere['average_successfulProgressivePasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Angribere['Successful attacking actions per 90 score'] = pd.qcut(df_Angribere['average_successfulAttackingActions'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Angribere['Successful dribbles #'] = pd.qcut(df_Angribere['average_newSuccessfulDribbles'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)

    df_Angriberesæsonen = df_Angribere.rename(columns={'total_minutesOnField_x':'Total minutes'},inplace=True)
    df_Angriberesæsonen = df_Angribere.groupby(['Player name','Team name','Total minutes','label']).mean(numeric_only=True)

    df_Angriberesæsonen['Sparkefærdigheder'] = (df_Angriberesæsonen['xG per 90 score'] + df_Angriberesæsonen['xG per 90 score'] + df_Angriberesæsonen['Goals per 90 score'] + df_Angriberesæsonen['Shots on target, % score'])/4
    df_Angriberesæsonen['Boldfast'] = (df_Angriberesæsonen['Offensive duels won, % score'] + df_Angriberesæsonen['Offensive duels won, % score'] + df_Angriberesæsonen['Duels won, % score'] + df_Angriberesæsonen['Accurate passes, % score'] + df_Angriberesæsonen['Successful dribbles, % score'])/5
    df_Angriberesæsonen['Spilintelligens offensivt'] = (df_Angriberesæsonen['xA per 90 score'] + df_Angriberesæsonen['xG per 90 score'] + df_Angriberesæsonen['Touches in box per 90 score'] + df_Angriberesæsonen['Progressive passes per 90 score'] + df_Angriberesæsonen['Successful attacking actions per 90 score'] + df_Angriberesæsonen['Touches in box per 90 score'] + df_Angriberesæsonen['xG per 90 score'])/7
    df_Angriberesæsonen['Målfarlighed'] = (df_Angriberesæsonen['xG per 90 score']+df_Angriberesæsonen['Goals per 90 score']+df_Angriberesæsonen['xG per 90 score'] + df_Angriberesæsonen['Målfarlighed score'])/4
    df_Angriberesæsonen['Fart'] = (df_Angriberesæsonen['Progressive runs'] + + df_Angriberesæsonen['Progressive runs'] + df_Angriberesæsonen['Progressive runs'] + df_Angriberesæsonen['Successful dribbles #'] + df_Angriberesæsonen['Successful dribbles, % score'] + df_Angriberesæsonen['Accelerations score'] + df_Angriberesæsonen['Offensive duels won, % score'])/7
    df_Angriberesæsonen = df_Angriberesæsonen[['Sparkefærdigheder','Boldfast','Spilintelligens offensivt','Målfarlighed','Fart']]
    df_Angriberesæsonen['Samlet'] = (df_Angriberesæsonen['Sparkefærdigheder']+df_Angriberesæsonen['Boldfast']+df_Angriberesæsonen['Spilintelligens offensivt']+df_Angriberesæsonen['Målfarlighed']+df_Angriberesæsonen['Målfarlighed']+df_Angriberesæsonen['Målfarlighed']+df_Angriberesæsonen['Fart'])/7
    df_Angriberesæsonen = df_Angriberesæsonen.sort_values(by='Samlet',ascending=False)

    with st.expander('Angribere kamp for kamp'):
        st.write(df_Angriberesæsonen)

    df_Angriberesæsonen = df_Angriberesæsonen.reset_index()
    df_Angriberesæsonen = df_Angriberesæsonen.drop('label',axis=1)
    df_Angriberesæsonen = df_Angriberesæsonen.groupby(['Player name','Team name','Total minutes']).mean(numeric_only=True)
    df_Angriberesæsonen = df_Angriberesæsonen.sort_values(by='Samlet',ascending=False)
    with st.expander('Angribere sæson'):
        st.write(df_Angriberesæsonen)
    df = pd.read_csv(r'xT/U17 Ligaen 23 24.csv')

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


    dfscore = pd.read_csv(r'xT/Zone scores.csv')

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

    xgc = df1
    xgchold = xgc.rename(columns={'shot.xg': 'Hold xG'})
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

def U19_liga ():
    col1,col2 = st.columns(2)
    with col1:
        samlettid = st.number_input('Minutter i sæsonen')
    with col2:    
        tidprkamp = st.number_input('Minutter pr. kamp')
        
    df = pd.read_csv(r'Individuelt dashboard/Individuelt dashboard U19.csv')
    df.rename(columns={'playerId': 'Player id'}, inplace=True)
    df = df.astype(str)
    dfevents = pd.read_csv('U19 eventdata alle.csv',low_memory=False)
    dfevents = dfevents[['Player id','Player name','team_name','label','date','matchId']]
    dfspillernavn = df[['Player id','matchId','positions','average','percent','total']]
    dfspillernavn = dfspillernavn.astype(str)
    dfevents['Player id'] = dfevents['Player id'].astype(str)
    dfevents['matchId'] = dfevents['matchId'].astype(str)
    df = dfspillernavn.merge(dfevents)

    df['Player&matchId'] = df['Player id'] + df['matchId']
    df['Player&matchId'] = df['Player&matchId'].drop_duplicates(keep='first')
    df = df.dropna()
    df = df[['Player id','Player name','team_name','matchId','label','date','positions','average','percent','total']]

    #df = df.set_index('Player id')

    data = df['positions']
    df1 = pd.DataFrame(data)
    # Funktion, der ekstraherer navne og koder fra strengdata og opretter en ny kolonne med disse værdier
    def extract_positions(data):
        positions_list = ast.literal_eval(data) # Konverterer strengen til en liste af ordbøger
        names = [pos['position']['name'] for pos in positions_list]
        codes = [pos['position']['code'] for pos in positions_list]
        return pd.Series({'position_names': names, 'position_codes': codes})

    # Anvender funktionen på kolonnen og tilføjer resultaterne som nye kolonner til dataframe
    df1[['position_names', 'position_codes']] = df1['positions'].apply(extract_positions)

    df = pd.merge(df,df1,left_index=True, right_index=True)
    df = df.set_index('Player id')
    df = df.drop(columns=['positions_x'])
    df = df.drop(columns=['positions_y'])
    df = df[['Player name','team_name','matchId','label','date','position_names','position_codes','average','percent','total']]
    df = df.rename(columns={'team_name':'Team name'})
    df['percent'] = df['percent'].apply(lambda x: ast.literal_eval(x))

    # Create a new dataframe with the columns as the dictionary keys and the values as a list
    new_df = pd.DataFrame(df['percent'].to_list(), index=df.index).add_prefix('percent_')

    # Concatenate the new dataframe with the original dataframe
    df = pd.concat([df, new_df], axis=1)

    # Drop the original 'percent' column
    df = df.drop('percent', axis=1)

    df['total'] = df['total'].apply(lambda x: ast.literal_eval(x))

    # Create a new dataframe with the columns as the dictionary keys and the values as a list
    new_df = pd.DataFrame(df['total'].to_list(), index=df.index).add_prefix('total_')

    # Concatenate the new dataframe with the original dataframe
    df = pd.concat([df, new_df], axis=1)

    # Drop the original 'percent' column
    df = df.drop('total', axis=1)

    df['average'] = df['average'].apply(lambda x: ast.literal_eval(x))

    # Create a new dataframe with the columns as the dictionary keys and the values as a list
    new_df = pd.DataFrame(df['average'].to_list(), index=df.index).add_prefix('average_')

    # Concatenate the new dataframe with the original dataframe
    df = pd.concat([df, new_df], axis=1)


    # Drop the original 'percent' column
    df = df.drop('average', axis=1)
    df['position_codes'] = df['position_codes'].astype(str)
    #df['date'] = df['date'].astype(str)
    #df['date'] = df['date'].apply(lambda x: parser.parse(x))

    # Sort the dataframe by the 'date' column
    #df = df.sort_values(by='date',ascending=False)

    # Format the 'date' column to day-month-year format
    #df['date'] = df['date'].apply(lambda x: x.strftime('%d-%m-%Y'))
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date',ascending=False)

    df_backs = df[df['position_codes'].str.contains('|'.join(['lb', 'rb']))]
    df_backs = df_backs[df_backs['total_minutesOnField'] >= tidprkamp]
    df_backsminutter = df_backs[['Player name','Team name','total_minutesOnField']]
    df_backsminutter = df_backsminutter.groupby(['Player id']).sum(numeric_only=True)
    df_backsminutter = df_backsminutter[df_backsminutter['total_minutesOnField'] >= samlettid]

    df_Stoppere = df[df['position_codes'].str.contains('|'.join(['cb']))]
    df_Stoppere = df_Stoppere[df_Stoppere['total_minutesOnField'] >= tidprkamp]
    df_stoppereminutter = df_Stoppere[['Player name','Team name','total_minutesOnField']]
    df_stoppereminutter = df_stoppereminutter.groupby(['Player id']).sum(numeric_only=True)
    df_stoppereminutter = df_stoppereminutter[df_stoppereminutter['total_minutesOnField'] >= samlettid]

    df_Centrale_midt = df[df['position_codes'].str.contains('|'.join(['cm','amf','dmf']))]
    df_Centrale_midt = df_Centrale_midt[df_Centrale_midt['total_minutesOnField'] >= tidprkamp]
    df_centraleminutter = df_Centrale_midt[['Player name','Team name','total_minutesOnField']]
    df_centraleminutter = df_centraleminutter.groupby(['Player id']).sum(numeric_only=True)
    df_centraleminutter = df_centraleminutter[df_centraleminutter['total_minutesOnField'] >= samlettid]

    df_Kanter = df[df['position_codes'].str.contains('|'.join(['rw','lw','ramf','lamf']))]
    df_Kanter = df_Kanter[df_Kanter['total_minutesOnField'] >=tidprkamp]
    df_kanterminutter = df_Kanter[['Player name','Team name','total_minutesOnField']]
    df_kanterminutter = df_kanterminutter.groupby(['Player id']).sum(numeric_only=True)
    df_kanterminutter = df_kanterminutter[df_kanterminutter['total_minutesOnField'] >=samlettid]


    df_Angribere = df[df['position_codes'].str.contains('|'.join(['cf','ss']))]
    df_Angribere = df_Angribere[df_Angribere['total_minutesOnField'] >= tidprkamp]
    df_angribereminutter = df_Angribere[['Player name','Team name','total_minutesOnField']]
    df_angribereminutter = df_angribereminutter.groupby(['Player id']).sum(numeric_only=True)
    df_angribereminutter = df_angribereminutter[df_angribereminutter['total_minutesOnField'] >= samlettid]


    df_backs = pd.merge(df_backsminutter,df_backs,on=('Player id'))
    df_backs = df_backs[df_backs['total_minutesOnField_y'] >=tidprkamp]

    df_backs['Accurate crosses score'] = pd.qcut(df_backs['percent_successfulCrosses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_backs['Number of crosses score'] = pd.qcut(df_backs['average_crosses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_backs['XA score'] = pd.qcut(df_backs['average_xgAssist'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_backs['Passes to final third score'] = pd.qcut(df_backs['average_successfulPassesToFinalThird'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_backs['Successful dribbles score'] = pd.qcut(df_backs['percent_newSuccessfulDribbles'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_backs['Defensive duels won score'] = pd.qcut(df_backs['percent_newDefensiveDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_backs['Progressive runs score'] = pd.qcut(df_backs['average_progressiveRun'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_backs['Offensive duels won score'] = pd.qcut(df_backs['percent_newOffensiveDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_backs['Accelerations score'] = pd.qcut(df_backs['average_accelerations'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_backs['Duels won score'] = pd.qcut(df_backs['percent_newDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_backs['Interceptions score'] = pd.qcut(df_backs['average_interceptions'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_backs['Successful defensive actions score'] = pd.qcut(df_backs['average_successfulDefensiveAction'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_backssæsonen = df_backs[['label','Player name','Team name','total_minutesOnField_x','total_minutesOnField_y','Number of crosses score','Accurate crosses score','XA score','Passes to final third score','Successful dribbles score','Defensive duels won score','Progressive runs score','Offensive duels won score','Accelerations score','Duels won score','Interceptions score','Successful defensive actions score']]
    df_backssæsonen.rename(columns={'total_minutesOnField_x':'Total minutes'},inplace=True)
    df_backssæsonen = df_backssæsonen.groupby(['Player name','Team name','Total minutes','label']).mean(numeric_only=True)

    df_backssæsonen['Indlægsstærk'] = (df_backssæsonen['Number of crosses score'] + df_backssæsonen['Accurate crosses score'] + df_backssæsonen['XA score'] + df_backssæsonen['Passes to final third score'])/4
    df_backssæsonen['1v1 færdigheder'] = (df_backssæsonen['Successful dribbles score'] + df_backssæsonen['Defensive duels won score'] + df_backssæsonen['Progressive runs score'] + df_backssæsonen['Offensive duels won score'] + df_backssæsonen['Accelerations score'] + df_backssæsonen['Duels won score'])/6
    df_backssæsonen['Spilintelligens defensivt'] = (df_backssæsonen['Interceptions score'] + df_backssæsonen['Successful defensive actions score'] + df_backssæsonen['Duels won score'] + df_backssæsonen['Defensive duels won score'])/4
    df_backssæsonen['Fart'] = (df_backssæsonen['Successful dribbles score'] + df_backssæsonen['Progressive runs score'] + df_backssæsonen['Offensive duels won score'] + df_backssæsonen['Accelerations score'])/4
    df_backssæsonen ['Samlet'] = (df_backssæsonen['Indlægsstærk'] + df_backssæsonen['1v1 færdigheder'] + df_backssæsonen['Spilintelligens defensivt'] + df_backssæsonen['Fart'])/4

    df_backssæsonen = df_backssæsonen[['Indlægsstærk','1v1 færdigheder','Spilintelligens defensivt','Fart','Samlet']]
    df_backssæsonen = df_backssæsonen.round(3).astype(float)
    df_backssæsonen = df_backssæsonen.sort_values(by='Samlet',ascending=False)
    with st.expander('Backs kamp for kamp'):
        st.write(df_backssæsonen)
    df_backssæsonen = df_backssæsonen.reset_index()
    df_backssæsonen = df_backssæsonen.drop('label',axis=1)
    df_backssæsonen = df_backssæsonen.groupby(['Player name','Team name','Total minutes']).mean(numeric_only=True)
    df_backssæsonen = df_backssæsonen.sort_values(by='Samlet',ascending=False)
    with st.expander('Backs'):
        st.dataframe(df_backssæsonen)
       
    df_Stoppere = pd.merge(df_stoppereminutter,df_Stoppere,on=('Player id'))
    df_Stoppere = df_Stoppere[df_Stoppere['total_minutesOnField_y'] >=tidprkamp]
    
    df_Stoppere['Accurate passes score'] = pd.qcut(df_Stoppere['percent_successfulPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Accurate long passes score'] = pd.qcut(df_Stoppere['percent_successfulLongPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Forward passes score'] = pd.qcut(df_Stoppere['average_successfulForwardPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Accurate forward passes score'] = pd.qcut(df_Stoppere['percent_successfulForwardPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Accurate progressive passes score'] = pd.qcut(df_Stoppere['percent_successfulProgressivePasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Accurate vertical passes score'] = pd.qcut(df_Stoppere['percent_successfulVerticalPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Interceptions score'] = pd.qcut(df_Stoppere['average_interceptions'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Succesful defensive actions score'] = pd.qcut(df_Stoppere['average_successfulDefensiveAction'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Shots blocked score'] = pd.qcut(df_Stoppere['average_shotsBlocked'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Defensive duels won score'] = pd.qcut(df_Stoppere['average_newDefensiveDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Defensive duels won % score'] = pd.qcut(df_Stoppere['percent_newDefensiveDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Accurate passes to final third'] = pd.qcut(df_Stoppere['percent_successfulPassesToFinalThird'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Accurate through passes'] = pd.qcut(df_Stoppere['percent_successfulThroughPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Vertical passes'] = pd.qcut(df_Stoppere['average_successfulVerticalPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Through passes'] = pd.qcut(df_Stoppere['average_successfulThroughPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Passes to final third'] = pd.qcut(df_Stoppere['average_successfulPassesToFinalThird'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Progressive runs'] = pd.qcut(df_Stoppere['average_progressiveRun'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Offensive duels won %'] = pd.qcut(df_Stoppere['percent_newOffensiveDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Successful dribbles %'] = pd.qcut(df_Stoppere['percent_newSuccessfulDribbles'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Progressive passes score'] = pd.qcut(df_Stoppere['average_successfulProgressivePasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Aerial duels won score'] = pd.qcut(df_Stoppere['average_fieldAerialDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Aerial duels won % score'] = pd.qcut(df_Stoppere['percent_aerialDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)

    df_Stopperesæsonen = df_Stoppere[['label','Player name','Team name','total_minutesOnField_x','total_minutesOnField_y','Accurate passes score','Accurate long passes score','Forward passes score','Accurate forward passes score','Accurate progressive passes score','Accurate vertical passes score','Interceptions score','Succesful defensive actions score','Shots blocked score','Defensive duels won score','Defensive duels won % score','Accurate passes to final third','Accurate through passes','Vertical passes','Through passes','Passes to final third','Progressive passes score','Aerial duels won score','Aerial duels won % score','Progressive runs','Offensive duels won %','Successful dribbles %']]
    df_Stopperesæsonen.rename(columns={'total_minutesOnField_x':'Total minutes'},inplace=True)
    df_Stopperesæsonen = df_Stopperesæsonen.groupby(['Player name','Team name','Total minutes','label']).mean(numeric_only=True)
    df_Stopperesæsonen['Pasningssikker'] = (df_Stopperesæsonen['Accurate passes score'] + df_Stopperesæsonen['Accurate long passes score'] + df_Stopperesæsonen['Forward passes score'] + df_Stopperesæsonen['Accurate forward passes score'] + df_Stopperesæsonen['Accurate progressive passes score'] + df_Stopperesæsonen['Accurate vertical passes score'])/6
    df_Stopperesæsonen['Spilintelligens defensivt'] = (df_Stopperesæsonen['Interceptions score'] + df_Stopperesæsonen['Succesful defensive actions score'] + df_Stopperesæsonen['Shots blocked score'] + df_Stopperesæsonen['Succesful defensive actions score'] + df_Stopperesæsonen['Defensive duels won % score']) /5
    df_Stopperesæsonen['Spilintelligens offensivt'] = (df_Stopperesæsonen['Forward passes score'] + df_Stopperesæsonen['Accurate forward passes score'] + df_Stopperesæsonen['Accurate passes to final third'] + df_Stopperesæsonen['Passes to final third'] + df_Stopperesæsonen['Accurate progressive passes score'] + df_Stopperesæsonen['Progressive passes score'] + df_Stopperesæsonen['Through passes'] + df_Stopperesæsonen['Accurate through passes']+ df_Stopperesæsonen['Progressive runs'] + df_Stopperesæsonen['Offensive duels won %'] + df_Stopperesæsonen['Successful dribbles %'])/11
    df_Stopperesæsonen['Nærkamps- og duelstærk'] = (df_Stopperesæsonen['Defensive duels won % score'] + df_Stopperesæsonen['Aerial duels won % score'] + df_Stopperesæsonen['Defensive duels won % score'])/3
    df_Stopperesæsonen['Samlet'] = (df_Stopperesæsonen['Pasningssikker'] + df_Stopperesæsonen['Spilintelligens defensivt'] + df_Stopperesæsonen['Spilintelligens offensivt'] + df_Stopperesæsonen['Nærkamps- og duelstærk'])/4

    df_Stopperesæsonen = df_Stopperesæsonen[['Pasningssikker','Spilintelligens defensivt','Spilintelligens offensivt','Nærkamps- og duelstærk','Samlet']]
    df_Stopperesæsonen = df_Stopperesæsonen.sort_values(by='Samlet',ascending=False)

    with st.expander('Stoppere kamp for kamp'):
        st.write(df_Stopperesæsonen)
    df_Stopperesæsonen = df_Stopperesæsonen.reset_index()
    df_Stopperesæsonen = df_Stopperesæsonen.drop('label',axis=1)
    df_Stopperesæsonen = df_Stopperesæsonen.groupby(['Player name','Team name','Total minutes']).mean(numeric_only=True)
    df_Stopperesæsonen = df_Stopperesæsonen.sort_values(by='Samlet',ascending=False)
    
    with st.expander('Stoppere sæson'):
        st.dataframe(df_Stopperesæsonen)

    df_Centrale_midt = pd.merge(df_centraleminutter,df_Centrale_midt,on=('Player id'))
    df_Centrale_midt = df_Centrale_midt[df_Centrale_midt['total_minutesOnField_y'] >=tidprkamp]

    df_Centrale_midt['Passes %'] = pd.qcut(df_Centrale_midt['percent_successfulPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Passes #'] = pd.qcut(df_Centrale_midt['average_successfulPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Forward Passes %'] = pd.qcut(df_Centrale_midt['percent_successfulForwardPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Forward Passes #'] = pd.qcut(df_Centrale_midt['average_successfulForwardPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Long Passes %'] = pd.qcut(df_Centrale_midt['percent_successfulLongPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Long Passes #'] = pd.qcut(df_Centrale_midt['average_successfulLongPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Smart passes %'] = pd.qcut(df_Centrale_midt['percent_successfulSmartPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Smart passes #'] = pd.qcut(df_Centrale_midt['average_successfulSmartPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Key passes %'] = pd.qcut(df_Centrale_midt['percent_successfulKeyPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Key passes #'] = pd.qcut(df_Centrale_midt['average_successfulKeyPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Passes to final third %'] = pd.qcut(df_Centrale_midt['percent_successfulPassesToFinalThird'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Passes to final third #'] = pd.qcut(df_Centrale_midt['average_successfulPassesToFinalThird'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Vertical passes %'] = pd.qcut(df_Centrale_midt['percent_successfulVerticalPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Vertical passes #'] = pd.qcut(df_Centrale_midt['average_successfulVerticalPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Through passes %'] = pd.qcut(df_Centrale_midt['percent_successfulThroughPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Through passes #'] = pd.qcut(df_Centrale_midt['average_successfulThroughPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Progressive passes %'] = pd.qcut(df_Centrale_midt['percent_successfulProgressivePasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Progressive passes #'] = pd.qcut(df_Centrale_midt['average_successfulProgressivePasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Offensive duels %'] = pd.qcut(df_Centrale_midt['percent_newOffensiveDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Received passes'] = pd.qcut(df_Centrale_midt['average_receivedPass'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Succesful dribbles %'] = pd.qcut(df_Centrale_midt['percent_newSuccessfulDribbles'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Succesful dribbles #'] = pd.qcut(df_Centrale_midt['average_newSuccessfulDribbles'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Duels won %'] = pd.qcut(df_Centrale_midt['percent_newDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Duels won #'] = pd.qcut(df_Centrale_midt['average_newDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Interceptions'] = pd.qcut(df_Centrale_midt['average_interceptions'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Counterpressing recoveries #'] = pd.qcut(df_Centrale_midt['average_counterpressingRecoveries'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Defensive duels won #'] = pd.qcut(df_Centrale_midt['average_newDefensiveDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Defensive duels won %'] = pd.qcut(df_Centrale_midt['percent_newDefensiveDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)

    df_Centrale_midtsæsonen = df_Centrale_midt.rename(columns={'total_minutesOnField_x':'Total minutes'},inplace=True)
    df_Centrale_midtsæsonen = df_Centrale_midt.groupby(['Player name','Team name','Total minutes','label']).mean(numeric_only=True)
    df_Centrale_midtsæsonen['Pasningssikker/Spilvendinger'] = (df_Centrale_midtsæsonen['Passes %'] + df_Centrale_midtsæsonen['Passes #'] + df_Centrale_midtsæsonen['Forward Passes %'] + df_Centrale_midtsæsonen['Forward Passes #'] + df_Centrale_midtsæsonen['Long Passes %'] + df_Centrale_midtsæsonen['Long Passes #']+ df_Centrale_midtsæsonen['Smart passes %'] + df_Centrale_midtsæsonen['Smart passes #'] + + df_Centrale_midtsæsonen['Key passes %'] + df_Centrale_midtsæsonen['Key passes #'] + df_Centrale_midtsæsonen['Passes to final third %'] + df_Centrale_midtsæsonen['Passes to final third #']+ df_Centrale_midtsæsonen['Vertical passes %'] + df_Centrale_midtsæsonen['Vertical passes #']+ df_Centrale_midtsæsonen['Through passes %'] + df_Centrale_midtsæsonen['Through passes #']+ df_Centrale_midtsæsonen['Progressive passes %'] + df_Centrale_midtsæsonen['Progressive passes #'])/18
    df_Centrale_midtsæsonen['Boldfast'] = (df_Centrale_midtsæsonen['Passes %'] + df_Centrale_midtsæsonen['Passes #']+ df_Centrale_midtsæsonen['Offensive duels %'] + df_Centrale_midtsæsonen['Received passes'] + df_Centrale_midtsæsonen['Succesful dribbles %'] + df_Centrale_midtsæsonen['Succesful dribbles #'])/6
    df_Centrale_midtsæsonen['Spilintelligens defensivt'] = (df_Centrale_midtsæsonen['Duels won %'] + df_Centrale_midtsæsonen['Duels won #'] +df_Centrale_midtsæsonen['Interceptions'] + df_Centrale_midtsæsonen['Counterpressing recoveries #'] + df_Centrale_midtsæsonen['Defensive duels won %'] + df_Centrale_midtsæsonen['Defensive duels won #'])/6
    df_Centrale_midtsæsonen['Samlet'] = (df_Centrale_midtsæsonen['Pasningssikker/Spilvendinger'] + df_Centrale_midtsæsonen['Boldfast'] + df_Centrale_midtsæsonen['Spilintelligens defensivt'])/3

    df_Centrale_midtsæsonen = df_Centrale_midtsæsonen[['Pasningssikker/Spilvendinger','Boldfast','Spilintelligens defensivt','Samlet']]
    df_Centrale_midtsæsonen = df_Centrale_midtsæsonen.sort_values(by='Samlet',ascending=False)
    with st.expander('Centrale midt kamp for kamp'):
        st.write(df_Centrale_midtsæsonen)

    df_Centrale_midtsæsonen = df_Centrale_midtsæsonen.reset_index()
    df_Centrale_midtsæsonen = df_Centrale_midtsæsonen.drop('label',axis=1)
    df_Centrale_midtsæsonen = df_Centrale_midtsæsonen.groupby(['Player name','Team name','Total minutes']).mean(numeric_only=True)
    df_Centrale_midtsæsonen = df_Centrale_midtsæsonen.sort_values(by='Samlet',ascending=False)
    with st.expander('Centrale midt sæson'):
        st.write(df_Centrale_midtsæsonen)


    df_Kanter = pd.merge(df_kanterminutter,df_Kanter,on=('Player id'))
    df_Kanter = df_Kanter[df_Kanter['total_minutesOnField_y'] >=tidprkamp]

    df_Kanter['Shots on target %'] = pd.qcut(df_Kanter['percent_shotsOnTarget'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Shots on target #'] = pd.qcut(df_Kanter['average_shotsOnTarget'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['XG'] = pd.qcut(df_Kanter['average_xgShot'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Successful dribbles #'] = pd.qcut(df_Kanter['average_newSuccessfulDribbles'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Successful dribbles %'] = pd.qcut(df_Kanter['percent_newSuccessfulDribbles'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Offensive duels %'] = pd.qcut(df_Kanter['percent_newOffensiveDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Offensive duels #'] = pd.qcut(df_Kanter['average_newOffensiveDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Passes %'] = pd.qcut(df_Kanter['percent_successfulPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Passes #'] = pd.qcut(df_Kanter['average_successfulPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Forward Passes %'] = pd.qcut(df_Kanter['percent_successfulForwardPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Forward Passes #'] = pd.qcut(df_Kanter['average_successfulForwardPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Smart passes %'] = pd.qcut(df_Kanter['percent_successfulSmartPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Smart passes #'] = pd.qcut(df_Kanter['average_successfulSmartPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Key passes %'] = pd.qcut(df_Kanter['percent_successfulKeyPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Key passes #'] = pd.qcut(df_Kanter['average_successfulKeyPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Passes to final third %'] = pd.qcut(df_Kanter['percent_successfulPassesToFinalThird'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Passes to final third #'] = pd.qcut(df_Kanter['average_successfulPassesToFinalThird'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Vertical passes %'] = pd.qcut(df_Kanter['percent_successfulVerticalPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Vertical passes #'] = pd.qcut(df_Kanter['average_successfulVerticalPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Through passes %'] = pd.qcut(df_Kanter['percent_successfulThroughPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Through passes #'] = pd.qcut(df_Kanter['average_successfulThroughPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Progressive passes %'] = pd.qcut(df_Kanter['percent_successfulProgressivePasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Progressive passes #'] = pd.qcut(df_Kanter['average_successfulProgressivePasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Goal conversion %'] = pd.qcut(df_Kanter['percent_goalConversion'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['XG per 90'] = pd.qcut(df_Kanter['average_xgShot'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['XA per 90'] = pd.qcut(df_Kanter['average_xgAssist'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Successful attacking actions'] = pd.qcut(df_Kanter['average_successfulAttackingActions'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Progressive runs'] = pd.qcut(df_Kanter['average_progressiveRun'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Accelerations score'] = pd.qcut(df_Kanter['average_accelerations'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)

    df_Kantersæsonen = df_Kanter.rename(columns={'total_minutesOnField_x':'Total minutes'},inplace=True)
    df_Kantersæsonen = df_Kanter.groupby(['Player name','Team name','Total minutes','label']).mean(numeric_only=True)

    df_Kantersæsonen['Sparkefærdigheder'] = (df_Kantersæsonen['Shots on target %'] + df_Kantersæsonen['Shots on target #'] + df_Kantersæsonen['XG'] + df_Kantersæsonen['Passes to final third %'] + df_Kantersæsonen['Forward Passes %'] + df_Kantersæsonen['Vertical passes %'])/6
    df_Kantersæsonen['Kombinationsstærk'] = (df_Kantersæsonen['Passes %'] + df_Kantersæsonen['Passes #'] + df_Kantersæsonen['Forward Passes %'] + df_Kantersæsonen['Forward Passes #'] + df_Kantersæsonen['Passes to final third %'] + df_Kantersæsonen['Passes to final third #'] + df_Kantersæsonen['Through passes %'] + df_Kantersæsonen['Through passes #'] + df_Kantersæsonen['Progressive passes %'] + df_Kantersæsonen['Progressive passes #'] + df_Kantersæsonen['Successful attacking actions'])/11
    df_Kantersæsonen['Spilintelligens offensivt/indlægsstærk'] = (df_Kantersæsonen['XA per 90'] + df_Kantersæsonen['XG per 90'] + df_Kantersæsonen['Through passes %'] + df_Kantersæsonen['Through passes #'] + df_Kantersæsonen['Smart passes %'] + df_Kantersæsonen['Smart passes #'] + df_Kantersæsonen['Progressive passes %'] + df_Kantersæsonen['Progressive passes #'] + df_Kantersæsonen['Key passes %'] + df_Kantersæsonen['Key passes #'] + df_Kantersæsonen['Successful attacking actions'])/11
    df_Kantersæsonen['1v1 offensivt'] = (df_Kantersæsonen['Successful dribbles #'] + df_Kantersæsonen['Successful dribbles %'] + df_Kantersæsonen['Offensive duels #'] + df_Kantersæsonen['Offensive duels %'] + df_Kantersæsonen['Progressive runs'])/5
    df_Kantersæsonen['Fart'] = (df_Kantersæsonen['Progressive runs'] + df_Kantersæsonen['Successful dribbles #'] + df_Kantersæsonen['Successful dribbles %'] + df_Kantersæsonen['Accelerations score'])/4
    df_Kantersæsonen['Samlet'] = (df_Kantersæsonen['Sparkefærdigheder'] + df_Kantersæsonen['Kombinationsstærk'] + df_Kantersæsonen['Spilintelligens offensivt/indlægsstærk'] + df_Kantersæsonen['1v1 offensivt'] + df_Kantersæsonen['Fart'])/5
    df_Kantersæsonen = df_Kantersæsonen[['Sparkefærdigheder','Kombinationsstærk','Spilintelligens offensivt/indlægsstærk','1v1 offensivt','Fart','Samlet']]
    df_Kantersæsonen = df_Kantersæsonen.sort_values(by='Samlet',ascending=False)

    with st.expander('Kanter kamp for kamp'):
        st.write(df_Kantersæsonen)

    df_Kantersæsonen = df_Kantersæsonen.reset_index()
    df_Kantersæsonen = df_Kantersæsonen.drop('label',axis=1)
    df_Kantersæsonen = df_Kantersæsonen.groupby(['Player name','Team name','Total minutes']).mean(numeric_only=True)
    df_Kantersæsonen = df_Kantersæsonen.sort_values(by='Samlet',ascending=False)
    with st.expander('Kanter sæson'):
        st.write(df_Kantersæsonen)


    df_Angribere = pd.merge(df_angribereminutter,df_Angribere,on=('Player id'))
    df_Angribere = df_Angribere[df_Angribere['total_minutesOnField_y'] >=tidprkamp]

    df_Angribere['Målfarlighed udregning'] = df_Angribere['average_goals'] - df_Angribere['average_xgShot']
    df_Angribere['Målfarlighed score'] =  pd.qcut(df_Angribere['Målfarlighed udregning'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Angribere['xG per 90 score'] = pd.qcut(df_Angribere['average_xgShot'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Angribere['Goals per 90 score'] = pd.qcut(df_Angribere['average_goals'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)  
    df_Angribere['Shots on target, % score'] = pd.qcut(df_Angribere['percent_shotsOnTarget'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)   
    df_Angribere['Offensive duels won, % score'] = pd.qcut(df_Angribere['percent_newOffensiveDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Angribere['Duels won, % score'] = pd.qcut(df_Angribere['percent_newDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Angribere['Accurate passes, % score'] = pd.qcut(df_Angribere['percent_successfulPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Angribere['Successful dribbles, % score'] = pd.qcut(df_Angribere['percent_newSuccessfulDribbles'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Angribere['xA per 90 score'] = pd.qcut(df_Angribere['average_xgAssist'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Angribere['Touches in box per 90 score'] = pd.qcut(df_Angribere['average_touchInBox'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Angribere['Progressive runs'] = pd.qcut(df_Angribere['average_progressiveRun'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Angribere['Accelerations score'] = pd.qcut(df_Angribere['average_accelerations'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Angribere['Progressive passes per 90 score'] = pd.qcut(df_Angribere['average_successfulProgressivePasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Angribere['Successful attacking actions per 90 score'] = pd.qcut(df_Angribere['average_successfulAttackingActions'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Angribere['Successful dribbles #'] = pd.qcut(df_Angribere['average_newSuccessfulDribbles'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)

    df_Angriberesæsonen = df_Angribere.rename(columns={'total_minutesOnField_x':'Total minutes'},inplace=True)
    df_Angriberesæsonen = df_Angribere.groupby(['Player name','Team name','Total minutes','label']).mean(numeric_only=True)

    df_Angriberesæsonen['Sparkefærdigheder'] = (df_Angriberesæsonen['xG per 90 score'] + df_Angriberesæsonen['xG per 90 score'] + df_Angriberesæsonen['Goals per 90 score'] + df_Angriberesæsonen['Shots on target, % score'])/4
    df_Angriberesæsonen['Boldfast'] = (df_Angriberesæsonen['Offensive duels won, % score'] + df_Angriberesæsonen['Offensive duels won, % score'] + df_Angriberesæsonen['Duels won, % score'] + df_Angriberesæsonen['Accurate passes, % score'] + df_Angriberesæsonen['Successful dribbles, % score'])/5
    df_Angriberesæsonen['Spilintelligens offensivt'] = (df_Angriberesæsonen['xA per 90 score'] + df_Angriberesæsonen['xG per 90 score'] + df_Angriberesæsonen['Touches in box per 90 score'] + df_Angriberesæsonen['Progressive passes per 90 score'] + df_Angriberesæsonen['Successful attacking actions per 90 score'] + df_Angriberesæsonen['Touches in box per 90 score'] + df_Angriberesæsonen['xG per 90 score'])/7
    df_Angriberesæsonen['Målfarlighed'] = (df_Angriberesæsonen['xG per 90 score']+df_Angriberesæsonen['Goals per 90 score']+df_Angriberesæsonen['xG per 90 score'] + df_Angriberesæsonen['Målfarlighed score'])/4
    df_Angriberesæsonen['Fart'] = (df_Angriberesæsonen['Progressive runs'] + + df_Angriberesæsonen['Progressive runs'] + df_Angriberesæsonen['Progressive runs'] + df_Angriberesæsonen['Successful dribbles #'] + df_Angriberesæsonen['Successful dribbles, % score'] + df_Angriberesæsonen['Accelerations score'] + df_Angriberesæsonen['Offensive duels won, % score'])/7
    df_Angriberesæsonen = df_Angriberesæsonen[['Sparkefærdigheder','Boldfast','Spilintelligens offensivt','Målfarlighed','Fart']]
    df_Angriberesæsonen['Samlet'] = (df_Angriberesæsonen['Sparkefærdigheder']+df_Angriberesæsonen['Boldfast']+df_Angriberesæsonen['Spilintelligens offensivt']+df_Angriberesæsonen['Målfarlighed']+df_Angriberesæsonen['Målfarlighed']+df_Angriberesæsonen['Målfarlighed']+df_Angriberesæsonen['Fart'])/7
    df_Angriberesæsonen = df_Angriberesæsonen.sort_values(by='Samlet',ascending=False)

    with st.expander('Angribere kamp for kamp'):
        st.write(df_Angriberesæsonen)

    df_Angriberesæsonen = df_Angriberesæsonen.reset_index()
    df_Angriberesæsonen = df_Angriberesæsonen.drop('label',axis=1)
    df_Angriberesæsonen = df_Angriberesæsonen.groupby(['Player name','Team name','Total minutes']).mean(numeric_only=True)
    df_Angriberesæsonen = df_Angriberesæsonen.sort_values(by='Samlet',ascending=False)
    with st.expander('Angribere sæson'):
        st.write(df_Angriberesæsonen)
    df = pd.read_csv(r'xT/U19 Ligaen 23 24.csv')

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


    dfscore = pd.read_csv(r'xT/Zone scores.csv')

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

    xgc = df1
    xgchold = xgc.rename(columns={'shot.xg': 'Hold xG'})
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

def U19_Division ():
    col1,col2 = st.columns(2)
    with col1:
        samlettid = st.number_input('Minutter i sæsonen')
    with col2:    
        tidprkamp = st.number_input('Minutter pr. kamp')
        
    df = pd.read_csv(r'Individuelt dashboard/Individuelt dashboard U19 div.csv')
    df.rename(columns={'playerId': 'Player id'}, inplace=True)
    df = df.astype(str)
    dfevents = pd.read_csv('U19 div eventdata alle.csv',low_memory=False)
    dfevents = dfevents[['Player id','Player name','team_name','label','date','matchId']]
    dfspillernavn = df[['Player id','matchId','positions','average','percent','total']]
    dfspillernavn = dfspillernavn.astype(str)
    dfevents['Player id'] = dfevents['Player id'].astype(str)
    dfevents['matchId'] = dfevents['matchId'].astype(str)
    df = dfspillernavn.merge(dfevents)

    df['Player&matchId'] = df['Player id'] + df['matchId']
    df['Player&matchId'] = df['Player&matchId'].drop_duplicates(keep='first')
    df = df.dropna()
    df = df[['Player id','Player name','team_name','matchId','label','date','positions','average','percent','total']]

    #df = df.set_index('Player id')

    data = df['positions']
    df1 = pd.DataFrame(data)
    # Funktion, der ekstraherer navne og koder fra strengdata og opretter en ny kolonne med disse værdier
    def extract_positions(data):
        positions_list = ast.literal_eval(data) # Konverterer strengen til en liste af ordbøger
        names = [pos['position']['name'] for pos in positions_list]
        codes = [pos['position']['code'] for pos in positions_list]
        return pd.Series({'position_names': names, 'position_codes': codes})

    # Anvender funktionen på kolonnen og tilføjer resultaterne som nye kolonner til dataframe
    df1[['position_names', 'position_codes']] = df1['positions'].apply(extract_positions)

    df = pd.merge(df,df1,left_index=True, right_index=True)
    df = df.set_index('Player id')
    df = df.drop(columns=['positions_x'])
    df = df.drop(columns=['positions_y'])
    df = df[['Player name','team_name','matchId','label','date','position_names','position_codes','average','percent','total']]
    df = df.rename(columns={'team_name':'Team name'})
    df['percent'] = df['percent'].apply(lambda x: ast.literal_eval(x))

    # Create a new dataframe with the columns as the dictionary keys and the values as a list
    new_df = pd.DataFrame(df['percent'].to_list(), index=df.index).add_prefix('percent_')

    # Concatenate the new dataframe with the original dataframe
    df = pd.concat([df, new_df], axis=1)

    # Drop the original 'percent' column
    df = df.drop('percent', axis=1)

    df['total'] = df['total'].apply(lambda x: ast.literal_eval(x))

    # Create a new dataframe with the columns as the dictionary keys and the values as a list
    new_df = pd.DataFrame(df['total'].to_list(), index=df.index).add_prefix('total_')

    # Concatenate the new dataframe with the original dataframe
    df = pd.concat([df, new_df], axis=1)

    # Drop the original 'percent' column
    df = df.drop('total', axis=1)

    df['average'] = df['average'].apply(lambda x: ast.literal_eval(x))

    # Create a new dataframe with the columns as the dictionary keys and the values as a list
    new_df = pd.DataFrame(df['average'].to_list(), index=df.index).add_prefix('average_')

    # Concatenate the new dataframe with the original dataframe
    df = pd.concat([df, new_df], axis=1)


    # Drop the original 'percent' column
    df = df.drop('average', axis=1)
    df['position_codes'] = df['position_codes'].astype(str)
    #df['date'] = df['date'].astype(str)
    #df['date'] = df['date'].apply(lambda x: parser.parse(x))

    # Sort the dataframe by the 'date' column
    #df = df.sort_values(by='date',ascending=False)

    # Format the 'date' column to day-month-year format
    #df['date'] = df['date'].apply(lambda x: x.strftime('%d-%m-%Y'))
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date',ascending=False)

    df_backs = df[df['position_codes'].str.contains('|'.join(['lb', 'rb']))]
    df_backs = df_backs[df_backs['total_minutesOnField'] >= tidprkamp]
    df_backsminutter = df_backs[['Player name','Team name','total_minutesOnField']]
    df_backsminutter = df_backsminutter.groupby(['Player id']).sum(numeric_only=True)
    df_backsminutter = df_backsminutter[df_backsminutter['total_minutesOnField'] >= samlettid]

    df_Stoppere = df[df['position_codes'].str.contains('|'.join(['cb']))]
    df_Stoppere = df_Stoppere[df_Stoppere['total_minutesOnField'] >= tidprkamp]
    df_stoppereminutter = df_Stoppere[['Player name','Team name','total_minutesOnField']]
    df_stoppereminutter = df_stoppereminutter.groupby(['Player id']).sum(numeric_only=True)
    df_stoppereminutter = df_stoppereminutter[df_stoppereminutter['total_minutesOnField'] >= samlettid]

    df_Centrale_midt = df[df['position_codes'].str.contains('|'.join(['cm','amf','dmf']))]
    df_Centrale_midt = df_Centrale_midt[df_Centrale_midt['total_minutesOnField'] >= tidprkamp]
    df_centraleminutter = df_Centrale_midt[['Player name','Team name','total_minutesOnField']]
    df_centraleminutter = df_centraleminutter.groupby(['Player id']).sum(numeric_only=True)
    df_centraleminutter = df_centraleminutter[df_centraleminutter['total_minutesOnField'] >= samlettid]

    df_Kanter = df[df['position_codes'].str.contains('|'.join(['rw','lw','ramf','lamf']))]
    df_Kanter = df_Kanter[df_Kanter['total_minutesOnField'] >=tidprkamp]
    df_kanterminutter = df_Kanter[['Player name','Team name','total_minutesOnField']]
    df_kanterminutter = df_kanterminutter.groupby(['Player id']).sum(numeric_only=True)
    df_kanterminutter = df_kanterminutter[df_kanterminutter['total_minutesOnField'] >=samlettid]


    df_Angribere = df[df['position_codes'].str.contains('|'.join(['cf','ss']))]
    df_Angribere = df_Angribere[df_Angribere['total_minutesOnField'] >= tidprkamp]
    df_angribereminutter = df_Angribere[['Player name','Team name','total_minutesOnField']]
    df_angribereminutter = df_angribereminutter.groupby(['Player id']).sum(numeric_only=True)
    df_angribereminutter = df_angribereminutter[df_angribereminutter['total_minutesOnField'] >= samlettid]


    df_backs = pd.merge(df_backsminutter,df_backs,on=('Player id'))
    df_backs = df_backs[df_backs['total_minutesOnField_y'] >=tidprkamp]

    df_backs['Accurate crosses score'] = pd.qcut(df_backs['percent_successfulCrosses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_backs['Number of crosses score'] = pd.qcut(df_backs['average_crosses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_backs['XA score'] = pd.qcut(df_backs['average_xgAssist'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_backs['Passes to final third score'] = pd.qcut(df_backs['average_successfulPassesToFinalThird'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_backs['Successful dribbles score'] = pd.qcut(df_backs['percent_newSuccessfulDribbles'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_backs['Defensive duels won score'] = pd.qcut(df_backs['percent_newDefensiveDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_backs['Progressive runs score'] = pd.qcut(df_backs['average_progressiveRun'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_backs['Offensive duels won score'] = pd.qcut(df_backs['percent_newOffensiveDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_backs['Accelerations score'] = pd.qcut(df_backs['average_accelerations'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_backs['Duels won score'] = pd.qcut(df_backs['percent_newDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_backs['Interceptions score'] = pd.qcut(df_backs['average_interceptions'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_backs['Successful defensive actions score'] = pd.qcut(df_backs['average_successfulDefensiveAction'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_backssæsonen = df_backs[['label','Player name','Team name','total_minutesOnField_x','total_minutesOnField_y','Number of crosses score','Accurate crosses score','XA score','Passes to final third score','Successful dribbles score','Defensive duels won score','Progressive runs score','Offensive duels won score','Accelerations score','Duels won score','Interceptions score','Successful defensive actions score']]
    df_backssæsonen.rename(columns={'total_minutesOnField_x':'Total minutes'},inplace=True)
    df_backssæsonen = df_backssæsonen.groupby(['Player name','Team name','Total minutes','label']).mean(numeric_only=True)

    df_backssæsonen['Indlægsstærk'] = (df_backssæsonen['Number of crosses score'] + df_backssæsonen['Accurate crosses score'] + df_backssæsonen['XA score'] + df_backssæsonen['Passes to final third score'])/4
    df_backssæsonen['1v1 færdigheder'] = (df_backssæsonen['Successful dribbles score'] + df_backssæsonen['Defensive duels won score'] + df_backssæsonen['Progressive runs score'] + df_backssæsonen['Offensive duels won score'] + df_backssæsonen['Accelerations score'] + df_backssæsonen['Duels won score'])/6
    df_backssæsonen['Spilintelligens defensivt'] = (df_backssæsonen['Interceptions score'] + df_backssæsonen['Successful defensive actions score'] + df_backssæsonen['Duels won score'] + df_backssæsonen['Defensive duels won score'])/4
    df_backssæsonen['Fart'] = (df_backssæsonen['Successful dribbles score'] + df_backssæsonen['Progressive runs score'] + df_backssæsonen['Offensive duels won score'] + df_backssæsonen['Accelerations score'])/4
    df_backssæsonen ['Samlet'] = (df_backssæsonen['Indlægsstærk'] + df_backssæsonen['1v1 færdigheder'] + df_backssæsonen['Spilintelligens defensivt'] + df_backssæsonen['Fart'])/4

    df_backssæsonen = df_backssæsonen[['Indlægsstærk','1v1 færdigheder','Spilintelligens defensivt','Fart','Samlet']]
    df_backssæsonen = df_backssæsonen.round(3).astype(float)
    df_backssæsonen = df_backssæsonen.sort_values(by='Samlet',ascending=False)
    with st.expander('Backs kamp for kamp'):
        st.write(df_backssæsonen)
    df_backssæsonen = df_backssæsonen.reset_index()
    df_backssæsonen = df_backssæsonen.drop('label',axis=1)
    df_backssæsonen = df_backssæsonen.groupby(['Player name','Team name','Total minutes']).mean(numeric_only=True)
    df_backssæsonen = df_backssæsonen.sort_values(by='Samlet',ascending=False)
    with st.expander('Backs'):
        st.dataframe(df_backssæsonen)
       
    df_Stoppere = pd.merge(df_stoppereminutter,df_Stoppere,on=('Player id'))
    df_Stoppere = df_Stoppere[df_Stoppere['total_minutesOnField_y'] >=tidprkamp]
    
    df_Stoppere['Accurate passes score'] = pd.qcut(df_Stoppere['percent_successfulPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Accurate long passes score'] = pd.qcut(df_Stoppere['percent_successfulLongPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Forward passes score'] = pd.qcut(df_Stoppere['average_successfulForwardPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Accurate forward passes score'] = pd.qcut(df_Stoppere['percent_successfulForwardPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Accurate progressive passes score'] = pd.qcut(df_Stoppere['percent_successfulProgressivePasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Accurate vertical passes score'] = pd.qcut(df_Stoppere['percent_successfulVerticalPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Interceptions score'] = pd.qcut(df_Stoppere['average_interceptions'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Succesful defensive actions score'] = pd.qcut(df_Stoppere['average_successfulDefensiveAction'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Shots blocked score'] = pd.qcut(df_Stoppere['average_shotsBlocked'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Defensive duels won score'] = pd.qcut(df_Stoppere['average_newDefensiveDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Defensive duels won % score'] = pd.qcut(df_Stoppere['percent_newDefensiveDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Accurate passes to final third'] = pd.qcut(df_Stoppere['percent_successfulPassesToFinalThird'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Accurate through passes'] = pd.qcut(df_Stoppere['percent_successfulThroughPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Vertical passes'] = pd.qcut(df_Stoppere['average_successfulVerticalPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Through passes'] = pd.qcut(df_Stoppere['average_successfulThroughPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Passes to final third'] = pd.qcut(df_Stoppere['average_successfulPassesToFinalThird'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Progressive runs'] = pd.qcut(df_Stoppere['average_progressiveRun'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Offensive duels won %'] = pd.qcut(df_Stoppere['percent_newOffensiveDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Successful dribbles %'] = pd.qcut(df_Stoppere['percent_newSuccessfulDribbles'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Progressive passes score'] = pd.qcut(df_Stoppere['average_successfulProgressivePasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Aerial duels won score'] = pd.qcut(df_Stoppere['average_fieldAerialDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Aerial duels won % score'] = pd.qcut(df_Stoppere['percent_aerialDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)

    df_Stopperesæsonen = df_Stoppere[['label','Player name','Team name','total_minutesOnField_x','total_minutesOnField_y','Accurate passes score','Accurate long passes score','Forward passes score','Accurate forward passes score','Accurate progressive passes score','Accurate vertical passes score','Interceptions score','Succesful defensive actions score','Shots blocked score','Defensive duels won score','Defensive duels won % score','Accurate passes to final third','Accurate through passes','Vertical passes','Through passes','Passes to final third','Progressive passes score','Aerial duels won score','Aerial duels won % score','Progressive runs','Offensive duels won %','Successful dribbles %']]
    df_Stopperesæsonen.rename(columns={'total_minutesOnField_x':'Total minutes'},inplace=True)
    df_Stopperesæsonen = df_Stopperesæsonen.groupby(['Player name','Team name','Total minutes','label']).mean(numeric_only=True)
    df_Stopperesæsonen['Pasningssikker'] = (df_Stopperesæsonen['Accurate passes score'] + df_Stopperesæsonen['Accurate long passes score'] + df_Stopperesæsonen['Forward passes score'] + df_Stopperesæsonen['Accurate forward passes score'] + df_Stopperesæsonen['Accurate progressive passes score'] + df_Stopperesæsonen['Accurate vertical passes score'])/6
    df_Stopperesæsonen['Spilintelligens defensivt'] = (df_Stopperesæsonen['Interceptions score'] + df_Stopperesæsonen['Succesful defensive actions score'] + df_Stopperesæsonen['Shots blocked score'] + df_Stopperesæsonen['Succesful defensive actions score'] + df_Stopperesæsonen['Defensive duels won % score']) /5
    df_Stopperesæsonen['Spilintelligens offensivt'] = (df_Stopperesæsonen['Forward passes score'] + df_Stopperesæsonen['Accurate forward passes score'] + df_Stopperesæsonen['Accurate passes to final third'] + df_Stopperesæsonen['Passes to final third'] + df_Stopperesæsonen['Accurate progressive passes score'] + df_Stopperesæsonen['Progressive passes score'] + df_Stopperesæsonen['Through passes'] + df_Stopperesæsonen['Accurate through passes']+ df_Stopperesæsonen['Progressive runs'] + df_Stopperesæsonen['Offensive duels won %'] + df_Stopperesæsonen['Successful dribbles %'])/11
    df_Stopperesæsonen['Nærkamps- og duelstærk'] = (df_Stopperesæsonen['Defensive duels won % score'] + df_Stopperesæsonen['Aerial duels won % score'] + df_Stopperesæsonen['Defensive duels won % score'])/3
    df_Stopperesæsonen['Samlet'] = (df_Stopperesæsonen['Pasningssikker'] + df_Stopperesæsonen['Spilintelligens defensivt'] + df_Stopperesæsonen['Spilintelligens offensivt'] + df_Stopperesæsonen['Nærkamps- og duelstærk'])/4

    df_Stopperesæsonen = df_Stopperesæsonen[['Pasningssikker','Spilintelligens defensivt','Spilintelligens offensivt','Nærkamps- og duelstærk','Samlet']]
    df_Stopperesæsonen = df_Stopperesæsonen.sort_values(by='Samlet',ascending=False)

    with st.expander('Stoppere kamp for kamp'):
        st.write(df_Stopperesæsonen)
    df_Stopperesæsonen = df_Stopperesæsonen.reset_index()
    df_Stopperesæsonen = df_Stopperesæsonen.drop('label',axis=1)
    df_Stopperesæsonen = df_Stopperesæsonen.groupby(['Player name','Team name','Total minutes']).mean(numeric_only=True)
    df_Stopperesæsonen = df_Stopperesæsonen.sort_values(by='Samlet',ascending=False)
    
    with st.expander('Stoppere sæson'):
        st.dataframe(df_Stopperesæsonen)

    df_Centrale_midt = pd.merge(df_centraleminutter,df_Centrale_midt,on=('Player id'))
    df_Centrale_midt = df_Centrale_midt[df_Centrale_midt['total_minutesOnField_y'] >=tidprkamp]

    df_Centrale_midt['Passes %'] = pd.qcut(df_Centrale_midt['percent_successfulPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Passes #'] = pd.qcut(df_Centrale_midt['average_successfulPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Forward Passes %'] = pd.qcut(df_Centrale_midt['percent_successfulForwardPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Forward Passes #'] = pd.qcut(df_Centrale_midt['average_successfulForwardPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Long Passes %'] = pd.qcut(df_Centrale_midt['percent_successfulLongPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Long Passes #'] = pd.qcut(df_Centrale_midt['average_successfulLongPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Smart passes %'] = pd.qcut(df_Centrale_midt['percent_successfulSmartPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Smart passes #'] = pd.qcut(df_Centrale_midt['average_successfulSmartPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Key passes %'] = pd.qcut(df_Centrale_midt['percent_successfulKeyPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Key passes #'] = pd.qcut(df_Centrale_midt['average_successfulKeyPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Passes to final third %'] = pd.qcut(df_Centrale_midt['percent_successfulPassesToFinalThird'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Passes to final third #'] = pd.qcut(df_Centrale_midt['average_successfulPassesToFinalThird'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Vertical passes %'] = pd.qcut(df_Centrale_midt['percent_successfulVerticalPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Vertical passes #'] = pd.qcut(df_Centrale_midt['average_successfulVerticalPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Through passes %'] = pd.qcut(df_Centrale_midt['percent_successfulThroughPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Through passes #'] = pd.qcut(df_Centrale_midt['average_successfulThroughPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Progressive passes %'] = pd.qcut(df_Centrale_midt['percent_successfulProgressivePasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Progressive passes #'] = pd.qcut(df_Centrale_midt['average_successfulProgressivePasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Offensive duels %'] = pd.qcut(df_Centrale_midt['percent_newOffensiveDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Received passes'] = pd.qcut(df_Centrale_midt['average_receivedPass'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Succesful dribbles %'] = pd.qcut(df_Centrale_midt['percent_newSuccessfulDribbles'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Succesful dribbles #'] = pd.qcut(df_Centrale_midt['average_newSuccessfulDribbles'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Duels won %'] = pd.qcut(df_Centrale_midt['percent_newDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Duels won #'] = pd.qcut(df_Centrale_midt['average_newDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Interceptions'] = pd.qcut(df_Centrale_midt['average_interceptions'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Counterpressing recoveries #'] = pd.qcut(df_Centrale_midt['average_counterpressingRecoveries'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Defensive duels won #'] = pd.qcut(df_Centrale_midt['average_newDefensiveDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Defensive duels won %'] = pd.qcut(df_Centrale_midt['percent_newDefensiveDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)

    df_Centrale_midtsæsonen = df_Centrale_midt.rename(columns={'total_minutesOnField_x':'Total minutes'},inplace=True)
    df_Centrale_midtsæsonen = df_Centrale_midt.groupby(['Player name','Team name','Total minutes','label']).mean(numeric_only=True)
    df_Centrale_midtsæsonen['Pasningssikker/Spilvendinger'] = (df_Centrale_midtsæsonen['Passes %'] + df_Centrale_midtsæsonen['Passes #'] + df_Centrale_midtsæsonen['Forward Passes %'] + df_Centrale_midtsæsonen['Forward Passes #'] + df_Centrale_midtsæsonen['Long Passes %'] + df_Centrale_midtsæsonen['Long Passes #']+ df_Centrale_midtsæsonen['Smart passes %'] + df_Centrale_midtsæsonen['Smart passes #'] + + df_Centrale_midtsæsonen['Key passes %'] + df_Centrale_midtsæsonen['Key passes #'] + df_Centrale_midtsæsonen['Passes to final third %'] + df_Centrale_midtsæsonen['Passes to final third #']+ df_Centrale_midtsæsonen['Vertical passes %'] + df_Centrale_midtsæsonen['Vertical passes #']+ df_Centrale_midtsæsonen['Through passes %'] + df_Centrale_midtsæsonen['Through passes #']+ df_Centrale_midtsæsonen['Progressive passes %'] + df_Centrale_midtsæsonen['Progressive passes #'])/18
    df_Centrale_midtsæsonen['Boldfast'] = (df_Centrale_midtsæsonen['Passes %'] + df_Centrale_midtsæsonen['Passes #']+ df_Centrale_midtsæsonen['Offensive duels %'] + df_Centrale_midtsæsonen['Received passes'] + df_Centrale_midtsæsonen['Succesful dribbles %'] + df_Centrale_midtsæsonen['Succesful dribbles #'])/6
    df_Centrale_midtsæsonen['Spilintelligens defensivt'] = (df_Centrale_midtsæsonen['Duels won %'] + df_Centrale_midtsæsonen['Duels won #'] +df_Centrale_midtsæsonen['Interceptions'] + df_Centrale_midtsæsonen['Counterpressing recoveries #'] + df_Centrale_midtsæsonen['Defensive duels won %'] + df_Centrale_midtsæsonen['Defensive duels won #'])/6
    df_Centrale_midtsæsonen['Samlet'] = (df_Centrale_midtsæsonen['Pasningssikker/Spilvendinger'] + df_Centrale_midtsæsonen['Boldfast'] + df_Centrale_midtsæsonen['Spilintelligens defensivt'])/3

    df_Centrale_midtsæsonen = df_Centrale_midtsæsonen[['Pasningssikker/Spilvendinger','Boldfast','Spilintelligens defensivt','Samlet']]
    df_Centrale_midtsæsonen = df_Centrale_midtsæsonen.sort_values(by='Samlet',ascending=False)
    with st.expander('Centrale midt kamp for kamp'):
        st.write(df_Centrale_midtsæsonen)

    df_Centrale_midtsæsonen = df_Centrale_midtsæsonen.reset_index()
    df_Centrale_midtsæsonen = df_Centrale_midtsæsonen.drop('label',axis=1)
    df_Centrale_midtsæsonen = df_Centrale_midtsæsonen.groupby(['Player name','Team name','Total minutes']).mean(numeric_only=True)
    df_Centrale_midtsæsonen = df_Centrale_midtsæsonen.sort_values(by='Samlet',ascending=False)
    with st.expander('Centrale midt sæson'):
        st.write(df_Centrale_midtsæsonen)


    df_Kanter = pd.merge(df_kanterminutter,df_Kanter,on=('Player id'))
    df_Kanter = df_Kanter[df_Kanter['total_minutesOnField_y'] >=tidprkamp]

    df_Kanter['Shots on target %'] = pd.qcut(df_Kanter['percent_shotsOnTarget'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Shots on target #'] = pd.qcut(df_Kanter['average_shotsOnTarget'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['XG'] = pd.qcut(df_Kanter['average_xgShot'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Successful dribbles #'] = pd.qcut(df_Kanter['average_newSuccessfulDribbles'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Successful dribbles %'] = pd.qcut(df_Kanter['percent_newSuccessfulDribbles'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Offensive duels %'] = pd.qcut(df_Kanter['percent_newOffensiveDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Offensive duels #'] = pd.qcut(df_Kanter['average_newOffensiveDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Passes %'] = pd.qcut(df_Kanter['percent_successfulPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Passes #'] = pd.qcut(df_Kanter['average_successfulPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Forward Passes %'] = pd.qcut(df_Kanter['percent_successfulForwardPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Forward Passes #'] = pd.qcut(df_Kanter['average_successfulForwardPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Smart passes %'] = pd.qcut(df_Kanter['percent_successfulSmartPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Smart passes #'] = pd.qcut(df_Kanter['average_successfulSmartPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Key passes %'] = pd.qcut(df_Kanter['percent_successfulKeyPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Key passes #'] = pd.qcut(df_Kanter['average_successfulKeyPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Passes to final third %'] = pd.qcut(df_Kanter['percent_successfulPassesToFinalThird'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Passes to final third #'] = pd.qcut(df_Kanter['average_successfulPassesToFinalThird'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Vertical passes %'] = pd.qcut(df_Kanter['percent_successfulVerticalPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Vertical passes #'] = pd.qcut(df_Kanter['average_successfulVerticalPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Through passes %'] = pd.qcut(df_Kanter['percent_successfulThroughPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Through passes #'] = pd.qcut(df_Kanter['average_successfulThroughPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Progressive passes %'] = pd.qcut(df_Kanter['percent_successfulProgressivePasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Progressive passes #'] = pd.qcut(df_Kanter['average_successfulProgressivePasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Goal conversion %'] = pd.qcut(df_Kanter['percent_goalConversion'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['XG per 90'] = pd.qcut(df_Kanter['average_xgShot'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['XA per 90'] = pd.qcut(df_Kanter['average_xgAssist'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Successful attacking actions'] = pd.qcut(df_Kanter['average_successfulAttackingActions'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Progressive runs'] = pd.qcut(df_Kanter['average_progressiveRun'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Accelerations score'] = pd.qcut(df_Kanter['average_accelerations'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)

    df_Kantersæsonen = df_Kanter.rename(columns={'total_minutesOnField_x':'Total minutes'},inplace=True)
    df_Kantersæsonen = df_Kanter.groupby(['Player name','Team name','Total minutes','label']).mean(numeric_only=True)

    df_Kantersæsonen['Sparkefærdigheder'] = (df_Kantersæsonen['Shots on target %'] + df_Kantersæsonen['Shots on target #'] + df_Kantersæsonen['XG'] + df_Kantersæsonen['Passes to final third %'] + df_Kantersæsonen['Forward Passes %'] + df_Kantersæsonen['Vertical passes %'])/6
    df_Kantersæsonen['Kombinationsstærk'] = (df_Kantersæsonen['Passes %'] + df_Kantersæsonen['Passes #'] + df_Kantersæsonen['Forward Passes %'] + df_Kantersæsonen['Forward Passes #'] + df_Kantersæsonen['Passes to final third %'] + df_Kantersæsonen['Passes to final third #'] + df_Kantersæsonen['Through passes %'] + df_Kantersæsonen['Through passes #'] + df_Kantersæsonen['Progressive passes %'] + df_Kantersæsonen['Progressive passes #'] + df_Kantersæsonen['Successful attacking actions'])/11
    df_Kantersæsonen['Spilintelligens offensivt/indlægsstærk'] = (df_Kantersæsonen['XA per 90'] + df_Kantersæsonen['XG per 90'] + df_Kantersæsonen['Through passes %'] + df_Kantersæsonen['Through passes #'] + df_Kantersæsonen['Smart passes %'] + df_Kantersæsonen['Smart passes #'] + df_Kantersæsonen['Progressive passes %'] + df_Kantersæsonen['Progressive passes #'] + df_Kantersæsonen['Key passes %'] + df_Kantersæsonen['Key passes #'] + df_Kantersæsonen['Successful attacking actions'])/11
    df_Kantersæsonen['1v1 offensivt'] = (df_Kantersæsonen['Successful dribbles #'] + df_Kantersæsonen['Successful dribbles %'] + df_Kantersæsonen['Offensive duels #'] + df_Kantersæsonen['Offensive duels %'] + df_Kantersæsonen['Progressive runs'])/5
    df_Kantersæsonen['Fart'] = (df_Kantersæsonen['Progressive runs'] + df_Kantersæsonen['Successful dribbles #'] + df_Kantersæsonen['Successful dribbles %'] + df_Kantersæsonen['Accelerations score'])/4
    df_Kantersæsonen['Samlet'] = (df_Kantersæsonen['Sparkefærdigheder'] + df_Kantersæsonen['Kombinationsstærk'] + df_Kantersæsonen['Spilintelligens offensivt/indlægsstærk'] + df_Kantersæsonen['1v1 offensivt'] + df_Kantersæsonen['Fart'])/5
    df_Kantersæsonen = df_Kantersæsonen[['Sparkefærdigheder','Kombinationsstærk','Spilintelligens offensivt/indlægsstærk','1v1 offensivt','Fart','Samlet']]
    df_Kantersæsonen = df_Kantersæsonen.sort_values(by='Samlet',ascending=False)

    with st.expander('Kanter kamp for kamp'):
        st.write(df_Kantersæsonen)

    df_Kantersæsonen = df_Kantersæsonen.reset_index()
    df_Kantersæsonen = df_Kantersæsonen.drop('label',axis=1)
    df_Kantersæsonen = df_Kantersæsonen.groupby(['Player name','Team name','Total minutes']).mean(numeric_only=True)
    df_Kantersæsonen = df_Kantersæsonen.sort_values(by='Samlet',ascending=False)
    with st.expander('Kanter sæson'):
        st.write(df_Kantersæsonen)


    df_Angribere = pd.merge(df_angribereminutter,df_Angribere,on=('Player id'))
    df_Angribere = df_Angribere[df_Angribere['total_minutesOnField_y'] >=tidprkamp]

    df_Angribere['Målfarlighed udregning'] = df_Angribere['average_goals'] - df_Angribere['average_xgShot']
    df_Angribere['Målfarlighed score'] =  pd.qcut(df_Angribere['Målfarlighed udregning'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Angribere['xG per 90 score'] = pd.qcut(df_Angribere['average_xgShot'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Angribere['Goals per 90 score'] = pd.qcut(df_Angribere['average_goals'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)  
    df_Angribere['Shots on target, % score'] = pd.qcut(df_Angribere['percent_shotsOnTarget'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)   
    df_Angribere['Offensive duels won, % score'] = pd.qcut(df_Angribere['percent_newOffensiveDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Angribere['Duels won, % score'] = pd.qcut(df_Angribere['percent_newDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Angribere['Accurate passes, % score'] = pd.qcut(df_Angribere['percent_successfulPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Angribere['Successful dribbles, % score'] = pd.qcut(df_Angribere['percent_newSuccessfulDribbles'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Angribere['xA per 90 score'] = pd.qcut(df_Angribere['average_xgAssist'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Angribere['Touches in box per 90 score'] = pd.qcut(df_Angribere['average_touchInBox'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Angribere['Progressive runs'] = pd.qcut(df_Angribere['average_progressiveRun'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Angribere['Accelerations score'] = pd.qcut(df_Angribere['average_accelerations'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Angribere['Progressive passes per 90 score'] = pd.qcut(df_Angribere['average_successfulProgressivePasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Angribere['Successful attacking actions per 90 score'] = pd.qcut(df_Angribere['average_successfulAttackingActions'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Angribere['Successful dribbles #'] = pd.qcut(df_Angribere['average_newSuccessfulDribbles'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)

    df_Angriberesæsonen = df_Angribere.rename(columns={'total_minutesOnField_x':'Total minutes'},inplace=True)
    df_Angriberesæsonen = df_Angribere.groupby(['Player name','Team name','Total minutes','label']).mean(numeric_only=True)

    df_Angriberesæsonen['Sparkefærdigheder'] = (df_Angriberesæsonen['xG per 90 score'] + df_Angriberesæsonen['xG per 90 score'] + df_Angriberesæsonen['Goals per 90 score'] + df_Angriberesæsonen['Shots on target, % score'])/4
    df_Angriberesæsonen['Boldfast'] = (df_Angriberesæsonen['Offensive duels won, % score'] + df_Angriberesæsonen['Offensive duels won, % score'] + df_Angriberesæsonen['Duels won, % score'] + df_Angriberesæsonen['Accurate passes, % score'] + df_Angriberesæsonen['Successful dribbles, % score'])/5
    df_Angriberesæsonen['Spilintelligens offensivt'] = (df_Angriberesæsonen['xA per 90 score'] + df_Angriberesæsonen['xG per 90 score'] + df_Angriberesæsonen['Touches in box per 90 score'] + df_Angriberesæsonen['Progressive passes per 90 score'] + df_Angriberesæsonen['Successful attacking actions per 90 score'] + df_Angriberesæsonen['Touches in box per 90 score'] + df_Angriberesæsonen['xG per 90 score'])/7
    df_Angriberesæsonen['Målfarlighed'] = (df_Angriberesæsonen['xG per 90 score']+df_Angriberesæsonen['Goals per 90 score']+df_Angriberesæsonen['xG per 90 score'] + df_Angriberesæsonen['Målfarlighed score'])/4
    df_Angriberesæsonen['Fart'] = (df_Angriberesæsonen['Progressive runs'] + + df_Angriberesæsonen['Progressive runs'] + df_Angriberesæsonen['Progressive runs'] + df_Angriberesæsonen['Successful dribbles #'] + df_Angriberesæsonen['Successful dribbles, % score'] + df_Angriberesæsonen['Accelerations score'] + df_Angriberesæsonen['Offensive duels won, % score'])/7
    df_Angriberesæsonen = df_Angriberesæsonen[['Sparkefærdigheder','Boldfast','Spilintelligens offensivt','Målfarlighed','Fart']]
    df_Angriberesæsonen['Samlet'] = (df_Angriberesæsonen['Sparkefærdigheder']+df_Angriberesæsonen['Boldfast']+df_Angriberesæsonen['Spilintelligens offensivt']+df_Angriberesæsonen['Målfarlighed']+df_Angriberesæsonen['Målfarlighed']+df_Angriberesæsonen['Målfarlighed']+df_Angriberesæsonen['Fart'])/7
    df_Angriberesæsonen = df_Angriberesæsonen.sort_values(by='Samlet',ascending=False)

    with st.expander('Angribere kamp for kamp'):
        st.write(df_Angriberesæsonen)

    df_Angriberesæsonen = df_Angriberesæsonen.reset_index()
    df_Angriberesæsonen = df_Angriberesæsonen.drop('label',axis=1)
    df_Angriberesæsonen = df_Angriberesæsonen.groupby(['Player name','Team name','Total minutes']).mean(numeric_only=True)
    df_Angriberesæsonen = df_Angriberesæsonen.sort_values(by='Samlet',ascending=False)
    with st.expander('Angribere sæson'):
        st.write(df_Angriberesæsonen)
    df = pd.read_csv(r'xT/U19 Division 23 24.csv')

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


    dfscore = pd.read_csv(r'xT/Zone scores.csv')

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

    xgc = df1
    xgchold = xgc.rename(columns={'shot.xg': 'Hold xG'})
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

def U17_Division ():
    col1,col2 = st.columns(2)
    with col1:
        samlettid = st.number_input('Minutter i sæsonen')
    with col2:    
        tidprkamp = st.number_input('Minutter pr. kamp')
        
    df = pd.read_csv(r'Individuelt dashboard/Individuelt dashboard U17 div.csv')
    df.rename(columns={'playerId': 'Player id'}, inplace=True)
    df = df.astype(str)
    dfevents = pd.read_csv('U17 div eventdata alle.csv',low_memory=False)
    dfevents = dfevents[['Player id','Player name','team_name','label','date','matchId']]
    dfspillernavn = df[['Player id','matchId','positions','average','percent','total']]
    dfspillernavn = dfspillernavn.astype(str)
    dfevents['Player id'] = dfevents['Player id'].astype(str)
    dfevents['matchId'] = dfevents['matchId'].astype(str)
    df = dfspillernavn.merge(dfevents)

    df['Player&matchId'] = df['Player id'] + df['matchId']
    df['Player&matchId'] = df['Player&matchId'].drop_duplicates(keep='first')
    df = df.dropna()
    df = df[['Player id','Player name','team_name','matchId','label','date','positions','average','percent','total']]

    #df = df.set_index('Player id')

    data = df['positions']
    df1 = pd.DataFrame(data)
    # Funktion, der ekstraherer navne og koder fra strengdata og opretter en ny kolonne med disse værdier
    def extract_positions(data):
        positions_list = ast.literal_eval(data) # Konverterer strengen til en liste af ordbøger
        names = [pos['position']['name'] for pos in positions_list]
        codes = [pos['position']['code'] for pos in positions_list]
        return pd.Series({'position_names': names, 'position_codes': codes})

    # Anvender funktionen på kolonnen og tilføjer resultaterne som nye kolonner til dataframe
    df1[['position_names', 'position_codes']] = df1['positions'].apply(extract_positions)

    df = pd.merge(df,df1,left_index=True, right_index=True)
    df = df.set_index('Player id')
    df = df.drop(columns=['positions_x'])
    df = df.drop(columns=['positions_y'])
    df = df[['Player name','team_name','matchId','label','date','position_names','position_codes','average','percent','total']]
    df = df.rename(columns={'team_name':'Team name'})
    df['percent'] = df['percent'].apply(lambda x: ast.literal_eval(x))

    # Create a new dataframe with the columns as the dictionary keys and the values as a list
    new_df = pd.DataFrame(df['percent'].to_list(), index=df.index).add_prefix('percent_')

    # Concatenate the new dataframe with the original dataframe
    df = pd.concat([df, new_df], axis=1)

    # Drop the original 'percent' column
    df = df.drop('percent', axis=1)

    df['total'] = df['total'].apply(lambda x: ast.literal_eval(x))

    # Create a new dataframe with the columns as the dictionary keys and the values as a list
    new_df = pd.DataFrame(df['total'].to_list(), index=df.index).add_prefix('total_')

    # Concatenate the new dataframe with the original dataframe
    df = pd.concat([df, new_df], axis=1)

    # Drop the original 'percent' column
    df = df.drop('total', axis=1)

    df['average'] = df['average'].apply(lambda x: ast.literal_eval(x))

    # Create a new dataframe with the columns as the dictionary keys and the values as a list
    new_df = pd.DataFrame(df['average'].to_list(), index=df.index).add_prefix('average_')

    # Concatenate the new dataframe with the original dataframe
    df = pd.concat([df, new_df], axis=1)


    # Drop the original 'percent' column
    df = df.drop('average', axis=1)
    df['position_codes'] = df['position_codes'].astype(str)
    #df['date'] = df['date'].astype(str)
    #df['date'] = df['date'].apply(lambda x: parser.parse(x))

    # Sort the dataframe by the 'date' column
    #df = df.sort_values(by='date',ascending=False)

    # Format the 'date' column to day-month-year format
    #df['date'] = df['date'].apply(lambda x: x.strftime('%d-%m-%Y'))
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date',ascending=False)

    df_backs = df[df['position_codes'].str.contains('|'.join(['lb', 'rb']))]
    df_backs = df_backs[df_backs['total_minutesOnField'] >= tidprkamp]
    df_backsminutter = df_backs[['Player name','Team name','total_minutesOnField']]
    df_backsminutter = df_backsminutter.groupby(['Player id']).sum(numeric_only=True)
    df_backsminutter = df_backsminutter[df_backsminutter['total_minutesOnField'] >= samlettid]

    df_Stoppere = df[df['position_codes'].str.contains('|'.join(['cb']))]
    df_Stoppere = df_Stoppere[df_Stoppere['total_minutesOnField'] >= tidprkamp]
    df_stoppereminutter = df_Stoppere[['Player name','Team name','total_minutesOnField']]
    df_stoppereminutter = df_stoppereminutter.groupby(['Player id']).sum(numeric_only=True)
    df_stoppereminutter = df_stoppereminutter[df_stoppereminutter['total_minutesOnField'] >= samlettid]

    df_Centrale_midt = df[df['position_codes'].str.contains('|'.join(['cm','amf','dmf']))]
    df_Centrale_midt = df_Centrale_midt[df_Centrale_midt['total_minutesOnField'] >= tidprkamp]
    df_centraleminutter = df_Centrale_midt[['Player name','Team name','total_minutesOnField']]
    df_centraleminutter = df_centraleminutter.groupby(['Player id']).sum(numeric_only=True)
    df_centraleminutter = df_centraleminutter[df_centraleminutter['total_minutesOnField'] >= samlettid]

    df_Kanter = df[df['position_codes'].str.contains('|'.join(['rw','lw','ramf','lamf']))]
    df_Kanter = df_Kanter[df_Kanter['total_minutesOnField'] >=tidprkamp]
    df_kanterminutter = df_Kanter[['Player name','Team name','total_minutesOnField']]
    df_kanterminutter = df_kanterminutter.groupby(['Player id']).sum(numeric_only=True)
    df_kanterminutter = df_kanterminutter[df_kanterminutter['total_minutesOnField'] >=samlettid]


    df_Angribere = df[df['position_codes'].str.contains('|'.join(['cf','ss']))]
    df_Angribere = df_Angribere[df_Angribere['total_minutesOnField'] >= tidprkamp]
    df_angribereminutter = df_Angribere[['Player name','Team name','total_minutesOnField']]
    df_angribereminutter = df_angribereminutter.groupby(['Player id']).sum(numeric_only=True)
    df_angribereminutter = df_angribereminutter[df_angribereminutter['total_minutesOnField'] >= samlettid]


    df_backs = pd.merge(df_backsminutter,df_backs,on=('Player id'))
    df_backs = df_backs[df_backs['total_minutesOnField_y'] >=tidprkamp]

    df_backs['Accurate crosses score'] = pd.qcut(df_backs['percent_successfulCrosses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_backs['Number of crosses score'] = pd.qcut(df_backs['average_crosses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_backs['XA score'] = pd.qcut(df_backs['average_xgAssist'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_backs['Passes to final third score'] = pd.qcut(df_backs['average_successfulPassesToFinalThird'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_backs['Successful dribbles score'] = pd.qcut(df_backs['percent_newSuccessfulDribbles'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_backs['Defensive duels won score'] = pd.qcut(df_backs['percent_newDefensiveDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_backs['Progressive runs score'] = pd.qcut(df_backs['average_progressiveRun'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_backs['Offensive duels won score'] = pd.qcut(df_backs['percent_newOffensiveDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_backs['Accelerations score'] = pd.qcut(df_backs['average_accelerations'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_backs['Duels won score'] = pd.qcut(df_backs['percent_newDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_backs['Interceptions score'] = pd.qcut(df_backs['average_interceptions'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_backs['Successful defensive actions score'] = pd.qcut(df_backs['average_successfulDefensiveAction'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_backssæsonen = df_backs[['label','Player name','Team name','total_minutesOnField_x','total_minutesOnField_y','Number of crosses score','Accurate crosses score','XA score','Passes to final third score','Successful dribbles score','Defensive duels won score','Progressive runs score','Offensive duels won score','Accelerations score','Duels won score','Interceptions score','Successful defensive actions score']]
    df_backssæsonen.rename(columns={'total_minutesOnField_x':'Total minutes'},inplace=True)
    df_backssæsonen = df_backssæsonen.groupby(['Player name','Team name','Total minutes','label']).mean(numeric_only=True)

    df_backssæsonen['Indlægsstærk'] = (df_backssæsonen['Number of crosses score'] + df_backssæsonen['Accurate crosses score'] + df_backssæsonen['XA score'] + df_backssæsonen['Passes to final third score'])/4
    df_backssæsonen['1v1 færdigheder'] = (df_backssæsonen['Successful dribbles score'] + df_backssæsonen['Defensive duels won score'] + df_backssæsonen['Progressive runs score'] + df_backssæsonen['Offensive duels won score'] + df_backssæsonen['Accelerations score'] + df_backssæsonen['Duels won score'])/6
    df_backssæsonen['Spilintelligens defensivt'] = (df_backssæsonen['Interceptions score'] + df_backssæsonen['Successful defensive actions score'] + df_backssæsonen['Duels won score'] + df_backssæsonen['Defensive duels won score'])/4
    df_backssæsonen['Fart'] = (df_backssæsonen['Successful dribbles score'] + df_backssæsonen['Progressive runs score'] + df_backssæsonen['Offensive duels won score'] + df_backssæsonen['Accelerations score'])/4
    df_backssæsonen ['Samlet'] = (df_backssæsonen['Indlægsstærk'] + df_backssæsonen['1v1 færdigheder'] + df_backssæsonen['Spilintelligens defensivt'] + df_backssæsonen['Fart'])/4

    df_backssæsonen = df_backssæsonen[['Indlægsstærk','1v1 færdigheder','Spilintelligens defensivt','Fart','Samlet']]
    df_backssæsonen = df_backssæsonen.round(3).astype(float)
    df_backssæsonen = df_backssæsonen.sort_values(by='Samlet',ascending=False)
    with st.expander('Backs kamp for kamp'):
        st.write(df_backssæsonen)
    df_backssæsonen = df_backssæsonen.reset_index()
    df_backssæsonen = df_backssæsonen.drop('label',axis=1)
    df_backssæsonen = df_backssæsonen.groupby(['Player name','Team name','Total minutes']).mean(numeric_only=True)
    df_backssæsonen = df_backssæsonen.sort_values(by='Samlet',ascending=False)
    with st.expander('Backs'):
        st.dataframe(df_backssæsonen)
       
    df_Stoppere = pd.merge(df_stoppereminutter,df_Stoppere,on=('Player id'))
    df_Stoppere = df_Stoppere[df_Stoppere['total_minutesOnField_y'] >=tidprkamp]
    
    df_Stoppere['Accurate passes score'] = pd.qcut(df_Stoppere['percent_successfulPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Accurate long passes score'] = pd.qcut(df_Stoppere['percent_successfulLongPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Forward passes score'] = pd.qcut(df_Stoppere['average_successfulForwardPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Accurate forward passes score'] = pd.qcut(df_Stoppere['percent_successfulForwardPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Accurate progressive passes score'] = pd.qcut(df_Stoppere['percent_successfulProgressivePasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Accurate vertical passes score'] = pd.qcut(df_Stoppere['percent_successfulVerticalPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Interceptions score'] = pd.qcut(df_Stoppere['average_interceptions'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Succesful defensive actions score'] = pd.qcut(df_Stoppere['average_successfulDefensiveAction'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Shots blocked score'] = pd.qcut(df_Stoppere['average_shotsBlocked'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Defensive duels won score'] = pd.qcut(df_Stoppere['average_newDefensiveDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Defensive duels won % score'] = pd.qcut(df_Stoppere['percent_newDefensiveDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Accurate passes to final third'] = pd.qcut(df_Stoppere['percent_successfulPassesToFinalThird'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Accurate through passes'] = pd.qcut(df_Stoppere['percent_successfulThroughPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Vertical passes'] = pd.qcut(df_Stoppere['average_successfulVerticalPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Through passes'] = pd.qcut(df_Stoppere['average_successfulThroughPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Passes to final third'] = pd.qcut(df_Stoppere['average_successfulPassesToFinalThird'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Progressive runs'] = pd.qcut(df_Stoppere['average_progressiveRun'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Offensive duels won %'] = pd.qcut(df_Stoppere['percent_newOffensiveDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Successful dribbles %'] = pd.qcut(df_Stoppere['percent_newSuccessfulDribbles'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Progressive passes score'] = pd.qcut(df_Stoppere['average_successfulProgressivePasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Aerial duels won score'] = pd.qcut(df_Stoppere['average_fieldAerialDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Aerial duels won % score'] = pd.qcut(df_Stoppere['percent_aerialDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)

    df_Stopperesæsonen = df_Stoppere[['label','Player name','Team name','total_minutesOnField_x','total_minutesOnField_y','Accurate passes score','Accurate long passes score','Forward passes score','Accurate forward passes score','Accurate progressive passes score','Accurate vertical passes score','Interceptions score','Succesful defensive actions score','Shots blocked score','Defensive duels won score','Defensive duels won % score','Accurate passes to final third','Accurate through passes','Vertical passes','Through passes','Passes to final third','Progressive passes score','Aerial duels won score','Aerial duels won % score','Progressive runs','Offensive duels won %','Successful dribbles %']]
    df_Stopperesæsonen.rename(columns={'total_minutesOnField_x':'Total minutes'},inplace=True)
    df_Stopperesæsonen = df_Stopperesæsonen.groupby(['Player name','Team name','Total minutes','label']).mean(numeric_only=True)
    df_Stopperesæsonen['Pasningssikker'] = (df_Stopperesæsonen['Accurate passes score'] + df_Stopperesæsonen['Accurate long passes score'] + df_Stopperesæsonen['Forward passes score'] + df_Stopperesæsonen['Accurate forward passes score'] + df_Stopperesæsonen['Accurate progressive passes score'] + df_Stopperesæsonen['Accurate vertical passes score'])/6
    df_Stopperesæsonen['Spilintelligens defensivt'] = (df_Stopperesæsonen['Interceptions score'] + df_Stopperesæsonen['Succesful defensive actions score'] + df_Stopperesæsonen['Shots blocked score'] + df_Stopperesæsonen['Succesful defensive actions score'] + df_Stopperesæsonen['Defensive duels won % score']) /5
    df_Stopperesæsonen['Spilintelligens offensivt'] = (df_Stopperesæsonen['Forward passes score'] + df_Stopperesæsonen['Accurate forward passes score'] + df_Stopperesæsonen['Accurate passes to final third'] + df_Stopperesæsonen['Passes to final third'] + df_Stopperesæsonen['Accurate progressive passes score'] + df_Stopperesæsonen['Progressive passes score'] + df_Stopperesæsonen['Through passes'] + df_Stopperesæsonen['Accurate through passes']+ df_Stopperesæsonen['Progressive runs'] + df_Stopperesæsonen['Offensive duels won %'] + df_Stopperesæsonen['Successful dribbles %'])/11
    df_Stopperesæsonen['Nærkamps- og duelstærk'] = (df_Stopperesæsonen['Defensive duels won % score'] + df_Stopperesæsonen['Aerial duels won % score'] + df_Stopperesæsonen['Defensive duels won % score'])/3
    df_Stopperesæsonen['Samlet'] = (df_Stopperesæsonen['Pasningssikker'] + df_Stopperesæsonen['Spilintelligens defensivt'] + df_Stopperesæsonen['Spilintelligens offensivt'] + df_Stopperesæsonen['Nærkamps- og duelstærk'])/4

    df_Stopperesæsonen = df_Stopperesæsonen[['Pasningssikker','Spilintelligens defensivt','Spilintelligens offensivt','Nærkamps- og duelstærk','Samlet']]
    df_Stopperesæsonen = df_Stopperesæsonen.sort_values(by='Samlet',ascending=False)

    with st.expander('Stoppere kamp for kamp'):
        st.write(df_Stopperesæsonen)
    df_Stopperesæsonen = df_Stopperesæsonen.reset_index()
    df_Stopperesæsonen = df_Stopperesæsonen.drop('label',axis=1)
    df_Stopperesæsonen = df_Stopperesæsonen.groupby(['Player name','Team name','Total minutes']).mean(numeric_only=True)
    df_Stopperesæsonen = df_Stopperesæsonen.sort_values(by='Samlet',ascending=False)
    
    with st.expander('Stoppere sæson'):
        st.dataframe(df_Stopperesæsonen)

    df_Centrale_midt = pd.merge(df_centraleminutter,df_Centrale_midt,on=('Player id'))
    df_Centrale_midt = df_Centrale_midt[df_Centrale_midt['total_minutesOnField_y'] >=tidprkamp]

    df_Centrale_midt['Passes %'] = pd.qcut(df_Centrale_midt['percent_successfulPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Passes #'] = pd.qcut(df_Centrale_midt['average_successfulPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Forward Passes %'] = pd.qcut(df_Centrale_midt['percent_successfulForwardPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Forward Passes #'] = pd.qcut(df_Centrale_midt['average_successfulForwardPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Long Passes %'] = pd.qcut(df_Centrale_midt['percent_successfulLongPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Long Passes #'] = pd.qcut(df_Centrale_midt['average_successfulLongPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Smart passes %'] = pd.qcut(df_Centrale_midt['percent_successfulSmartPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Smart passes #'] = pd.qcut(df_Centrale_midt['average_successfulSmartPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Key passes %'] = pd.qcut(df_Centrale_midt['percent_successfulKeyPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Key passes #'] = pd.qcut(df_Centrale_midt['average_successfulKeyPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Passes to final third %'] = pd.qcut(df_Centrale_midt['percent_successfulPassesToFinalThird'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Passes to final third #'] = pd.qcut(df_Centrale_midt['average_successfulPassesToFinalThird'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Vertical passes %'] = pd.qcut(df_Centrale_midt['percent_successfulVerticalPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Vertical passes #'] = pd.qcut(df_Centrale_midt['average_successfulVerticalPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Through passes %'] = pd.qcut(df_Centrale_midt['percent_successfulThroughPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Through passes #'] = pd.qcut(df_Centrale_midt['average_successfulThroughPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Progressive passes %'] = pd.qcut(df_Centrale_midt['percent_successfulProgressivePasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Progressive passes #'] = pd.qcut(df_Centrale_midt['average_successfulProgressivePasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Offensive duels %'] = pd.qcut(df_Centrale_midt['percent_newOffensiveDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Received passes'] = pd.qcut(df_Centrale_midt['average_receivedPass'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Succesful dribbles %'] = pd.qcut(df_Centrale_midt['percent_newSuccessfulDribbles'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Succesful dribbles #'] = pd.qcut(df_Centrale_midt['average_newSuccessfulDribbles'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Duels won %'] = pd.qcut(df_Centrale_midt['percent_newDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Duels won #'] = pd.qcut(df_Centrale_midt['average_newDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Interceptions'] = pd.qcut(df_Centrale_midt['average_interceptions'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Counterpressing recoveries #'] = pd.qcut(df_Centrale_midt['average_counterpressingRecoveries'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Defensive duels won #'] = pd.qcut(df_Centrale_midt['average_newDefensiveDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Defensive duels won %'] = pd.qcut(df_Centrale_midt['percent_newDefensiveDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)

    df_Centrale_midtsæsonen = df_Centrale_midt.rename(columns={'total_minutesOnField_x':'Total minutes'},inplace=True)
    df_Centrale_midtsæsonen = df_Centrale_midt.groupby(['Player name','Team name','Total minutes','label']).mean(numeric_only=True)
    df_Centrale_midtsæsonen['Pasningssikker/Spilvendinger'] = (df_Centrale_midtsæsonen['Passes %'] + df_Centrale_midtsæsonen['Passes #'] + df_Centrale_midtsæsonen['Forward Passes %'] + df_Centrale_midtsæsonen['Forward Passes #'] + df_Centrale_midtsæsonen['Long Passes %'] + df_Centrale_midtsæsonen['Long Passes #']+ df_Centrale_midtsæsonen['Smart passes %'] + df_Centrale_midtsæsonen['Smart passes #'] + + df_Centrale_midtsæsonen['Key passes %'] + df_Centrale_midtsæsonen['Key passes #'] + df_Centrale_midtsæsonen['Passes to final third %'] + df_Centrale_midtsæsonen['Passes to final third #']+ df_Centrale_midtsæsonen['Vertical passes %'] + df_Centrale_midtsæsonen['Vertical passes #']+ df_Centrale_midtsæsonen['Through passes %'] + df_Centrale_midtsæsonen['Through passes #']+ df_Centrale_midtsæsonen['Progressive passes %'] + df_Centrale_midtsæsonen['Progressive passes #'])/18
    df_Centrale_midtsæsonen['Boldfast'] = (df_Centrale_midtsæsonen['Passes %'] + df_Centrale_midtsæsonen['Passes #']+ df_Centrale_midtsæsonen['Offensive duels %'] + df_Centrale_midtsæsonen['Received passes'] + df_Centrale_midtsæsonen['Succesful dribbles %'] + df_Centrale_midtsæsonen['Succesful dribbles #'])/6
    df_Centrale_midtsæsonen['Spilintelligens defensivt'] = (df_Centrale_midtsæsonen['Duels won %'] + df_Centrale_midtsæsonen['Duels won #'] +df_Centrale_midtsæsonen['Interceptions'] + df_Centrale_midtsæsonen['Counterpressing recoveries #'] + df_Centrale_midtsæsonen['Defensive duels won %'] + df_Centrale_midtsæsonen['Defensive duels won #'])/6
    df_Centrale_midtsæsonen['Samlet'] = (df_Centrale_midtsæsonen['Pasningssikker/Spilvendinger'] + df_Centrale_midtsæsonen['Boldfast'] + df_Centrale_midtsæsonen['Spilintelligens defensivt'])/3

    df_Centrale_midtsæsonen = df_Centrale_midtsæsonen[['Pasningssikker/Spilvendinger','Boldfast','Spilintelligens defensivt','Samlet']]
    df_Centrale_midtsæsonen = df_Centrale_midtsæsonen.sort_values(by='Samlet',ascending=False)
    with st.expander('Centrale midt kamp for kamp'):
        st.write(df_Centrale_midtsæsonen)

    df_Centrale_midtsæsonen = df_Centrale_midtsæsonen.reset_index()
    df_Centrale_midtsæsonen = df_Centrale_midtsæsonen.drop('label',axis=1)
    df_Centrale_midtsæsonen = df_Centrale_midtsæsonen.groupby(['Player name','Team name','Total minutes']).mean(numeric_only=True)
    df_Centrale_midtsæsonen = df_Centrale_midtsæsonen.sort_values(by='Samlet',ascending=False)
    with st.expander('Centrale midt sæson'):
        st.write(df_Centrale_midtsæsonen)


    df_Kanter = pd.merge(df_kanterminutter,df_Kanter,on=('Player id'))
    df_Kanter = df_Kanter[df_Kanter['total_minutesOnField_y'] >=tidprkamp]

    df_Kanter['Shots on target %'] = pd.qcut(df_Kanter['percent_shotsOnTarget'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Shots on target #'] = pd.qcut(df_Kanter['average_shotsOnTarget'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['XG'] = pd.qcut(df_Kanter['average_xgShot'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Successful dribbles #'] = pd.qcut(df_Kanter['average_newSuccessfulDribbles'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Successful dribbles %'] = pd.qcut(df_Kanter['percent_newSuccessfulDribbles'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Offensive duels %'] = pd.qcut(df_Kanter['percent_newOffensiveDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Offensive duels #'] = pd.qcut(df_Kanter['average_newOffensiveDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Passes %'] = pd.qcut(df_Kanter['percent_successfulPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Passes #'] = pd.qcut(df_Kanter['average_successfulPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Forward Passes %'] = pd.qcut(df_Kanter['percent_successfulForwardPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Forward Passes #'] = pd.qcut(df_Kanter['average_successfulForwardPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Smart passes %'] = pd.qcut(df_Kanter['percent_successfulSmartPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Smart passes #'] = pd.qcut(df_Kanter['average_successfulSmartPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Key passes %'] = pd.qcut(df_Kanter['percent_successfulKeyPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Key passes #'] = pd.qcut(df_Kanter['average_successfulKeyPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Passes to final third %'] = pd.qcut(df_Kanter['percent_successfulPassesToFinalThird'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Passes to final third #'] = pd.qcut(df_Kanter['average_successfulPassesToFinalThird'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Vertical passes %'] = pd.qcut(df_Kanter['percent_successfulVerticalPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Vertical passes #'] = pd.qcut(df_Kanter['average_successfulVerticalPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Through passes %'] = pd.qcut(df_Kanter['percent_successfulThroughPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Through passes #'] = pd.qcut(df_Kanter['average_successfulThroughPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Progressive passes %'] = pd.qcut(df_Kanter['percent_successfulProgressivePasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Progressive passes #'] = pd.qcut(df_Kanter['average_successfulProgressivePasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Goal conversion %'] = pd.qcut(df_Kanter['percent_goalConversion'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['XG per 90'] = pd.qcut(df_Kanter['average_xgShot'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['XA per 90'] = pd.qcut(df_Kanter['average_xgAssist'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Successful attacking actions'] = pd.qcut(df_Kanter['average_successfulAttackingActions'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Progressive runs'] = pd.qcut(df_Kanter['average_progressiveRun'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Accelerations score'] = pd.qcut(df_Kanter['average_accelerations'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)

    df_Kantersæsonen = df_Kanter.rename(columns={'total_minutesOnField_x':'Total minutes'},inplace=True)
    df_Kantersæsonen = df_Kanter.groupby(['Player name','Team name','Total minutes','label']).mean(numeric_only=True)

    df_Kantersæsonen['Sparkefærdigheder'] = (df_Kantersæsonen['Shots on target %'] + df_Kantersæsonen['Shots on target #'] + df_Kantersæsonen['XG'] + df_Kantersæsonen['Passes to final third %'] + df_Kantersæsonen['Forward Passes %'] + df_Kantersæsonen['Vertical passes %'])/6
    df_Kantersæsonen['Kombinationsstærk'] = (df_Kantersæsonen['Passes %'] + df_Kantersæsonen['Passes #'] + df_Kantersæsonen['Forward Passes %'] + df_Kantersæsonen['Forward Passes #'] + df_Kantersæsonen['Passes to final third %'] + df_Kantersæsonen['Passes to final third #'] + df_Kantersæsonen['Through passes %'] + df_Kantersæsonen['Through passes #'] + df_Kantersæsonen['Progressive passes %'] + df_Kantersæsonen['Progressive passes #'] + df_Kantersæsonen['Successful attacking actions'])/11
    df_Kantersæsonen['Spilintelligens offensivt/indlægsstærk'] = (df_Kantersæsonen['XA per 90'] + df_Kantersæsonen['XG per 90'] + df_Kantersæsonen['Through passes %'] + df_Kantersæsonen['Through passes #'] + df_Kantersæsonen['Smart passes %'] + df_Kantersæsonen['Smart passes #'] + df_Kantersæsonen['Progressive passes %'] + df_Kantersæsonen['Progressive passes #'] + df_Kantersæsonen['Key passes %'] + df_Kantersæsonen['Key passes #'] + df_Kantersæsonen['Successful attacking actions'])/11
    df_Kantersæsonen['1v1 offensivt'] = (df_Kantersæsonen['Successful dribbles #'] + df_Kantersæsonen['Successful dribbles %'] + df_Kantersæsonen['Offensive duels #'] + df_Kantersæsonen['Offensive duels %'] + df_Kantersæsonen['Progressive runs'])/5
    df_Kantersæsonen['Fart'] = (df_Kantersæsonen['Progressive runs'] + df_Kantersæsonen['Successful dribbles #'] + df_Kantersæsonen['Successful dribbles %'] + df_Kantersæsonen['Accelerations score'])/4
    df_Kantersæsonen['Samlet'] = (df_Kantersæsonen['Sparkefærdigheder'] + df_Kantersæsonen['Kombinationsstærk'] + df_Kantersæsonen['Spilintelligens offensivt/indlægsstærk'] + df_Kantersæsonen['1v1 offensivt'] + df_Kantersæsonen['Fart'])/5
    df_Kantersæsonen = df_Kantersæsonen[['Sparkefærdigheder','Kombinationsstærk','Spilintelligens offensivt/indlægsstærk','1v1 offensivt','Fart','Samlet']]
    df_Kantersæsonen = df_Kantersæsonen.sort_values(by='Samlet',ascending=False)

    with st.expander('Kanter kamp for kamp'):
        st.write(df_Kantersæsonen)

    df_Kantersæsonen = df_Kantersæsonen.reset_index()
    df_Kantersæsonen = df_Kantersæsonen.drop('label',axis=1)
    df_Kantersæsonen = df_Kantersæsonen.groupby(['Player name','Team name','Total minutes']).mean(numeric_only=True)
    df_Kantersæsonen = df_Kantersæsonen.sort_values(by='Samlet',ascending=False)
    with st.expander('Kanter sæson'):
        st.write(df_Kantersæsonen)


    df_Angribere = pd.merge(df_angribereminutter,df_Angribere,on=('Player id'))
    df_Angribere = df_Angribere[df_Angribere['total_minutesOnField_y'] >=tidprkamp]

    df_Angribere['Målfarlighed udregning'] = df_Angribere['average_goals'] - df_Angribere['average_xgShot']
    df_Angribere['Målfarlighed score'] =  pd.qcut(df_Angribere['Målfarlighed udregning'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Angribere['xG per 90 score'] = pd.qcut(df_Angribere['average_xgShot'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Angribere['Goals per 90 score'] = pd.qcut(df_Angribere['average_goals'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)  
    df_Angribere['Shots on target, % score'] = pd.qcut(df_Angribere['percent_shotsOnTarget'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)   
    df_Angribere['Offensive duels won, % score'] = pd.qcut(df_Angribere['percent_newOffensiveDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Angribere['Duels won, % score'] = pd.qcut(df_Angribere['percent_newDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Angribere['Accurate passes, % score'] = pd.qcut(df_Angribere['percent_successfulPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Angribere['Successful dribbles, % score'] = pd.qcut(df_Angribere['percent_newSuccessfulDribbles'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Angribere['xA per 90 score'] = pd.qcut(df_Angribere['average_xgAssist'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Angribere['Touches in box per 90 score'] = pd.qcut(df_Angribere['average_touchInBox'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Angribere['Progressive runs'] = pd.qcut(df_Angribere['average_progressiveRun'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Angribere['Accelerations score'] = pd.qcut(df_Angribere['average_accelerations'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Angribere['Progressive passes per 90 score'] = pd.qcut(df_Angribere['average_successfulProgressivePasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Angribere['Successful attacking actions per 90 score'] = pd.qcut(df_Angribere['average_successfulAttackingActions'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Angribere['Successful dribbles #'] = pd.qcut(df_Angribere['average_newSuccessfulDribbles'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)

    df_Angriberesæsonen = df_Angribere.rename(columns={'total_minutesOnField_x':'Total minutes'},inplace=True)
    df_Angriberesæsonen = df_Angribere.groupby(['Player name','Team name','Total minutes','label']).mean(numeric_only=True)

    df_Angriberesæsonen['Sparkefærdigheder'] = (df_Angriberesæsonen['xG per 90 score'] + df_Angriberesæsonen['xG per 90 score'] + df_Angriberesæsonen['Goals per 90 score'] + df_Angriberesæsonen['Shots on target, % score'])/4
    df_Angriberesæsonen['Boldfast'] = (df_Angriberesæsonen['Offensive duels won, % score'] + df_Angriberesæsonen['Offensive duels won, % score'] + df_Angriberesæsonen['Duels won, % score'] + df_Angriberesæsonen['Accurate passes, % score'] + df_Angriberesæsonen['Successful dribbles, % score'])/5
    df_Angriberesæsonen['Spilintelligens offensivt'] = (df_Angriberesæsonen['xA per 90 score'] + df_Angriberesæsonen['xG per 90 score'] + df_Angriberesæsonen['Touches in box per 90 score'] + df_Angriberesæsonen['Progressive passes per 90 score'] + df_Angriberesæsonen['Successful attacking actions per 90 score'] + df_Angriberesæsonen['Touches in box per 90 score'] + df_Angriberesæsonen['xG per 90 score'])/7
    df_Angriberesæsonen['Målfarlighed'] = (df_Angriberesæsonen['xG per 90 score']+df_Angriberesæsonen['Goals per 90 score']+df_Angriberesæsonen['xG per 90 score'] + df_Angriberesæsonen['Målfarlighed score'])/4
    df_Angriberesæsonen['Fart'] = (df_Angriberesæsonen['Progressive runs'] + + df_Angriberesæsonen['Progressive runs'] + df_Angriberesæsonen['Progressive runs'] + df_Angriberesæsonen['Successful dribbles #'] + df_Angriberesæsonen['Successful dribbles, % score'] + df_Angriberesæsonen['Accelerations score'] + df_Angriberesæsonen['Offensive duels won, % score'])/7
    df_Angriberesæsonen = df_Angriberesæsonen[['Sparkefærdigheder','Boldfast','Spilintelligens offensivt','Målfarlighed','Fart']]
    df_Angriberesæsonen['Samlet'] = (df_Angriberesæsonen['Sparkefærdigheder']+df_Angriberesæsonen['Boldfast']+df_Angriberesæsonen['Spilintelligens offensivt']+df_Angriberesæsonen['Målfarlighed']+df_Angriberesæsonen['Målfarlighed']+df_Angriberesæsonen['Målfarlighed']+df_Angriberesæsonen['Fart'])/7
    df_Angriberesæsonen = df_Angriberesæsonen.sort_values(by='Samlet',ascending=False)

    with st.expander('Angribere kamp for kamp'):
        st.write(df_Angriberesæsonen)

    df_Angriberesæsonen = df_Angriberesæsonen.reset_index()
    df_Angriberesæsonen = df_Angriberesæsonen.drop('label',axis=1)
    df_Angriberesæsonen = df_Angriberesæsonen.groupby(['Player name','Team name','Total minutes']).mean(numeric_only=True)
    df_Angriberesæsonen = df_Angriberesæsonen.sort_values(by='Samlet',ascending=False)
    with st.expander('Angribere sæson'):
        st.write(df_Angriberesæsonen)
    df = pd.read_csv(r'xT/U17 Division 23 24.csv')

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


    dfscore = pd.read_csv(r'xT/Zone scores.csv')

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

    xgc = df1
    xgchold = xgc.rename(columns={'shot.xg': 'Hold xG'})
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

def Superliga ():
    col1,col2 = st.columns(2)
    with col1:
        samlettid = st.number_input('Minutter i sæsonen')
    with col2:    
        tidprkamp = st.number_input('Minutter pr. kamp')
        
    df = pd.read_csv(r'Individuelt dashboard/Individuelt dashboard Superliga.csv')
    df.rename(columns={'playerId': 'Player id'}, inplace=True)
    df = df.astype(str)
    dfevents = pd.read_csv('Superliga eventdata alle.csv',low_memory=False)
    dfevents = dfevents[['Player id','Player name','team_name','label','date','matchId']]
    dfspillernavn = df[['Player id','matchId','positions','average','percent','total']]
    dfspillernavn = dfspillernavn.astype(str)
    dfevents['Player id'] = dfevents['Player id'].astype(str)
    dfevents['matchId'] = dfevents['matchId'].astype(str)
    df = dfspillernavn.merge(dfevents)

    df['Player&matchId'] = df['Player id'] + df['matchId']
    df['Player&matchId'] = df['Player&matchId'].drop_duplicates(keep='first')
    df = df.dropna()

    #df = df.set_index('Player id')

    data = df['positions']
    df1 = pd.DataFrame(data)
    # Funktion, der ekstraherer navne og koder fra strengdata og opretter en ny kolonne med disse værdier
    def extract_positions(data):
        positions_list = ast.literal_eval(data) # Konverterer strengen til en liste af ordbøger
        names = [pos['position']['name'] for pos in positions_list]
        codes = [pos['position']['code'] for pos in positions_list]
        return pd.Series({'position_names': names, 'position_codes': codes})

    # Anvender funktionen på kolonnen og tilføjer resultaterne som nye kolonner til dataframe
    df1[['position_names', 'position_codes']] = df1['positions'].apply(extract_positions)

    df = pd.merge(df,df1,left_index=True, right_index=True)
    df = df.set_index('Player id')
    df = df.drop(columns=['positions_x'])
    df = df.drop(columns=['positions_y'])
    df = df[['Player name','team_name','matchId','label','date','position_names','position_codes','average','percent','total']]
    df = df.rename(columns={'team_name':'Team name'})
    df['percent'] = df['percent'].apply(lambda x: ast.literal_eval(x))

    # Create a new dataframe with the columns as the dictionary keys and the values as a list
    new_df = pd.DataFrame(df['percent'].to_list(), index=df.index).add_prefix('percent_')

    # Concatenate the new dataframe with the original dataframe
    df = pd.concat([df, new_df], axis=1)

    # Drop the original 'percent' column
    df = df.drop('percent', axis=1)

    df['total'] = df['total'].apply(lambda x: ast.literal_eval(x))

    # Create a new dataframe with the columns as the dictionary keys and the values as a list
    new_df = pd.DataFrame(df['total'].to_list(), index=df.index).add_prefix('total_')

    # Concatenate the new dataframe with the original dataframe
    df = pd.concat([df, new_df], axis=1)

    # Drop the original 'percent' column
    df = df.drop('total', axis=1)

    df['average'] = df['average'].apply(lambda x: ast.literal_eval(x))

    # Create a new dataframe with the columns as the dictionary keys and the values as a list
    new_df = pd.DataFrame(df['average'].to_list(), index=df.index).add_prefix('average_')

    # Concatenate the new dataframe with the original dataframe
    df = pd.concat([df, new_df], axis=1)


    # Drop the original 'percent' column
    df = df.drop('average', axis=1)
    df['position_codes'] = df['position_codes'].astype(str)
    #df['date'] = df['date'].astype(str)
    #df['date'] = df['date'].apply(lambda x: parser.parse(x))

    # Sort the dataframe by the 'date' column
    #df = df.sort_values(by='date',ascending=False)

    # Format the 'date' column to day-month-year format
    #df['date'] = df['date'].apply(lambda x: x.strftime('%d-%m-%Y'))
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date',ascending=False)

    df_backs = df[df['position_codes'].str.contains('|'.join(['lb', 'rb']))]
    df_backs = df_backs[df_backs['total_minutesOnField'] >= tidprkamp]
    df_backsminutter = df_backs[['Player name','Team name','total_minutesOnField']]
    df_backsminutter = df_backsminutter.groupby(['Player id']).sum(numeric_only=True)
    df_backsminutter = df_backsminutter[df_backsminutter['total_minutesOnField'] >= samlettid]

    df_Stoppere = df[df['position_codes'].str.contains('|'.join(['cb']))]
    df_Stoppere = df_Stoppere[df_Stoppere['total_minutesOnField'] >= tidprkamp]
    df_stoppereminutter = df_Stoppere[['Player name','Team name','total_minutesOnField']]
    df_stoppereminutter = df_stoppereminutter.groupby(['Player id']).sum(numeric_only=True)
    df_stoppereminutter = df_stoppereminutter[df_stoppereminutter['total_minutesOnField'] >= samlettid]

    df_Centrale_midt = df[df['position_codes'].str.contains('|'.join(['cm','amf','dmf']))]
    df_Centrale_midt = df_Centrale_midt[df_Centrale_midt['total_minutesOnField'] >= tidprkamp]
    df_centraleminutter = df_Centrale_midt[['Player name','Team name','total_minutesOnField']]
    df_centraleminutter = df_centraleminutter.groupby(['Player id']).sum(numeric_only=True)
    df_centraleminutter = df_centraleminutter[df_centraleminutter['total_minutesOnField'] >= samlettid]

    df_Kanter = df[df['position_codes'].str.contains('|'.join(['rw','lw','ramf','lamf']))]
    df_Kanter = df_Kanter[df_Kanter['total_minutesOnField'] >=tidprkamp]
    df_kanterminutter = df_Kanter[['Player name','Team name','total_minutesOnField']]
    df_kanterminutter = df_kanterminutter.groupby(['Player id']).sum(numeric_only=True)
    df_kanterminutter = df_kanterminutter[df_kanterminutter['total_minutesOnField'] >=samlettid]


    df_Angribere = df[df['position_codes'].str.contains('|'.join(['cf','ss']))]
    df_Angribere = df_Angribere[df_Angribere['total_minutesOnField'] >= tidprkamp]
    df_angribereminutter = df_Angribere[['Player name','Team name','total_minutesOnField']]
    df_angribereminutter = df_angribereminutter.groupby(['Player id']).sum(numeric_only=True)
    df_angribereminutter = df_angribereminutter[df_angribereminutter['total_minutesOnField'] >= samlettid]


    df_backs = pd.merge(df_backsminutter,df_backs,on=('Player id'))
    df_backs = df_backs[df_backs['total_minutesOnField_y'] >=tidprkamp]

    df_backs['Accurate crosses score'] = pd.qcut(df_backs['percent_successfulCrosses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_backs['Number of crosses score'] = pd.qcut(df_backs['average_crosses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_backs['XA score'] = pd.qcut(df_backs['average_xgAssist'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_backs['Passes to final third score'] = pd.qcut(df_backs['average_successfulPassesToFinalThird'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_backs['Successful dribbles score'] = pd.qcut(df_backs['percent_newSuccessfulDribbles'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_backs['Defensive duels won score'] = pd.qcut(df_backs['percent_newDefensiveDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_backs['Progressive runs score'] = pd.qcut(df_backs['average_progressiveRun'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_backs['Offensive duels won score'] = pd.qcut(df_backs['percent_newOffensiveDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_backs['Accelerations score'] = pd.qcut(df_backs['average_accelerations'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_backs['Duels won score'] = pd.qcut(df_backs['percent_newDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_backs['Interceptions score'] = pd.qcut(df_backs['average_interceptions'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_backs['Successful defensive actions score'] = pd.qcut(df_backs['average_successfulDefensiveAction'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_backssæsonen = df_backs[['label','Player name','Team name','total_minutesOnField_x','total_minutesOnField_y','Number of crosses score','Accurate crosses score','XA score','Passes to final third score','Successful dribbles score','Defensive duels won score','Progressive runs score','Offensive duels won score','Accelerations score','Duels won score','Interceptions score','Successful defensive actions score']]
    df_backssæsonen.rename(columns={'total_minutesOnField_x':'Total minutes'},inplace=True)
    df_backssæsonen = df_backssæsonen.groupby(['Player name','Team name','Total minutes','label']).mean(numeric_only=True)

    df_backssæsonen['Indlægsstærk'] = (df_backssæsonen['Number of crosses score'] + df_backssæsonen['Accurate crosses score'] + df_backssæsonen['XA score'] + df_backssæsonen['Passes to final third score'])/4
    df_backssæsonen['1v1 færdigheder'] = (df_backssæsonen['Successful dribbles score'] + df_backssæsonen['Defensive duels won score'] + df_backssæsonen['Progressive runs score'] + df_backssæsonen['Offensive duels won score'] + df_backssæsonen['Accelerations score'] + df_backssæsonen['Duels won score'])/6
    df_backssæsonen['Spilintelligens defensivt'] = (df_backssæsonen['Interceptions score'] + df_backssæsonen['Successful defensive actions score'] + df_backssæsonen['Duels won score'] + df_backssæsonen['Defensive duels won score'])/4
    df_backssæsonen['Fart'] = (df_backssæsonen['Successful dribbles score'] + df_backssæsonen['Progressive runs score'] + df_backssæsonen['Offensive duels won score'] + df_backssæsonen['Accelerations score'])/4
    df_backssæsonen ['Samlet'] = (df_backssæsonen['Indlægsstærk'] + df_backssæsonen['1v1 færdigheder'] + df_backssæsonen['Spilintelligens defensivt'] + df_backssæsonen['Fart'])/4

    df_backssæsonen = df_backssæsonen[['Indlægsstærk','1v1 færdigheder','Spilintelligens defensivt','Fart','Samlet']]
    df_backssæsonen = df_backssæsonen.round(3).astype(float)
    df_backssæsonen = df_backssæsonen.sort_values(by='Samlet',ascending=False)
    with st.expander('Backs kamp for kamp'):
        st.write(df_backssæsonen)
    df_backssæsonen = df_backssæsonen.reset_index()
    df_backssæsonen = df_backssæsonen.drop('label',axis=1)
    df_backssæsonen = df_backssæsonen.groupby(['Player name','Team name','Total minutes']).mean(numeric_only=True)
    df_backssæsonen = df_backssæsonen.sort_values(by='Samlet',ascending=False)
    with st.expander('Backs'):
        st.dataframe(df_backssæsonen)
       
    df_Stoppere = pd.merge(df_stoppereminutter,df_Stoppere,on=('Player id'))
    df_Stoppere = df_Stoppere[df_Stoppere['total_minutesOnField_y'] >=tidprkamp]
    
    df_Stoppere['Accurate passes score'] = pd.qcut(df_Stoppere['percent_successfulPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Accurate long passes score'] = pd.qcut(df_Stoppere['percent_successfulLongPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Forward passes score'] = pd.qcut(df_Stoppere['average_successfulForwardPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Accurate forward passes score'] = pd.qcut(df_Stoppere['percent_successfulForwardPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Accurate progressive passes score'] = pd.qcut(df_Stoppere['percent_successfulProgressivePasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Accurate vertical passes score'] = pd.qcut(df_Stoppere['percent_successfulVerticalPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Interceptions score'] = pd.qcut(df_Stoppere['average_interceptions'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Succesful defensive actions score'] = pd.qcut(df_Stoppere['average_successfulDefensiveAction'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Shots blocked score'] = pd.qcut(df_Stoppere['average_shotsBlocked'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Defensive duels won score'] = pd.qcut(df_Stoppere['average_newDefensiveDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Defensive duels won % score'] = pd.qcut(df_Stoppere['percent_newDefensiveDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Accurate passes to final third'] = pd.qcut(df_Stoppere['percent_successfulPassesToFinalThird'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Accurate through passes'] = pd.qcut(df_Stoppere['percent_successfulThroughPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Vertical passes'] = pd.qcut(df_Stoppere['average_successfulVerticalPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Through passes'] = pd.qcut(df_Stoppere['average_successfulThroughPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Passes to final third'] = pd.qcut(df_Stoppere['average_successfulPassesToFinalThird'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Progressive runs'] = pd.qcut(df_Stoppere['average_progressiveRun'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Offensive duels won %'] = pd.qcut(df_Stoppere['percent_newOffensiveDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Successful dribbles %'] = pd.qcut(df_Stoppere['percent_newSuccessfulDribbles'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Progressive passes score'] = pd.qcut(df_Stoppere['average_successfulProgressivePasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Aerial duels won score'] = pd.qcut(df_Stoppere['average_fieldAerialDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Aerial duels won % score'] = pd.qcut(df_Stoppere['percent_aerialDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)

    df_Stopperesæsonen = df_Stoppere[['label','Player name','Team name','total_minutesOnField_x','total_minutesOnField_y','Accurate passes score','Accurate long passes score','Forward passes score','Accurate forward passes score','Accurate progressive passes score','Accurate vertical passes score','Interceptions score','Succesful defensive actions score','Shots blocked score','Defensive duels won score','Defensive duels won % score','Accurate passes to final third','Accurate through passes','Vertical passes','Through passes','Passes to final third','Progressive passes score','Aerial duels won score','Aerial duels won % score','Progressive runs','Offensive duels won %','Successful dribbles %']]
    df_Stopperesæsonen.rename(columns={'total_minutesOnField_x':'Total minutes'},inplace=True)
    df_Stopperesæsonen = df_Stopperesæsonen.groupby(['Player name','Team name','Total minutes','label']).mean(numeric_only=True)
    df_Stopperesæsonen['Pasningssikker'] = (df_Stopperesæsonen['Accurate passes score'] + df_Stopperesæsonen['Accurate long passes score'] + df_Stopperesæsonen['Forward passes score'] + df_Stopperesæsonen['Accurate forward passes score'] + df_Stopperesæsonen['Accurate progressive passes score'] + df_Stopperesæsonen['Accurate vertical passes score'])/6
    df_Stopperesæsonen['Spilintelligens defensivt'] = (df_Stopperesæsonen['Interceptions score'] + df_Stopperesæsonen['Succesful defensive actions score'] + df_Stopperesæsonen['Shots blocked score'] + df_Stopperesæsonen['Succesful defensive actions score'] + df_Stopperesæsonen['Defensive duels won % score']) /5
    df_Stopperesæsonen['Spilintelligens offensivt'] = (df_Stopperesæsonen['Forward passes score'] + df_Stopperesæsonen['Accurate forward passes score'] + df_Stopperesæsonen['Accurate passes to final third'] + df_Stopperesæsonen['Passes to final third'] + df_Stopperesæsonen['Accurate progressive passes score'] + df_Stopperesæsonen['Progressive passes score'] + df_Stopperesæsonen['Through passes'] + df_Stopperesæsonen['Accurate through passes']+ df_Stopperesæsonen['Progressive runs'] + df_Stopperesæsonen['Offensive duels won %'] + df_Stopperesæsonen['Successful dribbles %'])/11
    df_Stopperesæsonen['Nærkamps- og duelstærk'] = (df_Stopperesæsonen['Defensive duels won % score'] + df_Stopperesæsonen['Aerial duels won % score'] + df_Stopperesæsonen['Defensive duels won % score'])/3
    df_Stopperesæsonen['Samlet'] = (df_Stopperesæsonen['Pasningssikker'] + df_Stopperesæsonen['Spilintelligens defensivt'] + df_Stopperesæsonen['Spilintelligens offensivt'] + df_Stopperesæsonen['Nærkamps- og duelstærk'])/4

    df_Stopperesæsonen = df_Stopperesæsonen[['Pasningssikker','Spilintelligens defensivt','Spilintelligens offensivt','Nærkamps- og duelstærk','Samlet']]
    df_Stopperesæsonen = df_Stopperesæsonen.sort_values(by='Samlet',ascending=False)

    with st.expander('Stoppere kamp for kamp'):
        st.write(df_Stopperesæsonen)
    df_Stopperesæsonen = df_Stopperesæsonen.reset_index()
    df_Stopperesæsonen = df_Stopperesæsonen.drop('label',axis=1)
    df_Stopperesæsonen = df_Stopperesæsonen.groupby(['Player name','Team name','Total minutes']).mean(numeric_only=True)
    df_Stopperesæsonen = df_Stopperesæsonen.sort_values(by='Samlet',ascending=False)
    
    with st.expander('Stoppere sæson'):
        st.dataframe(df_Stopperesæsonen)

    df_Centrale_midt = pd.merge(df_centraleminutter,df_Centrale_midt,on=('Player id'))
    df_Centrale_midt = df_Centrale_midt[df_Centrale_midt['total_minutesOnField_y'] >=tidprkamp]

    df_Centrale_midt['Passes %'] = pd.qcut(df_Centrale_midt['percent_successfulPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Passes #'] = pd.qcut(df_Centrale_midt['average_successfulPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Forward Passes %'] = pd.qcut(df_Centrale_midt['percent_successfulForwardPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Forward Passes #'] = pd.qcut(df_Centrale_midt['average_successfulForwardPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Long Passes %'] = pd.qcut(df_Centrale_midt['percent_successfulLongPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Long Passes #'] = pd.qcut(df_Centrale_midt['average_successfulLongPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Smart passes %'] = pd.qcut(df_Centrale_midt['percent_successfulSmartPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Smart passes #'] = pd.qcut(df_Centrale_midt['average_successfulSmartPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Key passes %'] = pd.qcut(df_Centrale_midt['percent_successfulKeyPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Key passes #'] = pd.qcut(df_Centrale_midt['average_successfulKeyPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Passes to final third %'] = pd.qcut(df_Centrale_midt['percent_successfulPassesToFinalThird'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Passes to final third #'] = pd.qcut(df_Centrale_midt['average_successfulPassesToFinalThird'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Vertical passes %'] = pd.qcut(df_Centrale_midt['percent_successfulVerticalPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Vertical passes #'] = pd.qcut(df_Centrale_midt['average_successfulVerticalPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Through passes %'] = pd.qcut(df_Centrale_midt['percent_successfulThroughPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Through passes #'] = pd.qcut(df_Centrale_midt['average_successfulThroughPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Progressive passes %'] = pd.qcut(df_Centrale_midt['percent_successfulProgressivePasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Progressive passes #'] = pd.qcut(df_Centrale_midt['average_successfulProgressivePasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Offensive duels %'] = pd.qcut(df_Centrale_midt['percent_newOffensiveDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Received passes'] = pd.qcut(df_Centrale_midt['average_receivedPass'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Succesful dribbles %'] = pd.qcut(df_Centrale_midt['percent_newSuccessfulDribbles'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Succesful dribbles #'] = pd.qcut(df_Centrale_midt['average_newSuccessfulDribbles'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Duels won %'] = pd.qcut(df_Centrale_midt['percent_newDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Duels won #'] = pd.qcut(df_Centrale_midt['average_newDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Interceptions'] = pd.qcut(df_Centrale_midt['average_interceptions'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Counterpressing recoveries #'] = pd.qcut(df_Centrale_midt['average_counterpressingRecoveries'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Defensive duels won #'] = pd.qcut(df_Centrale_midt['average_newDefensiveDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Defensive duels won %'] = pd.qcut(df_Centrale_midt['percent_newDefensiveDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)

    df_Centrale_midtsæsonen = df_Centrale_midt.rename(columns={'total_minutesOnField_x':'Total minutes'},inplace=True)
    df_Centrale_midtsæsonen = df_Centrale_midt.groupby(['Player name','Team name','Total minutes','label']).mean(numeric_only=True)
    df_Centrale_midtsæsonen['Pasningssikker/Spilvendinger'] = (df_Centrale_midtsæsonen['Passes %'] + df_Centrale_midtsæsonen['Passes #'] + df_Centrale_midtsæsonen['Forward Passes %'] + df_Centrale_midtsæsonen['Forward Passes #'] + df_Centrale_midtsæsonen['Long Passes %'] + df_Centrale_midtsæsonen['Long Passes #']+ df_Centrale_midtsæsonen['Smart passes %'] + df_Centrale_midtsæsonen['Smart passes #'] + + df_Centrale_midtsæsonen['Key passes %'] + df_Centrale_midtsæsonen['Key passes #'] + df_Centrale_midtsæsonen['Passes to final third %'] + df_Centrale_midtsæsonen['Passes to final third #']+ df_Centrale_midtsæsonen['Vertical passes %'] + df_Centrale_midtsæsonen['Vertical passes #']+ df_Centrale_midtsæsonen['Through passes %'] + df_Centrale_midtsæsonen['Through passes #']+ df_Centrale_midtsæsonen['Progressive passes %'] + df_Centrale_midtsæsonen['Progressive passes #'])/18
    df_Centrale_midtsæsonen['Boldfast'] = (df_Centrale_midtsæsonen['Passes %'] + df_Centrale_midtsæsonen['Passes #']+ df_Centrale_midtsæsonen['Offensive duels %'] + df_Centrale_midtsæsonen['Received passes'] + df_Centrale_midtsæsonen['Succesful dribbles %'] + df_Centrale_midtsæsonen['Succesful dribbles #'])/6
    df_Centrale_midtsæsonen['Spilintelligens defensivt'] = (df_Centrale_midtsæsonen['Duels won %'] + df_Centrale_midtsæsonen['Duels won #'] +df_Centrale_midtsæsonen['Interceptions'] + df_Centrale_midtsæsonen['Counterpressing recoveries #'] + df_Centrale_midtsæsonen['Defensive duels won %'] + df_Centrale_midtsæsonen['Defensive duels won #'])/6
    df_Centrale_midtsæsonen['Samlet'] = (df_Centrale_midtsæsonen['Pasningssikker/Spilvendinger'] + df_Centrale_midtsæsonen['Boldfast'] + df_Centrale_midtsæsonen['Spilintelligens defensivt'])/3

    df_Centrale_midtsæsonen = df_Centrale_midtsæsonen[['Pasningssikker/Spilvendinger','Boldfast','Spilintelligens defensivt','Samlet']]
    df_Centrale_midtsæsonen = df_Centrale_midtsæsonen.sort_values(by='Samlet',ascending=False)
    with st.expander('Centrale midt kamp for kamp'):
        st.write(df_Centrale_midtsæsonen)

    df_Centrale_midtsæsonen = df_Centrale_midtsæsonen.reset_index()
    df_Centrale_midtsæsonen = df_Centrale_midtsæsonen.drop('label',axis=1)
    df_Centrale_midtsæsonen = df_Centrale_midtsæsonen.groupby(['Player name','Team name','Total minutes']).mean(numeric_only=True)
    df_Centrale_midtsæsonen = df_Centrale_midtsæsonen.sort_values(by='Samlet',ascending=False)
    with st.expander('Centrale midt sæson'):
        st.write(df_Centrale_midtsæsonen)


    df_Kanter = pd.merge(df_kanterminutter,df_Kanter,on=('Player id'))
    df_Kanter = df_Kanter[df_Kanter['total_minutesOnField_y'] >=tidprkamp]

    df_Kanter['Shots on target %'] = pd.qcut(df_Kanter['percent_shotsOnTarget'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Shots on target #'] = pd.qcut(df_Kanter['average_shotsOnTarget'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['XG'] = pd.qcut(df_Kanter['average_xgShot'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Successful dribbles #'] = pd.qcut(df_Kanter['average_newSuccessfulDribbles'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Successful dribbles %'] = pd.qcut(df_Kanter['percent_newSuccessfulDribbles'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Offensive duels %'] = pd.qcut(df_Kanter['percent_newOffensiveDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Offensive duels #'] = pd.qcut(df_Kanter['average_newOffensiveDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Passes %'] = pd.qcut(df_Kanter['percent_successfulPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Passes #'] = pd.qcut(df_Kanter['average_successfulPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Forward Passes %'] = pd.qcut(df_Kanter['percent_successfulForwardPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Forward Passes #'] = pd.qcut(df_Kanter['average_successfulForwardPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Smart passes %'] = pd.qcut(df_Kanter['percent_successfulSmartPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Smart passes #'] = pd.qcut(df_Kanter['average_successfulSmartPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Key passes %'] = pd.qcut(df_Kanter['percent_successfulKeyPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Key passes #'] = pd.qcut(df_Kanter['average_successfulKeyPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Passes to final third %'] = pd.qcut(df_Kanter['percent_successfulPassesToFinalThird'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Passes to final third #'] = pd.qcut(df_Kanter['average_successfulPassesToFinalThird'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Vertical passes %'] = pd.qcut(df_Kanter['percent_successfulVerticalPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Vertical passes #'] = pd.qcut(df_Kanter['average_successfulVerticalPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Through passes %'] = pd.qcut(df_Kanter['percent_successfulThroughPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Through passes #'] = pd.qcut(df_Kanter['average_successfulThroughPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Progressive passes %'] = pd.qcut(df_Kanter['percent_successfulProgressivePasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Progressive passes #'] = pd.qcut(df_Kanter['average_successfulProgressivePasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Goal conversion %'] = pd.qcut(df_Kanter['percent_goalConversion'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['XG per 90'] = pd.qcut(df_Kanter['average_xgShot'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['XA per 90'] = pd.qcut(df_Kanter['average_xgAssist'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Successful attacking actions'] = pd.qcut(df_Kanter['average_successfulAttackingActions'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Progressive runs'] = pd.qcut(df_Kanter['average_progressiveRun'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Accelerations score'] = pd.qcut(df_Kanter['average_accelerations'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)

    df_Kantersæsonen = df_Kanter.rename(columns={'total_minutesOnField_x':'Total minutes'},inplace=True)
    df_Kantersæsonen = df_Kanter.groupby(['Player name','Team name','Total minutes','label']).mean(numeric_only=True)

    df_Kantersæsonen['Sparkefærdigheder'] = (df_Kantersæsonen['Shots on target %'] + df_Kantersæsonen['Shots on target #'] + df_Kantersæsonen['XG'] + df_Kantersæsonen['Passes to final third %'] + df_Kantersæsonen['Forward Passes %'] + df_Kantersæsonen['Vertical passes %'])/6
    df_Kantersæsonen['Kombinationsstærk'] = (df_Kantersæsonen['Passes %'] + df_Kantersæsonen['Passes #'] + df_Kantersæsonen['Forward Passes %'] + df_Kantersæsonen['Forward Passes #'] + df_Kantersæsonen['Passes to final third %'] + df_Kantersæsonen['Passes to final third #'] + df_Kantersæsonen['Through passes %'] + df_Kantersæsonen['Through passes #'] + df_Kantersæsonen['Progressive passes %'] + df_Kantersæsonen['Progressive passes #'] + df_Kantersæsonen['Successful attacking actions'])/11
    df_Kantersæsonen['Spilintelligens offensivt/indlægsstærk'] = (df_Kantersæsonen['XA per 90'] + df_Kantersæsonen['XG per 90'] + df_Kantersæsonen['Through passes %'] + df_Kantersæsonen['Through passes #'] + df_Kantersæsonen['Smart passes %'] + df_Kantersæsonen['Smart passes #'] + df_Kantersæsonen['Progressive passes %'] + df_Kantersæsonen['Progressive passes #'] + df_Kantersæsonen['Key passes %'] + df_Kantersæsonen['Key passes #'] + df_Kantersæsonen['Successful attacking actions'])/11
    df_Kantersæsonen['1v1 offensivt'] = (df_Kantersæsonen['Successful dribbles #'] + df_Kantersæsonen['Successful dribbles %'] + df_Kantersæsonen['Offensive duels #'] + df_Kantersæsonen['Offensive duels %'] + df_Kantersæsonen['Progressive runs'])/5
    df_Kantersæsonen['Fart'] = (df_Kantersæsonen['Progressive runs'] + df_Kantersæsonen['Successful dribbles #'] + df_Kantersæsonen['Successful dribbles %'] + df_Kantersæsonen['Accelerations score'])/4
    df_Kantersæsonen['Samlet'] = (df_Kantersæsonen['Sparkefærdigheder'] + df_Kantersæsonen['Kombinationsstærk'] + df_Kantersæsonen['Spilintelligens offensivt/indlægsstærk'] + df_Kantersæsonen['1v1 offensivt'] + df_Kantersæsonen['Fart'])/5
    df_Kantersæsonen = df_Kantersæsonen[['Sparkefærdigheder','Kombinationsstærk','Spilintelligens offensivt/indlægsstærk','1v1 offensivt','Fart','Samlet']]
    df_Kantersæsonen = df_Kantersæsonen.sort_values(by='Samlet',ascending=False)

    with st.expander('Kanter kamp for kamp'):
        st.write(df_Kantersæsonen)

    df_Kantersæsonen = df_Kantersæsonen.reset_index()
    df_Kantersæsonen = df_Kantersæsonen.drop('label',axis=1)
    df_Kantersæsonen = df_Kantersæsonen.groupby(['Player name','Team name','Total minutes']).mean(numeric_only=True)
    df_Kantersæsonen = df_Kantersæsonen.sort_values(by='Samlet',ascending=False)
    with st.expander('Kanter sæson'):
        st.write(df_Kantersæsonen)


    df_Angribere = pd.merge(df_angribereminutter,df_Angribere,on=('Player id'))
    df_Angribere = df_Angribere[df_Angribere['total_minutesOnField_y'] >=tidprkamp]

    df_Angribere['Målfarlighed udregning'] = df_Angribere['average_goals'] - df_Angribere['average_xgShot']
    df_Angribere['Målfarlighed score'] =  pd.qcut(df_Angribere['Målfarlighed udregning'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Angribere['xG per 90 score'] = pd.qcut(df_Angribere['average_xgShot'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Angribere['Goals per 90 score'] = pd.qcut(df_Angribere['average_goals'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)  
    df_Angribere['Shots on target, % score'] = pd.qcut(df_Angribere['percent_shotsOnTarget'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)   
    df_Angribere['Offensive duels won, % score'] = pd.qcut(df_Angribere['percent_newOffensiveDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Angribere['Duels won, % score'] = pd.qcut(df_Angribere['percent_newDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Angribere['Accurate passes, % score'] = pd.qcut(df_Angribere['percent_successfulPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Angribere['Successful dribbles, % score'] = pd.qcut(df_Angribere['percent_newSuccessfulDribbles'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Angribere['xA per 90 score'] = pd.qcut(df_Angribere['average_xgAssist'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Angribere['Touches in box per 90 score'] = pd.qcut(df_Angribere['average_touchInBox'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Angribere['Progressive runs'] = pd.qcut(df_Angribere['average_progressiveRun'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Angribere['Accelerations score'] = pd.qcut(df_Angribere['average_accelerations'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Angribere['Progressive passes per 90 score'] = pd.qcut(df_Angribere['average_successfulProgressivePasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Angribere['Successful attacking actions per 90 score'] = pd.qcut(df_Angribere['average_successfulAttackingActions'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Angribere['Successful dribbles #'] = pd.qcut(df_Angribere['average_newSuccessfulDribbles'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)

    df_Angriberesæsonen = df_Angribere.rename(columns={'total_minutesOnField_x':'Total minutes'},inplace=True)
    df_Angriberesæsonen = df_Angribere.groupby(['Player name','Team name','Total minutes','label']).mean(numeric_only=True)

    df_Angriberesæsonen['Sparkefærdigheder'] = (df_Angriberesæsonen['xG per 90 score'] + df_Angriberesæsonen['xG per 90 score'] + df_Angriberesæsonen['Goals per 90 score'] + df_Angriberesæsonen['Shots on target, % score'])/4
    df_Angriberesæsonen['Boldfast'] = (df_Angriberesæsonen['Offensive duels won, % score'] + df_Angriberesæsonen['Offensive duels won, % score'] + df_Angriberesæsonen['Duels won, % score'] + df_Angriberesæsonen['Accurate passes, % score'] + df_Angriberesæsonen['Successful dribbles, % score'])/5
    df_Angriberesæsonen['Spilintelligens offensivt'] = (df_Angriberesæsonen['xA per 90 score'] + df_Angriberesæsonen['xG per 90 score'] + df_Angriberesæsonen['Touches in box per 90 score'] + df_Angriberesæsonen['Progressive passes per 90 score'] + df_Angriberesæsonen['Successful attacking actions per 90 score'] + df_Angriberesæsonen['Touches in box per 90 score'] + df_Angriberesæsonen['xG per 90 score'])/7
    df_Angriberesæsonen['Målfarlighed'] = (df_Angriberesæsonen['xG per 90 score']+df_Angriberesæsonen['Goals per 90 score']+df_Angriberesæsonen['xG per 90 score'] + df_Angriberesæsonen['Målfarlighed score'])/4
    df_Angriberesæsonen['Fart'] = (df_Angriberesæsonen['Progressive runs'] + + df_Angriberesæsonen['Progressive runs'] + df_Angriberesæsonen['Progressive runs'] + df_Angriberesæsonen['Successful dribbles #'] + df_Angriberesæsonen['Successful dribbles, % score'] + df_Angriberesæsonen['Accelerations score'] + df_Angriberesæsonen['Offensive duels won, % score'])/7
    df_Angriberesæsonen = df_Angriberesæsonen[['Sparkefærdigheder','Boldfast','Spilintelligens offensivt','Målfarlighed','Fart']]
    df_Angriberesæsonen['Samlet'] = (df_Angriberesæsonen['Sparkefærdigheder']+df_Angriberesæsonen['Boldfast']+df_Angriberesæsonen['Spilintelligens offensivt']+df_Angriberesæsonen['Målfarlighed']+df_Angriberesæsonen['Målfarlighed']+df_Angriberesæsonen['Målfarlighed']+df_Angriberesæsonen['Fart'])/7
    df_Angriberesæsonen = df_Angriberesæsonen.sort_values(by='Samlet',ascending=False)

    with st.expander('Angribere kamp for kamp'):
        st.write(df_Angriberesæsonen)

    df_Angriberesæsonen = df_Angriberesæsonen.reset_index()
    df_Angriberesæsonen = df_Angriberesæsonen.drop('label',axis=1)
    df_Angriberesæsonen = df_Angriberesæsonen.groupby(['Player name','Team name','Total minutes']).mean(numeric_only=True)
    df_Angriberesæsonen = df_Angriberesæsonen.sort_values(by='Samlet',ascending=False)
    with st.expander('Angribere sæson'):
        st.write(df_Angriberesæsonen)
    df = pd.read_csv(r'xT/Superliga 23 24.csv')

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


    dfscore = pd.read_csv(r'xT/Zone scores.csv')

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

    xgc = df1
    xgchold = xgc.rename(columns={'shot.xg': 'Hold xG'})
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
        
def Første_division ():
    col1,col2 = st.columns(2)
    with col1:
        samlettid = st.number_input('Minutter i sæsonen')
    with col2:    
        tidprkamp = st.number_input('Minutter pr. kamp')
        
    df = pd.read_csv(r'Individuelt dashboard/Individuelt dashboard 1.div.csv')
    df.rename(columns={'playerId': 'Player id'}, inplace=True)
    df = df.astype(str)
    dfevents = pd.read_csv('1.div eventdata alle.csv',low_memory=False)
    dfevents = dfevents[['Player id','Player name','team_name','label','date','matchId']]
    dfspillernavn = df[['Player id','matchId','positions','average','percent','total']]
    dfspillernavn = dfspillernavn.astype(str)
    dfevents['Player id'] = dfevents['Player id'].astype(str)
    dfevents['matchId'] = dfevents['matchId'].astype(str)
    df = dfspillernavn.merge(dfevents)

    df['Player&matchId'] = df['Player id'] + df['matchId']
    df['Player&matchId'] = df['Player&matchId'].drop_duplicates(keep='first')
    df = df.dropna()
    df = df[['Player id','Player name','team_name','matchId','label','date','positions','average','percent','total']]

    #df = df.set_index('Player id')

    data = df['positions']
    df1 = pd.DataFrame(data)
    # Funktion, der ekstraherer navne og koder fra strengdata og opretter en ny kolonne med disse værdier
    def extract_positions(data):
        positions_list = ast.literal_eval(data) # Konverterer strengen til en liste af ordbøger
        names = [pos['position']['name'] for pos in positions_list]
        codes = [pos['position']['code'] for pos in positions_list]
        return pd.Series({'position_names': names, 'position_codes': codes})

    # Anvender funktionen på kolonnen og tilføjer resultaterne som nye kolonner til dataframe
    df1[['position_names', 'position_codes']] = df1['positions'].apply(extract_positions)

    df = pd.merge(df,df1,left_index=True, right_index=True)
    df = df.set_index('Player id')
    df = df.drop(columns=['positions_x'])
    df = df.drop(columns=['positions_y'])
    df = df[['Player name','team_name','matchId','label','date','position_names','position_codes','average','percent','total']]
    df = df.rename(columns={'team_name':'Team name'})
    df['percent'] = df['percent'].apply(lambda x: ast.literal_eval(x))

    # Create a new dataframe with the columns as the dictionary keys and the values as a list
    new_df = pd.DataFrame(df['percent'].to_list(), index=df.index).add_prefix('percent_')

    # Concatenate the new dataframe with the original dataframe
    df = pd.concat([df, new_df], axis=1)

    # Drop the original 'percent' column
    df = df.drop('percent', axis=1)

    df['total'] = df['total'].apply(lambda x: ast.literal_eval(x))

    # Create a new dataframe with the columns as the dictionary keys and the values as a list
    new_df = pd.DataFrame(df['total'].to_list(), index=df.index).add_prefix('total_')

    # Concatenate the new dataframe with the original dataframe
    df = pd.concat([df, new_df], axis=1)

    # Drop the original 'percent' column
    df = df.drop('total', axis=1)

    df['average'] = df['average'].apply(lambda x: ast.literal_eval(x))

    # Create a new dataframe with the columns as the dictionary keys and the values as a list
    new_df = pd.DataFrame(df['average'].to_list(), index=df.index).add_prefix('average_')

    # Concatenate the new dataframe with the original dataframe
    df = pd.concat([df, new_df], axis=1)


    # Drop the original 'percent' column
    df = df.drop('average', axis=1)
    df['position_codes'] = df['position_codes'].astype(str)
    #df['date'] = df['date'].astype(str)
    #df['date'] = df['date'].apply(lambda x: parser.parse(x))

    # Sort the dataframe by the 'date' column
    #df = df.sort_values(by='date',ascending=False)

    # Format the 'date' column to day-month-year format
    #df['date'] = df['date'].apply(lambda x: x.strftime('%d-%m-%Y'))
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date',ascending=False)

    df_backs = df[df['position_codes'].str.contains('|'.join(['lb', 'rb']))]
    df_backs = df_backs[df_backs['total_minutesOnField'] >= tidprkamp]
    df_backsminutter = df_backs[['Player name','Team name','total_minutesOnField']]
    df_backsminutter = df_backsminutter.groupby(['Player id']).sum(numeric_only=True)
    df_backsminutter = df_backsminutter[df_backsminutter['total_minutesOnField'] >= samlettid]

    df_Stoppere = df[df['position_codes'].str.contains('|'.join(['cb']))]
    df_Stoppere = df_Stoppere[df_Stoppere['total_minutesOnField'] >= tidprkamp]
    df_stoppereminutter = df_Stoppere[['Player name','Team name','total_minutesOnField']]
    df_stoppereminutter = df_stoppereminutter.groupby(['Player id']).sum(numeric_only=True)
    df_stoppereminutter = df_stoppereminutter[df_stoppereminutter['total_minutesOnField'] >= samlettid]

    df_Centrale_midt = df[df['position_codes'].str.contains('|'.join(['cm','amf','dmf']))]
    df_Centrale_midt = df_Centrale_midt[df_Centrale_midt['total_minutesOnField'] >= tidprkamp]
    df_centraleminutter = df_Centrale_midt[['Player name','Team name','total_minutesOnField']]
    df_centraleminutter = df_centraleminutter.groupby(['Player id']).sum(numeric_only=True)
    df_centraleminutter = df_centraleminutter[df_centraleminutter['total_minutesOnField'] >= samlettid]

    df_Kanter = df[df['position_codes'].str.contains('|'.join(['rw','lw','ramf','lamf']))]
    df_Kanter = df_Kanter[df_Kanter['total_minutesOnField'] >=tidprkamp]
    df_kanterminutter = df_Kanter[['Player name','Team name','total_minutesOnField']]
    df_kanterminutter = df_kanterminutter.groupby(['Player id']).sum(numeric_only=True)
    df_kanterminutter = df_kanterminutter[df_kanterminutter['total_minutesOnField'] >=samlettid]


    df_Angribere = df[df['position_codes'].str.contains('|'.join(['cf','ss']))]
    df_Angribere = df_Angribere[df_Angribere['total_minutesOnField'] >= tidprkamp]
    df_angribereminutter = df_Angribere[['Player name','Team name','total_minutesOnField']]
    df_angribereminutter = df_angribereminutter.groupby(['Player id']).sum(numeric_only=True)
    df_angribereminutter = df_angribereminutter[df_angribereminutter['total_minutesOnField'] >= samlettid]


    df_backs = pd.merge(df_backsminutter,df_backs,on=('Player id'))
    df_backs = df_backs[df_backs['total_minutesOnField_y'] >=tidprkamp]

    df_backs['Accurate crosses score'] = pd.qcut(df_backs['percent_successfulCrosses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_backs['Number of crosses score'] = pd.qcut(df_backs['average_crosses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_backs['XA score'] = pd.qcut(df_backs['average_xgAssist'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_backs['Passes to final third score'] = pd.qcut(df_backs['average_successfulPassesToFinalThird'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_backs['Successful dribbles score'] = pd.qcut(df_backs['percent_newSuccessfulDribbles'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_backs['Defensive duels won score'] = pd.qcut(df_backs['percent_newDefensiveDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_backs['Progressive runs score'] = pd.qcut(df_backs['average_progressiveRun'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_backs['Offensive duels won score'] = pd.qcut(df_backs['percent_newOffensiveDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_backs['Accelerations score'] = pd.qcut(df_backs['average_accelerations'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_backs['Duels won score'] = pd.qcut(df_backs['percent_newDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_backs['Interceptions score'] = pd.qcut(df_backs['average_interceptions'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_backs['Successful defensive actions score'] = pd.qcut(df_backs['average_successfulDefensiveAction'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_backssæsonen = df_backs[['label','Player name','Team name','total_minutesOnField_x','total_minutesOnField_y','Number of crosses score','Accurate crosses score','XA score','Passes to final third score','Successful dribbles score','Defensive duels won score','Progressive runs score','Offensive duels won score','Accelerations score','Duels won score','Interceptions score','Successful defensive actions score']]
    df_backssæsonen.rename(columns={'total_minutesOnField_x':'Total minutes'},inplace=True)
    df_backssæsonen = df_backssæsonen.groupby(['Player name','Team name','Total minutes','label']).mean(numeric_only=True)

    df_backssæsonen['Indlægsstærk'] = (df_backssæsonen['Number of crosses score'] + df_backssæsonen['Accurate crosses score'] + df_backssæsonen['XA score'] + df_backssæsonen['Passes to final third score'])/4
    df_backssæsonen['1v1 færdigheder'] = (df_backssæsonen['Successful dribbles score'] + df_backssæsonen['Defensive duels won score'] + df_backssæsonen['Progressive runs score'] + df_backssæsonen['Offensive duels won score'] + df_backssæsonen['Accelerations score'] + df_backssæsonen['Duels won score'])/6
    df_backssæsonen['Spilintelligens defensivt'] = (df_backssæsonen['Interceptions score'] + df_backssæsonen['Successful defensive actions score'] + df_backssæsonen['Duels won score'] + df_backssæsonen['Defensive duels won score'])/4
    df_backssæsonen['Fart'] = (df_backssæsonen['Successful dribbles score'] + df_backssæsonen['Progressive runs score'] + df_backssæsonen['Offensive duels won score'] + df_backssæsonen['Accelerations score'])/4
    df_backssæsonen ['Samlet'] = (df_backssæsonen['Indlægsstærk'] + df_backssæsonen['1v1 færdigheder'] + df_backssæsonen['Spilintelligens defensivt'] + df_backssæsonen['Fart'])/4

    df_backssæsonen = df_backssæsonen[['Indlægsstærk','1v1 færdigheder','Spilintelligens defensivt','Fart','Samlet']]
    df_backssæsonen = df_backssæsonen.round(3).astype(float)
    df_backssæsonen = df_backssæsonen.sort_values(by='Samlet',ascending=False)
    with st.expander('Backs kamp for kamp'):
        st.write(df_backssæsonen)
    df_backssæsonen = df_backssæsonen.reset_index()
    df_backssæsonen = df_backssæsonen.drop('label',axis=1)
    df_backssæsonen = df_backssæsonen.groupby(['Player name','Team name','Total minutes']).mean(numeric_only=True)
    df_backssæsonen = df_backssæsonen.sort_values(by='Samlet',ascending=False)
    with st.expander('Backs'):
        st.dataframe(df_backssæsonen)
       
    df_Stoppere = pd.merge(df_stoppereminutter,df_Stoppere,on=('Player id'))
    df_Stoppere = df_Stoppere[df_Stoppere['total_minutesOnField_y'] >=tidprkamp]
    
    df_Stoppere['Accurate passes score'] = pd.qcut(df_Stoppere['percent_successfulPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Accurate long passes score'] = pd.qcut(df_Stoppere['percent_successfulLongPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Forward passes score'] = pd.qcut(df_Stoppere['average_successfulForwardPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Accurate forward passes score'] = pd.qcut(df_Stoppere['percent_successfulForwardPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Accurate progressive passes score'] = pd.qcut(df_Stoppere['percent_successfulProgressivePasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Accurate vertical passes score'] = pd.qcut(df_Stoppere['percent_successfulVerticalPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Interceptions score'] = pd.qcut(df_Stoppere['average_interceptions'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Succesful defensive actions score'] = pd.qcut(df_Stoppere['average_successfulDefensiveAction'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Shots blocked score'] = pd.qcut(df_Stoppere['average_shotsBlocked'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Defensive duels won score'] = pd.qcut(df_Stoppere['average_newDefensiveDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Defensive duels won % score'] = pd.qcut(df_Stoppere['percent_newDefensiveDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Accurate passes to final third'] = pd.qcut(df_Stoppere['percent_successfulPassesToFinalThird'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Accurate through passes'] = pd.qcut(df_Stoppere['percent_successfulThroughPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Vertical passes'] = pd.qcut(df_Stoppere['average_successfulVerticalPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Through passes'] = pd.qcut(df_Stoppere['average_successfulThroughPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Passes to final third'] = pd.qcut(df_Stoppere['average_successfulPassesToFinalThird'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Progressive runs'] = pd.qcut(df_Stoppere['average_progressiveRun'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Offensive duels won %'] = pd.qcut(df_Stoppere['percent_newOffensiveDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Successful dribbles %'] = pd.qcut(df_Stoppere['percent_newSuccessfulDribbles'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Progressive passes score'] = pd.qcut(df_Stoppere['average_successfulProgressivePasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Aerial duels won score'] = pd.qcut(df_Stoppere['average_fieldAerialDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Aerial duels won % score'] = pd.qcut(df_Stoppere['percent_aerialDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)

    df_Stopperesæsonen = df_Stoppere[['label','Player name','Team name','total_minutesOnField_x','total_minutesOnField_y','Accurate passes score','Accurate long passes score','Forward passes score','Accurate forward passes score','Accurate progressive passes score','Accurate vertical passes score','Interceptions score','Succesful defensive actions score','Shots blocked score','Defensive duels won score','Defensive duels won % score','Accurate passes to final third','Accurate through passes','Vertical passes','Through passes','Passes to final third','Progressive passes score','Aerial duels won score','Aerial duels won % score','Progressive runs','Offensive duels won %','Successful dribbles %']]
    df_Stopperesæsonen.rename(columns={'total_minutesOnField_x':'Total minutes'},inplace=True)
    df_Stopperesæsonen = df_Stopperesæsonen.groupby(['Player name','Team name','Total minutes','label']).mean(numeric_only=True)
    df_Stopperesæsonen['Pasningssikker'] = (df_Stopperesæsonen['Accurate passes score'] + df_Stopperesæsonen['Accurate long passes score'] + df_Stopperesæsonen['Forward passes score'] + df_Stopperesæsonen['Accurate forward passes score'] + df_Stopperesæsonen['Accurate progressive passes score'] + df_Stopperesæsonen['Accurate vertical passes score'])/6
    df_Stopperesæsonen['Spilintelligens defensivt'] = (df_Stopperesæsonen['Interceptions score'] + df_Stopperesæsonen['Succesful defensive actions score'] + df_Stopperesæsonen['Shots blocked score'] + df_Stopperesæsonen['Succesful defensive actions score'] + df_Stopperesæsonen['Defensive duels won % score']) /5
    df_Stopperesæsonen['Spilintelligens offensivt'] = (df_Stopperesæsonen['Forward passes score'] + df_Stopperesæsonen['Accurate forward passes score'] + df_Stopperesæsonen['Accurate passes to final third'] + df_Stopperesæsonen['Passes to final third'] + df_Stopperesæsonen['Accurate progressive passes score'] + df_Stopperesæsonen['Progressive passes score'] + df_Stopperesæsonen['Through passes'] + df_Stopperesæsonen['Accurate through passes']+ df_Stopperesæsonen['Progressive runs'] + df_Stopperesæsonen['Offensive duels won %'] + df_Stopperesæsonen['Successful dribbles %'])/11
    df_Stopperesæsonen['Nærkamps- og duelstærk'] = (df_Stopperesæsonen['Defensive duels won % score'] + df_Stopperesæsonen['Aerial duels won % score'] + df_Stopperesæsonen['Defensive duels won % score'])/3
    df_Stopperesæsonen['Samlet'] = (df_Stopperesæsonen['Pasningssikker'] + df_Stopperesæsonen['Spilintelligens defensivt'] + df_Stopperesæsonen['Spilintelligens offensivt'] + df_Stopperesæsonen['Nærkamps- og duelstærk'])/4

    df_Stopperesæsonen = df_Stopperesæsonen[['Pasningssikker','Spilintelligens defensivt','Spilintelligens offensivt','Nærkamps- og duelstærk','Samlet']]
    df_Stopperesæsonen = df_Stopperesæsonen.sort_values(by='Samlet',ascending=False)

    with st.expander('Stoppere kamp for kamp'):
        st.write(df_Stopperesæsonen)
    df_Stopperesæsonen = df_Stopperesæsonen.reset_index()
    df_Stopperesæsonen = df_Stopperesæsonen.drop('label',axis=1)
    df_Stopperesæsonen = df_Stopperesæsonen.groupby(['Player name','Team name','Total minutes']).mean(numeric_only=True)
    df_Stopperesæsonen = df_Stopperesæsonen.sort_values(by='Samlet',ascending=False)
    
    with st.expander('Stoppere sæson'):
        st.dataframe(df_Stopperesæsonen)

    df_Centrale_midt = pd.merge(df_centraleminutter,df_Centrale_midt,on=('Player id'))
    df_Centrale_midt = df_Centrale_midt[df_Centrale_midt['total_minutesOnField_y'] >=tidprkamp]

    df_Centrale_midt['Passes %'] = pd.qcut(df_Centrale_midt['percent_successfulPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Passes #'] = pd.qcut(df_Centrale_midt['average_successfulPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Forward Passes %'] = pd.qcut(df_Centrale_midt['percent_successfulForwardPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Forward Passes #'] = pd.qcut(df_Centrale_midt['average_successfulForwardPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Long Passes %'] = pd.qcut(df_Centrale_midt['percent_successfulLongPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Long Passes #'] = pd.qcut(df_Centrale_midt['average_successfulLongPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Smart passes %'] = pd.qcut(df_Centrale_midt['percent_successfulSmartPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Smart passes #'] = pd.qcut(df_Centrale_midt['average_successfulSmartPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Key passes %'] = pd.qcut(df_Centrale_midt['percent_successfulKeyPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Key passes #'] = pd.qcut(df_Centrale_midt['average_successfulKeyPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Passes to final third %'] = pd.qcut(df_Centrale_midt['percent_successfulPassesToFinalThird'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Passes to final third #'] = pd.qcut(df_Centrale_midt['average_successfulPassesToFinalThird'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Vertical passes %'] = pd.qcut(df_Centrale_midt['percent_successfulVerticalPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Vertical passes #'] = pd.qcut(df_Centrale_midt['average_successfulVerticalPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Through passes %'] = pd.qcut(df_Centrale_midt['percent_successfulThroughPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Through passes #'] = pd.qcut(df_Centrale_midt['average_successfulThroughPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Progressive passes %'] = pd.qcut(df_Centrale_midt['percent_successfulProgressivePasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Progressive passes #'] = pd.qcut(df_Centrale_midt['average_successfulProgressivePasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Offensive duels %'] = pd.qcut(df_Centrale_midt['percent_newOffensiveDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Received passes'] = pd.qcut(df_Centrale_midt['average_receivedPass'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Succesful dribbles %'] = pd.qcut(df_Centrale_midt['percent_newSuccessfulDribbles'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Succesful dribbles #'] = pd.qcut(df_Centrale_midt['average_newSuccessfulDribbles'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Duels won %'] = pd.qcut(df_Centrale_midt['percent_newDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Duels won #'] = pd.qcut(df_Centrale_midt['average_newDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Interceptions'] = pd.qcut(df_Centrale_midt['average_interceptions'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Counterpressing recoveries #'] = pd.qcut(df_Centrale_midt['average_counterpressingRecoveries'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Defensive duels won #'] = pd.qcut(df_Centrale_midt['average_newDefensiveDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Defensive duels won %'] = pd.qcut(df_Centrale_midt['percent_newDefensiveDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)

    df_Centrale_midtsæsonen = df_Centrale_midt.rename(columns={'total_minutesOnField_x':'Total minutes'},inplace=True)
    df_Centrale_midtsæsonen = df_Centrale_midt.groupby(['Player name','Team name','Total minutes','label']).mean(numeric_only=True)
    df_Centrale_midtsæsonen['Pasningssikker/Spilvendinger'] = (df_Centrale_midtsæsonen['Passes %'] + df_Centrale_midtsæsonen['Passes #'] + df_Centrale_midtsæsonen['Forward Passes %'] + df_Centrale_midtsæsonen['Forward Passes #'] + df_Centrale_midtsæsonen['Long Passes %'] + df_Centrale_midtsæsonen['Long Passes #']+ df_Centrale_midtsæsonen['Smart passes %'] + df_Centrale_midtsæsonen['Smart passes #'] + + df_Centrale_midtsæsonen['Key passes %'] + df_Centrale_midtsæsonen['Key passes #'] + df_Centrale_midtsæsonen['Passes to final third %'] + df_Centrale_midtsæsonen['Passes to final third #']+ df_Centrale_midtsæsonen['Vertical passes %'] + df_Centrale_midtsæsonen['Vertical passes #']+ df_Centrale_midtsæsonen['Through passes %'] + df_Centrale_midtsæsonen['Through passes #']+ df_Centrale_midtsæsonen['Progressive passes %'] + df_Centrale_midtsæsonen['Progressive passes #'])/18
    df_Centrale_midtsæsonen['Boldfast'] = (df_Centrale_midtsæsonen['Passes %'] + df_Centrale_midtsæsonen['Passes #']+ df_Centrale_midtsæsonen['Offensive duels %'] + df_Centrale_midtsæsonen['Received passes'] + df_Centrale_midtsæsonen['Succesful dribbles %'] + df_Centrale_midtsæsonen['Succesful dribbles #'])/6
    df_Centrale_midtsæsonen['Spilintelligens defensivt'] = (df_Centrale_midtsæsonen['Duels won %'] + df_Centrale_midtsæsonen['Duels won #'] +df_Centrale_midtsæsonen['Interceptions'] + df_Centrale_midtsæsonen['Counterpressing recoveries #'] + df_Centrale_midtsæsonen['Defensive duels won %'] + df_Centrale_midtsæsonen['Defensive duels won #'])/6
    df_Centrale_midtsæsonen['Samlet'] = (df_Centrale_midtsæsonen['Pasningssikker/Spilvendinger'] + df_Centrale_midtsæsonen['Boldfast'] + df_Centrale_midtsæsonen['Spilintelligens defensivt'])/3

    df_Centrale_midtsæsonen = df_Centrale_midtsæsonen[['Pasningssikker/Spilvendinger','Boldfast','Spilintelligens defensivt','Samlet']]
    df_Centrale_midtsæsonen = df_Centrale_midtsæsonen.sort_values(by='Samlet',ascending=False)
    with st.expander('Centrale midt kamp for kamp'):
        st.write(df_Centrale_midtsæsonen)

    df_Centrale_midtsæsonen = df_Centrale_midtsæsonen.reset_index()
    df_Centrale_midtsæsonen = df_Centrale_midtsæsonen.drop('label',axis=1)
    df_Centrale_midtsæsonen = df_Centrale_midtsæsonen.groupby(['Player name','Team name','Total minutes']).mean(numeric_only=True)
    df_Centrale_midtsæsonen = df_Centrale_midtsæsonen.sort_values(by='Samlet',ascending=False)
    with st.expander('Centrale midt sæson'):
        st.write(df_Centrale_midtsæsonen)


    df_Kanter = pd.merge(df_kanterminutter,df_Kanter,on=('Player id'))
    df_Kanter = df_Kanter[df_Kanter['total_minutesOnField_y'] >=tidprkamp]

    df_Kanter['Shots on target %'] = pd.qcut(df_Kanter['percent_shotsOnTarget'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Shots on target #'] = pd.qcut(df_Kanter['average_shotsOnTarget'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['XG'] = pd.qcut(df_Kanter['average_xgShot'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Successful dribbles #'] = pd.qcut(df_Kanter['average_newSuccessfulDribbles'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Successful dribbles %'] = pd.qcut(df_Kanter['percent_newSuccessfulDribbles'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Offensive duels %'] = pd.qcut(df_Kanter['percent_newOffensiveDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Offensive duels #'] = pd.qcut(df_Kanter['average_newOffensiveDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Passes %'] = pd.qcut(df_Kanter['percent_successfulPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Passes #'] = pd.qcut(df_Kanter['average_successfulPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Forward Passes %'] = pd.qcut(df_Kanter['percent_successfulForwardPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Forward Passes #'] = pd.qcut(df_Kanter['average_successfulForwardPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Smart passes %'] = pd.qcut(df_Kanter['percent_successfulSmartPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Smart passes #'] = pd.qcut(df_Kanter['average_successfulSmartPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Key passes %'] = pd.qcut(df_Kanter['percent_successfulKeyPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Key passes #'] = pd.qcut(df_Kanter['average_successfulKeyPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Passes to final third %'] = pd.qcut(df_Kanter['percent_successfulPassesToFinalThird'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Passes to final third #'] = pd.qcut(df_Kanter['average_successfulPassesToFinalThird'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Vertical passes %'] = pd.qcut(df_Kanter['percent_successfulVerticalPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Vertical passes #'] = pd.qcut(df_Kanter['average_successfulVerticalPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Through passes %'] = pd.qcut(df_Kanter['percent_successfulThroughPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Through passes #'] = pd.qcut(df_Kanter['average_successfulThroughPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Progressive passes %'] = pd.qcut(df_Kanter['percent_successfulProgressivePasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Progressive passes #'] = pd.qcut(df_Kanter['average_successfulProgressivePasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Goal conversion %'] = pd.qcut(df_Kanter['percent_goalConversion'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['XG per 90'] = pd.qcut(df_Kanter['average_xgShot'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['XA per 90'] = pd.qcut(df_Kanter['average_xgAssist'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Successful attacking actions'] = pd.qcut(df_Kanter['average_successfulAttackingActions'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Progressive runs'] = pd.qcut(df_Kanter['average_progressiveRun'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Accelerations score'] = pd.qcut(df_Kanter['average_accelerations'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)

    df_Kantersæsonen = df_Kanter.rename(columns={'total_minutesOnField_x':'Total minutes'},inplace=True)
    df_Kantersæsonen = df_Kanter.groupby(['Player name','Team name','Total minutes','label']).mean(numeric_only=True)

    df_Kantersæsonen['Sparkefærdigheder'] = (df_Kantersæsonen['Shots on target %'] + df_Kantersæsonen['Shots on target #'] + df_Kantersæsonen['XG'] + df_Kantersæsonen['Passes to final third %'] + df_Kantersæsonen['Forward Passes %'] + df_Kantersæsonen['Vertical passes %'])/6
    df_Kantersæsonen['Kombinationsstærk'] = (df_Kantersæsonen['Passes %'] + df_Kantersæsonen['Passes #'] + df_Kantersæsonen['Forward Passes %'] + df_Kantersæsonen['Forward Passes #'] + df_Kantersæsonen['Passes to final third %'] + df_Kantersæsonen['Passes to final third #'] + df_Kantersæsonen['Through passes %'] + df_Kantersæsonen['Through passes #'] + df_Kantersæsonen['Progressive passes %'] + df_Kantersæsonen['Progressive passes #'] + df_Kantersæsonen['Successful attacking actions'])/11
    df_Kantersæsonen['Spilintelligens offensivt/indlægsstærk'] = (df_Kantersæsonen['XA per 90'] + df_Kantersæsonen['XG per 90'] + df_Kantersæsonen['Through passes %'] + df_Kantersæsonen['Through passes #'] + df_Kantersæsonen['Smart passes %'] + df_Kantersæsonen['Smart passes #'] + df_Kantersæsonen['Progressive passes %'] + df_Kantersæsonen['Progressive passes #'] + df_Kantersæsonen['Key passes %'] + df_Kantersæsonen['Key passes #'] + df_Kantersæsonen['Successful attacking actions'])/11
    df_Kantersæsonen['1v1 offensivt'] = (df_Kantersæsonen['Successful dribbles #'] + df_Kantersæsonen['Successful dribbles %'] + df_Kantersæsonen['Offensive duels #'] + df_Kantersæsonen['Offensive duels %'] + df_Kantersæsonen['Progressive runs'])/5
    df_Kantersæsonen['Fart'] = (df_Kantersæsonen['Progressive runs'] + df_Kantersæsonen['Successful dribbles #'] + df_Kantersæsonen['Successful dribbles %'] + df_Kantersæsonen['Accelerations score'])/4
    df_Kantersæsonen['Samlet'] = (df_Kantersæsonen['Sparkefærdigheder'] + df_Kantersæsonen['Kombinationsstærk'] + df_Kantersæsonen['Spilintelligens offensivt/indlægsstærk'] + df_Kantersæsonen['1v1 offensivt'] + df_Kantersæsonen['Fart'])/5
    df_Kantersæsonen = df_Kantersæsonen[['Sparkefærdigheder','Kombinationsstærk','Spilintelligens offensivt/indlægsstærk','1v1 offensivt','Fart','Samlet']]
    df_Kantersæsonen = df_Kantersæsonen.sort_values(by='Samlet',ascending=False)

    with st.expander('Kanter kamp for kamp'):
        st.write(df_Kantersæsonen)

    df_Kantersæsonen = df_Kantersæsonen.reset_index()
    df_Kantersæsonen = df_Kantersæsonen.drop('label',axis=1)
    df_Kantersæsonen = df_Kantersæsonen.groupby(['Player name','Team name','Total minutes']).mean(numeric_only=True)
    df_Kantersæsonen = df_Kantersæsonen.sort_values(by='Samlet',ascending=False)
    with st.expander('Kanter sæson'):
        st.write(df_Kantersæsonen)


    df_Angribere = pd.merge(df_angribereminutter,df_Angribere,on=('Player id'))
    df_Angribere = df_Angribere[df_Angribere['total_minutesOnField_y'] >=tidprkamp]

    df_Angribere['Målfarlighed udregning'] = df_Angribere['average_goals'] - df_Angribere['average_xgShot']
    df_Angribere['Målfarlighed score'] =  pd.qcut(df_Angribere['Målfarlighed udregning'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Angribere['xG per 90 score'] = pd.qcut(df_Angribere['average_xgShot'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Angribere['Goals per 90 score'] = pd.qcut(df_Angribere['average_goals'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)  
    df_Angribere['Shots on target, % score'] = pd.qcut(df_Angribere['percent_shotsOnTarget'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)   
    df_Angribere['Offensive duels won, % score'] = pd.qcut(df_Angribere['percent_newOffensiveDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Angribere['Duels won, % score'] = pd.qcut(df_Angribere['percent_newDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Angribere['Accurate passes, % score'] = pd.qcut(df_Angribere['percent_successfulPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Angribere['Successful dribbles, % score'] = pd.qcut(df_Angribere['percent_newSuccessfulDribbles'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Angribere['xA per 90 score'] = pd.qcut(df_Angribere['average_xgAssist'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Angribere['Touches in box per 90 score'] = pd.qcut(df_Angribere['average_touchInBox'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Angribere['Progressive runs'] = pd.qcut(df_Angribere['average_progressiveRun'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Angribere['Accelerations score'] = pd.qcut(df_Angribere['average_accelerations'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Angribere['Progressive passes per 90 score'] = pd.qcut(df_Angribere['average_successfulProgressivePasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Angribere['Successful attacking actions per 90 score'] = pd.qcut(df_Angribere['average_successfulAttackingActions'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Angribere['Successful dribbles #'] = pd.qcut(df_Angribere['average_newSuccessfulDribbles'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)

    df_Angriberesæsonen = df_Angribere.rename(columns={'total_minutesOnField_x':'Total minutes'},inplace=True)
    df_Angriberesæsonen = df_Angribere.groupby(['Player name','Team name','Total minutes','label']).mean(numeric_only=True)

    df_Angriberesæsonen['Sparkefærdigheder'] = (df_Angriberesæsonen['xG per 90 score'] + df_Angriberesæsonen['xG per 90 score'] + df_Angriberesæsonen['Goals per 90 score'] + df_Angriberesæsonen['Shots on target, % score'])/4
    df_Angriberesæsonen['Boldfast'] = (df_Angriberesæsonen['Offensive duels won, % score'] + df_Angriberesæsonen['Offensive duels won, % score'] + df_Angriberesæsonen['Duels won, % score'] + df_Angriberesæsonen['Accurate passes, % score'] + df_Angriberesæsonen['Successful dribbles, % score'])/5
    df_Angriberesæsonen['Spilintelligens offensivt'] = (df_Angriberesæsonen['xA per 90 score'] + df_Angriberesæsonen['xG per 90 score'] + df_Angriberesæsonen['Touches in box per 90 score'] + df_Angriberesæsonen['Progressive passes per 90 score'] + df_Angriberesæsonen['Successful attacking actions per 90 score'] + df_Angriberesæsonen['Touches in box per 90 score'] + df_Angriberesæsonen['xG per 90 score'])/7
    df_Angriberesæsonen['Målfarlighed'] = (df_Angriberesæsonen['xG per 90 score']+df_Angriberesæsonen['Goals per 90 score']+df_Angriberesæsonen['xG per 90 score'] + df_Angriberesæsonen['Målfarlighed score'])/4
    df_Angriberesæsonen['Fart'] = (df_Angriberesæsonen['Progressive runs'] + + df_Angriberesæsonen['Progressive runs'] + df_Angriberesæsonen['Progressive runs'] + df_Angriberesæsonen['Successful dribbles #'] + df_Angriberesæsonen['Successful dribbles, % score'] + df_Angriberesæsonen['Accelerations score'] + df_Angriberesæsonen['Offensive duels won, % score'])/7
    df_Angriberesæsonen = df_Angriberesæsonen[['Sparkefærdigheder','Boldfast','Spilintelligens offensivt','Målfarlighed','Fart']]
    df_Angriberesæsonen['Samlet'] = (df_Angriberesæsonen['Sparkefærdigheder']+df_Angriberesæsonen['Boldfast']+df_Angriberesæsonen['Spilintelligens offensivt']+df_Angriberesæsonen['Målfarlighed']+df_Angriberesæsonen['Målfarlighed']+df_Angriberesæsonen['Målfarlighed']+df_Angriberesæsonen['Fart'])/7
    df_Angriberesæsonen = df_Angriberesæsonen.sort_values(by='Samlet',ascending=False)

    with st.expander('Angribere kamp for kamp'):
        st.write(df_Angriberesæsonen)

    df_Angriberesæsonen = df_Angriberesæsonen.reset_index()
    df_Angriberesæsonen = df_Angriberesæsonen.drop('label',axis=1)
    df_Angriberesæsonen = df_Angriberesæsonen.groupby(['Player name','Team name','Total minutes']).mean(numeric_only=True)
    df_Angriberesæsonen = df_Angriberesæsonen.sort_values(by='Samlet',ascending=False)
    with st.expander('Angribere sæson'):
        st.write(df_Angriberesæsonen)
    df = pd.read_csv(r'xT/1st Division 23 24.csv')

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


    dfscore = pd.read_csv(r'xT/Zone scores.csv')

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

    xgc = df1
    xgchold = xgc.rename(columns={'shot.xg': 'Hold xG'})
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
        
def Anden_division ():
    col1,col2 = st.columns(2)
    with col1:
        samlettid = st.number_input('Minutter i sæsonen')
    with col2:    
        tidprkamp = st.number_input('Minutter pr. kamp')
        
    df = pd.read_csv(r'Individuelt dashboard/Individuelt dashboard 2.div.csv')
    df.rename(columns={'playerId': 'Player id'}, inplace=True)
    df = df.astype(str)
    dfevents = pd.read_csv('2.div eventdata alle.csv',low_memory=False)
    dfevents = dfevents[['Player id','Player name','team_name','label','date','matchId']]
    dfspillernavn = df[['Player id','matchId','positions','average','percent','total']]
    dfspillernavn = dfspillernavn.astype(str)
    dfevents['Player id'] = dfevents['Player id'].astype(str)
    dfevents['matchId'] = dfevents['matchId'].astype(str)
    df = dfspillernavn.merge(dfevents)

    df['Player&matchId'] = df['Player id'] + df['matchId']
    df['Player&matchId'] = df['Player&matchId'].drop_duplicates(keep='first')
    df = df.dropna()
    df = df[['Player id','Player name','team_name','matchId','label','date','positions','average','percent','total']]

    #df = df.set_index('Player id')

    data = df['positions']
    df1 = pd.DataFrame(data)
    # Funktion, der ekstraherer navne og koder fra strengdata og opretter en ny kolonne med disse værdier
    def extract_positions(data):
        positions_list = ast.literal_eval(data) # Konverterer strengen til en liste af ordbøger
        names = [pos['position']['name'] for pos in positions_list]
        codes = [pos['position']['code'] for pos in positions_list]
        return pd.Series({'position_names': names, 'position_codes': codes})

    # Anvender funktionen på kolonnen og tilføjer resultaterne som nye kolonner til dataframe
    df1[['position_names', 'position_codes']] = df1['positions'].apply(extract_positions)

    df = pd.merge(df,df1,left_index=True, right_index=True)
    df = df.set_index('Player id')
    df = df.drop(columns=['positions_x'])
    df = df.drop(columns=['positions_y'])
    df = df[['Player name','team_name','matchId','label','date','position_names','position_codes','average','percent','total']]
    df = df.rename(columns={'team_name':'Team name'})
    df['percent'] = df['percent'].apply(lambda x: ast.literal_eval(x))

    # Create a new dataframe with the columns as the dictionary keys and the values as a list
    new_df = pd.DataFrame(df['percent'].to_list(), index=df.index).add_prefix('percent_')

    # Concatenate the new dataframe with the original dataframe
    df = pd.concat([df, new_df], axis=1)

    # Drop the original 'percent' column
    df = df.drop('percent', axis=1)

    df['total'] = df['total'].apply(lambda x: ast.literal_eval(x))

    # Create a new dataframe with the columns as the dictionary keys and the values as a list
    new_df = pd.DataFrame(df['total'].to_list(), index=df.index).add_prefix('total_')

    # Concatenate the new dataframe with the original dataframe
    df = pd.concat([df, new_df], axis=1)

    # Drop the original 'percent' column
    df = df.drop('total', axis=1)

    df['average'] = df['average'].apply(lambda x: ast.literal_eval(x))

    # Create a new dataframe with the columns as the dictionary keys and the values as a list
    new_df = pd.DataFrame(df['average'].to_list(), index=df.index).add_prefix('average_')

    # Concatenate the new dataframe with the original dataframe
    df = pd.concat([df, new_df], axis=1)


    # Drop the original 'percent' column
    df = df.drop('average', axis=1)
    df['position_codes'] = df['position_codes'].astype(str)
    #df['date'] = df['date'].astype(str)
    #df['date'] = df['date'].apply(lambda x: parser.parse(x))

    # Sort the dataframe by the 'date' column
    #df = df.sort_values(by='date',ascending=False)

    # Format the 'date' column to day-month-year format
    #df['date'] = df['date'].apply(lambda x: x.strftime('%d-%m-%Y'))
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date',ascending=False)

    df_backs = df[df['position_codes'].str.contains('|'.join(['lb', 'rb']))]
    df_backs = df_backs[df_backs['total_minutesOnField'] >= tidprkamp]
    df_backsminutter = df_backs[['Player name','Team name','total_minutesOnField']]
    df_backsminutter = df_backsminutter.groupby(['Player id']).sum(numeric_only=True)
    df_backsminutter = df_backsminutter[df_backsminutter['total_minutesOnField'] >= samlettid]

    df_Stoppere = df[df['position_codes'].str.contains('|'.join(['cb']))]
    df_Stoppere = df_Stoppere[df_Stoppere['total_minutesOnField'] >= tidprkamp]
    df_stoppereminutter = df_Stoppere[['Player name','Team name','total_minutesOnField']]
    df_stoppereminutter = df_stoppereminutter.groupby(['Player id']).sum(numeric_only=True)
    df_stoppereminutter = df_stoppereminutter[df_stoppereminutter['total_minutesOnField'] >= samlettid]

    df_Centrale_midt = df[df['position_codes'].str.contains('|'.join(['cm','amf','dmf']))]
    df_Centrale_midt = df_Centrale_midt[df_Centrale_midt['total_minutesOnField'] >= tidprkamp]
    df_centraleminutter = df_Centrale_midt[['Player name','Team name','total_minutesOnField']]
    df_centraleminutter = df_centraleminutter.groupby(['Player id']).sum(numeric_only=True)
    df_centraleminutter = df_centraleminutter[df_centraleminutter['total_minutesOnField'] >= samlettid]

    df_Kanter = df[df['position_codes'].str.contains('|'.join(['rw','lw','ramf','lamf']))]
    df_Kanter = df_Kanter[df_Kanter['total_minutesOnField'] >=tidprkamp]
    df_kanterminutter = df_Kanter[['Player name','Team name','total_minutesOnField']]
    df_kanterminutter = df_kanterminutter.groupby(['Player id']).sum(numeric_only=True)
    df_kanterminutter = df_kanterminutter[df_kanterminutter['total_minutesOnField'] >=samlettid]


    df_Angribere = df[df['position_codes'].str.contains('|'.join(['cf','ss']))]
    df_Angribere = df_Angribere[df_Angribere['total_minutesOnField'] >= tidprkamp]
    df_angribereminutter = df_Angribere[['Player name','Team name','total_minutesOnField']]
    df_angribereminutter = df_angribereminutter.groupby(['Player id']).sum(numeric_only=True)
    df_angribereminutter = df_angribereminutter[df_angribereminutter['total_minutesOnField'] >= samlettid]


    df_backs = pd.merge(df_backsminutter,df_backs,on=('Player id'))
    df_backs = df_backs[df_backs['total_minutesOnField_y'] >=tidprkamp]

    df_backs['Accurate crosses score'] = pd.qcut(df_backs['percent_successfulCrosses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_backs['Number of crosses score'] = pd.qcut(df_backs['average_crosses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_backs['XA score'] = pd.qcut(df_backs['average_xgAssist'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_backs['Passes to final third score'] = pd.qcut(df_backs['average_successfulPassesToFinalThird'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_backs['Successful dribbles score'] = pd.qcut(df_backs['percent_newSuccessfulDribbles'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_backs['Defensive duels won score'] = pd.qcut(df_backs['percent_newDefensiveDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_backs['Progressive runs score'] = pd.qcut(df_backs['average_progressiveRun'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_backs['Offensive duels won score'] = pd.qcut(df_backs['percent_newOffensiveDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_backs['Accelerations score'] = pd.qcut(df_backs['average_accelerations'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_backs['Duels won score'] = pd.qcut(df_backs['percent_newDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_backs['Interceptions score'] = pd.qcut(df_backs['average_interceptions'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_backs['Successful defensive actions score'] = pd.qcut(df_backs['average_successfulDefensiveAction'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_backssæsonen = df_backs[['label','Player name','Team name','total_minutesOnField_x','total_minutesOnField_y','Number of crosses score','Accurate crosses score','XA score','Passes to final third score','Successful dribbles score','Defensive duels won score','Progressive runs score','Offensive duels won score','Accelerations score','Duels won score','Interceptions score','Successful defensive actions score']]
    df_backssæsonen.rename(columns={'total_minutesOnField_x':'Total minutes'},inplace=True)
    df_backssæsonen = df_backssæsonen.groupby(['Player name','Team name','Total minutes','label']).mean(numeric_only=True)

    df_backssæsonen['Indlægsstærk'] = (df_backssæsonen['Number of crosses score'] + df_backssæsonen['Accurate crosses score'] + df_backssæsonen['XA score'] + df_backssæsonen['Passes to final third score'])/4
    df_backssæsonen['1v1 færdigheder'] = (df_backssæsonen['Successful dribbles score'] + df_backssæsonen['Defensive duels won score'] + df_backssæsonen['Progressive runs score'] + df_backssæsonen['Offensive duels won score'] + df_backssæsonen['Accelerations score'] + df_backssæsonen['Duels won score'])/6
    df_backssæsonen['Spilintelligens defensivt'] = (df_backssæsonen['Interceptions score'] + df_backssæsonen['Successful defensive actions score'] + df_backssæsonen['Duels won score'] + df_backssæsonen['Defensive duels won score'])/4
    df_backssæsonen['Fart'] = (df_backssæsonen['Successful dribbles score'] + df_backssæsonen['Progressive runs score'] + df_backssæsonen['Offensive duels won score'] + df_backssæsonen['Accelerations score'])/4
    df_backssæsonen ['Samlet'] = (df_backssæsonen['Indlægsstærk'] + df_backssæsonen['1v1 færdigheder'] + df_backssæsonen['Spilintelligens defensivt'] + df_backssæsonen['Fart'])/4

    df_backssæsonen = df_backssæsonen[['Indlægsstærk','1v1 færdigheder','Spilintelligens defensivt','Fart','Samlet']]
    df_backssæsonen = df_backssæsonen.round(3).astype(float)
    df_backssæsonen = df_backssæsonen.sort_values(by='Samlet',ascending=False)
    with st.expander('Backs kamp for kamp'):
        st.write(df_backssæsonen)
    df_backssæsonen = df_backssæsonen.reset_index()
    df_backssæsonen = df_backssæsonen.drop('label',axis=1)
    df_backssæsonen = df_backssæsonen.groupby(['Player name','Team name','Total minutes']).mean(numeric_only=True)
    df_backssæsonen = df_backssæsonen.sort_values(by='Samlet',ascending=False)
    with st.expander('Backs'):
        st.dataframe(df_backssæsonen)
       
    df_Stoppere = pd.merge(df_stoppereminutter,df_Stoppere,on=('Player id'))
    df_Stoppere = df_Stoppere[df_Stoppere['total_minutesOnField_y'] >=tidprkamp]
    
    df_Stoppere['Accurate passes score'] = pd.qcut(df_Stoppere['percent_successfulPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Accurate long passes score'] = pd.qcut(df_Stoppere['percent_successfulLongPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Forward passes score'] = pd.qcut(df_Stoppere['average_successfulForwardPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Accurate forward passes score'] = pd.qcut(df_Stoppere['percent_successfulForwardPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Accurate progressive passes score'] = pd.qcut(df_Stoppere['percent_successfulProgressivePasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Accurate vertical passes score'] = pd.qcut(df_Stoppere['percent_successfulVerticalPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Interceptions score'] = pd.qcut(df_Stoppere['average_interceptions'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Succesful defensive actions score'] = pd.qcut(df_Stoppere['average_successfulDefensiveAction'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Shots blocked score'] = pd.qcut(df_Stoppere['average_shotsBlocked'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Defensive duels won score'] = pd.qcut(df_Stoppere['average_newDefensiveDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Defensive duels won % score'] = pd.qcut(df_Stoppere['percent_newDefensiveDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Accurate passes to final third'] = pd.qcut(df_Stoppere['percent_successfulPassesToFinalThird'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Accurate through passes'] = pd.qcut(df_Stoppere['percent_successfulThroughPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Vertical passes'] = pd.qcut(df_Stoppere['average_successfulVerticalPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Through passes'] = pd.qcut(df_Stoppere['average_successfulThroughPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Passes to final third'] = pd.qcut(df_Stoppere['average_successfulPassesToFinalThird'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Progressive runs'] = pd.qcut(df_Stoppere['average_progressiveRun'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Offensive duels won %'] = pd.qcut(df_Stoppere['percent_newOffensiveDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Successful dribbles %'] = pd.qcut(df_Stoppere['percent_newSuccessfulDribbles'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Progressive passes score'] = pd.qcut(df_Stoppere['average_successfulProgressivePasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Aerial duels won score'] = pd.qcut(df_Stoppere['average_fieldAerialDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Aerial duels won % score'] = pd.qcut(df_Stoppere['percent_aerialDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)

    df_Stopperesæsonen = df_Stoppere[['label','Player name','Team name','total_minutesOnField_x','total_minutesOnField_y','Accurate passes score','Accurate long passes score','Forward passes score','Accurate forward passes score','Accurate progressive passes score','Accurate vertical passes score','Interceptions score','Succesful defensive actions score','Shots blocked score','Defensive duels won score','Defensive duels won % score','Accurate passes to final third','Accurate through passes','Vertical passes','Through passes','Passes to final third','Progressive passes score','Aerial duels won score','Aerial duels won % score','Progressive runs','Offensive duels won %','Successful dribbles %']]
    df_Stopperesæsonen.rename(columns={'total_minutesOnField_x':'Total minutes'},inplace=True)
    df_Stopperesæsonen = df_Stopperesæsonen.groupby(['Player name','Team name','Total minutes','label']).mean(numeric_only=True)
    df_Stopperesæsonen['Pasningssikker'] = (df_Stopperesæsonen['Accurate passes score'] + df_Stopperesæsonen['Accurate long passes score'] + df_Stopperesæsonen['Forward passes score'] + df_Stopperesæsonen['Accurate forward passes score'] + df_Stopperesæsonen['Accurate progressive passes score'] + df_Stopperesæsonen['Accurate vertical passes score'])/6
    df_Stopperesæsonen['Spilintelligens defensivt'] = (df_Stopperesæsonen['Interceptions score'] + df_Stopperesæsonen['Succesful defensive actions score'] + df_Stopperesæsonen['Shots blocked score'] + df_Stopperesæsonen['Succesful defensive actions score'] + df_Stopperesæsonen['Defensive duels won % score']) /5
    df_Stopperesæsonen['Spilintelligens offensivt'] = (df_Stopperesæsonen['Forward passes score'] + df_Stopperesæsonen['Accurate forward passes score'] + df_Stopperesæsonen['Accurate passes to final third'] + df_Stopperesæsonen['Passes to final third'] + df_Stopperesæsonen['Accurate progressive passes score'] + df_Stopperesæsonen['Progressive passes score'] + df_Stopperesæsonen['Through passes'] + df_Stopperesæsonen['Accurate through passes']+ df_Stopperesæsonen['Progressive runs'] + df_Stopperesæsonen['Offensive duels won %'] + df_Stopperesæsonen['Successful dribbles %'])/11
    df_Stopperesæsonen['Nærkamps- og duelstærk'] = (df_Stopperesæsonen['Defensive duels won % score'] + df_Stopperesæsonen['Aerial duels won % score'] + df_Stopperesæsonen['Defensive duels won % score'])/3
    df_Stopperesæsonen['Samlet'] = (df_Stopperesæsonen['Pasningssikker'] + df_Stopperesæsonen['Spilintelligens defensivt'] + df_Stopperesæsonen['Spilintelligens offensivt'] + df_Stopperesæsonen['Nærkamps- og duelstærk'])/4

    df_Stopperesæsonen = df_Stopperesæsonen[['Pasningssikker','Spilintelligens defensivt','Spilintelligens offensivt','Nærkamps- og duelstærk','Samlet']]
    df_Stopperesæsonen = df_Stopperesæsonen.sort_values(by='Samlet',ascending=False)

    with st.expander('Stoppere kamp for kamp'):
        st.write(df_Stopperesæsonen)
    df_Stopperesæsonen = df_Stopperesæsonen.reset_index()
    df_Stopperesæsonen = df_Stopperesæsonen.drop('label',axis=1)
    df_Stopperesæsonen = df_Stopperesæsonen.groupby(['Player name','Team name','Total minutes']).mean(numeric_only=True)
    df_Stopperesæsonen = df_Stopperesæsonen.sort_values(by='Samlet',ascending=False)
    
    with st.expander('Stoppere sæson'):
        st.dataframe(df_Stopperesæsonen)

    df_Centrale_midt = pd.merge(df_centraleminutter,df_Centrale_midt,on=('Player id'))
    df_Centrale_midt = df_Centrale_midt[df_Centrale_midt['total_minutesOnField_y'] >=tidprkamp]

    df_Centrale_midt['Passes %'] = pd.qcut(df_Centrale_midt['percent_successfulPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Passes #'] = pd.qcut(df_Centrale_midt['average_successfulPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Forward Passes %'] = pd.qcut(df_Centrale_midt['percent_successfulForwardPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Forward Passes #'] = pd.qcut(df_Centrale_midt['average_successfulForwardPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Long Passes %'] = pd.qcut(df_Centrale_midt['percent_successfulLongPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Long Passes #'] = pd.qcut(df_Centrale_midt['average_successfulLongPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Smart passes %'] = pd.qcut(df_Centrale_midt['percent_successfulSmartPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Smart passes #'] = pd.qcut(df_Centrale_midt['average_successfulSmartPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Key passes %'] = pd.qcut(df_Centrale_midt['percent_successfulKeyPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Key passes #'] = pd.qcut(df_Centrale_midt['average_successfulKeyPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Passes to final third %'] = pd.qcut(df_Centrale_midt['percent_successfulPassesToFinalThird'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Passes to final third #'] = pd.qcut(df_Centrale_midt['average_successfulPassesToFinalThird'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Vertical passes %'] = pd.qcut(df_Centrale_midt['percent_successfulVerticalPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Vertical passes #'] = pd.qcut(df_Centrale_midt['average_successfulVerticalPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Through passes %'] = pd.qcut(df_Centrale_midt['percent_successfulThroughPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Through passes #'] = pd.qcut(df_Centrale_midt['average_successfulThroughPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Progressive passes %'] = pd.qcut(df_Centrale_midt['percent_successfulProgressivePasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Progressive passes #'] = pd.qcut(df_Centrale_midt['average_successfulProgressivePasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Offensive duels %'] = pd.qcut(df_Centrale_midt['percent_newOffensiveDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Received passes'] = pd.qcut(df_Centrale_midt['average_receivedPass'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Succesful dribbles %'] = pd.qcut(df_Centrale_midt['percent_newSuccessfulDribbles'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Succesful dribbles #'] = pd.qcut(df_Centrale_midt['average_newSuccessfulDribbles'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Duels won %'] = pd.qcut(df_Centrale_midt['percent_newDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Duels won #'] = pd.qcut(df_Centrale_midt['average_newDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Interceptions'] = pd.qcut(df_Centrale_midt['average_interceptions'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Counterpressing recoveries #'] = pd.qcut(df_Centrale_midt['average_counterpressingRecoveries'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Defensive duels won #'] = pd.qcut(df_Centrale_midt['average_newDefensiveDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Defensive duels won %'] = pd.qcut(df_Centrale_midt['percent_newDefensiveDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)

    df_Centrale_midtsæsonen = df_Centrale_midt.rename(columns={'total_minutesOnField_x':'Total minutes'},inplace=True)
    df_Centrale_midtsæsonen = df_Centrale_midt.groupby(['Player name','Team name','Total minutes','label']).mean(numeric_only=True)
    df_Centrale_midtsæsonen['Pasningssikker/Spilvendinger'] = (df_Centrale_midtsæsonen['Passes %'] + df_Centrale_midtsæsonen['Passes #'] + df_Centrale_midtsæsonen['Forward Passes %'] + df_Centrale_midtsæsonen['Forward Passes #'] + df_Centrale_midtsæsonen['Long Passes %'] + df_Centrale_midtsæsonen['Long Passes #']+ df_Centrale_midtsæsonen['Smart passes %'] + df_Centrale_midtsæsonen['Smart passes #'] + + df_Centrale_midtsæsonen['Key passes %'] + df_Centrale_midtsæsonen['Key passes #'] + df_Centrale_midtsæsonen['Passes to final third %'] + df_Centrale_midtsæsonen['Passes to final third #']+ df_Centrale_midtsæsonen['Vertical passes %'] + df_Centrale_midtsæsonen['Vertical passes #']+ df_Centrale_midtsæsonen['Through passes %'] + df_Centrale_midtsæsonen['Through passes #']+ df_Centrale_midtsæsonen['Progressive passes %'] + df_Centrale_midtsæsonen['Progressive passes #'])/18
    df_Centrale_midtsæsonen['Boldfast'] = (df_Centrale_midtsæsonen['Passes %'] + df_Centrale_midtsæsonen['Passes #']+ df_Centrale_midtsæsonen['Offensive duels %'] + df_Centrale_midtsæsonen['Received passes'] + df_Centrale_midtsæsonen['Succesful dribbles %'] + df_Centrale_midtsæsonen['Succesful dribbles #'])/6
    df_Centrale_midtsæsonen['Spilintelligens defensivt'] = (df_Centrale_midtsæsonen['Duels won %'] + df_Centrale_midtsæsonen['Duels won #'] +df_Centrale_midtsæsonen['Interceptions'] + df_Centrale_midtsæsonen['Counterpressing recoveries #'] + df_Centrale_midtsæsonen['Defensive duels won %'] + df_Centrale_midtsæsonen['Defensive duels won #'])/6
    df_Centrale_midtsæsonen['Samlet'] = (df_Centrale_midtsæsonen['Pasningssikker/Spilvendinger'] + df_Centrale_midtsæsonen['Boldfast'] + df_Centrale_midtsæsonen['Spilintelligens defensivt'])/3

    df_Centrale_midtsæsonen = df_Centrale_midtsæsonen[['Pasningssikker/Spilvendinger','Boldfast','Spilintelligens defensivt','Samlet']]
    df_Centrale_midtsæsonen = df_Centrale_midtsæsonen.sort_values(by='Samlet',ascending=False)
    with st.expander('Centrale midt kamp for kamp'):
        st.write(df_Centrale_midtsæsonen)

    df_Centrale_midtsæsonen = df_Centrale_midtsæsonen.reset_index()
    df_Centrale_midtsæsonen = df_Centrale_midtsæsonen.drop('label',axis=1)
    df_Centrale_midtsæsonen = df_Centrale_midtsæsonen.groupby(['Player name','Team name','Total minutes']).mean(numeric_only=True)
    df_Centrale_midtsæsonen = df_Centrale_midtsæsonen.sort_values(by='Samlet',ascending=False)
    with st.expander('Centrale midt sæson'):
        st.write(df_Centrale_midtsæsonen)


    df_Kanter = pd.merge(df_kanterminutter,df_Kanter,on=('Player id'))
    df_Kanter = df_Kanter[df_Kanter['total_minutesOnField_y'] >=tidprkamp]

    df_Kanter['Shots on target %'] = pd.qcut(df_Kanter['percent_shotsOnTarget'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Shots on target #'] = pd.qcut(df_Kanter['average_shotsOnTarget'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['XG'] = pd.qcut(df_Kanter['average_xgShot'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Successful dribbles #'] = pd.qcut(df_Kanter['average_newSuccessfulDribbles'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Successful dribbles %'] = pd.qcut(df_Kanter['percent_newSuccessfulDribbles'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Offensive duels %'] = pd.qcut(df_Kanter['percent_newOffensiveDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Offensive duels #'] = pd.qcut(df_Kanter['average_newOffensiveDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Passes %'] = pd.qcut(df_Kanter['percent_successfulPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Passes #'] = pd.qcut(df_Kanter['average_successfulPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Forward Passes %'] = pd.qcut(df_Kanter['percent_successfulForwardPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Forward Passes #'] = pd.qcut(df_Kanter['average_successfulForwardPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Smart passes %'] = pd.qcut(df_Kanter['percent_successfulSmartPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Smart passes #'] = pd.qcut(df_Kanter['average_successfulSmartPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Key passes %'] = pd.qcut(df_Kanter['percent_successfulKeyPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Key passes #'] = pd.qcut(df_Kanter['average_successfulKeyPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Passes to final third %'] = pd.qcut(df_Kanter['percent_successfulPassesToFinalThird'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Passes to final third #'] = pd.qcut(df_Kanter['average_successfulPassesToFinalThird'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Vertical passes %'] = pd.qcut(df_Kanter['percent_successfulVerticalPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Vertical passes #'] = pd.qcut(df_Kanter['average_successfulVerticalPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Through passes %'] = pd.qcut(df_Kanter['percent_successfulThroughPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Through passes #'] = pd.qcut(df_Kanter['average_successfulThroughPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Progressive passes %'] = pd.qcut(df_Kanter['percent_successfulProgressivePasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Progressive passes #'] = pd.qcut(df_Kanter['average_successfulProgressivePasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Goal conversion %'] = pd.qcut(df_Kanter['percent_goalConversion'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['XG per 90'] = pd.qcut(df_Kanter['average_xgShot'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['XA per 90'] = pd.qcut(df_Kanter['average_xgAssist'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Successful attacking actions'] = pd.qcut(df_Kanter['average_successfulAttackingActions'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Progressive runs'] = pd.qcut(df_Kanter['average_progressiveRun'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Accelerations score'] = pd.qcut(df_Kanter['average_accelerations'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)

    df_Kantersæsonen = df_Kanter.rename(columns={'total_minutesOnField_x':'Total minutes'},inplace=True)
    df_Kantersæsonen = df_Kanter.groupby(['Player name','Team name','Total minutes','label']).mean(numeric_only=True)

    df_Kantersæsonen['Sparkefærdigheder'] = (df_Kantersæsonen['Shots on target %'] + df_Kantersæsonen['Shots on target #'] + df_Kantersæsonen['XG'] + df_Kantersæsonen['Passes to final third %'] + df_Kantersæsonen['Forward Passes %'] + df_Kantersæsonen['Vertical passes %'])/6
    df_Kantersæsonen['Kombinationsstærk'] = (df_Kantersæsonen['Passes %'] + df_Kantersæsonen['Passes #'] + df_Kantersæsonen['Forward Passes %'] + df_Kantersæsonen['Forward Passes #'] + df_Kantersæsonen['Passes to final third %'] + df_Kantersæsonen['Passes to final third #'] + df_Kantersæsonen['Through passes %'] + df_Kantersæsonen['Through passes #'] + df_Kantersæsonen['Progressive passes %'] + df_Kantersæsonen['Progressive passes #'] + df_Kantersæsonen['Successful attacking actions'])/11
    df_Kantersæsonen['Spilintelligens offensivt/indlægsstærk'] = (df_Kantersæsonen['XA per 90'] + df_Kantersæsonen['XG per 90'] + df_Kantersæsonen['Through passes %'] + df_Kantersæsonen['Through passes #'] + df_Kantersæsonen['Smart passes %'] + df_Kantersæsonen['Smart passes #'] + df_Kantersæsonen['Progressive passes %'] + df_Kantersæsonen['Progressive passes #'] + df_Kantersæsonen['Key passes %'] + df_Kantersæsonen['Key passes #'] + df_Kantersæsonen['Successful attacking actions'])/11
    df_Kantersæsonen['1v1 offensivt'] = (df_Kantersæsonen['Successful dribbles #'] + df_Kantersæsonen['Successful dribbles %'] + df_Kantersæsonen['Offensive duels #'] + df_Kantersæsonen['Offensive duels %'] + df_Kantersæsonen['Progressive runs'])/5
    df_Kantersæsonen['Fart'] = (df_Kantersæsonen['Progressive runs'] + df_Kantersæsonen['Successful dribbles #'] + df_Kantersæsonen['Successful dribbles %'] + df_Kantersæsonen['Accelerations score'])/4
    df_Kantersæsonen['Samlet'] = (df_Kantersæsonen['Sparkefærdigheder'] + df_Kantersæsonen['Kombinationsstærk'] + df_Kantersæsonen['Spilintelligens offensivt/indlægsstærk'] + df_Kantersæsonen['1v1 offensivt'] + df_Kantersæsonen['Fart'])/5
    df_Kantersæsonen = df_Kantersæsonen[['Sparkefærdigheder','Kombinationsstærk','Spilintelligens offensivt/indlægsstærk','1v1 offensivt','Fart','Samlet']]
    df_Kantersæsonen = df_Kantersæsonen.sort_values(by='Samlet',ascending=False)

    with st.expander('Kanter kamp for kamp'):
        st.write(df_Kantersæsonen)

    df_Kantersæsonen = df_Kantersæsonen.reset_index()
    df_Kantersæsonen = df_Kantersæsonen.drop('label',axis=1)
    df_Kantersæsonen = df_Kantersæsonen.groupby(['Player name','Team name','Total minutes']).mean(numeric_only=True)
    df_Kantersæsonen = df_Kantersæsonen.sort_values(by='Samlet',ascending=False)
    with st.expander('Kanter sæson'):
        st.write(df_Kantersæsonen)


    df_Angribere = pd.merge(df_angribereminutter,df_Angribere,on=('Player id'))
    df_Angribere = df_Angribere[df_Angribere['total_minutesOnField_y'] >=tidprkamp]

    df_Angribere['Målfarlighed udregning'] = df_Angribere['average_goals'] - df_Angribere['average_xgShot']
    df_Angribere['Målfarlighed score'] =  pd.qcut(df_Angribere['Målfarlighed udregning'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Angribere['xG per 90 score'] = pd.qcut(df_Angribere['average_xgShot'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Angribere['Goals per 90 score'] = pd.qcut(df_Angribere['average_goals'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)  
    df_Angribere['Shots on target, % score'] = pd.qcut(df_Angribere['percent_shotsOnTarget'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)   
    df_Angribere['Offensive duels won, % score'] = pd.qcut(df_Angribere['percent_newOffensiveDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Angribere['Duels won, % score'] = pd.qcut(df_Angribere['percent_newDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Angribere['Accurate passes, % score'] = pd.qcut(df_Angribere['percent_successfulPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Angribere['Successful dribbles, % score'] = pd.qcut(df_Angribere['percent_newSuccessfulDribbles'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Angribere['xA per 90 score'] = pd.qcut(df_Angribere['average_xgAssist'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Angribere['Touches in box per 90 score'] = pd.qcut(df_Angribere['average_touchInBox'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Angribere['Progressive runs'] = pd.qcut(df_Angribere['average_progressiveRun'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Angribere['Accelerations score'] = pd.qcut(df_Angribere['average_accelerations'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Angribere['Progressive passes per 90 score'] = pd.qcut(df_Angribere['average_successfulProgressivePasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Angribere['Successful attacking actions per 90 score'] = pd.qcut(df_Angribere['average_successfulAttackingActions'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Angribere['Successful dribbles #'] = pd.qcut(df_Angribere['average_newSuccessfulDribbles'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)

    df_Angriberesæsonen = df_Angribere.rename(columns={'total_minutesOnField_x':'Total minutes'},inplace=True)
    df_Angriberesæsonen = df_Angribere.groupby(['Player name','Team name','Total minutes','label']).mean(numeric_only=True)

    df_Angriberesæsonen['Sparkefærdigheder'] = (df_Angriberesæsonen['xG per 90 score'] + df_Angriberesæsonen['xG per 90 score'] + df_Angriberesæsonen['Goals per 90 score'] + df_Angriberesæsonen['Shots on target, % score'])/4
    df_Angriberesæsonen['Boldfast'] = (df_Angriberesæsonen['Offensive duels won, % score'] + df_Angriberesæsonen['Offensive duels won, % score'] + df_Angriberesæsonen['Duels won, % score'] + df_Angriberesæsonen['Accurate passes, % score'] + df_Angriberesæsonen['Successful dribbles, % score'])/5
    df_Angriberesæsonen['Spilintelligens offensivt'] = (df_Angriberesæsonen['xA per 90 score'] + df_Angriberesæsonen['xG per 90 score'] + df_Angriberesæsonen['Touches in box per 90 score'] + df_Angriberesæsonen['Progressive passes per 90 score'] + df_Angriberesæsonen['Successful attacking actions per 90 score'] + df_Angriberesæsonen['Touches in box per 90 score'] + df_Angriberesæsonen['xG per 90 score'])/7
    df_Angriberesæsonen['Målfarlighed'] = (df_Angriberesæsonen['xG per 90 score']+df_Angriberesæsonen['Goals per 90 score']+df_Angriberesæsonen['xG per 90 score'] + df_Angriberesæsonen['Målfarlighed score'])/4
    df_Angriberesæsonen['Fart'] = (df_Angriberesæsonen['Progressive runs'] + + df_Angriberesæsonen['Progressive runs'] + df_Angriberesæsonen['Progressive runs'] + df_Angriberesæsonen['Successful dribbles #'] + df_Angriberesæsonen['Successful dribbles, % score'] + df_Angriberesæsonen['Accelerations score'] + df_Angriberesæsonen['Offensive duels won, % score'])/7
    df_Angriberesæsonen = df_Angriberesæsonen[['Sparkefærdigheder','Boldfast','Spilintelligens offensivt','Målfarlighed','Fart']]
    df_Angriberesæsonen['Samlet'] = (df_Angriberesæsonen['Sparkefærdigheder']+df_Angriberesæsonen['Boldfast']+df_Angriberesæsonen['Spilintelligens offensivt']+df_Angriberesæsonen['Målfarlighed']+df_Angriberesæsonen['Målfarlighed']+df_Angriberesæsonen['Målfarlighed']+df_Angriberesæsonen['Fart'])/7
    df_Angriberesæsonen = df_Angriberesæsonen.sort_values(by='Samlet',ascending=False)

    with st.expander('Angribere kamp for kamp'):
        st.write(df_Angriberesæsonen)

    df_Angriberesæsonen = df_Angriberesæsonen.reset_index()
    df_Angriberesæsonen = df_Angriberesæsonen.drop('label',axis=1)
    df_Angriberesæsonen = df_Angriberesæsonen.groupby(['Player name','Team name','Total minutes']).mean(numeric_only=True)
    df_Angriberesæsonen = df_Angriberesæsonen.sort_values(by='Samlet',ascending=False)
    with st.expander('Angribere sæson'):
        st.write(df_Angriberesæsonen)
    df = pd.read_csv(r'xT/2nd Division 23 24.csv')

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


    dfscore = pd.read_csv(r'xT/Zone scores.csv')

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

    xgc = df1
    xgchold = xgc.rename(columns={'shot.xg': 'Hold xG'})
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

def Tredje_division ():
    col1,col2 = st.columns(2)
    with col1:
        samlettid = st.number_input('Minutter i sæsonen')
    with col2:    
        tidprkamp = st.number_input('Minutter pr. kamp')
        
    df = pd.read_csv(r'Individuelt dashboard/Individuelt dashboard 3.div.csv')
    df.rename(columns={'playerId': 'Player id'}, inplace=True)
    df = df.astype(str)
    dfevents = pd.read_csv('3.div eventdata alle.csv',low_memory=False)
    dfevents = dfevents[['Player id','Player name','team_name','label','date','matchId']]
    dfspillernavn = df[['Player id','matchId','positions','average','percent','total']]
    dfspillernavn = dfspillernavn.astype(str)
    dfevents['Player id'] = dfevents['Player id'].astype(str)
    dfevents['matchId'] = dfevents['matchId'].astype(str)
    df = dfspillernavn.merge(dfevents)

    df['Player&matchId'] = df['Player id'] + df['matchId']
    df['Player&matchId'] = df['Player&matchId'].drop_duplicates(keep='first')
    df = df.dropna()
    df = df[['Player id','Player name','team_name','matchId','label','date','positions','average','percent','total']]

    #df = df.set_index('Player id')

    data = df['positions']
    df1 = pd.DataFrame(data)
    # Funktion, der ekstraherer navne og koder fra strengdata og opretter en ny kolonne med disse værdier
    def extract_positions(data):
        positions_list = ast.literal_eval(data) # Konverterer strengen til en liste af ordbøger
        names = [pos['position']['name'] for pos in positions_list]
        codes = [pos['position']['code'] for pos in positions_list]
        return pd.Series({'position_names': names, 'position_codes': codes})

    # Anvender funktionen på kolonnen og tilføjer resultaterne som nye kolonner til dataframe
    df1[['position_names', 'position_codes']] = df1['positions'].apply(extract_positions)

    df = pd.merge(df,df1,left_index=True, right_index=True)
    df = df.set_index('Player id')
    df = df.drop(columns=['positions_x'])
    df = df.drop(columns=['positions_y'])
    df = df[['Player name','team_name','matchId','label','date','position_names','position_codes','average','percent','total']]
    df = df.rename(columns={'team_name':'Team name'})
    df['percent'] = df['percent'].apply(lambda x: ast.literal_eval(x))

    # Create a new dataframe with the columns as the dictionary keys and the values as a list
    new_df = pd.DataFrame(df['percent'].to_list(), index=df.index).add_prefix('percent_')

    # Concatenate the new dataframe with the original dataframe
    df = pd.concat([df, new_df], axis=1)

    # Drop the original 'percent' column
    df = df.drop('percent', axis=1)

    df['total'] = df['total'].apply(lambda x: ast.literal_eval(x))

    # Create a new dataframe with the columns as the dictionary keys and the values as a list
    new_df = pd.DataFrame(df['total'].to_list(), index=df.index).add_prefix('total_')

    # Concatenate the new dataframe with the original dataframe
    df = pd.concat([df, new_df], axis=1)

    # Drop the original 'percent' column
    df = df.drop('total', axis=1)

    df['average'] = df['average'].apply(lambda x: ast.literal_eval(x))

    # Create a new dataframe with the columns as the dictionary keys and the values as a list
    new_df = pd.DataFrame(df['average'].to_list(), index=df.index).add_prefix('average_')

    # Concatenate the new dataframe with the original dataframe
    df = pd.concat([df, new_df], axis=1)


    # Drop the original 'percent' column
    df = df.drop('average', axis=1)
    df['position_codes'] = df['position_codes'].astype(str)
    #df['date'] = df['date'].astype(str)
    #df['date'] = df['date'].apply(lambda x: parser.parse(x))

    # Sort the dataframe by the 'date' column
    #df = df.sort_values(by='date',ascending=False)

    # Format the 'date' column to day-month-year format
    #df['date'] = df['date'].apply(lambda x: x.strftime('%d-%m-%Y'))
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date',ascending=False)

    df_backs = df[df['position_codes'].str.contains('|'.join(['lb', 'rb']))]
    df_backs = df_backs[df_backs['total_minutesOnField'] >= tidprkamp]
    df_backsminutter = df_backs[['Player name','Team name','total_minutesOnField']]
    df_backsminutter = df_backsminutter.groupby(['Player id']).sum(numeric_only=True)
    df_backsminutter = df_backsminutter[df_backsminutter['total_minutesOnField'] >= samlettid]

    df_Stoppere = df[df['position_codes'].str.contains('|'.join(['cb']))]
    df_Stoppere = df_Stoppere[df_Stoppere['total_minutesOnField'] >= tidprkamp]
    df_stoppereminutter = df_Stoppere[['Player name','Team name','total_minutesOnField']]
    df_stoppereminutter = df_stoppereminutter.groupby(['Player id']).sum(numeric_only=True)
    df_stoppereminutter = df_stoppereminutter[df_stoppereminutter['total_minutesOnField'] >= samlettid]

    df_Centrale_midt = df[df['position_codes'].str.contains('|'.join(['cm','amf','dmf']))]
    df_Centrale_midt = df_Centrale_midt[df_Centrale_midt['total_minutesOnField'] >= tidprkamp]
    df_centraleminutter = df_Centrale_midt[['Player name','Team name','total_minutesOnField']]
    df_centraleminutter = df_centraleminutter.groupby(['Player id']).sum(numeric_only=True)
    df_centraleminutter = df_centraleminutter[df_centraleminutter['total_minutesOnField'] >= samlettid]

    df_Kanter = df[df['position_codes'].str.contains('|'.join(['rw','lw','ramf','lamf']))]
    df_Kanter = df_Kanter[df_Kanter['total_minutesOnField'] >=tidprkamp]
    df_kanterminutter = df_Kanter[['Player name','Team name','total_minutesOnField']]
    df_kanterminutter = df_kanterminutter.groupby(['Player id']).sum(numeric_only=True)
    df_kanterminutter = df_kanterminutter[df_kanterminutter['total_minutesOnField'] >=samlettid]


    df_Angribere = df[df['position_codes'].str.contains('|'.join(['cf','ss']))]
    df_Angribere = df_Angribere[df_Angribere['total_minutesOnField'] >= tidprkamp]
    df_angribereminutter = df_Angribere[['Player name','Team name','total_minutesOnField']]
    df_angribereminutter = df_angribereminutter.groupby(['Player id']).sum(numeric_only=True)
    df_angribereminutter = df_angribereminutter[df_angribereminutter['total_minutesOnField'] >= samlettid]


    df_backs = pd.merge(df_backsminutter,df_backs,on=('Player id'))
    df_backs = df_backs[df_backs['total_minutesOnField_y'] >=tidprkamp]

    df_backs['Accurate crosses score'] = pd.qcut(df_backs['percent_successfulCrosses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_backs['Number of crosses score'] = pd.qcut(df_backs['average_crosses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_backs['XA score'] = pd.qcut(df_backs['average_xgAssist'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_backs['Passes to final third score'] = pd.qcut(df_backs['average_successfulPassesToFinalThird'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_backs['Successful dribbles score'] = pd.qcut(df_backs['percent_newSuccessfulDribbles'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_backs['Defensive duels won score'] = pd.qcut(df_backs['percent_newDefensiveDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_backs['Progressive runs score'] = pd.qcut(df_backs['average_progressiveRun'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_backs['Offensive duels won score'] = pd.qcut(df_backs['percent_newOffensiveDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_backs['Accelerations score'] = pd.qcut(df_backs['average_accelerations'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_backs['Duels won score'] = pd.qcut(df_backs['percent_newDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_backs['Interceptions score'] = pd.qcut(df_backs['average_interceptions'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_backs['Successful defensive actions score'] = pd.qcut(df_backs['average_successfulDefensiveAction'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_backssæsonen = df_backs[['label','Player name','Team name','total_minutesOnField_x','total_minutesOnField_y','Number of crosses score','Accurate crosses score','XA score','Passes to final third score','Successful dribbles score','Defensive duels won score','Progressive runs score','Offensive duels won score','Accelerations score','Duels won score','Interceptions score','Successful defensive actions score']]
    df_backssæsonen.rename(columns={'total_minutesOnField_x':'Total minutes'},inplace=True)
    df_backssæsonen = df_backssæsonen.groupby(['Player name','Team name','Total minutes','label']).mean(numeric_only=True)

    df_backssæsonen['Indlægsstærk'] = (df_backssæsonen['Number of crosses score'] + df_backssæsonen['Accurate crosses score'] + df_backssæsonen['XA score'] + df_backssæsonen['Passes to final third score'])/4
    df_backssæsonen['1v1 færdigheder'] = (df_backssæsonen['Successful dribbles score'] + df_backssæsonen['Defensive duels won score'] + df_backssæsonen['Progressive runs score'] + df_backssæsonen['Offensive duels won score'] + df_backssæsonen['Accelerations score'] + df_backssæsonen['Duels won score'])/6
    df_backssæsonen['Spilintelligens defensivt'] = (df_backssæsonen['Interceptions score'] + df_backssæsonen['Successful defensive actions score'] + df_backssæsonen['Duels won score'] + df_backssæsonen['Defensive duels won score'])/4
    df_backssæsonen['Fart'] = (df_backssæsonen['Successful dribbles score'] + df_backssæsonen['Progressive runs score'] + df_backssæsonen['Offensive duels won score'] + df_backssæsonen['Accelerations score'])/4
    df_backssæsonen ['Samlet'] = (df_backssæsonen['Indlægsstærk'] + df_backssæsonen['1v1 færdigheder'] + df_backssæsonen['Spilintelligens defensivt'] + df_backssæsonen['Fart'])/4

    df_backssæsonen = df_backssæsonen[['Indlægsstærk','1v1 færdigheder','Spilintelligens defensivt','Fart','Samlet']]
    df_backssæsonen = df_backssæsonen.round(3).astype(float)
    df_backssæsonen = df_backssæsonen.sort_values(by='Samlet',ascending=False)
    with st.expander('Backs kamp for kamp'):
        st.write(df_backssæsonen)
    df_backssæsonen = df_backssæsonen.reset_index()
    df_backssæsonen = df_backssæsonen.drop('label',axis=1)
    df_backssæsonen = df_backssæsonen.groupby(['Player name','Team name','Total minutes']).mean(numeric_only=True)
    df_backssæsonen = df_backssæsonen.sort_values(by='Samlet',ascending=False)
    with st.expander('Backs'):
        st.dataframe(df_backssæsonen)
       
    df_Stoppere = pd.merge(df_stoppereminutter,df_Stoppere,on=('Player id'))
    df_Stoppere = df_Stoppere[df_Stoppere['total_minutesOnField_y'] >=tidprkamp]
    
    df_Stoppere['Accurate passes score'] = pd.qcut(df_Stoppere['percent_successfulPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Accurate long passes score'] = pd.qcut(df_Stoppere['percent_successfulLongPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Forward passes score'] = pd.qcut(df_Stoppere['average_successfulForwardPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Accurate forward passes score'] = pd.qcut(df_Stoppere['percent_successfulForwardPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Accurate progressive passes score'] = pd.qcut(df_Stoppere['percent_successfulProgressivePasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Accurate vertical passes score'] = pd.qcut(df_Stoppere['percent_successfulVerticalPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Interceptions score'] = pd.qcut(df_Stoppere['average_interceptions'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Succesful defensive actions score'] = pd.qcut(df_Stoppere['average_successfulDefensiveAction'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Shots blocked score'] = pd.qcut(df_Stoppere['average_shotsBlocked'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Defensive duels won score'] = pd.qcut(df_Stoppere['average_newDefensiveDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Defensive duels won % score'] = pd.qcut(df_Stoppere['percent_newDefensiveDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Accurate passes to final third'] = pd.qcut(df_Stoppere['percent_successfulPassesToFinalThird'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Accurate through passes'] = pd.qcut(df_Stoppere['percent_successfulThroughPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Vertical passes'] = pd.qcut(df_Stoppere['average_successfulVerticalPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Through passes'] = pd.qcut(df_Stoppere['average_successfulThroughPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Passes to final third'] = pd.qcut(df_Stoppere['average_successfulPassesToFinalThird'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Progressive runs'] = pd.qcut(df_Stoppere['average_progressiveRun'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Offensive duels won %'] = pd.qcut(df_Stoppere['percent_newOffensiveDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Successful dribbles %'] = pd.qcut(df_Stoppere['percent_newSuccessfulDribbles'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Progressive passes score'] = pd.qcut(df_Stoppere['average_successfulProgressivePasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Aerial duels won score'] = pd.qcut(df_Stoppere['average_fieldAerialDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Stoppere['Aerial duels won % score'] = pd.qcut(df_Stoppere['percent_aerialDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)

    df_Stopperesæsonen = df_Stoppere[['label','Player name','Team name','total_minutesOnField_x','total_minutesOnField_y','Accurate passes score','Accurate long passes score','Forward passes score','Accurate forward passes score','Accurate progressive passes score','Accurate vertical passes score','Interceptions score','Succesful defensive actions score','Shots blocked score','Defensive duels won score','Defensive duels won % score','Accurate passes to final third','Accurate through passes','Vertical passes','Through passes','Passes to final third','Progressive passes score','Aerial duels won score','Aerial duels won % score','Progressive runs','Offensive duels won %','Successful dribbles %']]
    df_Stopperesæsonen.rename(columns={'total_minutesOnField_x':'Total minutes'},inplace=True)
    df_Stopperesæsonen = df_Stopperesæsonen.groupby(['Player name','Team name','Total minutes','label']).mean(numeric_only=True)
    df_Stopperesæsonen['Pasningssikker'] = (df_Stopperesæsonen['Accurate passes score'] + df_Stopperesæsonen['Accurate long passes score'] + df_Stopperesæsonen['Forward passes score'] + df_Stopperesæsonen['Accurate forward passes score'] + df_Stopperesæsonen['Accurate progressive passes score'] + df_Stopperesæsonen['Accurate vertical passes score'])/6
    df_Stopperesæsonen['Spilintelligens defensivt'] = (df_Stopperesæsonen['Interceptions score'] + df_Stopperesæsonen['Succesful defensive actions score'] + df_Stopperesæsonen['Shots blocked score'] + df_Stopperesæsonen['Succesful defensive actions score'] + df_Stopperesæsonen['Defensive duels won % score']) /5
    df_Stopperesæsonen['Spilintelligens offensivt'] = (df_Stopperesæsonen['Forward passes score'] + df_Stopperesæsonen['Accurate forward passes score'] + df_Stopperesæsonen['Accurate passes to final third'] + df_Stopperesæsonen['Passes to final third'] + df_Stopperesæsonen['Accurate progressive passes score'] + df_Stopperesæsonen['Progressive passes score'] + df_Stopperesæsonen['Through passes'] + df_Stopperesæsonen['Accurate through passes']+ df_Stopperesæsonen['Progressive runs'] + df_Stopperesæsonen['Offensive duels won %'] + df_Stopperesæsonen['Successful dribbles %'])/11
    df_Stopperesæsonen['Nærkamps- og duelstærk'] = (df_Stopperesæsonen['Defensive duels won % score'] + df_Stopperesæsonen['Aerial duels won % score'] + df_Stopperesæsonen['Defensive duels won % score'])/3
    df_Stopperesæsonen['Samlet'] = (df_Stopperesæsonen['Pasningssikker'] + df_Stopperesæsonen['Spilintelligens defensivt'] + df_Stopperesæsonen['Spilintelligens offensivt'] + df_Stopperesæsonen['Nærkamps- og duelstærk'])/4

    df_Stopperesæsonen = df_Stopperesæsonen[['Pasningssikker','Spilintelligens defensivt','Spilintelligens offensivt','Nærkamps- og duelstærk','Samlet']]
    df_Stopperesæsonen = df_Stopperesæsonen.sort_values(by='Samlet',ascending=False)

    with st.expander('Stoppere kamp for kamp'):
        st.write(df_Stopperesæsonen)
    df_Stopperesæsonen = df_Stopperesæsonen.reset_index()
    df_Stopperesæsonen = df_Stopperesæsonen.drop('label',axis=1)
    df_Stopperesæsonen = df_Stopperesæsonen.groupby(['Player name','Team name','Total minutes']).mean(numeric_only=True)
    df_Stopperesæsonen = df_Stopperesæsonen.sort_values(by='Samlet',ascending=False)
    
    with st.expander('Stoppere sæson'):
        st.dataframe(df_Stopperesæsonen)

    df_Centrale_midt = pd.merge(df_centraleminutter,df_Centrale_midt,on=('Player id'))
    df_Centrale_midt = df_Centrale_midt[df_Centrale_midt['total_minutesOnField_y'] >=tidprkamp]

    df_Centrale_midt['Passes %'] = pd.qcut(df_Centrale_midt['percent_successfulPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Passes #'] = pd.qcut(df_Centrale_midt['average_successfulPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Forward Passes %'] = pd.qcut(df_Centrale_midt['percent_successfulForwardPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Forward Passes #'] = pd.qcut(df_Centrale_midt['average_successfulForwardPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Long Passes %'] = pd.qcut(df_Centrale_midt['percent_successfulLongPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Long Passes #'] = pd.qcut(df_Centrale_midt['average_successfulLongPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Smart passes %'] = pd.qcut(df_Centrale_midt['percent_successfulSmartPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Smart passes #'] = pd.qcut(df_Centrale_midt['average_successfulSmartPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Key passes %'] = pd.qcut(df_Centrale_midt['percent_successfulKeyPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Key passes #'] = pd.qcut(df_Centrale_midt['average_successfulKeyPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Passes to final third %'] = pd.qcut(df_Centrale_midt['percent_successfulPassesToFinalThird'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Passes to final third #'] = pd.qcut(df_Centrale_midt['average_successfulPassesToFinalThird'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Vertical passes %'] = pd.qcut(df_Centrale_midt['percent_successfulVerticalPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Vertical passes #'] = pd.qcut(df_Centrale_midt['average_successfulVerticalPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Through passes %'] = pd.qcut(df_Centrale_midt['percent_successfulThroughPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Through passes #'] = pd.qcut(df_Centrale_midt['average_successfulThroughPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Progressive passes %'] = pd.qcut(df_Centrale_midt['percent_successfulProgressivePasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Progressive passes #'] = pd.qcut(df_Centrale_midt['average_successfulProgressivePasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Offensive duels %'] = pd.qcut(df_Centrale_midt['percent_newOffensiveDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Received passes'] = pd.qcut(df_Centrale_midt['average_receivedPass'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Succesful dribbles %'] = pd.qcut(df_Centrale_midt['percent_newSuccessfulDribbles'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Succesful dribbles #'] = pd.qcut(df_Centrale_midt['average_newSuccessfulDribbles'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Duels won %'] = pd.qcut(df_Centrale_midt['percent_newDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Duels won #'] = pd.qcut(df_Centrale_midt['average_newDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Interceptions'] = pd.qcut(df_Centrale_midt['average_interceptions'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Counterpressing recoveries #'] = pd.qcut(df_Centrale_midt['average_counterpressingRecoveries'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Defensive duels won #'] = pd.qcut(df_Centrale_midt['average_newDefensiveDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Centrale_midt['Defensive duels won %'] = pd.qcut(df_Centrale_midt['percent_newDefensiveDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)

    df_Centrale_midtsæsonen = df_Centrale_midt.rename(columns={'total_minutesOnField_x':'Total minutes'},inplace=True)
    df_Centrale_midtsæsonen = df_Centrale_midt.groupby(['Player name','Team name','Total minutes','label']).mean(numeric_only=True)
    df_Centrale_midtsæsonen['Pasningssikker/Spilvendinger'] = (df_Centrale_midtsæsonen['Passes %'] + df_Centrale_midtsæsonen['Passes #'] + df_Centrale_midtsæsonen['Forward Passes %'] + df_Centrale_midtsæsonen['Forward Passes #'] + df_Centrale_midtsæsonen['Long Passes %'] + df_Centrale_midtsæsonen['Long Passes #']+ df_Centrale_midtsæsonen['Smart passes %'] + df_Centrale_midtsæsonen['Smart passes #'] + + df_Centrale_midtsæsonen['Key passes %'] + df_Centrale_midtsæsonen['Key passes #'] + df_Centrale_midtsæsonen['Passes to final third %'] + df_Centrale_midtsæsonen['Passes to final third #']+ df_Centrale_midtsæsonen['Vertical passes %'] + df_Centrale_midtsæsonen['Vertical passes #']+ df_Centrale_midtsæsonen['Through passes %'] + df_Centrale_midtsæsonen['Through passes #']+ df_Centrale_midtsæsonen['Progressive passes %'] + df_Centrale_midtsæsonen['Progressive passes #'])/18
    df_Centrale_midtsæsonen['Boldfast'] = (df_Centrale_midtsæsonen['Passes %'] + df_Centrale_midtsæsonen['Passes #']+ df_Centrale_midtsæsonen['Offensive duels %'] + df_Centrale_midtsæsonen['Received passes'] + df_Centrale_midtsæsonen['Succesful dribbles %'] + df_Centrale_midtsæsonen['Succesful dribbles #'])/6
    df_Centrale_midtsæsonen['Spilintelligens defensivt'] = (df_Centrale_midtsæsonen['Duels won %'] + df_Centrale_midtsæsonen['Duels won #'] +df_Centrale_midtsæsonen['Interceptions'] + df_Centrale_midtsæsonen['Counterpressing recoveries #'] + df_Centrale_midtsæsonen['Defensive duels won %'] + df_Centrale_midtsæsonen['Defensive duels won #'])/6
    df_Centrale_midtsæsonen['Samlet'] = (df_Centrale_midtsæsonen['Pasningssikker/Spilvendinger'] + df_Centrale_midtsæsonen['Boldfast'] + df_Centrale_midtsæsonen['Spilintelligens defensivt'])/3

    df_Centrale_midtsæsonen = df_Centrale_midtsæsonen[['Pasningssikker/Spilvendinger','Boldfast','Spilintelligens defensivt','Samlet']]
    df_Centrale_midtsæsonen = df_Centrale_midtsæsonen.sort_values(by='Samlet',ascending=False)
    with st.expander('Centrale midt kamp for kamp'):
        st.write(df_Centrale_midtsæsonen)

    df_Centrale_midtsæsonen = df_Centrale_midtsæsonen.reset_index()
    df_Centrale_midtsæsonen = df_Centrale_midtsæsonen.drop('label',axis=1)
    df_Centrale_midtsæsonen = df_Centrale_midtsæsonen.groupby(['Player name','Team name','Total minutes']).mean(numeric_only=True)
    df_Centrale_midtsæsonen = df_Centrale_midtsæsonen.sort_values(by='Samlet',ascending=False)
    with st.expander('Centrale midt sæson'):
        st.write(df_Centrale_midtsæsonen)


    df_Kanter = pd.merge(df_kanterminutter,df_Kanter,on=('Player id'))
    df_Kanter = df_Kanter[df_Kanter['total_minutesOnField_y'] >=tidprkamp]

    df_Kanter['Shots on target %'] = pd.qcut(df_Kanter['percent_shotsOnTarget'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Shots on target #'] = pd.qcut(df_Kanter['average_shotsOnTarget'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['XG'] = pd.qcut(df_Kanter['average_xgShot'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Successful dribbles #'] = pd.qcut(df_Kanter['average_newSuccessfulDribbles'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Successful dribbles %'] = pd.qcut(df_Kanter['percent_newSuccessfulDribbles'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Offensive duels %'] = pd.qcut(df_Kanter['percent_newOffensiveDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Offensive duels #'] = pd.qcut(df_Kanter['average_newOffensiveDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Passes %'] = pd.qcut(df_Kanter['percent_successfulPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Passes #'] = pd.qcut(df_Kanter['average_successfulPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Forward Passes %'] = pd.qcut(df_Kanter['percent_successfulForwardPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Forward Passes #'] = pd.qcut(df_Kanter['average_successfulForwardPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Smart passes %'] = pd.qcut(df_Kanter['percent_successfulSmartPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Smart passes #'] = pd.qcut(df_Kanter['average_successfulSmartPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Key passes %'] = pd.qcut(df_Kanter['percent_successfulKeyPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Key passes #'] = pd.qcut(df_Kanter['average_successfulKeyPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Passes to final third %'] = pd.qcut(df_Kanter['percent_successfulPassesToFinalThird'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Passes to final third #'] = pd.qcut(df_Kanter['average_successfulPassesToFinalThird'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Vertical passes %'] = pd.qcut(df_Kanter['percent_successfulVerticalPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Vertical passes #'] = pd.qcut(df_Kanter['average_successfulVerticalPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Through passes %'] = pd.qcut(df_Kanter['percent_successfulThroughPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Through passes #'] = pd.qcut(df_Kanter['average_successfulThroughPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Progressive passes %'] = pd.qcut(df_Kanter['percent_successfulProgressivePasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Progressive passes #'] = pd.qcut(df_Kanter['average_successfulProgressivePasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Goal conversion %'] = pd.qcut(df_Kanter['percent_goalConversion'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['XG per 90'] = pd.qcut(df_Kanter['average_xgShot'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['XA per 90'] = pd.qcut(df_Kanter['average_xgAssist'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Successful attacking actions'] = pd.qcut(df_Kanter['average_successfulAttackingActions'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Progressive runs'] = pd.qcut(df_Kanter['average_progressiveRun'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Kanter['Accelerations score'] = pd.qcut(df_Kanter['average_accelerations'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)

    df_Kantersæsonen = df_Kanter.rename(columns={'total_minutesOnField_x':'Total minutes'},inplace=True)
    df_Kantersæsonen = df_Kanter.groupby(['Player name','Team name','Total minutes','label']).mean(numeric_only=True)

    df_Kantersæsonen['Sparkefærdigheder'] = (df_Kantersæsonen['Shots on target %'] + df_Kantersæsonen['Shots on target #'] + df_Kantersæsonen['XG'] + df_Kantersæsonen['Passes to final third %'] + df_Kantersæsonen['Forward Passes %'] + df_Kantersæsonen['Vertical passes %'])/6
    df_Kantersæsonen['Kombinationsstærk'] = (df_Kantersæsonen['Passes %'] + df_Kantersæsonen['Passes #'] + df_Kantersæsonen['Forward Passes %'] + df_Kantersæsonen['Forward Passes #'] + df_Kantersæsonen['Passes to final third %'] + df_Kantersæsonen['Passes to final third #'] + df_Kantersæsonen['Through passes %'] + df_Kantersæsonen['Through passes #'] + df_Kantersæsonen['Progressive passes %'] + df_Kantersæsonen['Progressive passes #'] + df_Kantersæsonen['Successful attacking actions'])/11
    df_Kantersæsonen['Spilintelligens offensivt/indlægsstærk'] = (df_Kantersæsonen['XA per 90'] + df_Kantersæsonen['XG per 90'] + df_Kantersæsonen['Through passes %'] + df_Kantersæsonen['Through passes #'] + df_Kantersæsonen['Smart passes %'] + df_Kantersæsonen['Smart passes #'] + df_Kantersæsonen['Progressive passes %'] + df_Kantersæsonen['Progressive passes #'] + df_Kantersæsonen['Key passes %'] + df_Kantersæsonen['Key passes #'] + df_Kantersæsonen['Successful attacking actions'])/11
    df_Kantersæsonen['1v1 offensivt'] = (df_Kantersæsonen['Successful dribbles #'] + df_Kantersæsonen['Successful dribbles %'] + df_Kantersæsonen['Offensive duels #'] + df_Kantersæsonen['Offensive duels %'] + df_Kantersæsonen['Progressive runs'])/5
    df_Kantersæsonen['Fart'] = (df_Kantersæsonen['Progressive runs'] + df_Kantersæsonen['Successful dribbles #'] + df_Kantersæsonen['Successful dribbles %'] + df_Kantersæsonen['Accelerations score'])/4
    df_Kantersæsonen['Samlet'] = (df_Kantersæsonen['Sparkefærdigheder'] + df_Kantersæsonen['Kombinationsstærk'] + df_Kantersæsonen['Spilintelligens offensivt/indlægsstærk'] + df_Kantersæsonen['1v1 offensivt'] + df_Kantersæsonen['Fart'])/5
    df_Kantersæsonen = df_Kantersæsonen[['Sparkefærdigheder','Kombinationsstærk','Spilintelligens offensivt/indlægsstærk','1v1 offensivt','Fart','Samlet']]
    df_Kantersæsonen = df_Kantersæsonen.sort_values(by='Samlet',ascending=False)

    with st.expander('Kanter kamp for kamp'):
        st.write(df_Kantersæsonen)

    df_Kantersæsonen = df_Kantersæsonen.reset_index()
    df_Kantersæsonen = df_Kantersæsonen.drop('label',axis=1)
    df_Kantersæsonen = df_Kantersæsonen.groupby(['Player name','Team name','Total minutes']).mean(numeric_only=True)
    df_Kantersæsonen = df_Kantersæsonen.sort_values(by='Samlet',ascending=False)
    with st.expander('Kanter sæson'):
        st.write(df_Kantersæsonen)


    df_Angribere = pd.merge(df_angribereminutter,df_Angribere,on=('Player id'))
    df_Angribere = df_Angribere[df_Angribere['total_minutesOnField_y'] >=tidprkamp]

    df_Angribere['Målfarlighed udregning'] = df_Angribere['average_goals'] - df_Angribere['average_xgShot']
    df_Angribere['Målfarlighed score'] =  pd.qcut(df_Angribere['Målfarlighed udregning'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Angribere['xG per 90 score'] = pd.qcut(df_Angribere['average_xgShot'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Angribere['Goals per 90 score'] = pd.qcut(df_Angribere['average_goals'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)  
    df_Angribere['Shots on target, % score'] = pd.qcut(df_Angribere['percent_shotsOnTarget'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)   
    df_Angribere['Offensive duels won, % score'] = pd.qcut(df_Angribere['percent_newOffensiveDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Angribere['Duels won, % score'] = pd.qcut(df_Angribere['percent_newDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Angribere['Accurate passes, % score'] = pd.qcut(df_Angribere['percent_successfulPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Angribere['Successful dribbles, % score'] = pd.qcut(df_Angribere['percent_newSuccessfulDribbles'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Angribere['xA per 90 score'] = pd.qcut(df_Angribere['average_xgAssist'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Angribere['Touches in box per 90 score'] = pd.qcut(df_Angribere['average_touchInBox'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Angribere['Progressive runs'] = pd.qcut(df_Angribere['average_progressiveRun'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Angribere['Accelerations score'] = pd.qcut(df_Angribere['average_accelerations'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Angribere['Progressive passes per 90 score'] = pd.qcut(df_Angribere['average_successfulProgressivePasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Angribere['Successful attacking actions per 90 score'] = pd.qcut(df_Angribere['average_successfulAttackingActions'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    df_Angribere['Successful dribbles #'] = pd.qcut(df_Angribere['average_newSuccessfulDribbles'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)

    df_Angriberesæsonen = df_Angribere.rename(columns={'total_minutesOnField_x':'Total minutes'},inplace=True)
    df_Angriberesæsonen = df_Angribere.groupby(['Player name','Team name','Total minutes','label']).mean(numeric_only=True)

    df_Angriberesæsonen['Sparkefærdigheder'] = (df_Angriberesæsonen['xG per 90 score'] + df_Angriberesæsonen['xG per 90 score'] + df_Angriberesæsonen['Goals per 90 score'] + df_Angriberesæsonen['Shots on target, % score'])/4
    df_Angriberesæsonen['Boldfast'] = (df_Angriberesæsonen['Offensive duels won, % score'] + df_Angriberesæsonen['Offensive duels won, % score'] + df_Angriberesæsonen['Duels won, % score'] + df_Angriberesæsonen['Accurate passes, % score'] + df_Angriberesæsonen['Successful dribbles, % score'])/5
    df_Angriberesæsonen['Spilintelligens offensivt'] = (df_Angriberesæsonen['xA per 90 score'] + df_Angriberesæsonen['xG per 90 score'] + df_Angriberesæsonen['Touches in box per 90 score'] + df_Angriberesæsonen['Progressive passes per 90 score'] + df_Angriberesæsonen['Successful attacking actions per 90 score'] + df_Angriberesæsonen['Touches in box per 90 score'] + df_Angriberesæsonen['xG per 90 score'])/7
    df_Angriberesæsonen['Målfarlighed'] = (df_Angriberesæsonen['xG per 90 score']+df_Angriberesæsonen['Goals per 90 score']+df_Angriberesæsonen['xG per 90 score'] + df_Angriberesæsonen['Målfarlighed score'])/4
    df_Angriberesæsonen['Fart'] = (df_Angriberesæsonen['Progressive runs'] + + df_Angriberesæsonen['Progressive runs'] + df_Angriberesæsonen['Progressive runs'] + df_Angriberesæsonen['Successful dribbles #'] + df_Angriberesæsonen['Successful dribbles, % score'] + df_Angriberesæsonen['Accelerations score'] + df_Angriberesæsonen['Offensive duels won, % score'])/7
    df_Angriberesæsonen = df_Angriberesæsonen[['Sparkefærdigheder','Boldfast','Spilintelligens offensivt','Målfarlighed','Fart']]
    df_Angriberesæsonen['Samlet'] = (df_Angriberesæsonen['Sparkefærdigheder']+df_Angriberesæsonen['Boldfast']+df_Angriberesæsonen['Spilintelligens offensivt']+df_Angriberesæsonen['Målfarlighed']+df_Angriberesæsonen['Målfarlighed']+df_Angriberesæsonen['Målfarlighed']+df_Angriberesæsonen['Fart'])/7
    df_Angriberesæsonen = df_Angriberesæsonen.sort_values(by='Samlet',ascending=False)

    with st.expander('Angribere kamp for kamp'):
        st.write(df_Angriberesæsonen)

    df_Angriberesæsonen = df_Angriberesæsonen.reset_index()
    df_Angriberesæsonen = df_Angriberesæsonen.drop('label',axis=1)
    df_Angriberesæsonen = df_Angriberesæsonen.groupby(['Player name','Team name','Total minutes']).mean(numeric_only=True)
    df_Angriberesæsonen = df_Angriberesæsonen.sort_values(by='Samlet',ascending=False)
    with st.expander('Angribere sæson'):
        st.write(df_Angriberesæsonen)
    df = pd.read_csv(r'xT/3. Division 23 24.csv')

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


    dfscore = pd.read_csv(r'xT/Zone scores.csv')

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

    xgc = df1
    xgchold = xgc.rename(columns={'shot.xg': 'Hold xG'})
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

def scouting_database ():
    import gspread
    import pandas as pd

    gc = gspread.service_account('wellness-1123-178fea106d0a.json')
    sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1khFGHAR_pHKwhas7yBwz_asga6yFmTzUykUs_-J43VY/edit#gid=282879453')
    ws = sh.worksheet('Data')
    df = pd.DataFrame(ws.get_all_records())
    df = df[['Spillernavn','Hold (Klubben staves på samme måde som DBU appen)','Årgang','Scout','Den kampafgørende (nutid)','Udviklingspotentiale (fremtid)','Yderlig kommentar på spilleren?:']]
    df['Den kampafgørende (nutid)'] = pd.to_numeric(df['Den kampafgørende (nutid)'],errors='coerce')
    df['Udviklingspotentiale (fremtid)'] = pd.to_numeric(df['Udviklingspotentiale (fremtid)'],errors='coerce')
    df['Samlet'] = df['Den kampafgørende (nutid)'] + df['Udviklingspotentiale (fremtid)']    
    
    df['Årgang'] = df['Årgang'].astype(str)
    unique_årgang = sorted(df['Årgang'].unique())

    df['Spillernavn'] = df['Spillernavn'].astype(str)

    selected_årgang = st.multiselect("Vælg Årgang", unique_årgang)

    filtered_df = df[df['Årgang'].isin(selected_årgang)]

    grouped_df = filtered_df.groupby(['Spillernavn','Hold (Klubben staves på samme måde som DBU appen)', 'Årgang','Scout']).mean()

    st.dataframe(grouped_df)

Ligaer = {'U15 Ligaen':U15_liga,
          'U17 Ligaen':U17_liga,
          'U19 Ligaen':U19_liga,
          'U17 Divisionen':U17_Division,
          'U19 Divisionen':U19_Division,
          'Superligaen':Superliga,
          '1. Division':Første_division,
          '2. Division':Anden_division,
          '3. Division':Tredje_division,
          'Scoutingdatabasen':scouting_database,}

rullemenu = st.selectbox('Vælg liga',Ligaer.keys())
Ligaer[rullemenu]()