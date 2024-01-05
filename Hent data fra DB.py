#hent GPS data
import pandas as pd
import streamlit as st
import seaborn as sns
import os
import glob
import matplotlib.pyplot as plt
import openpyxl as xlsxwriter
from pandas import DataFrame
from dateutil import parser
os.chdir(r'C:\Users\SéamusPeareBartholdy\OneDrive - AC Horsens A S\Akademi\Excel Organisering og indhold af træning framework\GPS udtræk')
extension = 'csv'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames])
df = pd.DataFrame(combined_csv)
df = df.dropna()
print ('GPS csv filer kombineret')
df2 = pd.read_excel(r'C:\Users\SéamusPeareBartholdy\Documents\GitHub\ACH\Fysisk data\GPS spillere.xlsx')
dforiginal = df.merge(df2)
os.chdir(r'C:\Users\SéamusPeareBartholdy\Documents\GitHub\ACH')
dforiginal.to_excel(r'Fysisk data\samlet gps data.xlsx', index=False)
dforiginal = pd.read_excel(r'Fysisk data/samlet gps data.xlsx')
writer = pd.ExcelWriter(r'Fysisk data/samlet gps data.xlsx', engine='xlsxwriter')
dforiginal.to_excel(writer,sheet_name='Sheet1', index=None, header=True)


workbook  = writer.book
worksheet = writer.sheets['Sheet1']

formatdict = {'num_format':'dd-mm-yyyy'}
fmt = workbook.add_format(formatdict)
worksheet.set_column('A:A', None, fmt)

formatdict = {'num_format':'hh:mm:ss'}
fmt = workbook.add_format(formatdict)
worksheet.set_column('F:G', None, fmt)

writer.close()
dforiginal = pd.read_excel(r'Fysisk data/samlet gps data.xlsx',decimal=',')
Ugenummer = dforiginal['Date'].apply(lambda x: x.isocalendar()[1])
dforiginal.insert(loc = 48, column = 'Ugenummer', value= Ugenummer)
dforiginal.to_csv(r'Fysisk data/samlet gps data.csv', index=False)
os.remove(r'Fysisk data/samlet gps data.xlsx')
print('GPS færdig')

#Hent eventdata
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


from azure.storage.fileshare import ShareServiceClient
import json
import pandas as pd
from pandas import json_normalize
import numpy as np
import os
import streamlit as st
connection_string = 'SharedAccessSignature=sv=2020-08-04&ss=f&srt=sco&sp=rl&se=2025-01-11T22:47:25Z&st=2022-01-11T14:47:25Z&spr=https&sig=CXdXPlHz%2FhW0IRugFTfCrB7osNQVZJ%2BHjNR1EM2s6RU%3D;FileEndpoint=https://divforeningendataout1.file.core.windows.net/;'
share_name = 'divisionsforeningen-outgoingdata'
dir_path = 'KampData/Sæson 22-23/U15 Ligaen/'


service_client = ShareServiceClient.from_connection_string(connection_string)
share_client = service_client.get_share_client(share_name)
directory_client = share_client.get_directory_client(dir_path)

json_files = []

def find_json_files(directory_client):
    for item in directory_client.list_directories_and_files():
        if item.is_directory:
            if 'AC Horsens' in item.name:
                # Recursively search for JSON files in the subdirectory if it contains 'AC Horsens' in its name
                sub_directory_client = directory_client.get_subdirectory_client(item.name)
                find_json_files(sub_directory_client)
            else:
                # Otherwise, continue searching in the current directory
                find_json_files(directory_client.get_subdirectory_client(item.name))
        elif item.name.endswith('.json') and 'MatchAdvanceStats' in item.name:
            # If the item is a JSON file with 'MatchAdvanceStats' in the name, download it and append its data to the list
            json_files.append(json.loads(directory_client.get_file_client(item.name).download_file().readall().decode()))
find_json_files(directory_client)
df = pd.json_normalize(json_files)
df = pd.DataFrame(df)
df.columns = df.columns.str.replace('66870','Horsens U15 sidste sæson')
df.columns = df.columns.str.replace('65133','Esbjerg U15')
df.columns = df.columns.str.replace('65132','København U15')
df.columns = df.columns.str.replace('65130','Silkeborg IF U15')
df.columns = df.columns.str.replace('65129','SønderjyskE U15')
df.columns = df.columns.str.replace('65128','AaB U15')
df.columns = df.columns.str.replace('65127','OB U15')
df.columns = df.columns.str.replace('65126','Vejle U15')
df.columns = df.columns.str.replace('65125','Randers U15')
df.columns = df.columns.str.replace('65124','FC Nordsjælland U15')
df.columns = df.columns.str.replace('65122','Midtjylland U15')
df.columns = df.columns.str.replace('65121','AGF U15')
df.columns = df.columns.str.replace('64359','Lyngby U15')
df.columns = df.columns.str.replace('22392','Brøndby U15')
#df.columns = df.columns.str.replace('general.','')
#possession_cols = [col for col in df.columns if col.startswith('possession')]
#df.columns = df.columns.where(~df.columns.str.startswith('possession.'), df.columns.str.replace('possession.', ''))
#df.columns = df.columns.str.replace('openplay.','')
#df.columns = df.columns.str.replace('attacks.','')
#df.columns = df.columns.str.replace('transitions.','')
#df.columns = df.columns.str.replace('passes.','')
#df.columns = df.columns.str.replace('defence.','')
#df.columns = df.columns.str.replace('duels.','')
#df.columns = df.columns.str.replace('flanks.','')


json_files = []

def find_json_files(directory_client):
    for item in directory_client.list_directories_and_files():
        if item.is_directory:
            if 'AC Horsens' in item.name:
                # Recursively search for JSON files in the subdirectory if it contains 'AC Horsens' in its name
                sub_directory_client = directory_client.get_subdirectory_client(item.name)
                find_json_files(sub_directory_client)
            else:
                # Otherwise, continue searching in the current directory
                find_json_files(directory_client.get_subdirectory_client(item.name))
        elif item.name.endswith('.json') and 'MatchDetail' in item.name:
            # If the item is a JSON file with 'MatchEvents' in the name, download it and append its data to the list
            json_files.append(json.loads(directory_client.get_file_client(item.name).download_file().readall().decode()))
find_json_files(directory_client)
kampdetaljer = json_normalize(json_files)
kampdetaljer = kampdetaljer[['wyId','label','date']]
kampdetaljer = kampdetaljer.rename(columns={'wyId':'matchId'})

