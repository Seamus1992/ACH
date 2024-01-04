from azure.storage.fileshare import ShareServiceClient
import json
import pandas as pd
from pandas import json_normalize
import numpy as np

connection_string = 'SharedAccessSignature=sv=2020-08-04&ss=f&srt=sco&sp=rl&se=2025-01-11T22:47:25Z&st=2022-01-11T14:47:25Z&spr=https&sig=CXdXPlHz%2FhW0IRugFTfCrB7osNQVZJ%2BHjNR1EM2s6RU%3D;FileEndpoint=https://divforeningendataout1.file.core.windows.net/;'
share_name = 'divisionsforeningen-outgoingdata'
dir_path = 'KampData/Sæson 23-24/U15 Ligaen/'

service_client = ShareServiceClient.from_connection_string(connection_string)
share_client = service_client.get_share_client(share_name)
directory_client = share_client.get_directory_client(dir_path)

json_files = []

def find_json_files(directory_client):
    for item in directory_client.list_directories_and_files():
        if item.is_directory:
            sub_directory_client = directory_client.get_subdirectory_client(item.name)
            find_json_files(sub_directory_client)
        elif item.name.endswith('.json') and 'MatchEvents' in item.name:
            json_files.append(json.loads(directory_client.get_file_client(item.name).download_file().readall().decode()))

find_json_files(directory_client)

events_list = []

for item in json_files:
    events_list.extend(item['events'])

df = pd.json_normalize(events_list)

json_files = []

def find_json_files(directory_client):
    for item in directory_client.list_directories_and_files():
        if item.is_directory:
            sub_directory_client = directory_client.get_subdirectory_client(item.name)
            find_json_files(sub_directory_client)
        elif item.name.endswith('.json') and 'MatchDetail' in item.name:
            json_files.append(json.loads(directory_client.get_file_client(item.name).download_file().readall().decode()))
            
find_json_files(directory_client)
kampdetaljer = json_normalize(json_files)
kampdetaljer = kampdetaljer[['wyId','label','date']]
kampdetaljer = kampdetaljer.rename(columns={'wyId':'matchId'})
df = kampdetaljer.merge(df)
df = df[['label','date','shot.isGoal','shot.xg','type.primary','type.secondary','location.x','location.y','team.name','opponentTeam.name','player.id','player.name','pass.accurate','pass.endLocation.x','pass.endLocation.y','pass.recipient.id','pass.recipient.name','possession.id','possession.eventsNumber','possession.eventIndex','possession.types','possession.team.name','possession.attack.xg','carry.progression','carry.endLocation.x','carry.endLocation.y']]

df.to_csv('xT/U15 Ligaen 23 24.csv',index=False)

connection_string = 'SharedAccessSignature=sv=2020-08-04&ss=f&srt=sco&sp=rl&se=2025-01-11T22:47:25Z&st=2022-01-11T14:47:25Z&spr=https&sig=CXdXPlHz%2FhW0IRugFTfCrB7osNQVZJ%2BHjNR1EM2s6RU%3D;FileEndpoint=https://divforeningendataout1.file.core.windows.net/;'
share_name = 'divisionsforeningen-outgoingdata'
dir_path = 'KampData/Sæson 23-24/U17 Ligaen/'

service_client = ShareServiceClient.from_connection_string(connection_string)
share_client = service_client.get_share_client(share_name)
directory_client = share_client.get_directory_client(dir_path)

json_files = []

def find_json_files(directory_client):
    for item in directory_client.list_directories_and_files():
        if item.is_directory:
            sub_directory_client = directory_client.get_subdirectory_client(item.name)
            find_json_files(sub_directory_client)
        elif item.name.endswith('.json') and 'MatchEvents' in item.name:
            json_files.append(json.loads(directory_client.get_file_client(item.name).download_file().readall().decode()))

find_json_files(directory_client)

events_list = []

for item in json_files:
    events_list.extend(item['events'])

df = pd.json_normalize(events_list)

json_files = []

def find_json_files(directory_client):
    for item in directory_client.list_directories_and_files():
        if item.is_directory:
            sub_directory_client = directory_client.get_subdirectory_client(item.name)
            find_json_files(sub_directory_client)
        elif item.name.endswith('.json') and 'MatchDetail' in item.name:
            json_files.append(json.loads(directory_client.get_file_client(item.name).download_file().readall().decode()))
            
