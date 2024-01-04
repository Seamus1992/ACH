import pandas as pd
import numpy as np
import streamlit as st
from datetime import date

df = pd.read_excel(r'C:/Users/SéamusPeareBartholdy/OneDrive - AC Horsens A S/Akademi/Fysisk træning/Testresultater/Test til DBU/Test til app/PHV/PHV U13 App.xlsx',sheet_name='PHV Calculator (Team 1)')
df.to_csv(r'Fysisk data/U13 PHV.csv',index=False)

df = pd.read_excel(r'C:/Users/SéamusPeareBartholdy/OneDrive - AC Horsens A S/Akademi/Fysisk træning/Testresultater/Test til DBU/Test til app/PHV/PHV U14 App.xlsx',sheet_name='PHV Calculator (Team 1)')
df.to_csv(r'Fysisk data/U14 PHV.csv',index=False)

df = pd.read_excel(r'C:/Users/SéamusPeareBartholdy/OneDrive - AC Horsens A S/Akademi/Fysisk træning/Testresultater/Test til DBU/Test til app/PHV/PHV U15 App.xlsx',sheet_name='PHV Calculator (Team 1)')
df.to_csv(r'Fysisk data/U15 PHV.csv',index=False)

df = pd.read_excel(r'C:/Users/SéamusPeareBartholdy/OneDrive - AC Horsens A S/Akademi/Fysisk træning/Testresultater/Test til DBU/Test til app/Fysiske test/Fysisk test App.xlsx')
df.to_csv(r'Fysisk data/Fysiske test U15.csv',index=False)

df = pd.read_excel(r'C:/Users/SéamusPeareBartholdy/OneDrive - AC Horsens A S/Akademi/Fysisk træning/Testresultater/Test til DBU/Test til app/Fysiske test/Fysisk test App.xlsx',sheet_name='U17')
df.to_csv(r'Fysisk data/Fysiske test U17.csv',index=False)

df = pd.read_excel(r'C:/Users/SéamusPeareBartholdy/OneDrive - AC Horsens A S/Akademi/Fysisk træning/Testresultater/Test til DBU/Test til app/Fysiske test/Fysisk test App.xlsx',sheet_name='U19')
df.to_csv(r'Fysisk data/Fysiske test U19.csv',index=False)


print('Fysisk data hentet')