dfegnekampe = kampdetaljer.merge(df)
dfegnekampe['label'] = dfegnekampe['label'].astype(str)
dfegnekampe = dfegnekampe[dfegnekampe['label'].str.contains('Horsens')]
dfegnekampe.to_csv(r'Teamsheet alle kampe U15 sidste sæson.csv',index=False)
print('U15 data til teamsheet hentet')
from azure.storage.fileshare import ShareServiceClient
import json
import pandas as pd
from pandas import json_normalize
import numpy as np
import os
import streamlit as st
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
            if 'AC Horsens' in item.name:
                # Recursively search for JSON files in the subdirectory if it contains 'AC Horsens' in its name
                sub_directory_client = directory_client.get_subdirectory_client(item.name)
                find_json_files(sub_directory_client)
            else:
                # Otherwise, continue searching in the current directory
                find_json_files(directory_client.get_subdirectory_client(item.name))
        elif item.name.endswith('.json') and 'MatchAdvanceStats' in item.name:
            # If the item is a JSON file with 'MatchAdvanceStats' in the name, download it and append its data to the list
            json_files.append(json.loads(directory_client.get_file_client(item.name).download_file().readall().decode()))
find_json_files(directory_client)
df = pd.json_normalize(json_files)
df = pd.DataFrame(df)
df.columns = df.columns.str.replace('66870','Horsens U15')
df.columns = df.columns.str.replace('65133','Esbjerg U15')
df.columns = df.columns.str.replace('65132','København U15')
df.columns = df.columns.str.replace('65130','Silkeborg IF U15')
df.columns = df.columns.str.replace('65129','SønderjyskE U15')
df.columns = df.columns.str.replace('65128','AaB U15')
df.columns = df.columns.str.replace('65127','OB U15')
df.columns = df.columns.str.replace('65126','Vejle U15')
df.columns = df.columns.str.replace('65125','Randers U15')
df.columns = df.columns.str.replace('65124','FC Nordsjælland U15')
df.columns = df.columns.str.replace('65122','Midtjylland U15')
df.columns = df.columns.str.replace('65121','AGF U15')
df.columns = df.columns.str.replace('64359','Lyngby U15')
df.columns = df.columns.str.replace('22392','Brøndby U15')
#df.columns = df.columns.str.replace('general.','')
#possession_cols = [col for col in df.columns if col.startswith('possession')]
#df.columns = df.columns.where(~df.columns.str.startswith('possession.'), df.columns.str.replace('possession.', ''))
#df.columns = df.columns.str.replace('openplay.','')
#df.columns = df.columns.str.replace('attacks.','')
#df.columns = df.columns.str.replace('transitions.','')
#df.columns = df.columns.str.replace('passes.','')
#df.columns = df.columns.str.replace('defence.','')
#df.columns = df.columns.str.replace('duels.','')
#df.columns = df.columns.str.replace('flanks.','')


json_files = []

def find_json_files(directory_client):
    for item in directory_client.list_directories_and_files():
        if item.is_directory:
            if 'AC Horsens' in item.name:
                # Recursively search for JSON files in the subdirectory if it contains 'AC Horsens' in its name
                sub_directory_client = directory_client.get_subdirectory_client(item.name)
                find_json_files(sub_directory_client)
            else:
                # Otherwise, continue searching in the current directory
                find_json_files(directory_client.get_subdirectory_client(item.name))
        elif item.name.endswith('.json') and 'MatchDetail' in item.name:
            # If the item is a JSON file with 'MatchEvents' in the name, download it and append its data to the list
            json_files.append(json.loads(directory_client.get_file_client(item.name).download_file().readall().decode()))
find_json_files(directory_client)
kampdetaljer = json_normalize(json_files)
kampdetaljer = kampdetaljer[['wyId','label','date']]
kampdetaljer = kampdetaljer.rename(columns={'wyId':'matchId'})

dfegnekampe = kampdetaljer.merge(df)
dfegnekampe['label'] = dfegnekampe['label'].astype(str)
#dfegnekampe = dfegnekampe[dfegnekampe['label'].str.contains('Horsens')]
dfegnekampe.to_csv(r'Teamsheet alle kampe U15.csv',index=False)
print('U15 data til benchmark hentet')
from azure.storage.fileshare import ShareServiceClient
import json
import pandas as pd
from pandas import json_normalize
import numpy as np
import os
import streamlit as st
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
            if 'AC Horsens' in item.name:
                # Recursively search for JSON files in the subdirectory if it contains 'AC Horsens' in its name
                sub_directory_client = directory_client.get_subdirectory_client(item.name)
                find_json_files(sub_directory_client)
            else:
                # Otherwise, continue searching in the current directory
                find_json_files(directory_client.get_subdirectory_client(item.name))
        elif item.name.endswith('.json') and 'MatchAdvanceStats' in item.name:
            # If the item is a JSON file with 'MatchAdvanceStats' in the name, download it and append its data to the list
            json_files.append(json.loads(directory_client.get_file_client(item.name).download_file().readall().decode()))
find_json_files(directory_client)
df = pd.json_normalize(json_files)
df = pd.DataFrame(df)
df.columns = df.columns.str.replace('66870','Horsens U15')
df.columns = df.columns.str.replace('65133','Esbjerg U15')
df.columns = df.columns.str.replace('65132','København U15')
df.columns = df.columns.str.replace('65130','Silkeborg IF U15')
df.columns = df.columns.str.replace('65129','SønderjyskE U15')
df.columns = df.columns.str.replace('65128','AaB U15')
df.columns = df.columns.str.replace('65127','OB U15')
df.columns = df.columns.str.replace('65126','Vejle U15')
df.columns = df.columns.str.replace('65125','Randers U15')
df.columns = df.columns.str.replace('65124','FC Nordsjælland U15')
df.columns = df.columns.str.replace('65122','Midtjylland U15')
df.columns = df.columns.str.replace('65121','AGF U15')
df.columns = df.columns.str.replace('64359','Lyngby U15')
df.columns = df.columns.str.replace('22392','Brøndby U15')
#df.columns = df.columns.str.replace('general.','')
#possession_cols = [col for col in df.columns if col.startswith('possession')]
#df.columns = df.columns.where(~df.columns.str.startswith('possession.'), df.columns.str.replace('possession.', ''))
#df.columns = df.columns.str.replace('openplay.','')
#df.columns = df.columns.str.replace('attacks.','')
#df.columns = df.columns.str.replace('transitions.','')
#df.columns = df.columns.str.replace('passes.','')
#df.columns = df.columns.str.replace('defence.','')
#df.columns = df.columns.str.replace('duels.','')
#df.columns = df.columns.str.replace('flanks.','')


json_files = []

def find_json_files(directory_client):
    for item in directory_client.list_directories_and_files():
        if item.is_directory:
            if 'AC Horsens' in item.name:
                # Recursively search for JSON files in the subdirectory if it contains 'AC Horsens' in its name
                sub_directory_client = directory_client.get_subdirectory_client(item.name)
                find_json_files(sub_directory_client)
            else:
                # Otherwise, continue searching in the current directory
                find_json_files(directory_client.get_subdirectory_client(item.name))
        elif item.name.endswith('.json') and 'MatchDetail' in item.name:
            # If the item is a JSON file with 'MatchEvents' in the name, download it and append its data to the list
            json_files.append(json.loads(directory_client.get_file_client(item.name).download_file().readall().decode()))