find_json_files(directory_client)
kampdetaljer = json_normalize(json_files)
kampdetaljer = kampdetaljer[['wyId','label','date']]
kampdetaljer = kampdetaljer.rename(columns={'wyId':'matchId'})
df = kampdetaljer.merge(df)
df = df[['label','date','shot.isGoal','shot.xg','type.primary','type.secondary','location.x','location.y','team.name','opponentTeam.name','player.id','player.name','pass.accurate','pass.endLocation.x','pass.endLocation.y','pass.recipient.id','pass.recipient.name','possession.id','possession.eventsNumber','possession.eventIndex','possession.types','possession.team.name','possession.attack.xg','carry.progression','carry.endLocation.x','carry.endLocation.y']]

df.to_csv('xT/U17 Ligaen 23 24.csv',index=False)

connection_string = 'SharedAccessSignature=sv=2020-08-04&ss=f&srt=sco&sp=rl&se=2025-01-11T22:47:25Z&st=2022-01-11T14:47:25Z&spr=https&sig=CXdXPlHz%2FhW0IRugFTfCrB7osNQVZJ%2BHjNR1EM2s6RU%3D;FileEndpoint=https://divforeningendataout1.file.core.windows.net/;'
share_name = 'divisionsforeningen-outgoingdata'
dir_path = 'KampData/Sæson 23-24/U19 Ligaen/'

service_client = ShareServiceClient.from_connection_string(connection_string)
share_client = service_client.get_share_client(share_name)
directory_client = share_client.get_directory_client(dir_path)

json_files = []

def find_json_files(directory_client):
    for item in directory_client.list_directories_and_files():
        if item.is_directory:
            sub_directory_client = directory_client.get_subdirectory_client(item.name)
            find_json_files(sub_directory_client)
        elif item.name.endswith('.json') and 'MatchEvents' in item.name:
            json_files.append(json.loads(directory_client.get_file_client(item.name).download_file().readall().decode()))

find_json_files(directory_client)

events_list = []

for item in json_files:
    events_list.extend(item['events'])

df = pd.json_normalize(events_list)

json_files = []

def find_json_files(directory_client):
    for item in directory_client.list_directories_and_files():
        if item.is_directory:
            sub_directory_client = directory_client.get_subdirectory_client(item.name)
            find_json_files(sub_directory_client)
        elif item.name.endswith('.json') and 'MatchDetail' in item.name:
            json_files.append(json.loads(directory_client.get_file_client(item.name).download_file().readall().decode()))
            
find_json_files(directory_client)
kampdetaljer = json_normalize(json_files)
kampdetaljer = kampdetaljer[['wyId','label','date']]
kampdetaljer = kampdetaljer.rename(columns={'wyId':'matchId'})
df = kampdetaljer.merge(df)
df = df[['label','date','shot.isGoal','shot.xg','type.primary','type.secondary','location.x','location.y','team.name','opponentTeam.name','player.id','player.name','pass.accurate','pass.endLocation.x','pass.endLocation.y','pass.recipient.id','pass.recipient.name','possession.id','possession.eventsNumber','possession.eventIndex','possession.types','possession.team.name','possession.attack.xg','carry.progression','carry.endLocation.x','carry.endLocation.y']]

df.to_csv('xT/U19 Ligaen 23 24.csv',index=False)

connection_string = 'SharedAccessSignature=sv=2020-08-04&ss=f&srt=sco&sp=rl&se=2025-01-11T22:47:25Z&st=2022-01-11T14:47:25Z&spr=https&sig=CXdXPlHz%2FhW0IRugFTfCrB7osNQVZJ%2BHjNR1EM2s6RU%3D;FileEndpoint=https://divforeningendataout1.file.core.windows.net/;'
share_name = 'divisionsforeningen-outgoingdata'
dir_path = 'KampData/Sæson 23-24/Superliga/'

service_client = ShareServiceClient.from_connection_string(connection_string)
share_client = service_client.get_share_client(share_name)
directory_client = share_client.get_directory_client(dir_path)

json_files = []

def find_json_files(directory_client):
    for item in directory_client.list_directories_and_files():
        if item.is_directory:
            sub_directory_client = directory_client.get_subdirectory_client(item.name)
            find_json_files(sub_directory_client)
        elif item.name.endswith('.json') and 'MatchEvents' in item.name:
            json_files.append(json.loads(directory_client.get_file_client(item.name).download_file().readall().decode()))

find_json_files(directory_client)

events_list = []

for item in json_files:
    events_list.extend(item['events'])

df = pd.json_normalize(events_list)

json_files = []