find_json_files(directory_client)
kampdetaljer = json_normalize(json_files)
kampdetaljer = kampdetaljer[['wyId','label','date']]
kampdetaljer = kampdetaljer.rename(columns={'wyId':'matchId'})

dfegnekampe = kampdetaljer.merge(df)
dfegnekampe['label'] = dfegnekampe['label'].astype(str)
dfegnekampe = dfegnekampe[dfegnekampe['label'].str.contains('Horsens')]
dfegnekampe['date'] = dfegnekampe['date'].astype(str)
dfegnekampe['date'] = dfegnekampe['date'].apply(lambda x: parser.parse(x))

# Sort the dataframe by the 'date' column
dfegnekampe = dfegnekampe.sort_values(by='date',ascending=False)

# Format the 'date' column to day-month-year format
dfegnekampe['date'] = dfegnekampe['date'].apply(lambda x: x.strftime('%d-%m-%Y'))
dfegnekampe.to_csv(r'Teamsheet egne kampe U15.csv',index=False)
print('Alt data hentet til teamsheet')

#Start på U17
connection_string = 'SharedAccessSignature=sv=2020-08-04&ss=f&srt=sco&sp=rl&se=2025-01-11T22:47:25Z&st=2022-01-11T14:47:25Z&spr=https&sig=CXdXPlHz%2FhW0IRugFTfCrB7osNQVZJ%2BHjNR1EM2s6RU%3D;FileEndpoint=https://divforeningendataout1.file.core.windows.net/;'
share_name = 'divisionsforeningen-outgoingdata'
dir_path = 'KampData/Sæson 22-23/U17 Ligaen/'


service_client = ShareServiceClient.from_connection_string(connection_string)
share_client = service_client.get_share_client(share_name)
directory_client = share_client.get_directory_client(dir_path)

json_files = []

def find_json_files(directory_client):
    for item in directory_client.list_directories_and_files():
        if item.is_directory:
            if 'AC Horsens' in item.name:
                # Recursively search for JSON files in the subdirectory if it contains 'AC Horsens' in its name
                sub_directory_client = directory_client.get_subdirectory_client(item.name)
                find_json_files(sub_directory_client)
            else:
                # Otherwise, continue searching in the current directory
                find_json_files(directory_client.get_subdirectory_client(item.name))
        elif item.name.endswith('.json') and 'MatchAdvanceStats' in item.name:
            # If the item is a JSON file with 'MatchAdvanceStats' in the name, download it and append its data to the list
            json_files.append(json.loads(directory_client.get_file_client(item.name).download_file().readall().decode()))
find_json_files(directory_client)
df = pd.json_normalize(json_files)
df = pd.DataFrame(df)
df.columns = df.columns.str.replace('30685','Horsens U17 sidste sæson')
df.columns = df.columns.str.replace('27148','Esbjerg U17')
df.columns = df.columns.str.replace('27144','København U17')
df.columns = df.columns.str.replace('27147','Silkeborg U17')
df.columns = df.columns.str.replace('62977','SønderjyskE U17')
df.columns = df.columns.str.replace('27142','AaB U17')
df.columns = df.columns.str.replace('27143','OB U17')
df.columns = df.columns.str.replace('27141','Vejle U17')
df.columns = df.columns.str.replace('27140','Randers U17')
df.columns = df.columns.str.replace('27149','FC Nordsjælland U17')
df.columns = df.columns.str.replace('27139','Midtjylland U17')
df.columns = df.columns.str.replace('27145','AGF U17')
df.columns = df.columns.str.replace('27152','Lyngby U17')
df.columns = df.columns.str.replace('27146','Brøndby U17')
#df.columns = df.columns.str.replace('general.','')
#possession_cols = [col for col in df.columns if col.startswith('possession')]
#df.columns = df.columns.where(~df.columns.str.startswith('possession.'), df.columns.str.replace('possession.', ''))
#df.columns = df.columns.str.replace('openplay.','')
#df.columns = df.columns.str.replace('attacks.','')
#df.columns = df.columns.str.replace('transitions.','')
#df.columns = df.columns.str.replace('passes.','')
#df.columns = df.columns.str.replace('defence.','')
#df.columns = df.columns.str.replace('duels.','')
#df.columns = df.columns.str.replace('flanks.','')


json_files = []

def find_json_files(directory_client):
    for item in directory_client.list_directories_and_files():
        if item.is_directory:
            if 'AC Horsens' in item.name:
                # Recursively search for JSON files in the subdirectory if it contains 'AC Horsens' in its name
                sub_directory_client = directory_client.get_subdirectory_client(item.name)
                find_json_files(sub_directory_client)
            else:
                # Otherwise, continue searching in the current directory
                find_json_files(directory_client.get_subdirectory_client(item.name))
        elif item.name.endswith('.json') and 'MatchDetail' in item.name:
            # If the item is a JSON file with 'MatchEvents' in the name, download it and append its data to the list
            json_files.append(json.loads(directory_client.get_file_client(item.name).download_file().readall().decode()))
find_json_files(directory_client)
kampdetaljer = json_normalize(json_files)
kampdetaljer = kampdetaljer[['wyId','label','date']]
kampdetaljer = kampdetaljer.rename(columns={'wyId':'matchId'})

dfegnekampe = kampdetaljer.merge(df)
dfegnekampe['label'] = dfegnekampe['label'].astype(str)
dfegnekampe = dfegnekampe[dfegnekampe['label'].str.contains('Horsens')]
dfegnekampe.to_csv(r'Teamsheet alle kampe U17 sidste sæson.csv',index=False)
print('U17 kampe seneste sæson hentet til teamsheet')

from azure.storage.fileshare import ShareServiceClient
import json
import pandas as pd
from pandas import json_normalize
import numpy as np
import os
import streamlit as st
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
            if 'AC Horsens' in item.name:
                # Recursively search for JSON files in the subdirectory if it contains 'AC Horsens' in its name
                sub_directory_client = directory_client.get_subdirectory_client(item.name)
                find_json_files(sub_directory_client)
            else:
                # Otherwise, continue searching in the current directory
                find_json_files(directory_client.get_subdirectory_client(item.name))
        elif item.name.endswith('.json') and 'MatchAdvanceStats' in item.name:
            # If the item is a JSON file with 'MatchAdvanceStats' in the name, download it and append its data to the list
            json_files.append(json.loads(directory_client.get_file_client(item.name).download_file().readall().decode()))
find_json_files(directory_client)
df = pd.json_normalize(json_files)
df = pd.DataFrame(df)
df.columns = df.columns.str.replace('30685','Horsens U17')
df.columns = df.columns.str.replace('27148','Esbjerg U17')
df.columns = df.columns.str.replace('27144','København U17')
df.columns = df.columns.str.replace('27147','Silkeborg U17')
df.columns = df.columns.str.replace('62977','SønderjyskE U17')
df.columns = df.columns.str.replace('27142','AaB U17')
df.columns = df.columns.str.replace('27143','OB U17')
df.columns = df.columns.str.replace('27141','Vejle U17')
df.columns = df.columns.str.replace('27140','Randers U17')
df.columns = df.columns.str.replace('27149','FC Nordsjælland U17')
df.columns = df.columns.str.replace('27139','Midtjylland U17')
df.columns = df.columns.str.replace('27145','AGF U17')
df.columns = df.columns.str.replace('27152','Lyngby U17')
df.columns = df.columns.str.replace('27146','Brøndby U17')
#df.columns = df.columns.str.replace('general.','')
#possession_cols = [col for col in df.columns if col.startswith('possession')]
#df.columns = df.columns.where(~df.columns.str.startswith('possession.'), df.columns.str.replace('possession.', ''))
#df.columns = df.columns.str.replace('openplay.','')
#df.columns = df.columns.str.replace('attacks.','')
#df.columns = df.columns.str.replace('transitions.','')
#df.columns = df.columns.str.replace('passes.','')
#df.columns = df.columns.str.replace('defence.','')
#df.columns = df.columns.str.replace('duels.','')
#df.columns = df.columns.str.replace('flanks.','')


json_files = []

def find_json_files(directory_client):
    for item in directory_client.list_directories_and_files():
        if item.is_directory:
            if 'AC Horsens' in item.name:
                # Recursively search for JSON files in the subdirectory if it contains 'AC Horsens' in its name
                sub_directory_client = directory_client.get_subdirectory_client(item.name)
                find_json_files(sub_directory_client)
            else:
                # Otherwise, continue searching in the current directory
                find_json_files(directory_client.get_subdirectory_client(item.name))
        elif item.name.endswith('.json') and 'MatchDetail' in item.name:
            # If the item is a JSON file with 'MatchEvents' in the name, download it and append its data to the list
            json_files.append(json.loads(directory_client.get_file_client(item.name).download_file().readall().decode()))
find_json_files(directory_client)
kampdetaljer = json_normalize(json_files)
kampdetaljer = kampdetaljer[['wyId','label','date']]
kampdetaljer = kampdetaljer.rename(columns={'wyId':'matchId'})

dfegnekampe = kampdetaljer.merge(df)
dfegnekampe['label'] = dfegnekampe['label'].astype(str)
#dfegnekampe = dfegnekampe[dfegnekampe['label'].str.contains('Horsens')]
dfegnekampe.to_csv(r'Teamsheet alle kampe U17.csv',index=False)
print('Alle U17 kampe hentet til teamsheet')
from azure.storage.fileshare import ShareServiceClient
import json
import pandas as pd
from pandas import json_normalize
import numpy as np
import os
import streamlit as st
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
            if 'AC Horsens' in item.name:
                # Recursively search for JSON files in the subdirectory if it contains 'AC Horsens' in its name
                sub_directory_client = directory_client.get_subdirectory_client(item.name)
                find_json_files(sub_directory_client)
            else:
                # Otherwise, continue searching in the current directory
                find_json_files(directory_client.get_subdirectory_client(item.name))
        elif item.name.endswith('.json') and 'MatchAdvanceStats' in item.name:
            # If the item is a JSON file with 'MatchAdvanceStats' in the name, download it and append its data to the list
            json_files.append(json.loads(directory_client.get_file_client(item.name).download_file().readall().decode()))
find_json_files(directory_client)
df = pd.json_normalize(json_files)
df = pd.DataFrame(df)
df.columns = df.columns.str.replace('30685','Horsens U17')
df.columns = df.columns.str.replace('27148','Esbjerg U17')
df.columns = df.columns.str.replace('27144','København U17')
df.columns = df.columns.str.replace('27147','Silkeborg U17')
df.columns = df.columns.str.replace('62977','SønderjyskE U17')
df.columns = df.columns.str.replace('27142','AaB U17')
df.columns = df.columns.str.replace('27143','OB U17')
df.columns = df.columns.str.replace('27141','Vejle U17')
df.columns = df.columns.str.replace('27140','Randers U17')
df.columns = df.columns.str.replace('27149','FC Nordsjælland U17')
df.columns = df.columns.str.replace('27139','Midtjylland U17')
df.columns = df.columns.str.replace('27145','AGF U17')
df.columns = df.columns.str.replace('27152','Lyngby U17')
df.columns = df.columns.str.replace('27146','Brøndby U17')
#df.columns = df.columns.str.replace('general.','')
#possession_cols = [col for col in df.columns if col.startswith('possession')]
#df.columns = df.columns.where(~df.columns.str.startswith('possession.'), df.columns.str.replace('possession.', ''))
#df.columns = df.columns.str.replace('openplay.','')
#df.columns = df.columns.str.replace('attacks.','')
#df.columns = df.columns.str.replace('transitions.','')
#df.columns = df.columns.str.replace('passes.','')
#df.columns = df.columns.str.replace('defence.','')
#df.columns = df.columns.str.replace('duels.','')
#df.columns = df.columns.str.replace('flanks.','')


json_files = []

def find_json_files(directory_client):
    for item in directory_client.list_directories_and_files():
        if item.is_directory:
            if 'AC Horsens' in item.name:
                # Recursively search for JSON files in the subdirectory if it contains 'AC Horsens' in its name
                sub_directory_client = directory_client.get_subdirectory_client(item.name)
                find_json_files(sub_directory_client)
            else:
                # Otherwise, continue searching in the current directory
                find_json_files(directory_client.get_subdirectory_client(item.name))
        elif item.name.endswith('.json') and 'MatchDetail' in item.name:
            # If the item is a JSON file with 'MatchEvents' in the name, download it and append its data to the list
            json_files.append(json.loads(directory_client.get_file_client(item.name).download_file().readall().decode()))
find_json_files(directory_client)
kampdetaljer = json_normalize(json_files)
kampdetaljer = kampdetaljer[['wyId','label','date']]
kampdetaljer = kampdetaljer.rename(columns={'wyId':'matchId'})

dfegnekampe = kampdetaljer.merge(df)
dfegnekampe['label'] = dfegnekampe['label'].astype(str)
dfegnekampe = dfegnekampe[dfegnekampe['label'].str.contains('Horsens')]
dfegnekampe['date'] = dfegnekampe['date'].astype(str)
dfegnekampe['date'] = dfegnekampe['date'].apply(lambda x: parser.parse(x))

# Sort the dataframe by the 'date' column
dfegnekampe = dfegnekampe.sort_values(by='date',ascending=False)

# Format the 'date' column to day-month-year format
dfegnekampe['date'] = dfegnekampe['date'].apply(lambda x: x.strftime('%d-%m-%Y'))