def find_json_files(directory_client):
    for item in directory_client.list_directories_and_files():
        if item.is_directory:
            sub_directory_client = directory_client.get_subdirectory_client(item.name)
            find_json_files(sub_directory_client)
        elif item.name.endswith('.json') and 'MatchDetail' in item.name:
            json_files.append(json.loads(directory_client.get_file_client(item.name).download_file().readall().decode()))
            
find_json_files(directory_client)
kampdetaljer = json_normalize(json_files)
kampdetaljer = kampdetaljer[['wyId','label','date']]
kampdetaljer = kampdetaljer.rename(columns={'wyId':'matchId'})
df = kampdetaljer.merge(df)
df = df[['label','date','shot.isGoal','shot.xg','type.primary','type.secondary','location.x','location.y','team.name','opponentTeam.name','player.id','player.name','pass.accurate','pass.endLocation.x','pass.endLocation.y','pass.recipient.id','pass.recipient.name','possession.id','possession.eventsNumber','possession.eventIndex','possession.types','possession.team.name','possession.attack.xg','carry.progression','carry.endLocation.x','carry.endLocation.y']]

df.to_csv('xT/Superliga 23 24.csv',index=False)

connection_string = 'SharedAccessSignature=sv=2020-08-04&ss=f&srt=sco&sp=rl&se=2025-01-11T22:47:25Z&st=2022-01-11T14:47:25Z&spr=https&sig=CXdXPlHz%2FhW0IRugFTfCrB7osNQVZJ%2BHjNR1EM2s6RU%3D;FileEndpoint=https://divforeningendataout1.file.core.windows.net/;'
share_name = 'divisionsforeningen-outgoingdata'
dir_path = 'KampData/Sæson 23-24/1st Division/'

service_client = ShareServiceClient.from_connection_string(connection_string)
share_client = service_client.get_share_client(share_name)
directory_client = share_client.get_directory_client(dir_path)

json_files = []

def find_json_files(directory_client):
    for item in directory_client.list_directories_and_files():
        if item.is_directory:
            sub_directory_client = directory_client.get_subdirectory_client(item.name)
            find_json_files(sub_directory_client)
        elif item.name.endswith('.json') and 'MatchEvents' in item.name:
            json_files.append(json.loads(directory_client.get_file_client(item.name).download_file().readall().decode()))

find_json_files(directory_client)

events_list = []

for item in json_files:
    events_list.extend(item['events'])

df = pd.json_normalize(events_list)

json_files = []

def find_json_files(directory_client):
    for item in directory_client.list_directories_and_files():
        if item.is_directory:
            sub_directory_client = directory_client.get_subdirectory_client(item.name)
            find_json_files(sub_directory_client)
        elif item.name.endswith('.json') and 'MatchDetail' in item.name:
            json_files.append(json.loads(directory_client.get_file_client(item.name).download_file().readall().decode()))
            
find_json_files(directory_client)
kampdetaljer = json_normalize(json_files)
kampdetaljer = kampdetaljer[['wyId','label','date']]
kampdetaljer = kampdetaljer.rename(columns={'wyId':'matchId'})
df = kampdetaljer.merge(df)
df = df[['label','date','shot.isGoal','shot.xg','type.primary','type.secondary','location.x','location.y','team.name','opponentTeam.name','player.id','player.name','pass.accurate','pass.endLocation.x','pass.endLocation.y','pass.recipient.id','pass.recipient.name','possession.id','possession.eventsNumber','possession.eventIndex','possession.types','possession.team.name','possession.attack.xg','carry.progression','carry.endLocation.x','carry.endLocation.y']]

df.to_csv('xT/1st Division 23 24.csv',index=False)

connection_string = 'SharedAccessSignature=sv=2020-08-04&ss=f&srt=sco&sp=rl&se=2025-01-11T22:47:25Z&st=2022-01-11T14:47:25Z&spr=https&sig=CXdXPlHz%2FhW0IRugFTfCrB7osNQVZJ%2BHjNR1EM2s6RU%3D;FileEndpoint=https://divforeningendataout1.file.core.windows.net/;'
share_name = 'divisionsforeningen-outgoingdata'
dir_path = 'KampData/Sæson 23-24/2nd Division/'

service_client = ShareServiceClient.from_connection_string(connection_string)
share_client = service_client.get_share_client(share_name)
directory_client = share_client.get_directory_client(dir_path)

json_files = []