dfegnekampe.to_csv(r'Teamsheet egne kampe U17.csv',index=False)


#Start på U19
connection_string = 'SharedAccessSignature=sv=2020-08-04&ss=f&srt=sco&sp=rl&se=2025-01-11T22:47:25Z&st=2022-01-11T14:47:25Z&spr=https&sig=CXdXPlHz%2FhW0IRugFTfCrB7osNQVZJ%2BHjNR1EM2s6RU%3D;FileEndpoint=https://divforeningendataout1.file.core.windows.net/;'
share_name = 'divisionsforeningen-outgoingdata'
dir_path = 'KampData/Sæson 22-23/U19 Ligaen/'


service_client = ShareServiceClient.from_connection_string(connection_string)
share_client = service_client.get_share_client(share_name)
directory_client = share_client.get_directory_client(dir_path)

json_files = []

def find_json_files(directory_client):
    for item in directory_client.list_directories_and_files():
        if item.is_directory:
            if 'AC Horsens' in item.name:
                # Recursively search for JSON files in the subdirectory if it contains 'AC Horsens' in its name
                sub_directory_client = directory_client.get_subdirectory_client(item.name)
                find_json_files(sub_directory_client)
            else:
                # Otherwise, continue searching in the current directory
                find_json_files(directory_client.get_subdirectory_client(item.name))
        elif item.name.endswith('.json') and 'MatchAdvanceStats' in item.name:
            # If the item is a JSON file with 'MatchAdvanceStats' in the name, download it and append its data to the list
            json_files.append(json.loads(directory_client.get_file_client(item.name).download_file().readall().decode()))
find_json_files(directory_client)
df = pd.json_normalize(json_files)
df = pd.DataFrame(df)
df.columns = df.columns.str.replace('38324','Horsens U19 sidste sæson')
df.columns = df.columns.str.replace('23735','Esbjerg U19')
df.columns = df.columns.str.replace('23732','København U19')
df.columns = df.columns.str.replace('23736','Silkeborg U19')
df.columns = df.columns.str.replace('23738','SønderjyskE U19')
df.columns = df.columns.str.replace('23730','AaB U19')
df.columns = df.columns.str.replace('23726','OB U19')
df.columns = df.columns.str.replace('23733','Vejle U19')
df.columns = df.columns.str.replace('23737','Randers U19')
df.columns = df.columns.str.replace('23727','FC Nordsjælland U19')
df.columns = df.columns.str.replace('23729','Midtjylland U19')
df.columns = df.columns.str.replace('25612','AGF U19')
df.columns = df.columns.str.replace('23731','Lyngby U19')
df.columns = df.columns.str.replace('23734','Brøndby IF U19')
#df.columns = df.columns.str.replace('general.','')
#possession_cols = [col for col in df.columns if col.startswith('possession')]
#df.columns = df.columns.where(~df.columns.str.startswith('possession.'), df.columns.str.replace('possession.', ''))
#df.columns = df.columns.str.replace('openplay.','')
#df.columns = df.columns.str.replace('attacks.','')
#df.columns = df.columns.str.replace('transitions.','')
#df.columns = df.columns.str.replace('passes.','')
#df.columns = df.columns.str.replace('defence.','')
#df.columns = df.columns.str.replace('duels.','')
#df.columns = df.columns.str.replace('flanks.','')


json_files = []

def find_json_files(directory_client):
    for item in directory_client.list_directories_and_files():
        if item.is_directory:
            if 'AC Horsens' in item.name:
                # Recursively search for JSON files in the subdirectory if it contains 'AC Horsens' in its name
                sub_directory_client = directory_client.get_subdirectory_client(item.name)
                find_json_files(sub_directory_client)
            else:
                # Otherwise, continue searching in the current directory
                find_json_files(directory_client.get_subdirectory_client(item.name))
        elif item.name.endswith('.json') and 'MatchDetail' in item.name:
            # If the item is a JSON file with 'MatchEvents' in the name, download it and append its data to the list
            json_files.append(json.loads(directory_client.get_file_client(item.name).download_file().readall().decode()))
find_json_files(directory_client)
kampdetaljer = json_normalize(json_files)
kampdetaljer = kampdetaljer[['wyId','label','date']]
kampdetaljer = kampdetaljer.rename(columns={'wyId':'matchId'})

dfegnekampe = kampdetaljer.merge(df)
dfegnekampe['label'] = dfegnekampe['label'].astype(str)
dfegnekampe = dfegnekampe[dfegnekampe['label'].str.contains('Horsens')]
dfegnekampe.to_csv(r'Teamsheet alle kampe U19 sidste sæson.csv',index=False)
print('U19 data hentet til teamsheet')
from azure.storage.fileshare import ShareServiceClient
import json
import pandas as pd
from pandas import json_normalize
import numpy as np
import os
import streamlit as st
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
            if 'AC Horsens' in item.name:
                # Recursively search for JSON files in the subdirectory if it contains 'AC Horsens' in its name
                sub_directory_client = directory_client.get_subdirectory_client(item.name)
                find_json_files(sub_directory_client)
            else:
                # Otherwise, continue searching in the current directory
                find_json_files(directory_client.get_subdirectory_client(item.name))
        elif item.name.endswith('.json') and 'MatchAdvanceStats' in item.name:
            # If the item is a JSON file with 'MatchAdvanceStats' in the name, download it and append its data to the list
            json_files.append(json.loads(directory_client.get_file_client(item.name).download_file().readall().decode()))
find_json_files(directory_client)
df = pd.json_normalize(json_files)
df = pd.DataFrame(df)
df.columns = df.columns.str.replace('38324','Horsens U19')
df.columns = df.columns.str.replace('23735','Esbjerg U19')
df.columns = df.columns.str.replace('23732','København U19')
df.columns = df.columns.str.replace('23736','Silkeborg U19')
df.columns = df.columns.str.replace('23738','SønderjyskE U19')
df.columns = df.columns.str.replace('23730','AaB U19')
df.columns = df.columns.str.replace('23726','OB U19')
df.columns = df.columns.str.replace('23733','Vejle U19')
df.columns = df.columns.str.replace('23737','Randers U19')
df.columns = df.columns.str.replace('23727','FC Nordsjælland U19')
df.columns = df.columns.str.replace('23729','Midtjylland U19')
df.columns = df.columns.str.replace('25612','AGF U19')
df.columns = df.columns.str.replace('23731','Lyngby U19')
df.columns = df.columns.str.replace('23734','Brøndby U19')
#df.columns = df.columns.str.replace('general.','')
#possession_cols = [col for col in df.columns if col.startswith('possession')]
#df.columns = df.columns.where(~df.columns.str.startswith('possession.'), df.columns.str.replace('possession.', ''))
#df.columns = df.columns.str.replace('openplay.','')
#df.columns = df.columns.str.replace('attacks.','')
#df.columns = df.columns.str.replace('transitions.','')
#df.columns = df.columns.str.replace('passes.','')
#df.columns = df.columns.str.replace('defence.','')
#df.columns = df.columns.str.replace('duels.','')
#df.columns = df.columns.str.replace('flanks.','')