def find_json_files(directory_client):
    for item in directory_client.list_directories_and_files():
        if item.is_directory:
            sub_directory_client = directory_client.get_subdirectory_client(item.name)
            find_json_files(sub_directory_client)
        elif item.name.endswith('.json') and 'MatchEvents' in item.name:
            json_files.append(json.loads(directory_client.get_file_client(item.name).download_file().readall().decode()))

find_json_files(directory_client)

events_list = []

for item in json_files:
    events_list.extend(item['events'])

df = pd.json_normalize(events_list)

json_files = []

def find_json_files(directory_client):
    for item in directory_client.list_directories_and_files():
        if item.is_directory:
            sub_directory_client = directory_client.get_subdirectory_client(item.name)
            find_json_files(sub_directory_client)
        elif item.name.endswith('.json') and 'MatchDetail' in item.name:
            json_files.append(json.loads(directory_client.get_file_client(item.name).download_file().readall().decode()))
            
find_json_files(directory_client)
kampdetaljer = json_normalize(json_files)
kampdetaljer = kampdetaljer[['wyId','label','date']]
kampdetaljer = kampdetaljer.rename(columns={'wyId':'matchId'})
df = kampdetaljer.merge(df)
df = df[['label','date','shot.isGoal','shot.xg','type.primary','type.secondary','location.x','location.y','team.name','opponentTeam.name','player.id','player.name','pass.accurate','pass.endLocation.x','pass.endLocation.y','pass.recipient.id','pass.recipient.name','possession.id','possession.eventsNumber','possession.eventIndex','possession.types','possession.team.name','possession.attack.xg','carry.progression','carry.endLocation.x','carry.endLocation.y']]

df.to_csv('xT/2nd Division 23 24.csv',index=False)

connection_string = 'SharedAccessSignature=sv=2020-08-04&ss=f&srt=sco&sp=rl&se=2025-01-11T22:47:25Z&st=2022-01-11T14:47:25Z&spr=https&sig=CXdXPlHz%2FhW0IRugFTfCrB7osNQVZJ%2BHjNR1EM2s6RU%3D;FileEndpoint=https://divforeningendataout1.file.core.windows.net/;'
share_name = 'divisionsforeningen-outgoingdata'
dir_path = 'KampData/Sæson 23-24/3. Division/'

service_client = ShareServiceClient.from_connection_string(connection_string)
share_client = service_client.get_share_client(share_name)
directory_client = share_client.get_directory_client(dir_path)

json_files = []

def find_json_files(directory_client):
    for item in directory_client.list_directories_and_files():
        if item.is_directory:
            sub_directory_client = directory_client.get_subdirectory_client(item.name)
            find_json_files(sub_directory_client)
        elif item.name.endswith('.json') and 'MatchEvents' in item.name:
            json_files.append(json.loads(directory_client.get_file_client(item.name).download_file().readall().decode()))

find_json_files(directory_client)

events_list = []

for item in json_files:
    events_list.extend(item['events'])

df = pd.json_normalize(events_list)

json_files = []

def find_json_files(directory_client):
    for item in directory_client.list_directories_and_files():
        if item.is_directory:
            sub_directory_client = directory_client.get_subdirectory_client(item.name)
            find_json_files(sub_directory_client)
        elif item.name.endswith('.json') and 'MatchDetail' in item.name:
            json_files.append(json.loads(directory_client.get_file_client(item.name).download_file().readall().decode()))
            
find_json_files(directory_client)
kampdetaljer = json_normalize(json_files)
kampdetaljer = kampdetaljer[['wyId','label','date']]
kampdetaljer = kampdetaljer.rename(columns={'wyId':'matchId'})
df = kampdetaljer.merge(df)
df = df[['label','date','shot.isGoal','shot.xg','type.primary','type.secondary','location.x','location.y','team.name','opponentTeam.name','player.id','player.name','pass.accurate','pass.endLocation.x','pass.endLocation.y','pass.recipient.id','pass.recipient.name','possession.id','possession.eventsNumber','possession.eventIndex','possession.types','possession.team.name','possession.attack.xg','carry.progression','carry.endLocation.x','carry.endLocation.y']]

df.to_csv('xT/3. Division 23 24.csv',index=False)

connection_string = 'SharedAccessSignature=sv=2020-08-04&ss=f&srt=sco&sp=rl&se=2025-01-11T22:47:25Z&st=2022-01-11T14:47:25Z&spr=https&sig=CXdXPlHz%2FhW0IRugFTfCrB7osNQVZJ%2BHjNR1EM2s6RU%3D;FileEndpoint=https://divforeningendataout1.file.core.windows.net/;'
share_name = 'divisionsforeningen-outgoingdata'
dir_path = 'KampData/Sæson 23-24/U17 Division/'