json_files = []

def find_json_files(directory_client):
    for item in directory_client.list_directories_and_files():
        if item.is_directory:
            if 'AC Horsens' in item.name:
                # Recursively search for JSON files in the subdirectory if it contains 'AC Horsens' in its name
                sub_directory_client = directory_client.get_subdirectory_client(item.name)
                find_json_files(sub_directory_client)
            else:
                # Otherwise, continue searching in the current directory
                find_json_files(directory_client.get_subdirectory_client(item.name))
        elif item.name.endswith('.json') and 'MatchDetail' in item.name:
            # If the item is a JSON file with 'MatchEvents' in the name, download it and append its data to the list
            json_files.append(json.loads(directory_client.get_file_client(item.name).download_file().readall().decode()))
find_json_files(directory_client)
kampdetaljer = json_normalize(json_files)
kampdetaljer = kampdetaljer[['wyId','label','date']]
kampdetaljer = kampdetaljer.rename(columns={'wyId':'matchId'})

dfegnekampe = kampdetaljer.merge(df)
dfegnekampe['label'] = dfegnekampe['label'].astype(str)
#dfegnekampe = dfegnekampe[dfegnekampe['label'].str.contains('Horsens')]
dfegnekampe.to_csv(r'Teamsheet alle kampe U19.csv',index=False)

from azure.storage.fileshare import ShareServiceClient
import json
import pandas as pd
from pandas import json_normalize
import numpy as np
import os
import streamlit as st
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
            if 'AC Horsens' in item.name:
                # Recursively search for JSON files in the subdirectory if it contains 'AC Horsens' in its name
                sub_directory_client = directory_client.get_subdirectory_client(item.name)
                find_json_files(sub_directory_client)
            else:
                # Otherwise, continue searching in the current directory
                find_json_files(directory_client.get_subdirectory_client(item.name))
        elif item.name.endswith('.json') and 'MatchAdvanceStats' in item.name:
            # If the item is a JSON file with 'MatchAdvanceStats' in the name, download it and append its data to the list
            json_files.append(json.loads(directory_client.get_file_client(item.name).download_file().readall().decode()))
find_json_files(directory_client)
df = pd.json_normalize(json_files)
df = pd.DataFrame(df)
df.columns = df.columns.str.replace('38324','Horsens U19')
df.columns = df.columns.str.replace('23735','Esbjerg U19')
df.columns = df.columns.str.replace('23732','København U19')
df.columns = df.columns.str.replace('23736','Silkeborg U19')
df.columns = df.columns.str.replace('23738','SønderjyskE U19')
df.columns = df.columns.str.replace('23730','AaB U19')
df.columns = df.columns.str.replace('23726','OB U19')
df.columns = df.columns.str.replace('23733','Vejle U19')
df.columns = df.columns.str.replace('23737','Randers U19')
df.columns = df.columns.str.replace('23727','FC Nordsjælland U19')
df.columns = df.columns.str.replace('23729','Midtjylland U19')
df.columns = df.columns.str.replace('25612','AGF U19')
df.columns = df.columns.str.replace('23731','Lyngby U19')
df.columns = df.columns.str.replace('23734','Brøndby U19')
#df.columns = df.columns.str.replace('general.','')
#possession_cols = [col for col in df.columns if col.startswith('possession')]
#df.columns = df.columns.where(~df.columns.str.startswith('possession.'), df.columns.str.replace('possession.', ''))
#df.columns = df.columns.str.replace('openplay.','')
#df.columns = df.columns.str.replace('attacks.','')
#df.columns = df.columns.str.replace('transitions.','')
#df.columns = df.columns.str.replace('passes.','')
#df.columns = df.columns.str.replace('defence.','')
#df.columns = df.columns.str.replace('duels.','')
#df.columns = df.columns.str.replace('flanks.','')


json_files = []

def find_json_files(directory_client):
    for item in directory_client.list_directories_and_files():
        if item.is_directory:
            if 'AC Horsens' in item.name:
                # Recursively search for JSON files in the subdirectory if it contains 'AC Horsens' in its name
                sub_directory_client = directory_client.get_subdirectory_client(item.name)
                find_json_files(sub_directory_client)
            else:
                # Otherwise, continue searching in the current directory
                find_json_files(directory_client.get_subdirectory_client(item.name))
        elif item.name.endswith('.json') and 'MatchDetail' in item.name:
            # If the item is a JSON file with 'MatchEvents' in the name, download it and append its data to the list
            json_files.append(json.loads(directory_client.get_file_client(item.name).download_file().readall().decode()))
find_json_files(directory_client)
kampdetaljer = json_normalize(json_files)
kampdetaljer = kampdetaljer[['wyId','label','date']]
kampdetaljer = kampdetaljer.rename(columns={'wyId':'matchId'})

dfegnekampe = kampdetaljer.merge(df)
dfegnekampe['label'] = dfegnekampe['label'].astype(str)
dfegnekampe = dfegnekampe[dfegnekampe['label'].str.contains('Horsens')]

dfegnekampe['date'] = dfegnekampe['date'].astype(str)
dfegnekampe['date'] = dfegnekampe['date'].apply(lambda x: parser.parse(x))

# Sort the dataframe by the 'date' column
dfegnekampe = dfegnekampe.sort_values(by='date',ascending=False)

# Format the 'date' column to day-month-year format
dfegnekampe['date'] = dfegnekampe['date'].apply(lambda x: x.strftime('%d-%m-%Y'))
dfegnekampe.to_csv(r'Teamsheet egne kampe U19.csv',index=False)
print('U19 data hentet til teamsheet')
from azure.storage.fileshare import ShareServiceClient
import json
import pandas as pd
from pandas import json_normalize
import numpy as np
import ast

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
            if 'AC Horsens' in item.name:
                # Recursively search for JSON files in the subdirectory if it contains 'AC Horsens' in its name
                sub_directory_client = directory_client.get_subdirectory_client(item.name)
                find_json_files(sub_directory_client)
            else:
                # Otherwise, continue searching in the current directory
                find_json_files(directory_client.get_subdirectory_client(item.name))
        elif item.name.endswith('.json') and 'MatchAdvancePlayerStats' in item.name:
            # If the item is a JSON file with 'MatchEvents' in the name, download it and append its data to the list
            json_files.append(json.loads(directory_client.get_file_client(item.name).download_file().readall().decode()))

find_json_files(directory_client)

# Create an empty list to store the events data
players_list = []
# Iterate over each item in the json_files list and append its 'events' data to the events_list
for item in json_files:
    players_list.extend(item['players'])


# Convert the events_list to a DataFrame
df = pd.DataFrame(players_list)
df.to_csv(r'Individuelt dashboard/Individuelt dashboard U15.csv',index=False)
print('Matchstats hentet til U15')
json_files = []

def find_json_files(directory_client):
    for item in directory_client.list_directories_and_files():
        if item.is_directory:
            if 'AC Horsens' in item.name:
                # Recursively search for JSON files in the subdirectory if it contains 'AC Horsens' in its name
                sub_directory_client = directory_client.get_subdirectory_client(item.name)
                find_json_files(sub_directory_client)
            else:
                # Otherwise, continue searching in the current directory
                find_json_files(directory_client.get_subdirectory_client(item.name))
        elif item.name.endswith('.json') and 'MatchEvents' in item.name:
            # If the item is a JSON file with 'MatchEvents' in the name, download it and append its data to the list
            json_files.append(json.loads(directory_client.get_file_client(item.name).download_file().readall().decode()))

find_json_files(directory_client)

# Create an empty list to store the events data
events_list = []

# Iterate over each item in the json_files list and append its 'events' data to the events_list
for item in json_files:
    events_list.extend(item['events'])

# Convert the events_list to a DataFrame
df = pd.DataFrame(events_list)
df = df[['matchId','team','opponentTeam','player']]
print('U15 eventdata hentet')
json_files = []

def find_json_files(directory_client):
    for item in directory_client.list_directories_and_files():
        if item.is_directory:
            if 'AC Horsens' in item.name:
                # Recursively search for JSON files in the subdirectory if it contains 'AC Horsens' in its name
                sub_directory_client = directory_client.get_subdirectory_client(item.name)
                find_json_files(sub_directory_client)
            else:
                # Otherwise, continue searching in the current directory
                find_json_files(directory_client.get_subdirectory_client(item.name))
        elif item.name.endswith('.json') and 'MatchDetail' in item.name:
            # If the item is a JSON file with 'MatchEvents' in the name, download it and append its data to the list
            json_files.append(json.loads(directory_client.get_file_client(item.name).download_file().readall().decode()))
            
find_json_files(directory_client)
kampdetaljer = json_normalize(json_files)
kampdetaljer = kampdetaljer[['wyId','label','date']]
kampdetaljer = kampdetaljer.rename(columns={'wyId':'matchId'})
df1 = kampdetaljer.merge(df)

df1.to_csv('U15 eventdata alle.csv',index=False)

df = pd.read_csv(r'U15 eventdata alle.csv')
df['team'] = df['team'].apply(lambda x: ast.literal_eval(x))

# Create a new dataframe with the columns as the dictionary keys and the values as a list
new_df = pd.DataFrame(df['team'].to_list(), index=df.index).add_prefix('team_')

# Concatenate the new dataframe with the original dataframe
df = pd.concat([df, new_df], axis=1)

# Drop the original 'percent' column
df = df.drop('team', axis=1)

df['opponentTeam'] = df['opponentTeam'].apply(lambda x: ast.literal_eval(x))

# Create a new dataframe with the columns as the dictionary keys and the values as a list
new_df = pd.DataFrame(df['opponentTeam'].to_list(), index=df.index).add_prefix('opponentTeam_')

# Concatenate the new dataframe with the original dataframe
df = pd.concat([df, new_df], axis=1)

# Drop the original 'percent' column
df = df.drop('opponentTeam', axis=1)

df['player'] = df['player'].apply(lambda x: ast.literal_eval(x))

# Create a new dataframe with the columns as the dictionary keys and the values as a list
new_df = pd.DataFrame(df['player'].to_list(), index=df.index).add_prefix('Player ')

# Concatenate the new dataframe with the original dataframe
df = pd.concat([df, new_df], axis=1)

# Drop the original 'percent' column
df = df.drop('player', axis=1)
df['matchId'] = df['matchId'].astype(str)
df['Player id'] = df['Player id'].astype(str)
df.to_csv(r'U15 eventdata alle.csv')

print('U15 Matchdetails hentet')


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
            if 'AC Horsens' in item.name:
                # Recursively search for JSON files in the subdirectory if it contains 'AC Horsens' in its name
                sub_directory_client = directory_client.get_subdirectory_client(item.name)
                find_json_files(sub_directory_client)
            else:
                # Otherwise, continue searching in the current directory
                find_json_files(directory_client.get_subdirectory_client(item.name))
        elif item.name.endswith('.json') and 'MatchAdvancePlayerStats' in item.name:
            # If the item is a JSON file with 'MatchEvents' in the name, download it and append its data to the list
            json_files.append(json.loads(directory_client.get_file_client(item.name).download_file().readall().decode()))

find_json_files(directory_client)

# Create an empty list to store the events data
players_list = []
# Iterate over each item in the json_files list and append its 'events' data to the events_list
for item in json_files:
    players_list.extend(item['players'])


# Convert the events_list to a DataFrame
df = pd.DataFrame(players_list)
df.to_csv(r'Individuelt dashboard/Individuelt dashboard U17.csv',index=False)
print('Matchstats hentet til U17')
json_files = []

def find_json_files(directory_client):
    for item in directory_client.list_directories_and_files():
        if item.is_directory:
            if 'AC Horsens' in item.name:
                # Recursively search for JSON files in the subdirectory if it contains 'AC Horsens' in its name
                sub_directory_client = directory_client.get_subdirectory_client(item.name)
                find_json_files(sub_directory_client)
            else:
                # Otherwise, continue searching in the current directory
                find_json_files(directory_client.get_subdirectory_client(item.name))
        elif item.name.endswith('.json') and 'MatchEvents' in item.name:
            # If the item is a JSON file with 'MatchEvents' in the name, download it and append its data to the list
            json_files.append(json.loads(directory_client.get_file_client(item.name).download_file().readall().decode()))

find_json_files(directory_client)

# Create an empty list to store the events data
events_list = []

# Iterate over each item in the json_files list and append its 'events' data to the events_list
for item in json_files:
    events_list.extend(item['events'])

# Convert the events_list to a DataFrame
df = pd.DataFrame(events_list)
df = df[['matchId','team','opponentTeam','player']]
print('U17 eventdata hentet')
json_files = []

def find_json_files(directory_client):
    for item in directory_client.list_directories_and_files():
        if item.is_directory:
            if 'AC Horsens' in item.name:
                # Recursively search for JSON files in the subdirectory if it contains 'AC Horsens' in its name
                sub_directory_client = directory_client.get_subdirectory_client(item.name)
                find_json_files(sub_directory_client)
            else:
                # Otherwise, continue searching in the current directory
                find_json_files(directory_client.get_subdirectory_client(item.name))
        elif item.name.endswith('.json') and 'MatchDetail' in item.name:
            # If the item is a JSON file with 'MatchEvents' in the name, download it and append its data to the list
            json_files.append(json.loads(directory_client.get_file_client(item.name).download_file().readall().decode()))
            