service_client = ShareServiceClient.from_connection_string(connection_string)
share_client = service_client.get_share_client(share_name)
directory_client = share_client.get_directory_client(dir_path)

json_files = []

def find_json_files(directory_client):
    for item in directory_client.list_directories_and_files():
        if item.is_directory:
            sub_directory_client = directory_client.get_subdirectory_client(item.name)
            find_json_files(sub_directory_client)
        elif item.name.endswith('.json') and 'MatchEvents' in item.name:
            json_files.append(json.loads(directory_client.get_file_client(item.name).download_file().readall().decode()))

find_json_files(directory_client)

events_list = []

for item in json_files:
    events_list.extend(item['events'])

df = pd.json_normalize(events_list)

json_files = []

def find_json_files(directory_client):
    for item in directory_client.list_directories_and_files():
        if item.is_directory:
            sub_directory_client = directory_client.get_subdirectory_client(item.name)
            find_json_files(sub_directory_client)
        elif item.name.endswith('.json') and 'MatchDetail' in item.name:
            json_files.append(json.loads(directory_client.get_file_client(item.name).download_file().readall().decode()))
            
find_json_files(directory_client)
kampdetaljer = json_normalize(json_files)
kampdetaljer = kampdetaljer[['wyId','label','date']]
kampdetaljer = kampdetaljer.rename(columns={'wyId':'matchId'})
df = kampdetaljer.merge(df)
df = df[['label','date','shot.isGoal','shot.xg','type.primary','type.secondary','location.x','location.y','team.name','opponentTeam.name','player.id','player.name','pass.accurate','pass.endLocation.x','pass.endLocation.y','pass.recipient.id','pass.recipient.name','possession.id','possession.eventsNumber','possession.eventIndex','possession.types','possession.team.name','possession.attack.xg','carry.progression','carry.endLocation.x','carry.endLocation.y']]

df.to_csv('xT/U17 Division 23 24.csv',index=False)

connection_string = 'SharedAccessSignature=sv=2020-08-04&ss=f&srt=sco&sp=rl&se=2025-01-11T22:47:25Z&st=2022-01-11T14:47:25Z&spr=https&sig=CXdXPlHz%2FhW0IRugFTfCrB7osNQVZJ%2BHjNR1EM2s6RU%3D;FileEndpoint=https://divforeningendataout1.file.core.windows.net/;'
share_name = 'divisionsforeningen-outgoingdata'
dir_path = 'KampData/Sæson 23-24/U19 Division/'

service_client = ShareServiceClient.from_connection_string(connection_string)
share_client = service_client.get_share_client(share_name)
directory_client = share_client.get_directory_client(dir_path)

json_files = []

def find_json_files(directory_client):
    for item in directory_client.list_directories_and_files():
        if item.is_directory:
            sub_directory_client = directory_client.get_subdirectory_client(item.name)
            find_json_files(sub_directory_client)
        elif item.name.endswith('.json') and 'MatchEvents' in item.name:
            json_files.append(json.loads(directory_client.get_file_client(item.name).download_file().readall().decode()))

find_json_files(directory_client)

events_list = []

for item in json_files:
    events_list.extend(item['events'])

df = pd.json_normalize(events_list)

json_files = []

def find_json_files(directory_client):
    for item in directory_client.list_directories_and_files():
        if item.is_directory:
            sub_directory_client = directory_client.get_subdirectory_client(item.name)
            find_json_files(sub_directory_client)
        elif item.name.endswith('.json') and 'MatchDetail' in item.name:
            json_files.append(json.loads(directory_client.get_file_client(item.name).download_file().readall().decode()))
            
find_json_files(directory_client)
kampdetaljer = json_normalize(json_files)
kampdetaljer = kampdetaljer[['wyId','label','date']]
kampdetaljer = kampdetaljer.rename(columns={'wyId':'matchId'})
df = kampdetaljer.merge(df)
df = df[['label','date','shot.isGoal','shot.xg','type.primary','type.secondary','location.x','location.y','team.name','opponentTeam.name','player.id','player.name','pass.accurate','pass.endLocation.x','pass.endLocation.y','pass.recipient.id','pass.recipient.name','possession.id','possession.eventsNumber','possession.eventIndex','possession.types','possession.team.name','possession.attack.xg','carry.progression','carry.endLocation.x','carry.endLocation.y']]

df.to_csv('xT/U19 Division 23 24.csv',index=False)