find_json_files(directory_client)
kampdetaljer = json_normalize(json_files)
kampdetaljer = kampdetaljer[['wyId','label','date']]
kampdetaljer = kampdetaljer.rename(columns={'wyId':'matchId'})
df1 = kampdetaljer.merge(df)

df1.to_csv('U17 eventdata alle.csv',index=False)

df = pd.read_csv(r'U17 eventdata alle.csv')
df['team'] = df['team'].apply(lambda x: ast.literal_eval(x))

# Create a new dataframe with the columns as the dictionary keys and the values as a list
new_df = pd.DataFrame(df['team'].to_list(), index=df.index).add_prefix('team_')

# Concatenate the new dataframe with the original dataframe
df = pd.concat([df, new_df], axis=1)

# Drop the original 'percent' column
df = df.drop('team', axis=1)

df['opponentTeam'] = df['opponentTeam'].apply(lambda x: ast.literal_eval(x))

# Create a new dataframe with the columns as the dictionary keys and the values as a list
new_df = pd.DataFrame(df['opponentTeam'].to_list(), index=df.index).add_prefix('opponentTeam_')

# Concatenate the new dataframe with the original dataframe
df = pd.concat([df, new_df], axis=1)

# Drop the original 'percent' column
df = df.drop('opponentTeam', axis=1)

df['player'] = df['player'].apply(lambda x: ast.literal_eval(x))

# Create a new dataframe with the columns as the dictionary keys and the values as a list
new_df = pd.DataFrame(df['player'].to_list(), index=df.index).add_prefix('Player ')

# Concatenate the new dataframe with the original dataframe
df = pd.concat([df, new_df], axis=1)

# Drop the original 'percent' column
df = df.drop('player', axis=1)
df['matchId'] = df['matchId'].astype(str)
df['Player id'] = df['Player id'].astype(str)
df.to_csv(r'U17 eventdata alle.csv')

print('Matchdetails hentet U17')

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
            if 'AC Horsens' in item.name:
                # Recursively search for JSON files in the subdirectory if it contains 'AC Horsens' in its name
                sub_directory_client = directory_client.get_subdirectory_client(item.name)
                find_json_files(sub_directory_client)
            else:
                # Otherwise, continue searching in the current directory
                find_json_files(directory_client.get_subdirectory_client(item.name))
        elif item.name.endswith('.json') and 'MatchAdvancePlayerStats' in item.name:
            # If the item is a JSON file with 'MatchEvents' in the name, download it and append its data to the list
            json_files.append(json.loads(directory_client.get_file_client(item.name).download_file().readall().decode()))

find_json_files(directory_client)

# Create an empty list to store the events data
players_list = []
# Iterate over each item in the json_files list and append its 'events' data to the events_list
for item in json_files:
    players_list.extend(item['players'])


# Convert the events_list to a DataFrame
df = pd.DataFrame(players_list)
df.to_csv(r'Individuelt dashboard/Individuelt dashboard U19.csv',index=False)
print('Matchstats hentet til U19')
json_files = []

def find_json_files(directory_client):
    for item in directory_client.list_directories_and_files():
        if item.is_directory:
            if 'AC Horsens' in item.name:
                # Recursively search for JSON files in the subdirectory if it contains 'AC Horsens' in its name
                sub_directory_client = directory_client.get_subdirectory_client(item.name)
                find_json_files(sub_directory_client)
            else:
                # Otherwise, continue searching in the current directory
                find_json_files(directory_client.get_subdirectory_client(item.name))
        elif item.name.endswith('.json') and 'MatchEvents' in item.name:
            # If the item is a JSON file with 'MatchEvents' in the name, download it and append its data to the list
            json_files.append(json.loads(directory_client.get_file_client(item.name).download_file().readall().decode()))

find_json_files(directory_client)

# Create an empty list to store the events data
events_list = []

# Iterate over each item in the json_files list and append its 'events' data to the events_list
for item in json_files:
    events_list.extend(item['events'])

# Convert the events_list to a DataFrame
df = pd.DataFrame(events_list)
df = df[['matchId','team','opponentTeam','player']]
print('eventdata hentet')
json_files = []

def find_json_files(directory_client):
    for item in directory_client.list_directories_and_files():
        if item.is_directory:
            if 'AC Horsens' in item.name:
                # Recursively search for JSON files in the subdirectory if it contains 'AC Horsens' in its name
                sub_directory_client = directory_client.get_subdirectory_client(item.name)
                find_json_files(sub_directory_client)
            else:
                # Otherwise, continue searching in the current directory
                find_json_files(directory_client.get_subdirectory_client(item.name))
        elif item.name.endswith('.json') and 'MatchDetail' in item.name:
            # If the item is a JSON file with 'MatchEvents' in the name, download it and append its data to the list
            json_files.append(json.loads(directory_client.get_file_client(item.name).download_file().readall().decode()))
            
find_json_files(directory_client)
kampdetaljer = json_normalize(json_files)
kampdetaljer = kampdetaljer[['wyId','label','date']]
kampdetaljer = kampdetaljer.rename(columns={'wyId':'matchId'})
df1 = kampdetaljer.merge(df)

df1.to_csv('U19 eventdata alle.csv',index=False)

df = pd.read_csv(r'U19 eventdata alle.csv')
df['team'] = df['team'].apply(lambda x: ast.literal_eval(x))

# Create a new dataframe with the columns as the dictionary keys and the values as a list
new_df = pd.DataFrame(df['team'].to_list(), index=df.index).add_prefix('team_')

# Concatenate the new dataframe with the original dataframe
df = pd.concat([df, new_df], axis=1)

# Drop the original 'percent' column
df = df.drop('team', axis=1)

df['opponentTeam'] = df['opponentTeam'].apply(lambda x: ast.literal_eval(x))

# Create a new dataframe with the columns as the dictionary keys and the values as a list
new_df = pd.DataFrame(df['opponentTeam'].to_list(), index=df.index).add_prefix('opponentTeam_')

# Concatenate the new dataframe with the original dataframe
df = pd.concat([df, new_df], axis=1)

# Drop the original 'percent' column
df = df.drop('opponentTeam', axis=1)

df['player'] = df['player'].apply(lambda x: ast.literal_eval(x))

# Create a new dataframe with the columns as the dictionary keys and the values as a list
new_df = pd.DataFrame(df['player'].to_list(), index=df.index).add_prefix('Player ')

# Concatenate the new dataframe with the original dataframe
df = pd.concat([df, new_df], axis=1)

# Drop the original 'percent' column
df = df.drop('player', axis=1)
df['matchId'] = df['matchId'].astype(str)
df['Player id'] = df['Player id'].astype(str)
df.to_csv(r'U19 eventdata alle.csv')

print('Matchdetails hentet U19')

print('Alt data hentet')