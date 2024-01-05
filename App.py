import streamlit as st
st.set_page_config(layout="wide")

valid_username = "AC Horsens"
valid_password = "Dataapp"

username = st.sidebar.text_input('Brugernavn')
password = st.sidebar.text_input('Kode', type='password')

if username == valid_username and password == valid_password:

    def Wellness_data():
        import gspread
        import pandas as pd
        import io
        import base64

        gc = gspread.service_account('wellness-1123-178fea106d0a.json')
        sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1haWEtNQdhthKaSQjb2BRHlq2FLexicUOAHbjNFRAUAk/edit#gid=1984878556')
        ws = sh.worksheet('Samlet')
        df = pd.DataFrame(ws.get_all_records())

        df['Tidsstempel'] = df['Tidsstempel'].apply(lambda x: pd.to_datetime(x, format='%d/%m/%Y %H.%M.%S') if x else x)

        df['Hvilken årgang er du?'] = df['Hvilken årgang er du?'].astype(str)
        df['Hvor frisk er du?'] = df['Hvor frisk er du?'].astype(str)
        df['Hvor frisk er du?'] = df['Hvor frisk er du?'].str.extract(r'(\d+)').astype(float)
        df['Hvordan har du det mentalt'] = df['Hvordan har du det mentalt'].astype(str)
        df['Hvordan har du det mentalt'] = df['Hvordan har du det mentalt'].str.extract(r'(\d+)').astype(float)
        df['Hvordan har din søvn været?'] = df['Hvordan har din søvn været?'].astype(str)
        df['Hvordan har din søvn været?'] = df['Hvordan har din søvn været?'].str.extract(r'(\d+)').astype(float)
        df['Hvor hård var træning/kamp? (10 er hårdest)'] = df['Hvor hård var træning/kamp? (10 er hårdest)'].astype(str)
        df['Hvor hård var træning/kamp? (10 er hårdest)'] = df['Hvor hård var træning/kamp? (10 er hårdest)'].str.extract(r'(\d+)').astype(float)
        df['Hvor udmattet er du?'] = df['Hvor udmattet er du?'].astype(str)
        df['Hvor udmattet er du?'] = df['Hvor udmattet er du?'].str.extract(r'(\d+)').astype(float)
        df['Bedøm din muskelømhed'] = df['Bedøm din muskelømhed'].astype(str)
        df['Bedøm din muskelømhed'] = df['Bedøm din muskelømhed'].str.extract(r'(\d+)').astype(float)
        df['Jeg følte mig tilpas udfordret under træning/kamp'] = df['Jeg følte mig tilpas udfordret under træning/kamp'].astype(str)
        df['Jeg følte mig tilpas udfordret under træning/kamp'] = df['Jeg følte mig tilpas udfordret under træning/kamp'].str.extract(r'(\d+)').astype(float)
        df['Min tidsfornemmelse forsvandt under træning/kamp'] = df['Min tidsfornemmelse forsvandt under træning/kamp'].astype(str)
        df['Min tidsfornemmelse forsvandt under træning/kamp'] = df['Min tidsfornemmelse forsvandt under træning/kamp'].str.extract(r'(\d+)').astype(float)
        df['Jeg oplevede at tanker og handlinger var rettet mod træning/kamp'] = df['Jeg oplevede at tanker og handlinger var rettet mod træning/kamp'].astype(str)
        df['Jeg oplevede at tanker og handlinger var rettet mod træning/kamp'] = df['Jeg oplevede at tanker og handlinger var rettet mod træning/kamp'].str.extract(r'(\d+)').astype(float)
        df['Hvordan har du det mentalt?'] = df['Hvordan har du det mentalt?'].astype(str)
        df['Hvordan har du det mentalt?'] = df['Hvordan har du det mentalt?'].str.extract(r'(\d+)').astype(float)

        df.rename(columns={'Hvor mange timer sov i du i nat?':'Hvor mange timer sov du i nat?'},inplace=True)
        df = pd.melt(df,id_vars=['Tidsstempel','Spørgsmål før eller efter træning','Hvor frisk er du?','Hvordan har du det mentalt','Har du fået nok at spise inden træning/kamp?','Hvordan har din søvn været?','Hvor mange timer sov du i nat?','Træning/kamp - tid i minutter?','Hvor hård var træning/kamp? (10 er hårdest)','Hvor udmattet er du?','Bedøm din muskelømhed','Hvordan har du det mentalt?','Jeg følte mig tilpas udfordret under træning/kamp','Min tidsfornemmelse forsvandt under træning/kamp','Jeg oplevede at tanker og handlinger var rettet mod træning/kamp','Hvilken årgang er du?'],value_vars=['Spillere U13','Spillere U14','Spillere U15','Spillere U16','Spillere U17','Spillere U18','Spillere U19','Spillere U20'],value_name='Spiller')
        df = df[df['Spiller'] != '']
        df['Hvilken årgang er du?'] = df['Hvilken årgang er du?'].astype(float)
        kampe = df['Hvilken årgang er du?'].drop_duplicates(keep='first')
        kampe = kampe.dropna().astype(int)
        kampe = sorted(kampe)
        option4 = st.multiselect('Vælg årgang (Hvis ingen årgang er valgt, vises alle)',kampe)
        if len(option4) > 0:
            filtreretdfkamp = option4
        else:
            filtreretdfkamp = kampe

        filtreretdfkamp = df.loc[df.loc[df['Hvilken årgang er du?'].isin(filtreretdfkamp),'Hvilken årgang er du?'].index.values]
        
        Spiller = filtreretdfkamp['Spiller'].drop_duplicates(keep='first')
        Spiller = Spiller.dropna().astype(str)
        Spiller = sorted(Spiller)
        option5 = st.multiselect('Vælg spiller (Hvis ingen spiller er valgt, vises alle)',Spiller)
        if len(option5) > 0:
            filtreretdfspiller = option5
        else:
            filtreretdfspiller = Spiller

        filtreretdfspiller = df.loc[df.loc[df['Spiller'].isin(filtreretdfspiller),'Spiller'].index.values]

        excel_buffer = io.BytesIO()


        if st.button("Download til Excel"):
        
            with pd.ExcelWriter(excel_buffer, engine="xlsxwriter", options={'strings_to_numbers': True}) as writer:
                filtreretdfspiller.to_excel(writer, index=False, sheet_name='Sheet1')

            excel_buffer.seek(0)

            st.markdown(f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{base64.b64encode(excel_buffer.read()).decode()}" download="wellness_rådata.xlsx">Tryk for at hente rådata</a>', unsafe_allow_html=True)

        førtræning = filtreretdfspiller[['Tidsstempel','Spiller','Hvilken årgang er du?','Hvor frisk er du?','Hvordan har du det mentalt','Har du fået nok at spise inden træning/kamp?','Hvordan har din søvn været?','Hvor mange timer sov du i nat?']]
        eftertræning = filtreretdfspiller[['Tidsstempel','Spiller','Hvilken årgang er du?','Træning/kamp - tid i minutter?','Hvor hård var træning/kamp? (10 er hårdest)','Hvor udmattet er du?','Bedøm din muskelømhed','Hvordan har du det mentalt?','Jeg følte mig tilpas udfordret under træning/kamp','Min tidsfornemmelse forsvandt under træning/kamp','Jeg oplevede at tanker og handlinger var rettet mod træning/kamp']]
        førtræning.dropna(inplace=True)
        eftertræning.dropna(inplace=True)

        dftilload = eftertræning[['Tidsstempel','Hvilken årgang er du?','Hvor hård var træning/kamp? (10 er hårdest)']]
        dftilload['Tidsstempel'] = pd.to_datetime(dftilload['Tidsstempel'])
        dftilload['Date'] = dftilload['Tidsstempel'].dt.date
        dftilloadU19 = dftilload[(dftilload['Hvilken årgang er du?'] == 2005) | (dftilload['Hvilken årgang er du?'] == 2006)]
        dagligt_gennemsnitU19 = dftilloadU19.groupby('Date')['Hvor hård var træning/kamp? (10 er hårdest)'].mean()
        #dagligt_gennemsnit = dagligt_gennemsnit.reset_index()
        dftilloadU17 = dftilload[(dftilload['Hvilken årgang er du?'] == 2007) | (dftilload['Hvilken årgang er du?'] == 2008)]
        dagligt_gennemsnitU17 = dftilloadU17.groupby('Date')['Hvor hård var træning/kamp? (10 er hårdest)'].mean()
        dftilloadU15 = dftilload[(dftilload['Hvilken årgang er du?'] == 2009)]
        dagligt_gennemsnitU15 = dftilloadU15.groupby('Date')['Hvor hård var træning/kamp? (10 er hårdest)'].mean()
        dftilloadU14 = dftilload[(dftilload['Hvilken årgang er du?'] == 2010)]
        dagligt_gennemsnitU14 = dftilloadU14.groupby('Date')['Hvor hård var træning/kamp? (10 er hårdest)'].mean()
        dftilloadU13 = dftilload[(dftilload['Hvilken årgang er du?'] == 2011)]
        dagligt_gennemsnitU13 = dftilloadU13.groupby('Date')['Hvor hård var træning/kamp? (10 er hårdest)'].mean()
        


        def color_row(row):
            color = ''
            if 'Hvor frisk er du?' in row and row['Hvor frisk er du?'] >= 6 or 'Hvordan har du det mentalt' in row and row['Hvordan har du det mentalt'] >= 6 or 'Hvordan har din søvn været?' in row and row['Hvordan har din søvn været?'] >= 6 or ('Har du fået nok at spise inden træning/kamp?' in row and row['Har du fået nok at spise inden træning/kamp?'] =='Nej') or ('Hvor mange timer sov du i nat?' in row and row['Hvor mange timer sov du i nat?'] == 'Under 7 timer'):
                color = 'red'
            elif 'Hvor frisk er du?' in row and row['Hvor frisk er du?'] == 5 or 'Hvordan har du det mentalt' in row and row['Hvordan har du det mentalt'] == 5 or 'Hvordan har din søvn været?' in row and row['Hvordan har din søvn været?'] == 5 or ('Har du fået nok at spise inden træning/kamp?' in row and row['Har du fået nok at spise inden træning/kamp?'] =='Ved ikke') or ('Hvor mange timer sov du i nat?' in row and row['Hvor mange timer sov du i nat?'] == '7-8 timer'):
                color = 'yellow'
            return ['background-color: %s' % color] * row.size
        førtræning.set_index('Tidsstempel', inplace=True)
        førtræning.sort_index(ascending=False, inplace=True)
        førtræning = førtræning.loc[~førtræning.index.duplicated(keep='first')]
        førtræning = førtræning.astype(int,errors='ignore')
        førtræning = førtræning.style.apply(color_row, axis=1, subset=pd.IndexSlice[:])

        def color_row(row):
            color = ''
            if 'Hvor udmattet er du?' in row and row['Hvor udmattet er du?'] >= 6 or 'Bedøm din muskelømhed' in row and row['Bedøm din muskelømhed'] >= 6 or 'Hvordan har du det mentalt?' in row and row['Hvordan har du det mentalt?'] >= 6 or ('Jeg følte mig tilpas udfordret under træning/kamp' in row and row['Jeg følte mig tilpas udfordret under træning/kamp'] >= 6) or ('Min tidsfornemmelse forsvandt under træning/kamp' in row and row['Min tidsfornemmelse forsvandt under træning/kamp'] >= 6 or 'Jeg oplevede at tanker og handlinger var rettet mod træning/kamp' in row and row['Jeg oplevede at tanker og handlinger var rettet mod træning/kamp'] >= 6):
                color = 'red'
            elif 'Hvor udmattet er du?' in row and row['Hvor udmattet er du?'] == 5 or 'Bedøm din muskelømhed' in row and row['Bedøm din muskelømhed'] == 5 or 'Hvordan har du det mentalt?' in row and row['Hvordan har du det mentalt?'] == 5 or ('Jeg følte mig tilpas udfordret under træning/kamp' in row and row['Jeg følte mig tilpas udfordret under træning/kamp'] == 5) or ('Min tidsfornemmelse forsvandt under træning/kamp' in row and row['Min tidsfornemmelse forsvandt under træning/kamp'] == 5 or 'Jeg oplevede at tanker og handlinger var rettet mod træning/kamp' in row and row['Jeg oplevede at tanker og handlinger var rettet mod træning/kamp'] == 5):
                color = 'yellow'
            return ['background-color: %s' % color] * row.size
        eftertræning.set_index('Tidsstempel', inplace=True)
        eftertræning.sort_index(ascending=False, inplace=True)
        eftertræning = eftertræning.loc[~eftertræning.index.duplicated(keep='first')]
        eftertræning = eftertræning.astype(int,errors='ignore')
        eftertræning = eftertræning.style.apply(color_row, axis=1, subset=pd.IndexSlice[:])


        # Display the styled dataframe
        st.write('Før aktivitet')
        st.dataframe(førtræning)
        st.write('Efter aktivitet')
        st.dataframe(eftertræning)
        st.write('U19')
        st.bar_chart(dagligt_gennemsnitU19,x=['Date'],y=['Hvor hård var træning/kamp? (10 er hårdest)'])
        st.write('U17')
        st.bar_chart(dagligt_gennemsnitU17,x=['Date'],y=['Hvor hård var træning/kamp? (10 er hårdest)'])
        st.write('U15')
        st.bar_chart(dagligt_gennemsnitU15,x=['Date'],y=['Hvor hård var træning/kamp? (10 er hårdest)'])
        st.write('U14')
        st.bar_chart(dagligt_gennemsnitU14,x=['Date'],y=['Hvor hård var træning/kamp? (10 er hårdest)'])
        st.write('U13')
        st.bar_chart(dagligt_gennemsnitU13,x=['Date'],y=['Hvor hård var træning/kamp? (10 er hårdest)'])

    def Kampregistrering():

        import streamlit as st
        import pandas as pd
        from datetime import datetime
        st.markdown(
            """
            <style>
                /* Reduce padding and spacing for Streamlit elements */
                .stCheckbox {
                    margin-bottom: -15px !important; /* Adjust the margin as needed */
                }
                /* Add margin between checkbox and input */
                .stNumberInput, .stTextInput {
                    margin-top: -15px !important; /* Adjust the margin as needed */
                }
                /* Adjust label styles if necessary */
                .stNumberInput label, .stTextInput label {
                    font-size: 8px !important;
                    color: black !important;
                }
            </style>
            """,
            unsafe_allow_html=True
        )


        st.markdown(
            f"""
                    <style>
                        /* Reduce padding and spacing for Streamlit elements */
                        .stTextInput, .stTextArea, .stSelectbox, .stMultiselect, .stCheckbox, .stNumberInput, .stNumberInput label, .stTextInput label, .stTextArea label, .stMultiselect label, .stSelectbox label{{
                            padding: 0px;
                            margin-top: -20px;
                            margin-bottom: -20px;
                        }}
                        .stNumberInput label, .stTextInput label, .stTextArea label, .stMultiselect label, .stSelectbox label{{
                            font-size: 8px !important;
                            color: black !important;
                        }}
                        /* Adjust line-height for specific input types */
                        .st-cc, .st-ag, .st-eb label, .st-ec, .st-ek {{
                            line-height: 1;
                        }}
                    </style>
                    """,
                    unsafe_allow_html=True
        )

        with st.expander('Retningslinjer for kampregistrering'):
            st.write('Cheftræneren for kampårgangen registrerer altid kampen')
            st.write('Afbud overruler alt, så man behøver ikke fjerne noget når man angiver en afbudsårsag')
            st.write('Ved "til rådighed" i afbudsårsag og 0 minutter spillet samt 0 minutter til rådighed så anses spilleren som spillet for et andet hold')


        Kamp_types = ["Starter inde","Starter ude","Minutter spillet","Minutter til rådighed","Mål","Assist","Afbud","Kamptype","Modstanderhold","Kampens resultat"]

        col1,col2,col3,col4,col5,col6,col7 = st.columns(7)
        with col1:
            st.markdown(
                "<p style='font-size:x-small; line-height: 5; margin-top: -15px; margin-bottom: -15px;'>Dato</p>",
                unsafe_allow_html=True
            )
            tidspunkt = datetime.now().strftime('%H:%M:%S')  # Tidspunkt som HH:MM:SS
            default_date = datetime.now().strftime('%d-%m-%Y')  # Standarddato som dd-mm-åååå
            dato = st.text_input('Dato', default_date,key='dato_input',label_visibility='collapsed')
            
        with col2:
            st.markdown(
            "<p style='font-size:x-small; line-height: 5; margin-top: -15px; margin-bottom: -15px;'>Kampårgang</p>",
            unsafe_allow_html=True
            )
            Kampårgang = st.selectbox('Kampårgang', ['U13', 'U14', 'U15', 'U17', 'U19', 'Førstehold'], placeholder='Vælg en kampårgang', label_visibility='hidden')

        with col3:
            st.markdown(
            "<p style='font-size:x-small; line-height: 5; margin-top: -15px; margin-bottom: -15px;'>Spillerens årgang</p>",
            unsafe_allow_html=True
            )      
            Spillerårgang = st.selectbox('Spillerens årgang', ['U13', 'U14', 'U15', 'U17', 'U19'],placeholder='Vælg spillerens årgang',label_visibility='hidden')
        with col4:
            st.markdown(
                "<p style='font-size:x-small; line-height: 5; margin-top: -15px; margin-bottom: -15px;'>Kamp varighed</p>",
                unsafe_allow_html=True
            )
            Kampvarighed = st.number_input('Kamp varighed',min_value=0, max_value=1000,step=1, label_visibility='hidden', key='col4_input')

        with col5:
            st.markdown(
                "<p style='font-size:x-small; line-height: 5; margin-top: -15px; margin-bottom: -15px;'>Kamptype</p>",
                unsafe_allow_html=True
            )
            Kamptype = st.selectbox('Kamptype',['Turneringskamp','Træningskamp','Stævnekamp'],placeholder='Vælg en kamptype',label_visibility='collapsed')

        with col6:
            st.markdown(
                "<p style='font-size:xx-small; line-height: 5; margin-top: -11px; margin-bottom: -11px;'>Modstanderhold</p>",
                unsafe_allow_html=True
            )
            Modstanderhold = st.text_input('Modstanderhold',label_visibility='collapsed')

        with col7:
            st.markdown(
                "<p style='font-size:x-small; line-height: 5; margin-top: -15px; margin-bottom: -15px;'>Kampens resultat</p>",
                unsafe_allow_html=True
            )
            Kampens_resultat = st.text_input('Kampens resultat',placeholder='AC-Modstander',label_visibility='collapsed')

        navne = pd.read_excel(r'Navne.xlsx')
        navne = navne[navne['Trup'] ==Spillerårgang]
        navne = navne['Spillere'].to_list()
        navne = sorted(navne)
        # Create an empty DataFrame with player names as rows and training types as columns
        data = pd.DataFrame(False, columns=['Dato','Kampårgang','Spillerens årgang'] + Kamp_types, index=navne)


        st.write('Kampregistrering')

        # Column titles
        col1, col2, col3, col4, col5, col6, col7, col8= st.columns([2,1,1,1,1,1,1,1])

        with col1:
            st.markdown(
                "<p style='font-size:xx-small; margin-top: 5px; margin-bottom: 20px;'>Spiller</p>",
                unsafe_allow_html=True
            )

        with col2:
            st.markdown(
                "<p style='font-size:xx-small; margin-top: 5px; margin-bottom: 20px;'>Starter inde</p>",
                unsafe_allow_html=True
            )

        with col3:
            st.markdown(
                "<p style='font-size:xx-small; margin-top: 5px; margin-bottom: 20px;'>Starter ude</p>",
                unsafe_allow_html=True
            )

        with col4:
            st.markdown(
                "<p style='font-size:xx-small; margin-top: 5px; margin-bottom: 20px;'>Minutter spillet</p>",
                unsafe_allow_html=True
            )

        with col5:
            st.markdown(
                "<p style='font-size:xx-small; margin-top: 5px; margin-bottom: 20px;'>Minutter til rådighed</p>",
                unsafe_allow_html=True
            )

        with col6:
            st.markdown(
                "<p style='font-size:xx-small; margin-top: 5px; margin-bottom: 20px;'>Mål</p>",
                unsafe_allow_html=True
            )

        with col7:
            st.markdown(
                "<p style='font-size:xx-small; margin-top: 5px; margin-bottom: 20px;'>Assist</p>",
                unsafe_allow_html=True
            )

        with col8:
            st.markdown(
                "<p style='font-size:xx-small; margin-top: 5px; margin-bottom: 20px;'>Rådighed</p>",
                unsafe_allow_html=True
            )


        for player in navne:
            col1, col2,col3,col4, col5,col6,col7,col8 = st.columns([2,1,1,1,1,1,1,1])
            data.loc[player, "Dato"] = dato
            data.loc[player, "Kampårgang"] = Kampårgang
            data.loc[player, "Spillerens årgang"] = Spillerårgang
            data.loc[player, "Spiller"] = player
            data.loc[player, "Kamptype"] = Kamptype
            data.loc[player, "Modstanderhold"] = Modstanderhold
            data.loc[player, "Kampens resultat"] = Kampens_resultat

            with col1:
                st.markdown(f"<p style='font-size:xx-small; margin-top: -15px; margin-bottom: -15px; font-weight: bold;'>{player}</p>", unsafe_allow_html=True)

            with col2:
                data.loc[player, "Starter inde"] = st.checkbox('Starter inde', key=f"{player}_Starter inde", value=(Kampvarighed > 0),label_visibility='collapsed')

                st.markdown(
                    f"""
                    <style>
                        /* Reduce padding, adjust font size, and line height for select boxes */
                        .st-cc, .st-ag, .st-eb label, .st-ec, .st-ek {{
                            padding: 0.1px;
                            font-size: 10px;
                            line-height: 1.3;
                            margin-top: 0px;
                            margin-bottom 0px;
                        }}
                    </style>
                    """,
                    unsafe_allow_html=True)


            with col3:
                data.loc[player, "Starter ude"] = st.checkbox('Starter ude', key=f"{player} Starter ude",label_visibility='collapsed')

            with col4:
                data.loc[player, "Minutter spillet"] = st.number_input('Minutter spillet',value=Kampvarighed,step=1, key=f"{player} Minutter spillet",label_visibility='collapsed')

            with col5:
                data.loc[player, "Minutter til rådighed"] = st.number_input('Minutter til rådighed',value=Kampvarighed,step=1, key=f"{player} Minutter til rådighed",label_visibility='collapsed')

            with col6:
                data.loc[player, "Mål"] = st.number_input('Mål',min_value=0,step=1, key=f"{player} Mål",label_visibility='collapsed')

            with col7:
                data.loc[player, "Assist"] = st.number_input('Assist',min_value=0,step=1, key=f"{player} Assist",label_visibility='collapsed')

            with col8:
                data.loc[player,"Rådighed"] = st.selectbox(f"Årsag", ['Til rådighed','Sygdom', 'Skadet', 'DBU samling', 'Andet afbud'], key=f"{player} Rådighed",placeholder='',label_visibility='collapsed')

            absence_columns = [col for col in data.columns if f"{player} Rådighed" in col]

            if any((data[col] != 'Til rådighed').any() for col in absence_columns):
                for column in data.columns:
                    if "Minutter" in column:
                        data.loc[player, column] = 0

            for player in data.index:
                if (data.loc[player, 'Minutter spillet'] == 0) and \
                (data.loc[player, 'Minutter til rådighed'] == 0) and \
                (data.loc[player, 'Rådighed'] == 'Til rådighed'):
                    data.loc[player, 'Modstanderhold'] = ''
                    data.loc[player, 'Kamptype'] = ''
                    data.loc[player, 'Kampårgang'] = ''
                    data.loc[player, 'Rådighed'] = ''

                
        data = data[data['Rådighed'] != '']
        st.write(data)

        import json
        import os.path

        json_filename = 'Kampregistrering.json'
        if st.button('Gem dataene'):
            if not os.path.exists(json_filename) or os.path.getsize(json_filename) == 0:
                with open(json_filename, 'w') as f:
                    json.dump(data.to_dict(orient='records'), f, indent=4)
                st.write("Dataene er gemt i Kampdata")
            else:
                existing_data = []
                with open(json_filename, 'r') as f:
                    try:
                        existing_data = json.load(f)
                    except json.JSONDecodeError:
                        st.error("Fejl: JSON-filen har ugyldig struktur.")

                existing_data += data.to_dict(orient='records')

                with open(json_filename, 'w') as f:
                    json.dump(existing_data, f, indent=4)
                st.write("Nye data er tilføjet til Kampdata")

        if st.button('Slet alle data'):
            if os.path.exists(json_filename):
                os.remove(json_filename)
                st.write("Alle data er blevet slettet fra JSON-filen.")
            else:
                st.write("Filen eksisterer ikke.")

        all_data = []
        if os.path.exists(json_filename) and os.path.getsize(json_filename) > 0:
            with open(json_filename, 'r') as f:
                try:
                    all_data = json.load(f)
                except json.JSONDecodeError:
                    st.error("Fejl: JSON-filen er tom eller har ugyldig struktur.")

        all_df = pd.DataFrame(all_data)

        st.write(all_df)

    def Træningsregistrering():
        import streamlit as st
        import pandas as pd
        from datetime import datetime

        st.markdown(
            """
            <style>
                /* Reduce padding and spacing for Streamlit elements */
                .stCheckbox {
                    margin-bottom: -15px !important; /* Adjust the margin as needed */
                }
                /* Add margin between checkbox and input */
                .stNumberInput, .stTextInput {
                    margin-top: -15px !important; /* Adjust the margin as needed */
                }
                /* Adjust label styles if necessary */
                .stNumberInput label, .stTextInput label {
                    font-size: 8px !important;
                    color: black !important;
                }
            </style>
            """,
            unsafe_allow_html=True
        )


        st.markdown(
            f"""
                    <style>
                        /* Reduce padding and spacing for Streamlit elements */
                        .stTextInput, .stTextArea, .stSelectbox, .stMultiselect, .stCheckbox, .stNumberInput, .stNumberInput label, .stTextInput label, .stTextArea label, .stMultiselect label, .stSelectbox label{{
                            padding: 0px;
                            margin-top: -20px;
                            margin-bottom: -20px;
                        }}
                        .stNumberInput label, .stTextInput label, .stTextArea label, .stMultiselect label, .stSelectbox label{{
                            font-size: 8px !important;
                            color: black !important;
                        }}
                        /* Adjust line-height for specific input types */
                        .st-cc, .st-ag, .st-eb label, .st-ec, .st-ek {{
                            line-height: 1;
                        }}
                    </style>
                    """,
                    unsafe_allow_html=True
        )

        with st.expander('Retningslinjer for træningsregistrering'):
            st.write('Cheftræneren for træningsårgangen står for registrering af al holdaktivitet (holdtræning, begge dele i en split-session, holdvideo og hold performance)')
            st.write('Fysisk træner registrerer styrketræning hvis det er eneste aktivitet i træningspasset')
            st.write('Afbud overruler alt, så man behøver ikke fjerne noget når man angiver en afbudsårsag')
            st.write('Personen med ansvaret for den enkelte spiller til individuel aktivitet har ansvaret for registrering af denne individuelle aktivitet')
            st.write('Individuelle aktiviteter skal altid indeholde kommentar')
            
        Kamp_types = ["Holdtræning","Holdvideo","Hold performance","Individuel træning","Individuel video","Individuel performance", "Styrketræning", "Afbud"]

        col1,col2,col3,col4,col5,col6,col7 = st.columns(7)
        with col1:
            st.markdown(
                "<p style='font-size:x-small; line-height: 5; margin-top: -15px; margin-bottom: -15px;'>Dato</p>",
                unsafe_allow_html=True
            )
            tidspunkt = datetime.now().strftime('%H:%M:%S')  # Tidspunkt som HH:MM:SS
            default_date = datetime.now().strftime('%d-%m-%Y')  # Standarddato som dd-mm-åååå
            dato = st.text_input('Dato', default_date,key='dato_input',label_visibility='collapsed')
            
        with col2:
            st.markdown(
            "<p style='font-size:x-small; line-height: 5; margin-top: -15px; margin-bottom: -15px;'>Træningsgruppe</p>",
            unsafe_allow_html=True
            )
            træningshold = st.selectbox('Træningshold', ['U13', 'U14', 'U15', 'U17', 'U19', 'Førstehold','Yngste matchningsgruppe','Ældste matchningsgruppe'], placeholder='Vælg en Kampårgang', label_visibility='hidden')

        with col3:
            st.markdown(
            "<p style='font-size:x-small; line-height: 5; margin-top: -15px; margin-bottom: -15px;'>Spillerens årgang</p>",
            unsafe_allow_html=True
            )      
            årgang = st.selectbox('Spillerens årgang', ['U13', 'U14', 'U15', 'U17', 'U19','Yngste matchningsgruppe','Ældste matchningsgruppe'],placeholder='Vælg spillerens årgang',label_visibility='hidden')
        with col4:
            st.markdown(
                "<p style='font-size:x-small; line-height: 5; margin-top: -15px; margin-bottom: -15px;'>Holdtræning varighed</p>",
                unsafe_allow_html=True
            )
            holdtræning_varighed = st.number_input('Holdtræning minutter', max_value=1000, label_visibility='hidden', key='col4_input')

        with col5:
            st.markdown(
                "<p style='font-size:x-small; line-height: 5; margin-top: -15px; margin-bottom: -15px;'>Holdvideo varighed</p>",
                unsafe_allow_html=True
            )
            holdvideo_varighed = st.number_input('Holdvideo varighed', min_value=0, max_value=1000, label_visibility='hidden', key='col5_input')

        with col6:
            st.markdown(
                "<p style='font-size:xx-small; line-height: 5; margin-top: -11px; margin-bottom: -11px;'>Holdperformance varighed</p>",
                unsafe_allow_html=True
            )
            holdperformance_varighed = st.number_input('Holdperformance minutter', min_value=0, max_value=1000, label_visibility='hidden', key='col6_input')

        with col7:
            st.markdown(
                "<p style='font-size:x-small; line-height: 5; margin-top: -15px; margin-bottom: -15px;'>Styrketræning varighed</p>",
                unsafe_allow_html=True
            )
            styrketræning_varighed = st.number_input('Styrketræning minutter', min_value=0, max_value=1200, label_visibility='collapsed', key='col7_input')

        navne = pd.read_excel(r'Navne.xlsx')
        navne = navne[navne['Trup']==årgang]
        navne = navne['Spillere'].to_list()
        navne = sorted(navne)
        # Create an empty DataFrame with player names as rows and training types as columns
        data = pd.DataFrame(False, columns=['Dato','Træningsgruppe','Spillerens årgang'] + Kamp_types, index=navne)


        st.write('Træningsregistrering')

        # Column titles
        col1, col2, col3, col4, col5, col6, col7, col8, col9 = st.columns([2,1,1,1,1,1,1,1,1])

        with col1:
            st.markdown(
                "<p style='font-size:xx-small; margin-top: 5px; margin-bottom: 20px;'>Spiller</p>",
                unsafe_allow_html=True
            )

        with col2:
            st.markdown(
                "<p style='font-size:xx-small; margin-top: 5px; margin-bottom: 20px;'>Holdtræning</p>",
                unsafe_allow_html=True
            )

        with col3:
            st.markdown(
                "<p style='font-size:xx-small; margin-top: 5px; margin-bottom: 20px;'>Holdvideo</p>",
                unsafe_allow_html=True
            )

        with col4:
            st.markdown(
                "<p style='font-size:xx-small; margin-top: 5px; margin-bottom: 20px;'>Hold performance</p>",
                unsafe_allow_html=True
            )

        with col8:
            st.markdown(
                "<p style='font-size:xx-small; margin-top: 5px; margin-bottom: 20px;'>Individuel træning</p>",
                unsafe_allow_html=True
            )

        with col6:
            st.markdown(
                "<p style='font-size:xx-small; margin-top: 5px; margin-bottom: 20px;'>Individuel video</p>",
                unsafe_allow_html=True
            )

        with col7:
            st.markdown(
                "<p style='font-size:xx-small; margin-top: 5px; margin-bottom: 20px;'>Ind. performance</p>",
                unsafe_allow_html=True
            )

        with col5:
            st.markdown(
                "<p style='font-size:xx-small; margin-top: 5px; margin-bottom: 20px;'>Styrketræning</p>",
                unsafe_allow_html=True
            )

        with col9:
            st.markdown(
                "<p style='font-size:xx-small; margin-top: 5px; margin-bottom: 20px;'>Afbud</p>",
                unsafe_allow_html=True
            )
        for player in navne:
            col1, col2,col3,col4, col5,col6,col7,col8,col9 = st.columns([2,1,1,1,1,1,1,1,1])
            data.loc[player, "Dato"] = dato
            data.loc[player, "Træningsgruppe"] = træningshold
            data.loc[player, "Spillerens årgang"] = årgang
            data.loc[player, "Spiller"] = player

            with col1:
                st.markdown(f"<p style='font-size:xx-small; margin-top: -15px; margin-bottom: -15px; font-weight: bold;'>{player}</p>", unsafe_allow_html=True)

            with col2:
                data.loc[player, "Holdtræning"] = st.checkbox('Holdtræning', key=f"{player}_Holdtræning", value=(holdtræning_varighed > 0),label_visibility='collapsed')
                if data.loc[player, "Holdtræning"]:
                    data[f"{player} Holdtræning minutter"] = st.number_input("Holdtræning varighed", min_value=0, value=holdtræning_varighed, key=f"{player} Holdtræning minutter",label_visibility='collapsed')
                    data[f"{player} Holdtræning kommentar"] = st.text_input("Holdtræning kommentar", key=f"{player}_Holdtræning kommentar",label_visibility='collapsed')

                st.markdown(
                    f"""
                    <style>
                        /* Reduce padding, adjust font size, and line height for select boxes */
                        .st-cc, .st-ag, .st-eb label, .st-ec, .st-ek {{
                            padding: 0.1px;
                            font-size: 10px;
                            line-height: 1.3;
                            margin-top: 0px;
                            margin-bottom 0px;
                        }}
                    </style>
                    """,
                    unsafe_allow_html=True)


            with col3:
                data.loc[player, "Holdvideo"] = st.checkbox('Holdvideo', key=f"{player} Holdvideo", value=(holdvideo_varighed > 0),label_visibility='collapsed')
                if data.loc[player, "Holdvideo"]:
                    data[f"{player} Holdvideo minutter"] = st.number_input(f"Holdvideo minutter", value=holdvideo_varighed, key=f"{player} Holdvideo minutter",label_visibility='collapsed')
                    data[f"{player} Holdvideo kommentar"] = st.text_input(f"Holdvideo kommentarer", key=f"{player}_Holdvideo kommentar",label_visibility='collapsed')

            with col8:
                data.loc[player, "Individuel træning"] = st.checkbox('Individuel træning', key=f"{player} Individuel træning",label_visibility='collapsed')
                if data.loc[player, "Individuel træning"]:
                    data[f"{player} Individuel træning minutter"] = st.number_input(f"Individuel træning minutter",value=40, key=f"{player} Individuel træning minutter",label_visibility='collapsed')
                    data[f"{player} Individuel træning kommentar"] = st.text_input(f"Individuel træning kommentar", key=f"{player}_Individuel træning kommentar",label_visibility='collapsed')

            with col6:
                data.loc[player, "Individuel video"] = st.checkbox('Individuel video', key=f"{player} Individuel video",label_visibility='collapsed')
                if data.loc[player, "Individuel video"]:
                    data[f"{player} Individuel video minutter"] = st.number_input(f"Individuel video",value=15, key=f"{player} Individuel video minutter",label_visibility='collapsed')
                    data[f"{player} Individuel video kommentar"] = st.text_input(f"Individuel video kommentar", key=f"{player} Individuel video kommentar",label_visibility='collapsed')

            with col4:
                data.loc[player, "Hold performance"] = st.checkbox('Holdperformance', key=f"{player} Holdperformance", value=(holdperformance_varighed > 0),label_visibility='collapsed')
                if data.loc[player, "Hold performance"]:
                    data[f"{player} Hold performance minutter"] = st.number_input(f"Hold performance minutter", 0, value=holdperformance_varighed, key=f"{player} Holdperformance minutter",label_visibility='collapsed')
                    data[f"{player} Hold performance kommentar"] = st.text_input(f"Hold performance kommentar", key=f"{player} Hold performance kommentar",label_visibility='collapsed')

            with col7:
                data.loc[player, "Individuel performance"] = st.checkbox('Individuel performance', key=f"{player} Individuel performance",label_visibility='collapsed')
                if data.loc[player, "Individuel performance"]:
                    data[f"{player} Individuel performance minutter"] = st.number_input(f"Individuel performance minutter",value=15, key=f"{player} Individuel performance minutter",label_visibility='collapsed')
                    data[f"{player} Individuel performance kommentar"] = st.text_input(f"Individuel performance kommentar", key=f"{player} Individuel performance kommentar",label_visibility='collapsed')

            with col5:
                data.loc[player, "Styrketræning"] = st.checkbox('Styrketræning', key=f"{player} Styrketræning",value = styrketræning_varighed,label_visibility='collapsed')
                if data.loc[player, "Styrketræning"]:
                    data[f"{player} Styrketræning minutter"] = st.number_input(f"Styrketræning minutter",value=styrketræning_varighed, key=f"{player} Styrketræning minutter",label_visibility='collapsed')
                    data[f"{player} Styrketræning kommentar"] = st.text_input(f"Styrketræning kommentar", key=f"{player} Styrketræning kommentar",label_visibility='collapsed')

            with col1:
                if data.loc[player, "Holdtræning"] or data.loc[player, "Holdvideo"] or data.loc[player, "Hold performance"] or data.loc[player, "Individuel træning"] or data.loc[player, "Individuel video"] or data.loc[player, "Individuel performance"] or data.loc[player, "Styrketræning"] or data.loc[player, "Afbud"]:
                    st.markdown(f"<p style='font-size:xx-small; margin-top: -15px; margin-bottom: -15px;'>Tid</p>", unsafe_allow_html=True)
                    st.markdown(f"<p style='font-size:xx-small; margin-top: -15px; margin-bottom: -15px;'>Kommentar</p>", unsafe_allow_html=True)

            with col9:
                data.loc[player, "Afbud"] = st.checkbox('Afbud', key=f"{player} Afbud", value=data.loc[player, "Afbud"],label_visibility='collapsed')
                if data.loc[player, "Afbud"]:
                    # Hvis afbud er markeret, nulstil andre træningstyper for denne spiller
                    for Kamp_type in Kamp_types:
                        if Kamp_type != "Afbud":
                            data.loc[player, Kamp_type] = False

                    data[f"{player}_Afbud_årsag"] = st.selectbox(f"Årsag", ['Sygdom', 'Skadet - i campus','Skadet - sidder over','Skadet - ved fys', 'DBU samling','Skole', 'Andet afbud'], key=f"{player}_Afbud_årsag",label_visibility='collapsed')

            if data.loc[player, "Afbud"]:
            # Set all minutes columns for the player to 0
                for column in data.columns:
                    if "minutter" in column:
                        data.loc[player, column] = 0
           
            if data.loc[player, "Afbud"]:
                data.loc[player,"Træningsgruppe"] = ''

        
        columns_to_keep = ['Dato', 'Træningsgruppe', 'Spillerens årgang', 'Spiller']
        hold_training_columns = [col for col in data.columns if 'Holdtræning minutter' in col]
        hold_training_kom_columns = [col for col in data.columns if 'Holdtræning kommentar' in col]
        holdvideo_columns = [col for col in data.columns if 'Holdvideo minutter' in col]
        holdvideo_kom_columns = [col for col in data.columns if 'Holdvideo kommentar' in col]
        holdperformance_columns = [col for col in data.columns if 'Hold performance minutter' in col]
        holdperformance_kom_columns = [col for col in data.columns if 'Hold performance kommentar' in col]
        individuelperformance_columns = [col for col in data.columns if 'Individuel performance minutter' in col]
        individuelperformance_kom_columns = [col for col in data.columns if 'Individuel performance kommentar' in col]
        indtræning_columns = [col for col in data.columns if 'Individuel træning minutter' in col]
        indtræning_kom_columns = [col for col in data.columns if 'Individuel træning kommentar' in col]        
        indvideo_columns = [col for col in data.columns if 'Individuel video minutter' in col]
        indvideo_kom_columns = [col for col in data.columns if 'Individuel video kommentar' in col]
        styrketræning_columns = [col for col in data.columns if 'Styrketræning minutter' in col]
        styrketræning_kom_columns = [col for col in data.columns if 'Styrketræning kommentar' in col]
        Afbud_årsag_columns = [col for col in data.columns if '_Afbud_årsag' in col]

        new_df = data[columns_to_keep + hold_training_columns + hold_training_kom_columns + holdvideo_columns + holdvideo_kom_columns + holdperformance_columns + holdperformance_kom_columns + individuelperformance_columns + individuelperformance_kom_columns + indtræning_columns + indtræning_kom_columns + indvideo_columns + indvideo_kom_columns + styrketræning_columns + styrketræning_kom_columns + Afbud_årsag_columns].copy()

        melted_df = pd.melt(new_df, id_vars=columns_to_keep, 
                            value_vars=hold_training_columns + hold_training_kom_columns + holdvideo_columns + holdvideo_kom_columns + holdperformance_columns + holdperformance_kom_columns + individuelperformance_columns + individuelperformance_kom_columns + indtræning_columns + indtræning_kom_columns + indvideo_columns + indvideo_kom_columns + styrketræning_columns + styrketræning_kom_columns + Afbud_årsag_columns, 
                            var_name='Kamp_type', value_name='Kamp_minutter')

        filtered_df = melted_df[melted_df.apply(lambda x: x['Spiller'] in x['Kamp_type'], axis=1)]
        
        holdtræning_df = filtered_df[['Dato', 'Spiller', 'Træningsgruppe', 'Spillerens årgang', 'Kamp_minutter']][filtered_df['Kamp_type'].str.contains('Holdtræning minutter')]
        holdtræning_kom_df = filtered_df[['Dato', 'Spiller', 'Træningsgruppe', 'Spillerens årgang', 'Kamp_minutter']][filtered_df['Kamp_type'].str.contains('Holdtræning kommentar')]
        holdvideo_df = filtered_df[['Dato', 'Spiller', 'Træningsgruppe', 'Spillerens årgang', 'Kamp_minutter']][filtered_df['Kamp_type'].str.contains('Holdvideo minutter')]
        holdvideo_kom_df = filtered_df[['Dato', 'Spiller', 'Træningsgruppe', 'Spillerens årgang', 'Kamp_minutter']][filtered_df['Kamp_type'].str.contains('Holdvideo kommentar')]
        holdperformance_df = filtered_df[['Dato', 'Spiller', 'Træningsgruppe', 'Spillerens årgang', 'Kamp_minutter']][filtered_df['Kamp_type'].str.contains('Hold performance minutter')]
        holdperformance_kom_df = filtered_df[['Dato', 'Spiller', 'Træningsgruppe', 'Spillerens årgang', 'Kamp_minutter']][filtered_df['Kamp_type'].str.contains('Hold performance kommentar')]
        indperformance_df = filtered_df[['Dato', 'Spiller', 'Træningsgruppe', 'Spillerens årgang', 'Kamp_minutter']][filtered_df['Kamp_type'].str.contains('Individuel performance minutter')]
        indperformance_kom_df = filtered_df[['Dato', 'Spiller', 'Træningsgruppe', 'Spillerens årgang', 'Kamp_minutter']][filtered_df['Kamp_type'].str.contains('Individuel performance kommentar')]
        indtræning_df = filtered_df[['Dato', 'Spiller', 'Træningsgruppe', 'Spillerens årgang', 'Kamp_minutter']][filtered_df['Kamp_type'].str.contains('Individuel træning minutter')]
        indtræning_kom_df = filtered_df[['Dato', 'Spiller', 'Træningsgruppe', 'Spillerens årgang', 'Kamp_minutter']][filtered_df['Kamp_type'].str.contains('Individuel træning kommentar')]
        indvideo_df = filtered_df[['Dato', 'Spiller', 'Træningsgruppe', 'Spillerens årgang', 'Kamp_minutter']][filtered_df['Kamp_type'].str.contains('Individuel video minutter')]
        indvideo_kom_df = filtered_df[['Dato', 'Spiller', 'Træningsgruppe', 'Spillerens årgang', 'Kamp_minutter']][filtered_df['Kamp_type'].str.contains('Individuel video kommentar')]
        Styrke_df = filtered_df[['Dato', 'Spiller', 'Træningsgruppe', 'Spillerens årgang', 'Kamp_minutter']][filtered_df['Kamp_type'].str.contains('Styrketræning minutter')]
        Styrke_kom_df = filtered_df[['Dato', 'Spiller', 'Træningsgruppe', 'Spillerens årgang', 'Kamp_minutter']][filtered_df['Kamp_type'].str.contains('Styrketræning kommentar')]
        Afbud_årsag_df = filtered_df[['Dato', 'Spiller', 'Træningsgruppe', 'Spillerens årgang', 'Kamp_minutter']][filtered_df['Kamp_type'].str.contains('_Afbud_årsag')]
        
        
        holdtræning_df = holdtræning_df.rename(columns={'Kamp_minutter': 'Holdtræning minutter'})
        holdtræning_kom_df = holdtræning_kom_df.rename(columns={'Kamp_minutter': 'Holdtræning kommentar'})
        holdvideo_df = holdvideo_df.rename(columns={'Kamp_minutter': 'Holdvideo minutter'})
        holdvideo_kom_df = holdvideo_kom_df.rename(columns={'Kamp_minutter': 'Holdvideo kommentar'})
        holdperformance_df = holdperformance_df.rename(columns={'Kamp_minutter': 'Holdperformance minutter'})
        holdperformance_kom_df = holdperformance_kom_df.rename(columns={'Kamp_minutter': 'Holdperformance kommentar'})
        indperformance_df = indperformance_df.rename(columns={'Kamp_minutter': 'Individuel performance minutter'})
        indperformance_kom_df = indperformance_kom_df.rename(columns={'Kamp_minutter': 'Individuel performance kommentar'})
        indtræning_df = indtræning_df.rename(columns={'Kamp_minutter': 'Individuel træning minutter'})
        indtræning_kom_df = indtræning_kom_df.rename(columns={'Kamp_minutter': 'Individuel træning kommentar'})
        indvideo_df = indvideo_df.rename(columns={'Kamp_minutter': 'Individuel video minutter'})
        indvideo_kom_df = indvideo_kom_df.rename(columns={'Kamp_minutter': 'Individuel video kommentar'})
        Styrke_df = Styrke_df.rename(columns={'Kamp_minutter': 'Styrketræning minutter'})
        Styrke_kom_df = Styrke_kom_df.rename(columns={'Kamp_minutter': 'Styrketræning kommentar'})
        Afbud_årsag_df = Afbud_årsag_df.rename(columns={'Kamp_minutter' : 'Afbud årsag'})

        merged_df = pd.merge(holdtræning_df, holdtræning_kom_df, on=['Dato', 'Spiller', 'Træningsgruppe', 'Spillerens årgang'], how='outer')
        merged_df = pd.merge(merged_df, holdvideo_df, on=['Dato', 'Spiller', 'Træningsgruppe', 'Spillerens årgang'], how='outer')
        merged_df = pd.merge(merged_df, holdvideo_kom_df, on=['Dato', 'Spiller', 'Træningsgruppe', 'Spillerens årgang'], how='outer')
        merged_df = pd.merge(merged_df, holdperformance_df, on=['Dato', 'Spiller', 'Træningsgruppe', 'Spillerens årgang'], how='outer')
        merged_df = pd.merge(merged_df, holdperformance_kom_df, on=['Dato', 'Spiller', 'Træningsgruppe', 'Spillerens årgang'], how='outer')
        merged_df = pd.merge(merged_df, Styrke_df, on=['Dato', 'Spiller', 'Træningsgruppe', 'Spillerens årgang'], how='outer')   
        merged_df = pd.merge(merged_df, Styrke_kom_df, on=['Dato', 'Spiller', 'Træningsgruppe', 'Spillerens årgang'], how='outer')   
        merged_df = pd.merge(merged_df, indperformance_df, on=['Dato', 'Spiller', 'Træningsgruppe', 'Spillerens årgang'], how='outer')
        merged_df = pd.merge(merged_df, indperformance_kom_df, on=['Dato', 'Spiller', 'Træningsgruppe', 'Spillerens årgang'], how='outer')
        merged_df = pd.merge(merged_df, indtræning_df, on=['Dato', 'Spiller', 'Træningsgruppe', 'Spillerens årgang'], how='outer')
        merged_df = pd.merge(merged_df, indtræning_kom_df, on=['Dato', 'Spiller', 'Træningsgruppe', 'Spillerens årgang'], how='outer')
        merged_df = pd.merge(merged_df, indvideo_df, on=['Dato', 'Spiller', 'Træningsgruppe', 'Spillerens årgang'], how='outer')
        merged_df = pd.merge(merged_df, indvideo_kom_df, on=['Dato', 'Spiller', 'Træningsgruppe', 'Spillerens årgang'], how='outer')
        merged_df = pd.merge(merged_df, Afbud_årsag_df, on=['Dato', 'Spiller', 'Træningsgruppe', 'Spillerens årgang'], how='outer')

        #merged_df = merged_df.set_index('Spiller')
        st.write(merged_df)

        import json
        import os.path
        json_filename = 'træningsregistrering.json'
        if st.button('Gem dataene'):
            if not os.path.exists(json_filename) or os.path.getsize(json_filename) == 0:
                with open(json_filename, 'w') as f:
                    json.dump(merged_df.to_dict(orient='records'), f, indent=4)
                st.write("Dataene er gemt i træningsdata")

            else:
                existing_data = []
                with open(json_filename, 'r') as f:
                    try:
                        existing_data = json.load(f)
                    except json.JSONDecodeError:
                        st.error("Fejl: JSON-filen har ugyldig struktur.")

                existing_data += merged_df.to_dict(orient='records')

                with open(json_filename, 'w') as f:
                    json.dump(existing_data, f, indent=4)
                st.write("Nye data er tilføjet til træningsdata")


        all_data = []
        if os.path.exists(json_filename) and os.path.getsize(json_filename) > 0:
            with open(json_filename, 'r') as f:
                try:
                    all_data = json.load(f)
                except json.JSONDecodeError:
                    st.error("Fejl: JSON-filen er tom eller har ugyldig struktur.")

        all_df = pd.DataFrame(all_data)            
        st.write(all_df)

    def Fysisk_træning():
        import pandas as pd
        import streamlit as st
        import seaborn as sns
        import matplotlib.pyplot as plt
        import openpyxl as xlsxwriter
        from pandas import DataFrame
        import plotly.graph_objects as go
        from datetime import datetime

        dforiginal = pd.read_csv(r'Fysisk data/samlet gps data.csv')
        dforiginal = dforiginal.loc[dforiginal['Split Name'] =='all']
        
        Højintens_løb = dforiginal['Distance in Speed Zone 4  (km)']
        Sprint = dforiginal['Distance in Speed Zone 5  (km)']
        Hårde_accelerationer = dforiginal['Accelerations Zone Count: 3 - 4 m/s/s'] + dforiginal['Accelerations Zone Count: > 4 m/s/s']
        Hårde_deccelerationer = dforiginal['Deceleration Zone Count: 3 - 4 m/s/s'] + dforiginal['Deceleration Zone Count: > 4 m/s/s']
        Tid_med_høj_puls = (dforiginal['Time in HR Load Zone 85% - 96% Max HR (secs)'] + dforiginal['Time in HR Load Zone 96% - 100% Max HR (secs)'])/60
        dforiginal.insert(loc = 42, column = 'Højintens løb', value= Højintens_løb)
        dforiginal.insert(loc = 43, column = 'Sprint', value= Sprint)
        dforiginal.insert(loc = 44, column = 'Hårde Accelerationer', value = Hårde_accelerationer)
        dforiginal.insert(loc = 45, column = 'Hårde deccelerationer', value=Hårde_deccelerationer)
        dforiginal.insert(loc = 46, column = 'Tid med høj puls', value=Tid_med_høj_puls)
        dforiginal['Date'] = dforiginal['Date'].astype(str)
        df_GPS = dforiginal[['Date','Player Name','Ugenummer','Distance (km)','Top Speed (km/h)','Højintens løb','Sprint','Hårde Accelerationer','Hårde deccelerationer','Tid med høj puls','Trup']]
        Trup = ['U17','U19']
        option0 = st.selectbox('Vælg trup',Trup)
        df_GPS = df_GPS.loc[df_GPS.loc[df_GPS['Trup'] == option0,'Trup'].index.values]
        df_GPSgennemsnit1 = df_GPS[['Ugenummer','Player Name','Date','Distance (km)', 'Top Speed (km/h)', 'Højintens løb', 'Sprint', 'Hårde Accelerationer', 'Hårde deccelerationer','Tid med høj puls']]
        df_GPSgennemsnit = df_GPSgennemsnit1.groupby(['Date']).mean(numeric_only=True)
        df_GPSgennemsnit['Ugenummer'] = df_GPSgennemsnit['Ugenummer'].astype(int)
        Ugenummer = df_GPSgennemsnit['Ugenummer'].drop_duplicates()
        df = df_GPSgennemsnit
        option2 = st.multiselect('Vælg ugenummer',Ugenummer)
        if len(option2) > 0:
            temp_select = option2
        else:
            temp_select = Ugenummer

        df_GPSgennemsnit = df.loc[df.loc[df.Ugenummer.isin(temp_select),'Ugenummer'].index.values]
        
        df_GPSgennemsnit = df_GPSgennemsnit.sort_values(by='Date', ascending=False)
        df_GPSgennemsnit = df_GPSgennemsnit.reset_index()
        columns_to_plot = ['Sprint','Distance (km)','Top Speed (km/h)','Højintens løb','Hårde Accelerationer','Hårde deccelerationer','Tid med høj puls']

        fig_GPS = go.Figure()
        for column in columns_to_plot:
            fig_GPS.add_trace(go.Scatter(
                x=df_GPSgennemsnit['Date'],
                y=df_GPSgennemsnit[column],
                mode='lines',
                name=column
            ))

            
            fig_GPS.update_layout(
            template='plotly_dark',
            title = 'Trup gennemsnit pr. dag',
            legend=dict(
                orientation="h",
                font=dict(
                    size=8
                )
            ))


        st.plotly_chart(fig_GPS,use_container_width=True)

        st.write('Tabel for trupgennemsnit pr. dag')
        st.dataframe(df_GPSgennemsnit,hide_index=True)
        spillere = df_GPSgennemsnit1.drop_duplicates(subset=['Player Name'])
        option4 = st.selectbox('Vælg spiller',spillere['Player Name'])
        
        df = df_GPSgennemsnit1.loc[df_GPSgennemsnit1.loc[df_GPSgennemsnit1['Player Name'] == option4,'Player Name'].index.values]
        df = df.loc[df.loc[df.Ugenummer.isin(temp_select),'Ugenummer'].index.values]

        df = df[df['Distance (km)'] !=0]
        df['Date'] = df['Date'].astype(str)
        df = df.reset_index()
        #df = df.rename(columns={'Date':'index'}).set_index('index')
        afvigelser = df.copy()
        afvigelser['Distance (km)'] = df['Distance (km)'] / df_GPSgennemsnit['Distance (km)']
        afvigelser['Top Speed (km/h)'] = df['Top Speed (km/h)'] / df_GPSgennemsnit['Top Speed (km/h)']
        afvigelser['Højintens løb'] = df['Højintens løb'] / df_GPSgennemsnit['Højintens løb']
        afvigelser['Sprint'] = df['Sprint'] / df_GPSgennemsnit['Sprint']
        afvigelser['Hårde Accelerationer'] = df['Hårde Accelerationer'] / df_GPSgennemsnit['Hårde Accelerationer']
        afvigelser['Hårde deccelerationer'] = df['Hårde deccelerationer'] / df_GPSgennemsnit['Hårde deccelerationer']
        afvigelser['Tid med høj puls'] = df['Tid med høj puls'] / df_GPSgennemsnit['Tid med høj puls']
        afvigelser = afvigelser.sort_values(by='Date', ascending=False)
        df = df.sort_values(by='Date', ascending=False)

        columns_to_plot = ['Sprint','Distance (km)','Top Speed (km/h)','Højintens løb','Hårde Accelerationer','Hårde deccelerationer','Tid med høj puls']

        fig_GPS = go.Figure()
        for column in columns_to_plot:
            fig_GPS.add_trace(go.Scatter(
                x=afvigelser['Date'],
                y=afvigelser[column],
                mode='lines',
                name=column
            ))

            
            fig_GPS.update_layout(
            template='plotly_dark',
            title = 'Afvigelser for den valgte spiller i forhold til truppens gennemsnit (1 = trupgennemsnittet for dagen)',
            legend=dict(
                orientation="h",
                font=dict(
                    size=8
                )
            ))


        st.plotly_chart(fig_GPS,use_container_width=True)
        st.write('Tabel for afvigelser (1 = trupgennemsnittet for dagen)')
        afvigelser = afvigelser.drop(columns = 'index')
        st.dataframe(afvigelser,hide_index=True)
        st.write('Absolutte tal for den valgte spiller')
        df = df.drop(columns = 'index')
        st.dataframe(df,hide_index=True)
        
        df = pd.read_csv(r'Fysisk data/U13 PHV.csv')
        df = df.drop(df.index[:6]).reset_index(drop=True)
        df.columns = df.iloc[0]
        df = df[1:].reset_index(drop=True)
        df1 = pd.read_csv(r'Fysisk data/U14 PHV.csv')
        df1 = df1.drop(df1.index[:6]).reset_index(drop=True)
        df1.columns = df1.iloc[0]
        df1 = df1[1:].reset_index(drop=True)
        df2 = pd.read_csv(r'Fysisk data/U15 PHV.csv')
        df2 = df2.drop(df2.index[:6]).reset_index(drop=True)
        df2.columns = df2.iloc[0]
        df2 = df2[1:].reset_index(drop=True)

        df = pd.concat([df,df1,df2],ignore_index=True)
        df = df.dropna(subset=['Last Name'])
        df['Fødselsdato'] = pd.to_datetime(df['Date of Birth (dd-mm-yy)']).dt.strftime('%d-%m-%Y')
        df['Navn'] = df['First Name'] +' '+ df['Last Name']
        df['Age @ PHV'] = df['Age @ PHV'].astype(float)
        df['PHV tal'] = df['Age @ PHV'].round(2)
        df = df[['Navn','Fødselsdato','PHV tal']]
        df['Fødselsdato'] = pd.to_datetime(df['Fødselsdato'], format='%d-%m-%Y')
        today = datetime.today()
        df['Alder'] = (today - df['Fødselsdato']).dt.days/365.25
        df['Fødselsdato'] = pd.to_datetime(df['Fødselsdato']).dt.strftime('%d-%m-%Y')
        df['Modenhed'] = df['Alder'] - df['PHV tal']
        df = df.sort_values(by='Modenhed',ascending=False)
        df = df[(df['Modenhed'] > -0.4) & (df['Modenhed'] < 0.4)]
        st.write('Spillere med et PHV tal mellem -0,4 og 0,4')
        st.dataframe(df,hide_index=True,use_container_width=True)

    def Teamsheet():
        import streamlit as st
        def U13():
            import pandas as pd
            from datetime import date
            import numpy as np
            import json
            import os
            json_filename = 'træningsregistrering.json'

            # Code in another part of your Streamlit app to read the JSON data into a DataFrame
            if os.path.exists(json_filename) and os.path.getsize(json_filename) > 0:
                with open(json_filename, 'r') as f:
                    try:
                        data = json.load(f)
                        df = pd.DataFrame(data)
                    except json.JSONDecodeError:
                        st.error("Fejl: JSON-filen har ugyldig struktur.")
            else:
                st.warning("Filen er ikke tilgængelig eller tom.")
            df = df[df['Spillerens årgang'] == 'U13']
            st.dataframe(df,hide_index=True)
            df = pd.read_csv(r'Fysisk data/U13 PHV.csv')
            df = df.drop(df.index[:6])
            df.columns = df.iloc[0]
            df = df.drop(df.index[:1])
            df['Navn'] = df['First Name'] + " " + df['Last Name']
            df = df[['Navn','Age @ PHV','Date of Birth (dd-mm-yy)']]
            df.dropna(subset=['Navn'], inplace=True)
            df['Date of Birth (dd-mm-yy)'] = pd.to_datetime(df['Date of Birth (dd-mm-yy)'])
            today = pd.Timestamp(date.today())
            df['Alder'] = (today- df['Date of Birth (dd-mm-yy)'])/ np.timedelta64(1,'Y')
            df['Alder'] = pd.to_numeric(df['Alder'])
            df['Age @ PHV'] = pd.to_numeric(df['Age @ PHV'])
            df['Modenhed'] = df['Alder'] - df['Age @ PHV']
            df = df.sort_values(by='Modenhed',ascending=False)
            
            st.dataframe(df,hide_index=True)
            
        def U14():
            import pandas as pd
            from datetime import date
            import numpy as np
            import json
            import os
            json_filename = 'træningsregistrering.json'

            # Code in another part of your Streamlit app to read the JSON data into a DataFrame
            if os.path.exists(json_filename) and os.path.getsize(json_filename) > 0:
                with open(json_filename, 'r') as f:
                    try:
                        data = json.load(f)
                        df = pd.DataFrame(data)
                    except json.JSONDecodeError:
                        st.error("Fejl: JSON-filen har ugyldig struktur.")
            else:
                st.warning("Filen er ikke tilgængelig eller tom.")
            df = df[df['Spillerens årgang'] == 'U14']
            st.dataframe(df,hide_index=True)
            df = pd.read_csv(r'Fysisk data/U14 PHV.csv')
            df = df.drop(df.index[:6])
            df.columns = df.iloc[0]
            df = df.drop(df.index[:1])
            df['Navn'] = df['First Name'] + " " + df['Last Name']
            df = df[['Navn','Age @ PHV','Date of Birth (dd-mm-yy)']]
            df.dropna(subset=['Navn'], inplace=True)
            df['Date of Birth (dd-mm-yy)'] = pd.to_datetime(df['Date of Birth (dd-mm-yy)'])
            today = pd.Timestamp(date.today())
            df['Alder'] = (today- df['Date of Birth (dd-mm-yy)'])/ np.timedelta64(1,'Y')
            df['Alder'] = pd.to_numeric(df['Alder'])
            df['Age @ PHV'] = pd.to_numeric(df['Age @ PHV'])
            df['Modenhed'] = df['Alder'] - df['Age @ PHV']
            df = df.sort_values(by='Modenhed',ascending=False)
            
            st.dataframe(df,hide_index=True)
                   
        def U15():
            import pandas as pd
            import csv
            import streamlit as st
            import numpy as np
            import json
            from datetime import datetime
            df = pd.read_csv('Teamsheet egne kampe U15.csv')
            kampe = df['label']
            option = st.multiselect('Vælg kamp (Hvis ingen kamp er valgt, vises gennemsnit for alle)',kampe)
            if len(option) > 0:
                temp_select = option
            else:
                temp_select = kampe

            dfsorteredekampe = df.loc[df.loc[df.label.isin(temp_select),'label'].index.values]
            dfsorteredekampe = dfsorteredekampe.iloc[: , 1:]
            #dfsorteredekampe['date'] = dfsorteredekampe['date'].astype(str)
            #dfsorteredekampe['date'] = dfsorteredekampe['date'].str.replace(r'\sGMT.*$', '', regex=True)
            #dfsorteredekampe['date'] = pd.to_datetime(dfsorteredekampe['date'], format="%B %d, %Y at %I:%M:%S %p")
            #dfsorteredekampe['date'] = dfsorteredekampe['date'].dt.strftime('%d-%m-%Y')
            dfsorteredekampe = dfsorteredekampe.transpose()
            dfoverskrifter = dfsorteredekampe[:2]
            dfsorteredekampe = dfsorteredekampe[2:].apply(pd.to_numeric, errors='coerce')
            dfsorteredekampe = pd.concat([dfoverskrifter,dfsorteredekampe])
            dfsorteredekampe = dfsorteredekampe.dropna(how='all')
            dfsorteredekampe = dfsorteredekampe.rename_axis('Parameter').astype(str)
            dfsorteredekampe = dfsorteredekampe.transpose()


            goals_cols = [col for col in dfsorteredekampe.columns if col.endswith('.goals')]
            shots_cols = [col for col in dfsorteredekampe.columns if col.endswith('.shots')]
            xg_cols = [col for col in dfsorteredekampe.columns if col.endswith('.xg')]
            duels_cols = [col for col in dfsorteredekampe.columns if col.endswith('.duels')]
            duelswon_cols = [col for col in dfsorteredekampe.columns if col.endswith('.duelsSuccessful')]
            possession_cols = [col for col in dfsorteredekampe.columns if col.endswith('.possessionPercent')]
            ppda_cols = [col for col in dfsorteredekampe.columns if col.endswith('.ppda')]

            # Create a new dataframe with the average values for each team
            team_data = {}
            for team in set([col.split('.')[1] for col in shots_cols]):
                team_goals = dfsorteredekampe[[col for col in goals_cols if(team) in col]].mean(axis=1)    
                team_shots = dfsorteredekampe[[col for col in shots_cols if(team) in col]].mean(axis=1)
                team_xg = dfsorteredekampe[[col for col in xg_cols if (team) in col]].mean(axis=1)
                team_duels = dfsorteredekampe[[col for col in duels_cols if (team) in col]].mean(axis=1)
                team_duelswon = dfsorteredekampe[[col for col in duelswon_cols if (team) in col]].mean(axis=1)
                team_possession = dfsorteredekampe[[col for col in possession_cols if (team) in col]].mean(axis=1)
                team_ppda = dfsorteredekampe[[col for col in ppda_cols if (team) in col]].mean(axis=1)

                team_data[team] = pd.concat([team_goals,team_shots, team_xg, team_duels,team_duelswon,team_possession,team_ppda], axis=1)
                
            team_df = pd.concat(team_data, axis=0, keys=team_data.keys())
            team_df.columns = ['Goals','Shots', 'Xg', 'Duels','Duels won','Possession %','PPDA']
            team_df = team_df.groupby(level=0).mean()

            st.write('Generelle stats')
            team_df= team_df.round(decimals=2)
            st.dataframe(team_df)

            forward_passes_cols = [col for col in dfsorteredekampe.columns if col.endswith('.forwardPasses')]
            forward_passes_successful_cols = [col for col in dfsorteredekampe.columns if col.endswith('.forwardPassesSuccessful')]
            passes_cols = [col for col in dfsorteredekampe.columns if col.endswith('.passes')]
            touches_in_box_cols = [col for col in dfsorteredekampe.columns if col.endswith('.touchesInBox')]
            xg_cols = [col for col in dfsorteredekampe.columns if col.endswith('.xg')]
            xgpershot_cols = [col for col in dfsorteredekampe.columns if col.endswith('.xgPerShot')]
            dzshots_cols = [col for col in dfsorteredekampe.columns if col.endswith('.shotsFromDangerZone')]
            possessionantal_cols = [col for col in dfsorteredekampe.columns if col.endswith('.possessionNumber')]
            possessionanmodstandershalvdel_cols = [col for col in dfsorteredekampe.columns if col.endswith('.reachingOpponentHalf')]
            possessionanmodstandersfelt_cols = [col for col in dfsorteredekampe.columns if col.endswith('.reachingOpponentBox')]
            challenge_intensity_cols = [col for col in dfsorteredekampe.columns if col.endswith('.challengeIntensity')]
            recoveries_cols = [col for col in dfsorteredekampe.columns if col.endswith('.recoveriesTotal')]
            opponenthalfrecoveries_cols = [col for col in dfsorteredekampe.columns if col.endswith('.opponentHalfRecoveries')]
            ppda_cols = [col for col in dfsorteredekampe.columns if col.endswith('.ppda')]

            # Create a new dataframe with the average values for each team
            team_data_målbare = {}
            for team in set([col.split('.')[1] for col in shots_cols]):
                team_forward_passes = dfsorteredekampe[[col for col in forward_passes_cols if(team) in col]].mean(axis=1)    
                team_forward_passes_successful = dfsorteredekampe[[col for col in forward_passes_successful_cols if(team) in col]].mean(axis=1)
                team_passes = dfsorteredekampe[[col for col in passes_cols if (team) in col]].mean(axis=1)
                team_touches_in_box = dfsorteredekampe[[col for col in touches_in_box_cols if (team) in col]].mean(axis=1)
                team_xg = dfsorteredekampe[[col for col in xg_cols if (team) in col]].mean(axis=1)
                team_xgpershot = dfsorteredekampe[[col for col in xgpershot_cols if (team) in col]].mean(axis=1)
                team_dzshots = dfsorteredekampe[[col for col in dzshots_cols if (team) in col]].mean(axis=1)
                team_possessionantal = dfsorteredekampe[[col for col in possessionantal_cols if (team) in col]].mean(axis=1)
                team_possessionmodstandershalvdel = dfsorteredekampe[[col for col in possessionanmodstandershalvdel_cols if (team) in col]].mean(axis=1)
                team_possessionmodstandersfelt = dfsorteredekampe[[col for col in possessionanmodstandersfelt_cols if (team) in col]].mean(axis=1)
                team_challenge_intensity = dfsorteredekampe[[col for col in challenge_intensity_cols if (team) in col]].mean(axis=1)
                team_recoveries = dfsorteredekampe[[col for col in recoveries_cols if (team) in col]].mean(axis=1)
                team_opponenthalfrecoveries = dfsorteredekampe[[col for col in opponenthalfrecoveries_cols if (team) in col]].mean(axis=1)

                team_ppda = dfsorteredekampe[[col for col in ppda_cols if (team) in col]].mean(axis=1)

                team_data_målbare[team] = pd.concat([team_forward_passes,team_forward_passes_successful, team_passes, team_touches_in_box,team_xg,team_xgpershot,team_dzshots,team_possessionantal,team_possessionmodstandershalvdel,team_possessionmodstandersfelt,team_challenge_intensity,team_recoveries,team_opponenthalfrecoveries,team_ppda], axis=1)
                
            team_df_målbare = pd.concat(team_data_målbare, axis=0, keys=team_data_målbare.keys())
            team_df_målbare.columns = ['Forward passes','Forward passes successful', 'Passes', 'Touches in box','xG','xG/shot','Dangerzone shots','Antal possessions','Antal possessions der når modstanders halvdel','Antal possessions der når modstanders felt','Challenge intensity','Recoveries','Opp half recoveries','PPDA']
            team_df_målbare = team_df_målbare.groupby(level=0).mean()
            team_df_målbare['Forward pass %'] = (team_df_målbare['Forward passes successful']/team_df_målbare['Forward passes'])*100
            team_df_målbare['Forward pass share'] = (team_df_målbare['Forward passes']/team_df_målbare['Passes'])*100
            team_df_målbare['Forward pass score'] = team_df_målbare[['Forward pass share','Forward pass %']].mean(axis=1)
            team_df_målbare['Possession to opp box'] = team_df_målbare['Antal possessions der når modstanders felt']
            team_df_målbare['Possession to opp half %'] = (team_df_målbare['Antal possessions der når modstanders halvdel']/team_df_målbare['Antal possessions'])*100
            team_df_målbare['Possession to opp box %'] = (team_df_målbare['Antal possessions der når modstanders felt']/team_df_målbare['Antal possessions'])*100
            team_df_målbare = team_df_målbare[['Forward pass score','Touches in box','xG','xG/shot','Dangerzone shots','Possession to opp box','Possession to opp half %','Possession to opp box %','Challenge intensity','Recoveries','Opp half recoveries','PPDA']]
            team_df_målbare = team_df_målbare.round(decimals=3)
            hold = 'Horsens U15'
            team_df_målbare_andre_hold = team_df_målbare.drop(hold)
            team_df_målbare['xG against'] = team_df_målbare_andre_hold['xG'].mean()
            team_df_målbare['Danger zone shots against'] = team_df_målbare_andre_hold['Dangerzone shots'].mean()
            team_df_målbare['Touches in box against'] = team_df_målbare_andre_hold['Touches in box'].mean()
            team_df_målbare['Duels won %'] = (team_df['Duels won']/team_df['Duels'])*100
            mask = team_df_målbare.index.str.contains('Horsens')
            team_df_målbare = team_df_målbare[mask]
            team_df_målbare = team_df_målbare.round(decimals=2)

            import pandas as pd
            import csv
            import streamlit as st
            import numpy as np
            from datetime import datetime

            df = pd.read_csv('Teamsheet alle kampe U15.csv')

            dfsorteredeallekampe = df.iloc[: , 1:]
            dfsorteredeallekampe['date'] = dfsorteredeallekampe['date'].astype(str)
            dfsorteredeallekampe['date'] = dfsorteredeallekampe['date'].str.replace(r'\sGMT.*$', '', regex=True)
            dfsorteredeallekampe['date'] = pd.to_datetime(dfsorteredeallekampe['date'], format="%B %d, %Y at %I:%M:%S %p")
            dfsorteredeallekampe['date'] = dfsorteredeallekampe['date'].dt.strftime('%d-%m-%Y')
            dfsorteredeallekampe = dfsorteredeallekampe.transpose()
            dfoverskrifter = dfsorteredeallekampe[:2]
            dfsorteredeallekampe = dfsorteredeallekampe[2:].apply(pd.to_numeric, errors='coerce')
            dfsorteredeallekampe = pd.concat([dfoverskrifter,dfsorteredeallekampe])
            dfsorteredeallekampe = dfsorteredeallekampe.dropna(how='all')
            dfsorteredeallekampe = dfsorteredeallekampe.rename_axis('Parameter').astype(str)
            dfsorteredeallekampe = dfsorteredeallekampe.transpose()


            goals_cols = [col for col in dfsorteredeallekampe.columns if col.endswith('.goals')]
            shots_cols = [col for col in dfsorteredeallekampe.columns if col.endswith('.shots')]
            xg_cols = [col for col in dfsorteredeallekampe.columns if col.endswith('.xg')]
            duels_cols = [col for col in dfsorteredeallekampe.columns if col.endswith('.duels')]
            duelswon_cols = [col for col in dfsorteredeallekampe.columns if col.endswith('.duelsSuccessful')]
            possession_cols = [col for col in dfsorteredeallekampe.columns if col.endswith('.possessionPercent')]
            ppda_cols = [col for col in dfsorteredeallekampe.columns if col.endswith('.ppda')]

            # Create a new dataframe with the average values for each team
            team_data = {}
            for team in set([col.split('.')[1] for col in shots_cols]):
                team_goals = dfsorteredeallekampe[[col for col in goals_cols if(team) in col]].mean(axis=1)    
                team_shots = dfsorteredeallekampe[[col for col in shots_cols if(team) in col]].mean(axis=1)
                team_xg = dfsorteredeallekampe[[col for col in xg_cols if (team) in col]].mean(axis=1)
                team_duels = dfsorteredeallekampe[[col for col in duels_cols if (team) in col]].mean(axis=1)
                team_duelswon = dfsorteredeallekampe[[col for col in duelswon_cols if (team) in col]].mean(axis=1)
                team_possession = dfsorteredeallekampe[[col for col in possession_cols if (team) in col]].mean(axis=1)
                team_ppda = dfsorteredeallekampe[[col for col in ppda_cols if (team) in col]].mean(axis=1)

                team_data[team] = pd.concat([team_goals,team_shots, team_xg, team_duels,team_duelswon,team_possession,team_ppda], axis=1)
                
            team_df = pd.concat(team_data, axis=0, keys=team_data.keys())
            team_df.columns = ['Goals','Shots', 'Xg', 'Duels','Duels won','Possession %','PPDA']
            team_df = team_df.groupby(level=0).mean()
            team_df= team_df.round(decimals=2)


            forward_passes_cols = [col for col in dfsorteredeallekampe.columns if col.endswith('.forwardPasses')]
            forward_passes_successful_cols = [col for col in dfsorteredeallekampe.columns if col.endswith('.forwardPassesSuccessful')]
            passes_cols = [col for col in dfsorteredeallekampe.columns if col.endswith('.passes')]
            touches_in_box_cols = [col for col in dfsorteredeallekampe.columns if col.endswith('.touchesInBox')]
            xg_cols = [col for col in dfsorteredeallekampe.columns if col.endswith('.xg')]
            xgpershot_cols = [col for col in dfsorteredeallekampe.columns if col.endswith('.xgPerShot')]
            dzshots_cols = [col for col in dfsorteredeallekampe.columns if col.endswith('.shotsFromDangerZone')]
            possessionantal_cols = [col for col in dfsorteredeallekampe.columns if col.endswith('.possessionNumber')]
            possessionanmodstandershalvdel_cols = [col for col in dfsorteredeallekampe.columns if col.endswith('.reachingOpponentHalf')]
            possessionanmodstandersfelt_cols = [col for col in dfsorteredeallekampe.columns if col.endswith('.reachingOpponentBox')]
            challenge_intensity_cols = [col for col in dfsorteredeallekampe.columns if col.endswith('.challengeIntensity')]
            recoveries_cols = [col for col in dfsorteredeallekampe.columns if col.endswith('.recoveriesTotal')]
            opponenthalfrecoveries_cols = [col for col in dfsorteredeallekampe.columns if col.endswith('.opponentHalfRecoveries')]
            ppda_cols = [col for col in dfsorteredeallekampe.columns if col.endswith('.ppda')]

            # Create a new dataframe with the average values for each team
            team_data_målbare_alle = {}
            for team in set([col.split('.')[1] for col in shots_cols]):
                team_forward_passes = dfsorteredeallekampe[[col for col in forward_passes_cols if(team) in col]].mean(axis=1)    
                team_forward_passes_successful = dfsorteredeallekampe[[col for col in forward_passes_successful_cols if(team) in col]].mean(axis=1)
                team_passes = dfsorteredeallekampe[[col for col in passes_cols if (team) in col]].mean(axis=1)
                team_touches_in_box = dfsorteredeallekampe[[col for col in touches_in_box_cols if (team) in col]].mean(axis=1)
                team_xg = dfsorteredeallekampe[[col for col in xg_cols if (team) in col]].mean(axis=1)
                team_xgpershot = dfsorteredeallekampe[[col for col in xgpershot_cols if (team) in col]].mean(axis=1)
                team_dzshots = dfsorteredeallekampe[[col for col in dzshots_cols if (team) in col]].mean(axis=1)
                team_possessionantal = dfsorteredeallekampe[[col for col in possessionantal_cols if (team) in col]].mean(axis=1)
                team_possessionmodstandershalvdel = dfsorteredeallekampe[[col for col in possessionanmodstandershalvdel_cols if (team) in col]].mean(axis=1)
                team_possessionmodstandersfelt = dfsorteredeallekampe[[col for col in possessionanmodstandersfelt_cols if (team) in col]].mean(axis=1)
                team_challenge_intensity = dfsorteredeallekampe[[col for col in challenge_intensity_cols if (team) in col]].mean(axis=1)
                team_recoveries = dfsorteredeallekampe[[col for col in recoveries_cols if (team) in col]].mean(axis=1)
                team_opponenthalfrecoveries = dfsorteredeallekampe[[col for col in opponenthalfrecoveries_cols if (team) in col]].mean(axis=1)

                team_ppda = dfsorteredeallekampe[[col for col in ppda_cols if (team) in col]].mean(axis=1)

                team_data_målbare_alle[team] = pd.concat([team_forward_passes,team_forward_passes_successful, team_passes, team_touches_in_box,team_xg,team_xgpershot,team_dzshots,team_possessionantal,team_possessionmodstandershalvdel,team_possessionmodstandersfelt,team_challenge_intensity,team_recoveries,team_opponenthalfrecoveries,team_ppda], axis=1)
                
            team_df_målbare_alle = pd.concat(team_data_målbare_alle, axis=0, keys=team_data_målbare_alle.keys())
            team_df_målbare_alle.columns = ['Forward passes','Forward passes successful', 'Passes', 'Touches in box','xG','xG/shot','Dangerzone shots','Antal possessions','Antal possessions der når modstanders halvdel','Antal possessions der når modstanders felt','Challenge intensity','Recoveries','Opp half recoveries','PPDA']
            team_df_målbare_alle = team_df_målbare_alle.groupby(level=0).mean()
            team_df_målbare_alle['Forward pass %'] = (team_df_målbare_alle['Forward passes successful']/team_df_målbare_alle['Forward passes'])*100
            team_df_målbare_alle['Forward pass share'] = (team_df_målbare_alle['Forward passes']/team_df_målbare_alle['Passes'])*100
            team_df_målbare_alle['Forward pass score'] = team_df_målbare_alle[['Forward pass share','Forward pass %']].mean(axis=1)
            team_df_målbare_alle['Possession to opp box'] = team_df_målbare_alle['Antal possessions der når modstanders felt']
            team_df_målbare_alle['Possession to opp half %'] = (team_df_målbare_alle['Antal possessions der når modstanders halvdel']/team_df_målbare_alle['Antal possessions'])*100
            team_df_målbare_alle['Possession to opp box %'] = (team_df_målbare_alle['Antal possessions der når modstanders felt']/team_df_målbare_alle['Antal possessions'])*100
            team_df_målbare_alle = team_df_målbare_alle[['Forward pass score','Touches in box','xG','xG/shot','Dangerzone shots','Possession to opp box','Possession to opp half %','Possession to opp box %','Challenge intensity','Recoveries','Opp half recoveries','PPDA']]
            team_df_målbare_alle = team_df_målbare_alle.round(decimals=3)
            #hold = 'Horsens U15'
            #team_df_målbare_andre_hold = team_df_målbare.drop(hold)
            team_df_målbare_alle['xG against'] = team_df_målbare_alle['xG'].mean()
            team_df_målbare_alle['Danger zone shots against'] = team_df_målbare_alle['Dangerzone shots'].mean()
            team_df_målbare_alle['Touches in box against'] = team_df_målbare_alle['Touches in box'].mean()
            team_df_målbare_alle['Duels won %'] = (team_df['Duels won']/team_df['Duels'])*100
            team_df_målbare_alle = team_df_målbare_alle.round(decimals=2)
            Benchmark = team_df_målbare_alle.mean(axis=0)
            team_df_målbare_alle.loc['Liga Gennemsnit'] = Benchmark
            mask = team_df_målbare_alle.index.str.contains('Liga Gennemsnit')
            team_df_målbare_alle = team_df_målbare_alle[mask]


            df = pd.read_csv('Teamsheet alle kampe U15 sidste sæson.csv')

            dfsorteredekampesidstesæson = df.iloc[: , 1:]
            dfsorteredekampesidstesæson['date'] = dfsorteredekampesidstesæson['date'].astype(str)
            dfsorteredekampesidstesæson['date'] = dfsorteredekampesidstesæson['date'].str.replace(r'\sGMT.*$', '', regex=True)
            dfsorteredekampesidstesæson['date'] = pd.to_datetime(dfsorteredekampesidstesæson['date'], format="%B %d, %Y at %I:%M:%S %p")
            dfsorteredekampesidstesæson['date'] = dfsorteredekampesidstesæson['date'].dt.strftime('%d-%m-%Y')
            dfsorteredekampesidstesæson = dfsorteredekampesidstesæson.transpose()
            dfoverskrifter = dfsorteredekampesidstesæson[:2]
            dfsorteredekampesidstesæson = dfsorteredekampesidstesæson[2:].apply(pd.to_numeric, errors='coerce')
            dfsorteredekampesidstesæson = pd.concat([dfoverskrifter,dfsorteredekampesidstesæson])
            dfsorteredekampesidstesæson = dfsorteredekampesidstesæson.dropna(how='all')
            dfsorteredekampesidstesæson = dfsorteredekampesidstesæson.rename_axis('Parameter').astype(str)
            dfsorteredekampesidstesæson = dfsorteredekampesidstesæson.transpose()


            goals_cols = [col for col in dfsorteredekampesidstesæson.columns if col.endswith('.goals')]
            shots_cols = [col for col in dfsorteredekampesidstesæson.columns if col.endswith('.shots')]
            xg_cols = [col for col in dfsorteredekampesidstesæson.columns if col.endswith('.xg')]
            duels_cols = [col for col in dfsorteredekampesidstesæson.columns if col.endswith('.duels')]
            duelswon_cols = [col for col in dfsorteredekampesidstesæson.columns if col.endswith('.duelsSuccessful')]
            possession_cols = [col for col in dfsorteredekampesidstesæson.columns if col.endswith('.possessionPercent')]
            ppda_cols = [col for col in dfsorteredekampesidstesæson.columns if col.endswith('.ppda')]

            # Create a new dataframe with the average values for each team
            team_data_sidstesæson = {}
            for team in set([col.split('.')[1] for col in shots_cols]):
                team_goals = dfsorteredekampesidstesæson[[col for col in goals_cols if(team) in col]].mean(axis=1)    
                team_shots = dfsorteredekampesidstesæson[[col for col in shots_cols if(team) in col]].mean(axis=1)
                team_xg = dfsorteredekampesidstesæson[[col for col in xg_cols if (team) in col]].mean(axis=1)
                team_duels = dfsorteredekampesidstesæson[[col for col in duels_cols if (team) in col]].mean(axis=1)
                team_duelswon = dfsorteredekampesidstesæson[[col for col in duelswon_cols if (team) in col]].mean(axis=1)
                team_possession = dfsorteredekampesidstesæson[[col for col in possession_cols if (team) in col]].mean(axis=1)
                team_ppda = dfsorteredekampesidstesæson[[col for col in ppda_cols if (team) in col]].mean(axis=1)

                team_data_sidstesæson[team] = pd.concat([team_goals,team_shots, team_xg, team_duels,team_duelswon,team_possession,team_ppda], axis=1)
                
            team_df_sidstesæson = pd.concat(team_data_sidstesæson, axis=0, keys=team_data_sidstesæson.keys())
            team_df_sidstesæson.columns = ['Goals','Shots', 'Xg', 'Duels','Duels won','Possession %','PPDA']
            team_df_sidstesæson = team_df_sidstesæson.groupby(level=0).mean()


            team_df_sidstesæson= team_df_sidstesæson.round(decimals=2)


            forward_passes_cols = [col for col in dfsorteredekampesidstesæson.columns if col.endswith('.forwardPasses')]
            forward_passes_successful_cols = [col for col in dfsorteredekampesidstesæson.columns if col.endswith('.forwardPassesSuccessful')]
            passes_cols = [col for col in dfsorteredekampesidstesæson.columns if col.endswith('.passes')]
            touches_in_box_cols = [col for col in dfsorteredekampesidstesæson.columns if col.endswith('.touchesInBox')]
            xg_cols = [col for col in dfsorteredekampesidstesæson.columns if col.endswith('.xg')]
            xgpershot_cols = [col for col in dfsorteredekampesidstesæson.columns if col.endswith('.xgPerShot')]
            dzshots_cols = [col for col in dfsorteredekampesidstesæson.columns if col.endswith('.shotsFromDangerZone')]
            possessionantal_cols = [col for col in dfsorteredekampesidstesæson.columns if col.endswith('.possessionNumber')]
            possessionanmodstandershalvdel_cols = [col for col in dfsorteredekampesidstesæson.columns if col.endswith('.reachingOpponentHalf')]
            possessionanmodstandersfelt_cols = [col for col in dfsorteredekampesidstesæson.columns if col.endswith('.reachingOpponentBox')]
            challenge_intensity_cols = [col for col in dfsorteredekampesidstesæson.columns if col.endswith('.challengeIntensity')]
            recoveries_cols = [col for col in dfsorteredekampesidstesæson.columns if col.endswith('.recoveriesTotal')]
            opponenthalfrecoveries_cols = [col for col in dfsorteredekampesidstesæson.columns if col.endswith('.opponentHalfRecoveries')]
            ppda_cols = [col for col in dfsorteredekampesidstesæson.columns if col.endswith('.ppda')]

            # Create a new dataframe with the average values for each team
            team_data_målbare_sidstesæson = {}
            for team in set([col.split('.')[1] for col in shots_cols]):
                team_forward_passes = dfsorteredekampesidstesæson[[col for col in forward_passes_cols if(team) in col]].mean(axis=1)    
                team_forward_passes_successful = dfsorteredekampesidstesæson[[col for col in forward_passes_successful_cols if(team) in col]].mean(axis=1)
                team_passes = dfsorteredekampesidstesæson[[col for col in passes_cols if (team) in col]].mean(axis=1)
                team_touches_in_box = dfsorteredekampesidstesæson[[col for col in touches_in_box_cols if (team) in col]].mean(axis=1)
                team_xg = dfsorteredekampesidstesæson[[col for col in xg_cols if (team) in col]].mean(axis=1)
                team_xgpershot = dfsorteredekampesidstesæson[[col for col in xgpershot_cols if (team) in col]].mean(axis=1)
                team_dzshots = dfsorteredekampesidstesæson[[col for col in dzshots_cols if (team) in col]].mean(axis=1)
                team_possessionantal = dfsorteredekampesidstesæson[[col for col in possessionantal_cols if (team) in col]].mean(axis=1)
                team_possessionmodstandershalvdel = dfsorteredekampesidstesæson[[col for col in possessionanmodstandershalvdel_cols if (team) in col]].mean(axis=1)
                team_possessionmodstandersfelt = dfsorteredekampesidstesæson[[col for col in possessionanmodstandersfelt_cols if (team) in col]].mean(axis=1)
                team_challenge_intensity = dfsorteredekampesidstesæson[[col for col in challenge_intensity_cols if (team) in col]].mean(axis=1)
                team_recoveries = dfsorteredekampesidstesæson[[col for col in recoveries_cols if (team) in col]].mean(axis=1)
                team_opponenthalfrecoveries = dfsorteredekampesidstesæson[[col for col in opponenthalfrecoveries_cols if (team) in col]].mean(axis=1)

                team_ppda = dfsorteredekampesidstesæson[[col for col in ppda_cols if (team) in col]].mean(axis=1)

                team_data_målbare_sidstesæson[team] = pd.concat([team_forward_passes,team_forward_passes_successful, team_passes, team_touches_in_box,team_xg,team_xgpershot,team_dzshots,team_possessionantal,team_possessionmodstandershalvdel,team_possessionmodstandersfelt,team_challenge_intensity,team_recoveries,team_opponenthalfrecoveries,team_ppda], axis=1)
                
            team_df_målbaresidstesæson = pd.concat(team_data_målbare_sidstesæson, axis=0, keys=team_data_målbare_sidstesæson.keys())
            team_df_målbaresidstesæson.columns = ['Forward passes','Forward passes successful', 'Passes', 'Touches in box','xG','xG/shot','Dangerzone shots','Antal possessions','Antal possessions der når modstanders halvdel','Antal possessions der når modstanders felt','Challenge intensity','Recoveries','Opp half recoveries','PPDA']
            team_df_målbaresidstesæson = team_df_målbaresidstesæson.groupby(level=0).mean()
            team_df_målbaresidstesæson['Forward pass %'] = (team_df_målbaresidstesæson['Forward passes successful']/team_df_målbaresidstesæson['Forward passes'])*100
            team_df_målbaresidstesæson['Forward pass share'] = (team_df_målbaresidstesæson['Forward passes']/team_df_målbaresidstesæson['Passes'])*100
            team_df_målbaresidstesæson['Forward pass score'] = team_df_målbaresidstesæson[['Forward pass share','Forward pass %']].mean(axis=1)
            team_df_målbaresidstesæson['Possession to opp box'] = team_df_målbaresidstesæson['Antal possessions der når modstanders felt']
            team_df_målbaresidstesæson['Possession to opp half %'] = (team_df_målbaresidstesæson['Antal possessions der når modstanders halvdel']/team_df_målbaresidstesæson['Antal possessions'])*100
            team_df_målbaresidstesæson['Possession to opp box %'] = (team_df_målbaresidstesæson['Antal possessions der når modstanders felt']/team_df_målbaresidstesæson['Antal possessions'])*100
            team_df_målbaresidstesæson = team_df_målbaresidstesæson[['Forward pass score','Touches in box','xG','xG/shot','Dangerzone shots','Possession to opp box','Possession to opp half %','Possession to opp box %','Challenge intensity','Recoveries','Opp half recoveries','PPDA']]
            team_df_målbaresidstesæson = team_df_målbaresidstesæson.round(decimals=3)

            team_df_målbaresidstesæson['xG against'] = team_df_målbaresidstesæson['xG'].mean()
            team_df_målbaresidstesæson['Danger zone shots against'] = team_df_målbaresidstesæson['Dangerzone shots'].mean()
            team_df_målbaresidstesæson['Touches in box against'] = team_df_målbaresidstesæson['Touches in box'].mean()
            team_df_målbaresidstesæson['Duels won %'] = (team_df_sidstesæson['Duels won']/team_df_sidstesæson['Duels'])*100
            mask = team_df_målbaresidstesæson.index.str.contains('Horsens')
            team_df_målbaresidstesæson = team_df_målbaresidstesæson[mask]
            team_df_målbaresidstesæson = team_df_målbaresidstesæson.round(decimals=2)
            frames = [team_df_målbare_alle,team_df_målbare,team_df_målbaresidstesæson]
            Benchmark = pd.concat(frames)
            st.dataframe(Benchmark)
            import plotly.graph_objs as go
            import numpy as np
            from plotly.subplots import make_subplots

            trace1 = go.Indicator(mode="gauge+number",    value=Benchmark['Forward pass score'][1],domain={'row' : 1, 'column' : 1},title={'text': "Forward pass score"},gauge={'axis': {'range': [min(Benchmark['Forward pass score'][0], Benchmark['Forward pass score'][2]),max(Benchmark['Forward pass score'][0], Benchmark['Forward pass score'][2])]}})
            trace2 = go.Indicator(mode="gauge+number",    value=Benchmark['Touches in box'][1],domain={'row' : 1, 'column' : 2},title={'text': "Touches in box"},gauge={'axis': {'range': [min(Benchmark['Touches in box'][0], Benchmark['Touches in box'][2]),max(Benchmark['Touches in box'][0], Benchmark['Touches in box'][2])]}})
            trace3 = go.Indicator(mode="gauge+number",    value=Benchmark['xG'][1],domain={'row' : 1, 'column' : 3},title={'text': "xG"},gauge={'axis': {'range': [min(Benchmark['xG'][0], Benchmark['xG'][2]),max(Benchmark['xG'][0], Benchmark['xG'][2])]}})
            trace4 = go.Indicator(mode="gauge+number",    value=Benchmark['xG/shot'][1],domain={'row' : 1, 'column' : 4},title={'text': "xG/shot"},gauge={'axis': {'range': [min(Benchmark['xG/shot'][0], Benchmark['xG/shot'][2]),max(Benchmark['xG/shot'][0], Benchmark['xG/shot'][2])]}})
            trace5 = go.Indicator(mode="gauge+number",    value=Benchmark['Dangerzone shots'][1],domain={'row' : 2, 'column' : 1},title={'text': "Dangerzone shots"},gauge={'axis': {'range': [min(Benchmark['Dangerzone shots'][0], Benchmark['Dangerzone shots'][2]),max(Benchmark['Dangerzone shots'][0], Benchmark['Dangerzone shots'][2])]}})
            trace6 = go.Indicator(mode="gauge+number",    value=Benchmark['Possession to opp box'][1],domain={'row' : 2, 'column' : 2},title={'text': "Possession to opp box"},gauge={'axis': {'range': [min(Benchmark['Possession to opp box'][0], Benchmark['Possession to opp box'][2]),max(Benchmark['Possession to opp box'][0], Benchmark['Possession to opp box'][2])]}})
            trace7 = go.Indicator(mode="gauge+number",    value=Benchmark['Possession to opp half %'][1],domain={'row' : 2, 'column' : 3},title={'text': "Possession to opp half %"},gauge={'axis': {'range': [min(Benchmark['Possession to opp half %'][0], Benchmark['Possession to opp half %'][2]),max(Benchmark['Possession to opp half %'][0], Benchmark['Possession to opp half %'][2])]}})
            trace8 = go.Indicator(mode="gauge+number",    value=Benchmark['Possession to opp box %'][1],domain={'row' : 2, 'column' : 4},title={'text': "Possession to opp box %"},gauge={'axis': {'range': [min(Benchmark['Possession to opp box %'][0], Benchmark['Possession to opp box %'][2]),max(Benchmark['Possession to opp box %'][0], Benchmark['Possession to opp box %'][2])]}})
            
            fig = make_subplots(
            rows=2,
            cols=4,
            specs=[[{'type' : 'indicator'},{'type' : 'indicator'},{'type' : 'indicator'},{'type' : 'indicator'}],[{'type' : 'indicator'},{'type' : 'indicator'},{'type' : 'indicator'},{'type' : 'indicator'}]],
            )

            fig.append_trace(trace1, row=1, col=1)
            fig.append_trace(trace2, row=1, col=2)
            fig.append_trace(trace3, row=1, col=3)
            fig.append_trace(trace4, row=1, col=4)
            fig.append_trace(trace5, row=2, col=1)
            fig.append_trace(trace6, row=2, col=2)
            fig.append_trace(trace7, row=2, col=3)
            fig.append_trace(trace8, row=2, col=4)
            
            st.title('Offensive parametre')
            st.write('Skalaen går fra eget gennemsnit i seneste sæson til denne sæsons ligagennemsnit, ved ingen udfyldning er den rød, delvis udfyldning er gul, helt fyldt er grøn')
            st.plotly_chart(fig,use_container_width=True)
            
            trace9 = go.Indicator(mode="gauge+number",    value=Benchmark['xG against'][1],domain={'row' : 1, 'column' : 1},title={'text': "xG against"},gauge={'axis': {'range': [max(Benchmark['xG against'][0], Benchmark['xG against'][2]),min(Benchmark['xG against'][0], Benchmark['xG against'][2])]}})
            trace10 = go.Indicator(mode="gauge+number",    value=Benchmark['PPDA'][1],domain={'row' : 1, 'column' : 2},title={'text': "PPDA"},gauge={'axis': {'range': [max(Benchmark['PPDA'][0], Benchmark['PPDA'][2]),min(Benchmark['PPDA'][0], Benchmark['PPDA'][2])]}})
            trace11 = go.Indicator(mode="gauge+number",    value=Benchmark['Danger zone shots against'][1],domain={'row' : 1, 'column' : 3},title={'text': "Danger zone shots against"},gauge={'axis': {'range': [max(Benchmark['Danger zone shots against'][0], Benchmark['Danger zone shots against'][2]),min(Benchmark['Danger zone shots against'][0], Benchmark['Danger zone shots against'][2])]}})
            trace12 = go.Indicator(mode="gauge+number",    value=Benchmark['Challenge intensity'][1],domain={'row' : 1, 'column' : 4},title={'text': "Challenge intensity"},gauge={'axis': {'range': [min(Benchmark['Challenge intensity'][0], Benchmark['Challenge intensity'][2]),max(Benchmark['Challenge intensity'][0], Benchmark['Challenge intensity'][2])]}})
            trace13 = go.Indicator(mode="gauge+number",    value=Benchmark['Recoveries'][1],domain={'row' : 2, 'column' : 1},title={'text': "Recoveries"},gauge={'axis': {'range': [min(Benchmark['Recoveries'][0], Benchmark['Recoveries'][2]),max(Benchmark['Recoveries'][0], Benchmark['Recoveries'][2])]}})
            trace14 = go.Indicator(mode="gauge+number",    value=Benchmark['Opp half recoveries'][1],domain={'row' : 2, 'column' : 2},title={'text': "Opp half recoveries"},gauge={'axis': {'range': [min(Benchmark['Opp half recoveries'][0], Benchmark['Opp half recoveries'][2]),max(Benchmark['Opp half recoveries'][0], Benchmark['Opp half recoveries'][2])]}})
            trace15 = go.Indicator(mode="gauge+number",    value=Benchmark['Touches in box against'][1],domain={'row' : 2, 'column' : 3},title={'text': "Touches in box against"},gauge={'axis': {'range': [max(Benchmark['Touches in box against'][0], Benchmark['Touches in box against'][2]),min(Benchmark['Touches in box against'][0], Benchmark['Touches in box against'][2])]}})
            trace16 = go.Indicator(mode="gauge+number",    value=Benchmark['Duels won %'][1],domain={'row' : 2, 'column' : 4},title={'text': "Duels won %"},gauge={'axis': {'range': [min(Benchmark['Duels won %'][0], Benchmark['Duels won %'][2]),max(Benchmark['Duels won %'][0], Benchmark['Duels won %'][2])]}})
            fig1 = make_subplots(
            rows=2,
            cols=4,
            specs=[[{'type' : 'indicator'},{'type' : 'indicator'},{'type' : 'indicator'},{'type' : 'indicator'}],[{'type' : 'indicator'},{'type' : 'indicator'},{'type' : 'indicator'},{'type' : 'indicator'}]],
            )

            fig1.append_trace(trace9, row=1, col=1)
            fig1.append_trace(trace10, row=1, col=2)
            fig1.append_trace(trace11, row=1, col=3)
            fig1.append_trace(trace12, row=1, col=4)
            fig1.append_trace(trace13, row=2, col=1)
            fig1.append_trace(trace14, row=2, col=2)
            fig1.append_trace(trace15, row=2, col=3)
            fig1.append_trace(trace16, row=2, col=4)
            st.title('Defensive parametre')
            st.write('Skalaen går fra eget gennemsnit i seneste sæson til denne sæsons ligagennemsnit, ved ingen udfyldning er den rød, delvis udfyldning er gul, helt fyldt er grøn')
            st.plotly_chart(fig1,use_container_width=True)    

        def U17():
            import pandas as pd
            import csv
            import streamlit as st
            import numpy as np
            from datetime import datetime
            df = pd.read_csv('Teamsheet egne kampe U17.csv')
            kampe = df['label']
            option = st.multiselect('Vælg kamp (Hvis ingen kamp er valgt, vises gennemsnit for alle)',kampe)
            if len(option) > 0:
                temp_select = option
            else:
                temp_select = kampe

            dfsorteredekampe = df.loc[df.loc[df.label.isin(temp_select),'label'].index.values]
            dfsorteredekampe = dfsorteredekampe.iloc[: , 1:]
            #dfsorteredekampe['date'] = dfsorteredekampe['date'].astype(str)
            #dfsorteredekampe['date'] = dfsorteredekampe['date'].str.replace(r'\sGMT.*$', '', regex=True)
            #dfsorteredekampe['date'] = pd.to_datetime(dfsorteredekampe['date'], format="%B %d, %Y at %I:%M:%S %p")
            #dfsorteredekampe['date'] = dfsorteredekampe['date'].dt.strftime('%d-%m-%Y')
            dfsorteredekampe = dfsorteredekampe.transpose()
            dfoverskrifter = dfsorteredekampe[:2]
            dfsorteredekampe = dfsorteredekampe[2:].apply(pd.to_numeric, errors='coerce')
            dfsorteredekampe = pd.concat([dfoverskrifter,dfsorteredekampe])
            dfsorteredekampe = dfsorteredekampe.dropna(how='all')
            dfsorteredekampe = dfsorteredekampe.rename_axis('Parameter').astype(str)
            dfsorteredekampe = dfsorteredekampe.transpose()


            goals_cols = [col for col in dfsorteredekampe.columns if col.endswith('.goals')]
            shots_cols = [col for col in dfsorteredekampe.columns if col.endswith('.shots')]
            xg_cols = [col for col in dfsorteredekampe.columns if col.endswith('.xg')]
            duels_cols = [col for col in dfsorteredekampe.columns if col.endswith('.duels')]
            duelswon_cols = [col for col in dfsorteredekampe.columns if col.endswith('.duelsSuccessful')]
            possession_cols = [col for col in dfsorteredekampe.columns if col.endswith('.possessionPercent')]
            ppda_cols = [col for col in dfsorteredekampe.columns if col.endswith('.ppda')]

            # Create a new dataframe with the average values for each team
            team_data = {}
            for team in set([col.split('.')[1] for col in shots_cols]):
                team_goals = dfsorteredekampe[[col for col in goals_cols if(team) in col]].mean(axis=1)    
                team_shots = dfsorteredekampe[[col for col in shots_cols if(team) in col]].mean(axis=1)
                team_xg = dfsorteredekampe[[col for col in xg_cols if (team) in col]].mean(axis=1)
                team_duels = dfsorteredekampe[[col for col in duels_cols if (team) in col]].mean(axis=1)
                team_duelswon = dfsorteredekampe[[col for col in duelswon_cols if (team) in col]].mean(axis=1)
                team_possession = dfsorteredekampe[[col for col in possession_cols if (team) in col]].mean(axis=1)
                team_ppda = dfsorteredekampe[[col for col in ppda_cols if (team) in col]].mean(axis=1)

                team_data[team] = pd.concat([team_goals,team_shots, team_xg, team_duels,team_duelswon,team_possession,team_ppda], axis=1)
                
            team_df = pd.concat(team_data, axis=0, keys=team_data.keys())
            team_df.columns = ['Goals','Shots', 'Xg', 'Duels','Duels won','Possession %','PPDA']
            team_df = team_df.groupby(level=0).mean()

            st.write('Generelle stats')
            team_df= team_df.round(decimals=2)
            st.dataframe(team_df)

            forward_passes_cols = [col for col in dfsorteredekampe.columns if col.endswith('.forwardPasses')]
            forward_passes_successful_cols = [col for col in dfsorteredekampe.columns if col.endswith('.forwardPassesSuccessful')]
            passes_cols = [col for col in dfsorteredekampe.columns if col.endswith('.passes')]
            touches_in_box_cols = [col for col in dfsorteredekampe.columns if col.endswith('.touchesInBox')]
            xg_cols = [col for col in dfsorteredekampe.columns if col.endswith('.xg')]
            xgpershot_cols = [col for col in dfsorteredekampe.columns if col.endswith('.xgPerShot')]
            dzshots_cols = [col for col in dfsorteredekampe.columns if col.endswith('.shotsFromDangerZone')]
            possessionantal_cols = [col for col in dfsorteredekampe.columns if col.endswith('.possessionNumber')]
            possessionanmodstandershalvdel_cols = [col for col in dfsorteredekampe.columns if col.endswith('.reachingOpponentHalf')]
            possessionanmodstandersfelt_cols = [col for col in dfsorteredekampe.columns if col.endswith('.reachingOpponentBox')]
            challenge_intensity_cols = [col for col in dfsorteredekampe.columns if col.endswith('.challengeIntensity')]
            recoveries_cols = [col for col in dfsorteredekampe.columns if col.endswith('.recoveriesTotal')]
            opponenthalfrecoveries_cols = [col for col in dfsorteredekampe.columns if col.endswith('.opponentHalfRecoveries')]
            ppda_cols = [col for col in dfsorteredekampe.columns if col.endswith('.ppda')]

            # Create a new dataframe with the average values for each team
            team_data_målbare = {}
            for team in set([col.split('.')[1] for col in shots_cols]):
                team_forward_passes = dfsorteredekampe[[col for col in forward_passes_cols if(team) in col]].mean(axis=1)    
                team_forward_passes_successful = dfsorteredekampe[[col for col in forward_passes_successful_cols if(team) in col]].mean(axis=1)
                team_passes = dfsorteredekampe[[col for col in passes_cols if (team) in col]].mean(axis=1)
                team_touches_in_box = dfsorteredekampe[[col for col in touches_in_box_cols if (team) in col]].mean(axis=1)
                team_xg = dfsorteredekampe[[col for col in xg_cols if (team) in col]].mean(axis=1)
                team_xgpershot = dfsorteredekampe[[col for col in xgpershot_cols if (team) in col]].mean(axis=1)
                team_dzshots = dfsorteredekampe[[col for col in dzshots_cols if (team) in col]].mean(axis=1)
                team_possessionantal = dfsorteredekampe[[col for col in possessionantal_cols if (team) in col]].mean(axis=1)
                team_possessionmodstandershalvdel = dfsorteredekampe[[col for col in possessionanmodstandershalvdel_cols if (team) in col]].mean(axis=1)
                team_possessionmodstandersfelt = dfsorteredekampe[[col for col in possessionanmodstandersfelt_cols if (team) in col]].mean(axis=1)
                team_challenge_intensity = dfsorteredekampe[[col for col in challenge_intensity_cols if (team) in col]].mean(axis=1)
                team_recoveries = dfsorteredekampe[[col for col in recoveries_cols if (team) in col]].mean(axis=1)
                team_opponenthalfrecoveries = dfsorteredekampe[[col for col in opponenthalfrecoveries_cols if (team) in col]].mean(axis=1)

                team_ppda = dfsorteredekampe[[col for col in ppda_cols if (team) in col]].mean(axis=1)

                team_data_målbare[team] = pd.concat([team_forward_passes,team_forward_passes_successful, team_passes, team_touches_in_box,team_xg,team_xgpershot,team_dzshots,team_possessionantal,team_possessionmodstandershalvdel,team_possessionmodstandersfelt,team_challenge_intensity,team_recoveries,team_opponenthalfrecoveries,team_ppda], axis=1)
                
            team_df_målbare = pd.concat(team_data_målbare, axis=0, keys=team_data_målbare.keys())
            team_df_målbare.columns = ['Forward passes','Forward passes successful', 'Passes', 'Touches in box','xG','xG/shot','Dangerzone shots','Antal possessions','Antal possessions der når modstanders halvdel','Antal possessions der når modstanders felt','Challenge intensity','Recoveries','Opp half recoveries','PPDA']
            team_df_målbare = team_df_målbare.groupby(level=0).mean()
            team_df_målbare['Forward pass %'] = (team_df_målbare['Forward passes successful']/team_df_målbare['Forward passes'])*100
            team_df_målbare['Forward pass share'] = (team_df_målbare['Forward passes']/team_df_målbare['Passes'])*100
            team_df_målbare['Forward pass score'] = team_df_målbare[['Forward pass share','Forward pass %']].mean(axis=1)
            team_df_målbare['Possession to opp box'] = team_df_målbare['Antal possessions der når modstanders felt']
            team_df_målbare['Possession to opp half %'] = (team_df_målbare['Antal possessions der når modstanders halvdel']/team_df_målbare['Antal possessions'])*100
            team_df_målbare['Possession to opp box %'] = (team_df_målbare['Antal possessions der når modstanders felt']/team_df_målbare['Antal possessions'])*100
            team_df_målbare = team_df_målbare[['Forward pass score','Touches in box','xG','xG/shot','Dangerzone shots','Possession to opp box','Possession to opp half %','Possession to opp box %','Challenge intensity','Recoveries','Opp half recoveries','PPDA']]
            team_df_målbare = team_df_målbare.round(decimals=3)
            hold = 'Horsens U17'
            team_df_målbare_andre_hold = team_df_målbare.drop(hold)
            team_df_målbare['xG against'] = team_df_målbare_andre_hold['xG'].mean()
            team_df_målbare['Danger zone shots against'] = team_df_målbare_andre_hold['Dangerzone shots'].mean()
            team_df_målbare['Touches in box against'] = team_df_målbare_andre_hold['Touches in box'].mean()
            team_df_målbare['Duels won %'] = (team_df['Duels won']/team_df['Duels'])*100
            mask = team_df_målbare.index.str.contains('Horsens')
            team_df_målbare = team_df_målbare[mask]
            team_df_målbare = team_df_målbare.round(decimals=2)

            import pandas as pd
            import csv
            import streamlit as st
            import numpy as np
            from datetime import datetime

            df = pd.read_csv('Teamsheet alle kampe U17.csv')

            dfsorteredeallekampe = df.iloc[: , 1:]
            dfsorteredeallekampe['date'] = dfsorteredeallekampe['date'].astype(str)
            dfsorteredeallekampe['date'] = dfsorteredeallekampe['date'].str.replace(r'\sGMT.*$', '', regex=True)
            dfsorteredeallekampe['date'] = pd.to_datetime(dfsorteredeallekampe['date'], format="%B %d, %Y at %I:%M:%S %p")
            dfsorteredeallekampe['date'] = dfsorteredeallekampe['date'].dt.strftime('%d-%m-%Y')
            dfsorteredeallekampe = dfsorteredeallekampe.transpose()
            dfoverskrifter = dfsorteredeallekampe[:2]
            dfsorteredeallekampe = dfsorteredeallekampe[2:].apply(pd.to_numeric, errors='coerce')
            dfsorteredeallekampe = pd.concat([dfoverskrifter,dfsorteredeallekampe])
            dfsorteredeallekampe = dfsorteredeallekampe.dropna(how='all')
            dfsorteredeallekampe = dfsorteredeallekampe.rename_axis('Parameter').astype(str)
            dfsorteredeallekampe = dfsorteredeallekampe.transpose()


            goals_cols = [col for col in dfsorteredeallekampe.columns if col.endswith('.goals')]
            shots_cols = [col for col in dfsorteredeallekampe.columns if col.endswith('.shots')]
            xg_cols = [col for col in dfsorteredeallekampe.columns if col.endswith('.xg')]
            duels_cols = [col for col in dfsorteredeallekampe.columns if col.endswith('.duels')]
            duelswon_cols = [col for col in dfsorteredeallekampe.columns if col.endswith('.duelsSuccessful')]
            possession_cols = [col for col in dfsorteredeallekampe.columns if col.endswith('.possessionPercent')]
            ppda_cols = [col for col in dfsorteredeallekampe.columns if col.endswith('.ppda')]

            # Create a new dataframe with the average values for each team
            team_data = {}
            for team in set([col.split('.')[1] for col in shots_cols]):
                team_goals = dfsorteredeallekampe[[col for col in goals_cols if(team) in col]].mean(axis=1)    
                team_shots = dfsorteredeallekampe[[col for col in shots_cols if(team) in col]].mean(axis=1)
                team_xg = dfsorteredeallekampe[[col for col in xg_cols if (team) in col]].mean(axis=1)
                team_duels = dfsorteredeallekampe[[col for col in duels_cols if (team) in col]].mean(axis=1)
                team_duelswon = dfsorteredeallekampe[[col for col in duelswon_cols if (team) in col]].mean(axis=1)
                team_possession = dfsorteredeallekampe[[col for col in possession_cols if (team) in col]].mean(axis=1)
                team_ppda = dfsorteredeallekampe[[col for col in ppda_cols if (team) in col]].mean(axis=1)

                team_data[team] = pd.concat([team_goals,team_shots, team_xg, team_duels,team_duelswon,team_possession,team_ppda], axis=1)
                
            team_df = pd.concat(team_data, axis=0, keys=team_data.keys())
            team_df.columns = ['Goals','Shots', 'Xg', 'Duels','Duels won','Possession %','PPDA']
            team_df = team_df.groupby(level=0).mean()
            team_df= team_df.round(decimals=2)


            forward_passes_cols = [col for col in dfsorteredeallekampe.columns if col.endswith('.forwardPasses')]
            forward_passes_successful_cols = [col for col in dfsorteredeallekampe.columns if col.endswith('.forwardPassesSuccessful')]
            passes_cols = [col for col in dfsorteredeallekampe.columns if col.endswith('.passes')]
            touches_in_box_cols = [col for col in dfsorteredeallekampe.columns if col.endswith('.touchesInBox')]
            xg_cols = [col for col in dfsorteredeallekampe.columns if col.endswith('.xg')]
            xgpershot_cols = [col for col in dfsorteredeallekampe.columns if col.endswith('.xgPerShot')]
            dzshots_cols = [col for col in dfsorteredeallekampe.columns if col.endswith('.shotsFromDangerZone')]
            possessionantal_cols = [col for col in dfsorteredeallekampe.columns if col.endswith('.possessionNumber')]
            possessionanmodstandershalvdel_cols = [col for col in dfsorteredeallekampe.columns if col.endswith('.reachingOpponentHalf')]
            possessionanmodstandersfelt_cols = [col for col in dfsorteredeallekampe.columns if col.endswith('.reachingOpponentBox')]
            challenge_intensity_cols = [col for col in dfsorteredeallekampe.columns if col.endswith('.challengeIntensity')]
            recoveries_cols = [col for col in dfsorteredeallekampe.columns if col.endswith('.recoveriesTotal')]
            opponenthalfrecoveries_cols = [col for col in dfsorteredeallekampe.columns if col.endswith('.opponentHalfRecoveries')]
            ppda_cols = [col for col in dfsorteredeallekampe.columns if col.endswith('.ppda')]

            # Create a new dataframe with the average values for each team
            team_data_målbare_alle = {}
            for team in set([col.split('.')[1] for col in shots_cols]):
                team_forward_passes = dfsorteredeallekampe[[col for col in forward_passes_cols if(team) in col]].mean(axis=1)    
                team_forward_passes_successful = dfsorteredeallekampe[[col for col in forward_passes_successful_cols if(team) in col]].mean(axis=1)
                team_passes = dfsorteredeallekampe[[col for col in passes_cols if (team) in col]].mean(axis=1)
                team_touches_in_box = dfsorteredeallekampe[[col for col in touches_in_box_cols if (team) in col]].mean(axis=1)
                team_xg = dfsorteredeallekampe[[col for col in xg_cols if (team) in col]].mean(axis=1)
                team_xgpershot = dfsorteredeallekampe[[col for col in xgpershot_cols if (team) in col]].mean(axis=1)
                team_dzshots = dfsorteredeallekampe[[col for col in dzshots_cols if (team) in col]].mean(axis=1)
                team_possessionantal = dfsorteredeallekampe[[col for col in possessionantal_cols if (team) in col]].mean(axis=1)
                team_possessionmodstandershalvdel = dfsorteredeallekampe[[col for col in possessionanmodstandershalvdel_cols if (team) in col]].mean(axis=1)
                team_possessionmodstandersfelt = dfsorteredeallekampe[[col for col in possessionanmodstandersfelt_cols if (team) in col]].mean(axis=1)
                team_challenge_intensity = dfsorteredeallekampe[[col for col in challenge_intensity_cols if (team) in col]].mean(axis=1)
                team_recoveries = dfsorteredeallekampe[[col for col in recoveries_cols if (team) in col]].mean(axis=1)
                team_opponenthalfrecoveries = dfsorteredeallekampe[[col for col in opponenthalfrecoveries_cols if (team) in col]].mean(axis=1)

                team_ppda = dfsorteredeallekampe[[col for col in ppda_cols if (team) in col]].mean(axis=1)

                team_data_målbare_alle[team] = pd.concat([team_forward_passes,team_forward_passes_successful, team_passes, team_touches_in_box,team_xg,team_xgpershot,team_dzshots,team_possessionantal,team_possessionmodstandershalvdel,team_possessionmodstandersfelt,team_challenge_intensity,team_recoveries,team_opponenthalfrecoveries,team_ppda], axis=1)
                
            team_df_målbare_alle = pd.concat(team_data_målbare_alle, axis=0, keys=team_data_målbare_alle.keys())
            team_df_målbare_alle.columns = ['Forward passes','Forward passes successful', 'Passes', 'Touches in box','xG','xG/shot','Dangerzone shots','Antal possessions','Antal possessions der når modstanders halvdel','Antal possessions der når modstanders felt','Challenge intensity','Recoveries','Opp half recoveries','PPDA']
            team_df_målbare_alle = team_df_målbare_alle.groupby(level=0).mean()
            team_df_målbare_alle['Forward pass %'] = (team_df_målbare_alle['Forward passes successful']/team_df_målbare_alle['Forward passes'])*100
            team_df_målbare_alle['Forward pass share'] = (team_df_målbare_alle['Forward passes']/team_df_målbare_alle['Passes'])*100
            team_df_målbare_alle['Forward pass score'] = team_df_målbare_alle[['Forward pass share','Forward pass %']].mean(axis=1)
            team_df_målbare_alle['Possession to opp box'] = team_df_målbare_alle['Antal possessions der når modstanders felt']
            team_df_målbare_alle['Possession to opp half %'] = (team_df_målbare_alle['Antal possessions der når modstanders halvdel']/team_df_målbare_alle['Antal possessions'])*100
            team_df_målbare_alle['Possession to opp box %'] = (team_df_målbare_alle['Antal possessions der når modstanders felt']/team_df_målbare_alle['Antal possessions'])*100
            team_df_målbare_alle = team_df_målbare_alle[['Forward pass score','Touches in box','xG','xG/shot','Dangerzone shots','Possession to opp box','Possession to opp half %','Possession to opp box %','Challenge intensity','Recoveries','Opp half recoveries','PPDA']]
            team_df_målbare_alle = team_df_målbare_alle.round(decimals=3)
            #hold = 'Horsens U15'
            #team_df_målbare_andre_hold = team_df_målbare.drop(hold)
            team_df_målbare_alle['xG against'] = team_df_målbare_alle['xG'].mean()
            team_df_målbare_alle['Danger zone shots against'] = team_df_målbare_alle['Dangerzone shots'].mean()
            team_df_målbare_alle['Touches in box against'] = team_df_målbare_alle['Touches in box'].mean()
            team_df_målbare_alle['Duels won %'] = (team_df['Duels won']/team_df['Duels'])*100
            team_df_målbare_alle = team_df_målbare_alle.round(decimals=2)
            Benchmark = team_df_målbare_alle.mean(axis=0)
            team_df_målbare_alle.loc['Liga Gennemsnit'] = Benchmark
            mask = team_df_målbare_alle.index.str.contains('Liga Gennemsnit')
            team_df_målbare_alle = team_df_målbare_alle[mask]


            df = pd.read_csv('Teamsheet alle kampe U17 sidste sæson.csv')

            dfsorteredekampesidstesæson = df.iloc[: , 1:]
            dfsorteredekampesidstesæson['date'] = dfsorteredekampesidstesæson['date'].astype(str)
            dfsorteredekampesidstesæson['date'] = dfsorteredekampesidstesæson['date'].str.replace(r'\sGMT.*$', '', regex=True)
            dfsorteredekampesidstesæson['date'] = pd.to_datetime(dfsorteredekampesidstesæson['date'], format="%B %d, %Y at %I:%M:%S %p")
            dfsorteredekampesidstesæson['date'] = dfsorteredekampesidstesæson['date'].dt.strftime('%d-%m-%Y')
            dfsorteredekampesidstesæson = dfsorteredekampesidstesæson.transpose()
            dfoverskrifter = dfsorteredekampesidstesæson[:2]
            dfsorteredekampesidstesæson = dfsorteredekampesidstesæson[2:].apply(pd.to_numeric, errors='coerce')
            dfsorteredekampesidstesæson = pd.concat([dfoverskrifter,dfsorteredekampesidstesæson])
            dfsorteredekampesidstesæson = dfsorteredekampesidstesæson.dropna(how='all')
            dfsorteredekampesidstesæson = dfsorteredekampesidstesæson.rename_axis('Parameter').astype(str)
            dfsorteredekampesidstesæson = dfsorteredekampesidstesæson.transpose()


            goals_cols = [col for col in dfsorteredekampesidstesæson.columns if col.endswith('.goals')]
            shots_cols = [col for col in dfsorteredekampesidstesæson.columns if col.endswith('.shots')]
            xg_cols = [col for col in dfsorteredekampesidstesæson.columns if col.endswith('.xg')]
            duels_cols = [col for col in dfsorteredekampesidstesæson.columns if col.endswith('.duels')]
            duelswon_cols = [col for col in dfsorteredekampesidstesæson.columns if col.endswith('.duelsSuccessful')]
            possession_cols = [col for col in dfsorteredekampesidstesæson.columns if col.endswith('.possessionPercent')]
            ppda_cols = [col for col in dfsorteredekampesidstesæson.columns if col.endswith('.ppda')]

            # Create a new dataframe with the average values for each team
            team_data_sidstesæson = {}
            for team in set([col.split('.')[1] for col in shots_cols]):
                team_goals = dfsorteredekampesidstesæson[[col for col in goals_cols if(team) in col]].mean(axis=1)    
                team_shots = dfsorteredekampesidstesæson[[col for col in shots_cols if(team) in col]].mean(axis=1)
                team_xg = dfsorteredekampesidstesæson[[col for col in xg_cols if (team) in col]].mean(axis=1)
                team_duels = dfsorteredekampesidstesæson[[col for col in duels_cols if (team) in col]].mean(axis=1)
                team_duelswon = dfsorteredekampesidstesæson[[col for col in duelswon_cols if (team) in col]].mean(axis=1)
                team_possession = dfsorteredekampesidstesæson[[col for col in possession_cols if (team) in col]].mean(axis=1)
                team_ppda = dfsorteredekampesidstesæson[[col for col in ppda_cols if (team) in col]].mean(axis=1)

                team_data_sidstesæson[team] = pd.concat([team_goals,team_shots, team_xg, team_duels,team_duelswon,team_possession,team_ppda], axis=1)
                
            team_df_sidstesæson = pd.concat(team_data_sidstesæson, axis=0, keys=team_data_sidstesæson.keys())
            team_df_sidstesæson.columns = ['Goals','Shots', 'Xg', 'Duels','Duels won','Possession %','PPDA']
            team_df_sidstesæson = team_df_sidstesæson.groupby(level=0).mean()


            team_df_sidstesæson= team_df_sidstesæson.round(decimals=2)


            forward_passes_cols = [col for col in dfsorteredekampesidstesæson.columns if col.endswith('.forwardPasses')]
            forward_passes_successful_cols = [col for col in dfsorteredekampesidstesæson.columns if col.endswith('.forwardPassesSuccessful')]
            passes_cols = [col for col in dfsorteredekampesidstesæson.columns if col.endswith('.passes')]
            touches_in_box_cols = [col for col in dfsorteredekampesidstesæson.columns if col.endswith('.touchesInBox')]
            xg_cols = [col for col in dfsorteredekampesidstesæson.columns if col.endswith('.xg')]
            xgpershot_cols = [col for col in dfsorteredekampesidstesæson.columns if col.endswith('.xgPerShot')]
            dzshots_cols = [col for col in dfsorteredekampesidstesæson.columns if col.endswith('.shotsFromDangerZone')]
            possessionantal_cols = [col for col in dfsorteredekampesidstesæson.columns if col.endswith('.possessionNumber')]
            possessionanmodstandershalvdel_cols = [col for col in dfsorteredekampesidstesæson.columns if col.endswith('.reachingOpponentHalf')]
            possessionanmodstandersfelt_cols = [col for col in dfsorteredekampesidstesæson.columns if col.endswith('.reachingOpponentBox')]
            challenge_intensity_cols = [col for col in dfsorteredekampesidstesæson.columns if col.endswith('.challengeIntensity')]
            recoveries_cols = [col for col in dfsorteredekampesidstesæson.columns if col.endswith('.recoveriesTotal')]
            opponenthalfrecoveries_cols = [col for col in dfsorteredekampesidstesæson.columns if col.endswith('.opponentHalfRecoveries')]
            ppda_cols = [col for col in dfsorteredekampesidstesæson.columns if col.endswith('.ppda')]

            # Create a new dataframe with the average values for each team
            team_data_målbare_sidstesæson = {}
            for team in set([col.split('.')[1] for col in shots_cols]):
                team_forward_passes = dfsorteredekampesidstesæson[[col for col in forward_passes_cols if(team) in col]].mean(axis=1)    
                team_forward_passes_successful = dfsorteredekampesidstesæson[[col for col in forward_passes_successful_cols if(team) in col]].mean(axis=1)
                team_passes = dfsorteredekampesidstesæson[[col for col in passes_cols if (team) in col]].mean(axis=1)
                team_touches_in_box = dfsorteredekampesidstesæson[[col for col in touches_in_box_cols if (team) in col]].mean(axis=1)
                team_xg = dfsorteredekampesidstesæson[[col for col in xg_cols if (team) in col]].mean(axis=1)
                team_xgpershot = dfsorteredekampesidstesæson[[col for col in xgpershot_cols if (team) in col]].mean(axis=1)
                team_dzshots = dfsorteredekampesidstesæson[[col for col in dzshots_cols if (team) in col]].mean(axis=1)
                team_possessionantal = dfsorteredekampesidstesæson[[col for col in possessionantal_cols if (team) in col]].mean(axis=1)
                team_possessionmodstandershalvdel = dfsorteredekampesidstesæson[[col for col in possessionanmodstandershalvdel_cols if (team) in col]].mean(axis=1)
                team_possessionmodstandersfelt = dfsorteredekampesidstesæson[[col for col in possessionanmodstandersfelt_cols if (team) in col]].mean(axis=1)
                team_challenge_intensity = dfsorteredekampesidstesæson[[col for col in challenge_intensity_cols if (team) in col]].mean(axis=1)
                team_recoveries = dfsorteredekampesidstesæson[[col for col in recoveries_cols if (team) in col]].mean(axis=1)
                team_opponenthalfrecoveries = dfsorteredekampesidstesæson[[col for col in opponenthalfrecoveries_cols if (team) in col]].mean(axis=1)

                team_ppda = dfsorteredekampesidstesæson[[col for col in ppda_cols if (team) in col]].mean(axis=1)

                team_data_målbare_sidstesæson[team] = pd.concat([team_forward_passes,team_forward_passes_successful, team_passes, team_touches_in_box,team_xg,team_xgpershot,team_dzshots,team_possessionantal,team_possessionmodstandershalvdel,team_possessionmodstandersfelt,team_challenge_intensity,team_recoveries,team_opponenthalfrecoveries,team_ppda], axis=1)
                
            team_df_målbaresidstesæson = pd.concat(team_data_målbare_sidstesæson, axis=0, keys=team_data_målbare_sidstesæson.keys())
            team_df_målbaresidstesæson.columns = ['Forward passes','Forward passes successful', 'Passes', 'Touches in box','xG','xG/shot','Dangerzone shots','Antal possessions','Antal possessions der når modstanders halvdel','Antal possessions der når modstanders felt','Challenge intensity','Recoveries','Opp half recoveries','PPDA']
            team_df_målbaresidstesæson = team_df_målbaresidstesæson.groupby(level=0).mean()
            team_df_målbaresidstesæson['Forward pass %'] = (team_df_målbaresidstesæson['Forward passes successful']/team_df_målbaresidstesæson['Forward passes'])*100
            team_df_målbaresidstesæson['Forward pass share'] = (team_df_målbaresidstesæson['Forward passes']/team_df_målbaresidstesæson['Passes'])*100
            team_df_målbaresidstesæson['Forward pass score'] = team_df_målbaresidstesæson[['Forward pass share','Forward pass %']].mean(axis=1)
            team_df_målbaresidstesæson['Possession to opp box'] = team_df_målbaresidstesæson['Antal possessions der når modstanders felt']
            team_df_målbaresidstesæson['Possession to opp half %'] = (team_df_målbaresidstesæson['Antal possessions der når modstanders halvdel']/team_df_målbaresidstesæson['Antal possessions'])*100
            team_df_målbaresidstesæson['Possession to opp box %'] = (team_df_målbaresidstesæson['Antal possessions der når modstanders felt']/team_df_målbaresidstesæson['Antal possessions'])*100
            team_df_målbaresidstesæson = team_df_målbaresidstesæson[['Forward pass score','Touches in box','xG','xG/shot','Dangerzone shots','Possession to opp box','Possession to opp half %','Possession to opp box %','Challenge intensity','Recoveries','Opp half recoveries','PPDA']]
            team_df_målbaresidstesæson = team_df_målbaresidstesæson.round(decimals=3)

            team_df_målbaresidstesæson['xG against'] = team_df_målbaresidstesæson['xG'].mean()
            team_df_målbaresidstesæson['Danger zone shots against'] = team_df_målbaresidstesæson['Dangerzone shots'].mean()
            team_df_målbaresidstesæson['Touches in box against'] = team_df_målbaresidstesæson['Touches in box'].mean()
            team_df_målbaresidstesæson['Duels won %'] = (team_df_sidstesæson['Duels won']/team_df_sidstesæson['Duels'])*100
            mask = team_df_målbaresidstesæson.index.str.contains('Horsens')
            team_df_målbaresidstesæson = team_df_målbaresidstesæson[mask]
            team_df_målbaresidstesæson = team_df_målbaresidstesæson.round(decimals=2)
            frames = [team_df_målbare_alle,team_df_målbare,team_df_målbaresidstesæson]
            Benchmark = pd.concat(frames)
            st.dataframe(Benchmark)
            import plotly.graph_objs as go
            import numpy as np
            from plotly.subplots import make_subplots

            trace1 = go.Indicator(mode="gauge+number",    value=Benchmark['Forward pass score'][1],domain={'row' : 1, 'column' : 1},title={'text': "Forward pass score"},gauge={'axis': {'range': [min(Benchmark['Forward pass score'][0], Benchmark['Forward pass score'][2]),max(Benchmark['Forward pass score'][0], Benchmark['Forward pass score'][2])]}})
            trace2 = go.Indicator(mode="gauge+number",    value=Benchmark['Touches in box'][1],domain={'row' : 1, 'column' : 2},title={'text': "Touches in box"},gauge={'axis': {'range': [min(Benchmark['Touches in box'][0], Benchmark['Touches in box'][2]),max(Benchmark['Touches in box'][0], Benchmark['Touches in box'][2])]}})
            trace3 = go.Indicator(mode="gauge+number",    value=Benchmark['xG'][1],domain={'row' : 1, 'column' : 3},title={'text': "xG"},gauge={'axis': {'range': [min(Benchmark['xG'][0], Benchmark['xG'][2]),max(Benchmark['xG'][0], Benchmark['xG'][2])]}})
            trace4 = go.Indicator(mode="gauge+number",    value=Benchmark['xG/shot'][1],domain={'row' : 1, 'column' : 4},title={'text': "xG/shot"},gauge={'axis': {'range': [min(Benchmark['xG/shot'][0], Benchmark['xG/shot'][2]),max(Benchmark['xG/shot'][0], Benchmark['xG/shot'][2])]}})
            trace5 = go.Indicator(mode="gauge+number",    value=Benchmark['Dangerzone shots'][1],domain={'row' : 2, 'column' : 1},title={'text': "Dangerzone shots"},gauge={'axis': {'range': [min(Benchmark['Dangerzone shots'][0], Benchmark['Dangerzone shots'][2]),max(Benchmark['Dangerzone shots'][0], Benchmark['Dangerzone shots'][2])]}})
            trace6 = go.Indicator(mode="gauge+number",    value=Benchmark['Possession to opp box'][1],domain={'row' : 2, 'column' : 2},title={'text': "Possession to opp box"},gauge={'axis': {'range': [min(Benchmark['Possession to opp box'][0], Benchmark['Possession to opp box'][2]),max(Benchmark['Possession to opp box'][0], Benchmark['Possession to opp box'][2])]}})
            trace7 = go.Indicator(mode="gauge+number",    value=Benchmark['Possession to opp half %'][1],domain={'row' : 2, 'column' : 3},title={'text': "Possession to opp half %"},gauge={'axis': {'range': [min(Benchmark['Possession to opp half %'][0], Benchmark['Possession to opp half %'][2]),max(Benchmark['Possession to opp half %'][0], Benchmark['Possession to opp half %'][2])]}})
            trace8 = go.Indicator(mode="gauge+number",    value=Benchmark['Possession to opp box %'][1],domain={'row' : 2, 'column' : 4},title={'text': "Possession to opp box %"},gauge={'axis': {'range': [min(Benchmark['Possession to opp box %'][0], Benchmark['Possession to opp box %'][2]),max(Benchmark['Possession to opp box %'][0], Benchmark['Possession to opp box %'][2])]}})
            
            fig = make_subplots(
            rows=2,
            cols=4,
            specs=[[{'type' : 'indicator'},{'type' : 'indicator'},{'type' : 'indicator'},{'type' : 'indicator'}],[{'type' : 'indicator'},{'type' : 'indicator'},{'type' : 'indicator'},{'type' : 'indicator'}]],
            )

            fig.append_trace(trace1, row=1, col=1)
            fig.append_trace(trace2, row=1, col=2)
            fig.append_trace(trace3, row=1, col=3)
            fig.append_trace(trace4, row=1, col=4)
            fig.append_trace(trace5, row=2, col=1)
            fig.append_trace(trace6, row=2, col=2)
            fig.append_trace(trace7, row=2, col=3)
            fig.append_trace(trace8, row=2, col=4)
            
            st.title('Offensive parametre')
            st.write('Skalaen går fra eget gennemsnit i seneste sæson til denne sæsons ligagennemsnit, ved ingen udfyldning er den rød, delvis udfyldning er gul, helt fyldt er grøn')
            st.plotly_chart(fig,use_container_width=True)
            
            trace9 = go.Indicator(mode="gauge+number",    value=Benchmark['xG against'][1],domain={'row' : 1, 'column' : 1},title={'text': "xG against"},gauge={'axis': {'range': [max(Benchmark['xG against'][0], Benchmark['xG against'][2]),min(Benchmark['xG against'][0], Benchmark['xG against'][2])]}})
            trace10 = go.Indicator(mode="gauge+number",    value=Benchmark['PPDA'][1],domain={'row' : 1, 'column' : 2},title={'text': "PPDA"},gauge={'axis': {'range': [max(Benchmark['PPDA'][0], Benchmark['PPDA'][2]),min(Benchmark['PPDA'][0], Benchmark['PPDA'][2])]}})
            trace11 = go.Indicator(mode="gauge+number",    value=Benchmark['Danger zone shots against'][1],domain={'row' : 1, 'column' : 3},title={'text': "Danger zone shots against"},gauge={'axis': {'range': [max(Benchmark['Danger zone shots against'][0], Benchmark['Danger zone shots against'][2]),min(Benchmark['Danger zone shots against'][0], Benchmark['Danger zone shots against'][2])]}})
            trace12 = go.Indicator(mode="gauge+number",    value=Benchmark['Challenge intensity'][1],domain={'row' : 1, 'column' : 4},title={'text': "Challenge intensity"},gauge={'axis': {'range': [min(Benchmark['Challenge intensity'][0], Benchmark['Challenge intensity'][2]),max(Benchmark['Challenge intensity'][0], Benchmark['Challenge intensity'][2])]}})
            trace13 = go.Indicator(mode="gauge+number",    value=Benchmark['Recoveries'][1],domain={'row' : 2, 'column' : 1},title={'text': "Recoveries"},gauge={'axis': {'range': [min(Benchmark['Recoveries'][0], Benchmark['Recoveries'][2]),max(Benchmark['Recoveries'][0], Benchmark['Recoveries'][2])]}})
            trace14 = go.Indicator(mode="gauge+number",    value=Benchmark['Opp half recoveries'][1],domain={'row' : 2, 'column' : 2},title={'text': "Opp half recoveries"},gauge={'axis': {'range': [min(Benchmark['Opp half recoveries'][0], Benchmark['Opp half recoveries'][2]),max(Benchmark['Opp half recoveries'][0], Benchmark['Opp half recoveries'][2])]}})
            trace15 = go.Indicator(mode="gauge+number",    value=Benchmark['Touches in box against'][1],domain={'row' : 2, 'column' : 3},title={'text': "Touches in box against"},gauge={'axis': {'range': [max(Benchmark['Touches in box against'][0], Benchmark['Touches in box against'][2]),min(Benchmark['Touches in box against'][0], Benchmark['Touches in box against'][2])]}})
            trace16 = go.Indicator(mode="gauge+number",    value=Benchmark['Duels won %'][1],domain={'row' : 2, 'column' : 4},title={'text': "Duels won %"},gauge={'axis': {'range': [min(Benchmark['Duels won %'][0], Benchmark['Duels won %'][2]),max(Benchmark['Duels won %'][0], Benchmark['Duels won %'][2])]}})
            fig1 = make_subplots(
            rows=2,
            cols=4,
            specs=[[{'type' : 'indicator'},{'type' : 'indicator'},{'type' : 'indicator'},{'type' : 'indicator'}],[{'type' : 'indicator'},{'type' : 'indicator'},{'type' : 'indicator'},{'type' : 'indicator'}]],
            )

            fig1.append_trace(trace9, row=1, col=1)
            fig1.append_trace(trace10, row=1, col=2)
            fig1.append_trace(trace11, row=1, col=3)
            fig1.append_trace(trace12, row=1, col=4)
            fig1.append_trace(trace13, row=2, col=1)
            fig1.append_trace(trace14, row=2, col=2)
            fig1.append_trace(trace15, row=2, col=3)
            fig1.append_trace(trace16, row=2, col=4)
            st.title('Defensive parametre')
            st.write('Skalaen går fra eget gennemsnit i seneste sæson til denne sæsons ligagennemsnit, ved ingen udfyldning er den rød, delvis udfyldning er gul, helt fyldt er grøn')
            st.plotly_chart(fig1,use_container_width=True)    
            
        def U19():
            import pandas as pd
            import csv
            import streamlit as st
            import numpy as np
            from datetime import datetime
            df = pd.read_csv('Teamsheet egne kampe U19.csv')
            kampe = df['label']
            option = st.multiselect('Vælg kamp (Hvis ingen kamp er valgt, vises gennemsnit for alle)',kampe)
            if len(option) > 0:
                temp_select = option
            else:
                temp_select = kampe

            dfsorteredekampe = df.loc[df.loc[df.label.isin(temp_select),'label'].index.values]
            dfsorteredekampe = dfsorteredekampe.iloc[: , 1:]
            #dfsorteredekampe['date'] = dfsorteredekampe['date'].astype(str)
            #dfsorteredekampe['date'] = dfsorteredekampe['date'].str.replace(r'\sGMT.*$', '', regex=True)
            #dfsorteredekampe['date'] = pd.to_datetime(dfsorteredekampe['date'], format="%B %d, %Y at %I:%M:%S %p")
            #dfsorteredekampe['date'] = dfsorteredekampe['date'].dt.strftime('%d-%m-%Y')
            dfsorteredekampe = dfsorteredekampe.transpose()
            dfoverskrifter = dfsorteredekampe[:2]
            dfsorteredekampe = dfsorteredekampe[2:].apply(pd.to_numeric, errors='coerce')
            dfsorteredekampe = pd.concat([dfoverskrifter,dfsorteredekampe])
            dfsorteredekampe = dfsorteredekampe.dropna(how='all')
            dfsorteredekampe = dfsorteredekampe.rename_axis('Parameter').astype(str)
            dfsorteredekampe = dfsorteredekampe.transpose()


            goals_cols = [col for col in dfsorteredekampe.columns if col.endswith('.goals')]
            shots_cols = [col for col in dfsorteredekampe.columns if col.endswith('.shots')]
            xg_cols = [col for col in dfsorteredekampe.columns if col.endswith('.xg')]
            duels_cols = [col for col in dfsorteredekampe.columns if col.endswith('.duels')]
            duelswon_cols = [col for col in dfsorteredekampe.columns if col.endswith('.duelsSuccessful')]
            possession_cols = [col for col in dfsorteredekampe.columns if col.endswith('.possessionPercent')]
            ppda_cols = [col for col in dfsorteredekampe.columns if col.endswith('.ppda')]

            # Create a new dataframe with the average values for each team
            team_data = {}
            for team in set([col.split('.')[1] for col in shots_cols]):
                team_goals = dfsorteredekampe[[col for col in goals_cols if(team) in col]].mean(axis=1)    
                team_shots = dfsorteredekampe[[col for col in shots_cols if(team) in col]].mean(axis=1)
                team_xg = dfsorteredekampe[[col for col in xg_cols if (team) in col]].mean(axis=1)
                team_duels = dfsorteredekampe[[col for col in duels_cols if (team) in col]].mean(axis=1)
                team_duelswon = dfsorteredekampe[[col for col in duelswon_cols if (team) in col]].mean(axis=1)
                team_possession = dfsorteredekampe[[col for col in possession_cols if (team) in col]].mean(axis=1)
                team_ppda = dfsorteredekampe[[col for col in ppda_cols if (team) in col]].mean(axis=1)

                team_data[team] = pd.concat([team_goals,team_shots, team_xg, team_duels,team_duelswon,team_possession,team_ppda], axis=1)
                
            team_df = pd.concat(team_data, axis=0, keys=team_data.keys())
            team_df.columns = ['Goals','Shots', 'Xg', 'Duels','Duels won','Possession %','PPDA']
            team_df = team_df.groupby(level=0).mean()

            st.write('Generelle stats')
            team_df= team_df.round(decimals=2)
            st.dataframe(team_df)

            forward_passes_cols = [col for col in dfsorteredekampe.columns if col.endswith('.forwardPasses')]
            forward_passes_successful_cols = [col for col in dfsorteredekampe.columns if col.endswith('.forwardPassesSuccessful')]
            passes_cols = [col for col in dfsorteredekampe.columns if col.endswith('.passes')]
            touches_in_box_cols = [col for col in dfsorteredekampe.columns if col.endswith('.touchesInBox')]
            xg_cols = [col for col in dfsorteredekampe.columns if col.endswith('.xg')]
            xgpershot_cols = [col for col in dfsorteredekampe.columns if col.endswith('.xgPerShot')]
            dzshots_cols = [col for col in dfsorteredekampe.columns if col.endswith('.shotsFromDangerZone')]
            possessionantal_cols = [col for col in dfsorteredekampe.columns if col.endswith('.possessionNumber')]
            possessionanmodstandershalvdel_cols = [col for col in dfsorteredekampe.columns if col.endswith('.reachingOpponentHalf')]
            possessionanmodstandersfelt_cols = [col for col in dfsorteredekampe.columns if col.endswith('.reachingOpponentBox')]
            challenge_intensity_cols = [col for col in dfsorteredekampe.columns if col.endswith('.challengeIntensity')]
            recoveries_cols = [col for col in dfsorteredekampe.columns if col.endswith('.recoveriesTotal')]
            opponenthalfrecoveries_cols = [col for col in dfsorteredekampe.columns if col.endswith('.opponentHalfRecoveries')]
            ppda_cols = [col for col in dfsorteredekampe.columns if col.endswith('.ppda')]

            # Create a new dataframe with the average values for each team
            team_data_målbare = {}
            for team in set([col.split('.')[1] for col in shots_cols]):
                team_forward_passes = dfsorteredekampe[[col for col in forward_passes_cols if(team) in col]].mean(axis=1)    
                team_forward_passes_successful = dfsorteredekampe[[col for col in forward_passes_successful_cols if(team) in col]].mean(axis=1)
                team_passes = dfsorteredekampe[[col for col in passes_cols if (team) in col]].mean(axis=1)
                team_touches_in_box = dfsorteredekampe[[col for col in touches_in_box_cols if (team) in col]].mean(axis=1)
                team_xg = dfsorteredekampe[[col for col in xg_cols if (team) in col]].mean(axis=1)
                team_xgpershot = dfsorteredekampe[[col for col in xgpershot_cols if (team) in col]].mean(axis=1)
                team_dzshots = dfsorteredekampe[[col for col in dzshots_cols if (team) in col]].mean(axis=1)
                team_possessionantal = dfsorteredekampe[[col for col in possessionantal_cols if (team) in col]].mean(axis=1)
                team_possessionmodstandershalvdel = dfsorteredekampe[[col for col in possessionanmodstandershalvdel_cols if (team) in col]].mean(axis=1)
                team_possessionmodstandersfelt = dfsorteredekampe[[col for col in possessionanmodstandersfelt_cols if (team) in col]].mean(axis=1)
                team_challenge_intensity = dfsorteredekampe[[col for col in challenge_intensity_cols if (team) in col]].mean(axis=1)
                team_recoveries = dfsorteredekampe[[col for col in recoveries_cols if (team) in col]].mean(axis=1)
                team_opponenthalfrecoveries = dfsorteredekampe[[col for col in opponenthalfrecoveries_cols if (team) in col]].mean(axis=1)

                team_ppda = dfsorteredekampe[[col for col in ppda_cols if (team) in col]].mean(axis=1)

                team_data_målbare[team] = pd.concat([team_forward_passes,team_forward_passes_successful, team_passes, team_touches_in_box,team_xg,team_xgpershot,team_dzshots,team_possessionantal,team_possessionmodstandershalvdel,team_possessionmodstandersfelt,team_challenge_intensity,team_recoveries,team_opponenthalfrecoveries,team_ppda], axis=1)
                
            team_df_målbare = pd.concat(team_data_målbare, axis=0, keys=team_data_målbare.keys())
            team_df_målbare.columns = ['Forward passes','Forward passes successful', 'Passes', 'Touches in box','xG','xG/shot','Dangerzone shots','Antal possessions','Antal possessions der når modstanders halvdel','Antal possessions der når modstanders felt','Challenge intensity','Recoveries','Opp half recoveries','PPDA']
            team_df_målbare = team_df_målbare.groupby(level=0).mean()
            team_df_målbare['Forward pass %'] = (team_df_målbare['Forward passes successful']/team_df_målbare['Forward passes'])*100
            team_df_målbare['Forward pass share'] = (team_df_målbare['Forward passes']/team_df_målbare['Passes'])*100
            team_df_målbare['Forward pass score'] = team_df_målbare[['Forward pass share','Forward pass %']].mean(axis=1)
            team_df_målbare['Possession to opp box'] = team_df_målbare['Antal possessions der når modstanders felt']
            team_df_målbare['Possession to opp half %'] = (team_df_målbare['Antal possessions der når modstanders halvdel']/team_df_målbare['Antal possessions'])*100
            team_df_målbare['Possession to opp box %'] = (team_df_målbare['Antal possessions der når modstanders felt']/team_df_målbare['Antal possessions'])*100
            team_df_målbare = team_df_målbare[['Forward pass score','Touches in box','xG','xG/shot','Dangerzone shots','Possession to opp box','Possession to opp half %','Possession to opp box %','Challenge intensity','Recoveries','Opp half recoveries','PPDA']]
            team_df_målbare = team_df_målbare.round(decimals=3)
            hold = 'Horsens U19'
            team_df_målbare_andre_hold = team_df_målbare.drop(hold)
            team_df_målbare['xG against'] = team_df_målbare_andre_hold['xG'].mean()
            team_df_målbare['Danger zone shots against'] = team_df_målbare_andre_hold['Dangerzone shots'].mean()
            team_df_målbare['Touches in box against'] = team_df_målbare_andre_hold['Touches in box'].mean()
            team_df_målbare['Duels won %'] = (team_df['Duels won']/team_df['Duels'])*100
            mask = team_df_målbare.index.str.contains('Horsens')
            team_df_målbare = team_df_målbare[mask]
            team_df_målbare = team_df_målbare.round(decimals=2)

            import pandas as pd
            import csv
            import streamlit as st
            import numpy as np
            from datetime import datetime

            df = pd.read_csv('Teamsheet alle kampe U19.csv')

            dfsorteredeallekampe = df.iloc[: , 1:]
            dfsorteredeallekampe['date'] = dfsorteredeallekampe['date'].astype(str)
            dfsorteredeallekampe['date'] = dfsorteredeallekampe['date'].str.replace(r'\sGMT.*$', '', regex=True)
            dfsorteredeallekampe['date'] = pd.to_datetime(dfsorteredeallekampe['date'], format="%B %d, %Y at %I:%M:%S %p")
            dfsorteredeallekampe['date'] = dfsorteredeallekampe['date'].dt.strftime('%d-%m-%Y')
            dfsorteredeallekampe = dfsorteredeallekampe.transpose()
            dfoverskrifter = dfsorteredeallekampe[:2]
            dfsorteredeallekampe = dfsorteredeallekampe[2:].apply(pd.to_numeric, errors='coerce')
            dfsorteredeallekampe = pd.concat([dfoverskrifter,dfsorteredeallekampe])
            dfsorteredeallekampe = dfsorteredeallekampe.dropna(how='all')
            dfsorteredeallekampe = dfsorteredeallekampe.rename_axis('Parameter').astype(str)
            dfsorteredeallekampe = dfsorteredeallekampe.transpose()


            goals_cols = [col for col in dfsorteredeallekampe.columns if col.endswith('.goals')]
            shots_cols = [col for col in dfsorteredeallekampe.columns if col.endswith('.shots')]
            xg_cols = [col for col in dfsorteredeallekampe.columns if col.endswith('.xg')]
            duels_cols = [col for col in dfsorteredeallekampe.columns if col.endswith('.duels')]
            duelswon_cols = [col for col in dfsorteredeallekampe.columns if col.endswith('.duelsSuccessful')]
            possession_cols = [col for col in dfsorteredeallekampe.columns if col.endswith('.possessionPercent')]
            ppda_cols = [col for col in dfsorteredeallekampe.columns if col.endswith('.ppda')]

            # Create a new dataframe with the average values for each team
            team_data = {}
            for team in set([col.split('.')[1] for col in shots_cols]):
                team_goals = dfsorteredeallekampe[[col for col in goals_cols if(team) in col]].mean(axis=1)    
                team_shots = dfsorteredeallekampe[[col for col in shots_cols if(team) in col]].mean(axis=1)
                team_xg = dfsorteredeallekampe[[col for col in xg_cols if (team) in col]].mean(axis=1)
                team_duels = dfsorteredeallekampe[[col for col in duels_cols if (team) in col]].mean(axis=1)
                team_duelswon = dfsorteredeallekampe[[col for col in duelswon_cols if (team) in col]].mean(axis=1)
                team_possession = dfsorteredeallekampe[[col for col in possession_cols if (team) in col]].mean(axis=1)
                team_ppda = dfsorteredeallekampe[[col for col in ppda_cols if (team) in col]].mean(axis=1)

                team_data[team] = pd.concat([team_goals,team_shots, team_xg, team_duels,team_duelswon,team_possession,team_ppda], axis=1)
                
            team_df = pd.concat(team_data, axis=0, keys=team_data.keys())
            team_df.columns = ['Goals','Shots', 'Xg', 'Duels','Duels won','Possession %','PPDA']
            team_df = team_df.groupby(level=0).mean()
            team_df= team_df.round(decimals=2)


            forward_passes_cols = [col for col in dfsorteredeallekampe.columns if col.endswith('.forwardPasses')]
            forward_passes_successful_cols = [col for col in dfsorteredeallekampe.columns if col.endswith('.forwardPassesSuccessful')]
            passes_cols = [col for col in dfsorteredeallekampe.columns if col.endswith('.passes')]
            touches_in_box_cols = [col for col in dfsorteredeallekampe.columns if col.endswith('.touchesInBox')]
            xg_cols = [col for col in dfsorteredeallekampe.columns if col.endswith('.xg')]
            xgpershot_cols = [col for col in dfsorteredeallekampe.columns if col.endswith('.xgPerShot')]
            dzshots_cols = [col for col in dfsorteredeallekampe.columns if col.endswith('.shotsFromDangerZone')]
            possessionantal_cols = [col for col in dfsorteredeallekampe.columns if col.endswith('.possessionNumber')]
            possessionanmodstandershalvdel_cols = [col for col in dfsorteredeallekampe.columns if col.endswith('.reachingOpponentHalf')]
            possessionanmodstandersfelt_cols = [col for col in dfsorteredeallekampe.columns if col.endswith('.reachingOpponentBox')]
            challenge_intensity_cols = [col for col in dfsorteredeallekampe.columns if col.endswith('.challengeIntensity')]
            recoveries_cols = [col for col in dfsorteredeallekampe.columns if col.endswith('.recoveriesTotal')]
            opponenthalfrecoveries_cols = [col for col in dfsorteredeallekampe.columns if col.endswith('.opponentHalfRecoveries')]
            ppda_cols = [col for col in dfsorteredeallekampe.columns if col.endswith('.ppda')]

            # Create a new dataframe with the average values for each team
            team_data_målbare_alle = {}
            for team in set([col.split('.')[1] for col in shots_cols]):
                team_forward_passes = dfsorteredeallekampe[[col for col in forward_passes_cols if(team) in col]].mean(axis=1)    
                team_forward_passes_successful = dfsorteredeallekampe[[col for col in forward_passes_successful_cols if(team) in col]].mean(axis=1)
                team_passes = dfsorteredeallekampe[[col for col in passes_cols if (team) in col]].mean(axis=1)
                team_touches_in_box = dfsorteredeallekampe[[col for col in touches_in_box_cols if (team) in col]].mean(axis=1)
                team_xg = dfsorteredeallekampe[[col for col in xg_cols if (team) in col]].mean(axis=1)
                team_xgpershot = dfsorteredeallekampe[[col for col in xgpershot_cols if (team) in col]].mean(axis=1)
                team_dzshots = dfsorteredeallekampe[[col for col in dzshots_cols if (team) in col]].mean(axis=1)
                team_possessionantal = dfsorteredeallekampe[[col for col in possessionantal_cols if (team) in col]].mean(axis=1)
                team_possessionmodstandershalvdel = dfsorteredeallekampe[[col for col in possessionanmodstandershalvdel_cols if (team) in col]].mean(axis=1)
                team_possessionmodstandersfelt = dfsorteredeallekampe[[col for col in possessionanmodstandersfelt_cols if (team) in col]].mean(axis=1)
                team_challenge_intensity = dfsorteredeallekampe[[col for col in challenge_intensity_cols if (team) in col]].mean(axis=1)
                team_recoveries = dfsorteredeallekampe[[col for col in recoveries_cols if (team) in col]].mean(axis=1)
                team_opponenthalfrecoveries = dfsorteredeallekampe[[col for col in opponenthalfrecoveries_cols if (team) in col]].mean(axis=1)

                team_ppda = dfsorteredeallekampe[[col for col in ppda_cols if (team) in col]].mean(axis=1)

                team_data_målbare_alle[team] = pd.concat([team_forward_passes,team_forward_passes_successful, team_passes, team_touches_in_box,team_xg,team_xgpershot,team_dzshots,team_possessionantal,team_possessionmodstandershalvdel,team_possessionmodstandersfelt,team_challenge_intensity,team_recoveries,team_opponenthalfrecoveries,team_ppda], axis=1)
                
            team_df_målbare_alle = pd.concat(team_data_målbare_alle, axis=0, keys=team_data_målbare_alle.keys())
            team_df_målbare_alle.columns = ['Forward passes','Forward passes successful', 'Passes', 'Touches in box','xG','xG/shot','Dangerzone shots','Antal possessions','Antal possessions der når modstanders halvdel','Antal possessions der når modstanders felt','Challenge intensity','Recoveries','Opp half recoveries','PPDA']
            team_df_målbare_alle = team_df_målbare_alle.groupby(level=0).mean()
            team_df_målbare_alle['Forward pass %'] = (team_df_målbare_alle['Forward passes successful']/team_df_målbare_alle['Forward passes'])*100
            team_df_målbare_alle['Forward pass share'] = (team_df_målbare_alle['Forward passes']/team_df_målbare_alle['Passes'])*100
            team_df_målbare_alle['Forward pass score'] = team_df_målbare_alle[['Forward pass share','Forward pass %']].mean(axis=1)
            team_df_målbare_alle['Possession to opp box'] = team_df_målbare_alle['Antal possessions der når modstanders felt']
            team_df_målbare_alle['Possession to opp half %'] = (team_df_målbare_alle['Antal possessions der når modstanders halvdel']/team_df_målbare_alle['Antal possessions'])*100
            team_df_målbare_alle['Possession to opp box %'] = (team_df_målbare_alle['Antal possessions der når modstanders felt']/team_df_målbare_alle['Antal possessions'])*100
            team_df_målbare_alle = team_df_målbare_alle[['Forward pass score','Touches in box','xG','xG/shot','Dangerzone shots','Possession to opp box','Possession to opp half %','Possession to opp box %','Challenge intensity','Recoveries','Opp half recoveries','PPDA']]
            team_df_målbare_alle = team_df_målbare_alle.round(decimals=3)
            #hold = 'Horsens U15'
            #team_df_målbare_andre_hold = team_df_målbare.drop(hold)
            team_df_målbare_alle['xG against'] = team_df_målbare_alle['xG'].mean()
            team_df_målbare_alle['Danger zone shots against'] = team_df_målbare_alle['Dangerzone shots'].mean()
            team_df_målbare_alle['Touches in box against'] = team_df_målbare_alle['Touches in box'].mean()
            team_df_målbare_alle['Duels won %'] = (team_df['Duels won']/team_df['Duels'])*100
            team_df_målbare_alle = team_df_målbare_alle.round(decimals=2)
            Benchmark = team_df_målbare_alle.mean(axis=0)
            team_df_målbare_alle.loc['Liga Gennemsnit'] = Benchmark
            mask = team_df_målbare_alle.index.str.contains('Liga Gennemsnit')
            team_df_målbare_alle = team_df_målbare_alle[mask]


            df = pd.read_csv('Teamsheet alle kampe U19 sidste sæson.csv')

            dfsorteredekampesidstesæson = df.iloc[: , 1:]
            dfsorteredekampesidstesæson['date'] = dfsorteredekampesidstesæson['date'].astype(str)
            dfsorteredekampesidstesæson['date'] = dfsorteredekampesidstesæson['date'].str.replace(r'\sGMT.*$', '', regex=True)
            dfsorteredekampesidstesæson['date'] = pd.to_datetime(dfsorteredekampesidstesæson['date'], format="%B %d, %Y at %I:%M:%S %p")
            dfsorteredekampesidstesæson['date'] = dfsorteredekampesidstesæson['date'].dt.strftime('%d-%m-%Y')
            dfsorteredekampesidstesæson = dfsorteredekampesidstesæson.transpose()
            dfoverskrifter = dfsorteredekampesidstesæson[:2]
            dfsorteredekampesidstesæson = dfsorteredekampesidstesæson[2:].apply(pd.to_numeric, errors='coerce')
            dfsorteredekampesidstesæson = pd.concat([dfoverskrifter,dfsorteredekampesidstesæson])
            dfsorteredekampesidstesæson = dfsorteredekampesidstesæson.dropna(how='all')
            dfsorteredekampesidstesæson = dfsorteredekampesidstesæson.rename_axis('Parameter').astype(str)
            dfsorteredekampesidstesæson = dfsorteredekampesidstesæson.transpose()


            goals_cols = [col for col in dfsorteredekampesidstesæson.columns if col.endswith('.goals')]
            shots_cols = [col for col in dfsorteredekampesidstesæson.columns if col.endswith('.shots')]
            xg_cols = [col for col in dfsorteredekampesidstesæson.columns if col.endswith('.xg')]
            duels_cols = [col for col in dfsorteredekampesidstesæson.columns if col.endswith('.duels')]
            duelswon_cols = [col for col in dfsorteredekampesidstesæson.columns if col.endswith('.duelsSuccessful')]
            possession_cols = [col for col in dfsorteredekampesidstesæson.columns if col.endswith('.possessionPercent')]
            ppda_cols = [col for col in dfsorteredekampesidstesæson.columns if col.endswith('.ppda')]

            # Create a new dataframe with the average values for each team
            team_data_sidstesæson = {}
            for team in set([col.split('.')[1] for col in shots_cols]):
                team_goals = dfsorteredekampesidstesæson[[col for col in goals_cols if(team) in col]].mean(axis=1)    
                team_shots = dfsorteredekampesidstesæson[[col for col in shots_cols if(team) in col]].mean(axis=1)
                team_xg = dfsorteredekampesidstesæson[[col for col in xg_cols if (team) in col]].mean(axis=1)
                team_duels = dfsorteredekampesidstesæson[[col for col in duels_cols if (team) in col]].mean(axis=1)
                team_duelswon = dfsorteredekampesidstesæson[[col for col in duelswon_cols if (team) in col]].mean(axis=1)
                team_possession = dfsorteredekampesidstesæson[[col for col in possession_cols if (team) in col]].mean(axis=1)
                team_ppda = dfsorteredekampesidstesæson[[col for col in ppda_cols if (team) in col]].mean(axis=1)

                team_data_sidstesæson[team] = pd.concat([team_goals,team_shots, team_xg, team_duels,team_duelswon,team_possession,team_ppda], axis=1)
                
            team_df_sidstesæson = pd.concat(team_data_sidstesæson, axis=0, keys=team_data_sidstesæson.keys())
            team_df_sidstesæson.columns = ['Goals','Shots', 'Xg', 'Duels','Duels won','Possession %','PPDA']
            team_df_sidstesæson = team_df_sidstesæson.groupby(level=0).mean()


            team_df_sidstesæson= team_df_sidstesæson.round(decimals=2)


            forward_passes_cols = [col for col in dfsorteredekampesidstesæson.columns if col.endswith('.forwardPasses')]
            forward_passes_successful_cols = [col for col in dfsorteredekampesidstesæson.columns if col.endswith('.forwardPassesSuccessful')]
            passes_cols = [col for col in dfsorteredekampesidstesæson.columns if col.endswith('.passes')]
            touches_in_box_cols = [col for col in dfsorteredekampesidstesæson.columns if col.endswith('.touchesInBox')]
            xg_cols = [col for col in dfsorteredekampesidstesæson.columns if col.endswith('.xg')]
            xgpershot_cols = [col for col in dfsorteredekampesidstesæson.columns if col.endswith('.xgPerShot')]
            dzshots_cols = [col for col in dfsorteredekampesidstesæson.columns if col.endswith('.shotsFromDangerZone')]
            possessionantal_cols = [col for col in dfsorteredekampesidstesæson.columns if col.endswith('.possessionNumber')]
            possessionanmodstandershalvdel_cols = [col for col in dfsorteredekampesidstesæson.columns if col.endswith('.reachingOpponentHalf')]
            possessionanmodstandersfelt_cols = [col for col in dfsorteredekampesidstesæson.columns if col.endswith('.reachingOpponentBox')]
            challenge_intensity_cols = [col for col in dfsorteredekampesidstesæson.columns if col.endswith('.challengeIntensity')]
            recoveries_cols = [col for col in dfsorteredekampesidstesæson.columns if col.endswith('.recoveriesTotal')]
            opponenthalfrecoveries_cols = [col for col in dfsorteredekampesidstesæson.columns if col.endswith('.opponentHalfRecoveries')]
            ppda_cols = [col for col in dfsorteredekampesidstesæson.columns if col.endswith('.ppda')]

            # Create a new dataframe with the average values for each team
            team_data_målbare_sidstesæson = {}
            for team in set([col.split('.')[1] for col in shots_cols]):
                team_forward_passes = dfsorteredekampesidstesæson[[col for col in forward_passes_cols if(team) in col]].mean(axis=1)    
                team_forward_passes_successful = dfsorteredekampesidstesæson[[col for col in forward_passes_successful_cols if(team) in col]].mean(axis=1)
                team_passes = dfsorteredekampesidstesæson[[col for col in passes_cols if (team) in col]].mean(axis=1)
                team_touches_in_box = dfsorteredekampesidstesæson[[col for col in touches_in_box_cols if (team) in col]].mean(axis=1)
                team_xg = dfsorteredekampesidstesæson[[col for col in xg_cols if (team) in col]].mean(axis=1)
                team_xgpershot = dfsorteredekampesidstesæson[[col for col in xgpershot_cols if (team) in col]].mean(axis=1)
                team_dzshots = dfsorteredekampesidstesæson[[col for col in dzshots_cols if (team) in col]].mean(axis=1)
                team_possessionantal = dfsorteredekampesidstesæson[[col for col in possessionantal_cols if (team) in col]].mean(axis=1)
                team_possessionmodstandershalvdel = dfsorteredekampesidstesæson[[col for col in possessionanmodstandershalvdel_cols if (team) in col]].mean(axis=1)
                team_possessionmodstandersfelt = dfsorteredekampesidstesæson[[col for col in possessionanmodstandersfelt_cols if (team) in col]].mean(axis=1)
                team_challenge_intensity = dfsorteredekampesidstesæson[[col for col in challenge_intensity_cols if (team) in col]].mean(axis=1)
                team_recoveries = dfsorteredekampesidstesæson[[col for col in recoveries_cols if (team) in col]].mean(axis=1)
                team_opponenthalfrecoveries = dfsorteredekampesidstesæson[[col for col in opponenthalfrecoveries_cols if (team) in col]].mean(axis=1)

                team_ppda = dfsorteredekampesidstesæson[[col for col in ppda_cols if (team) in col]].mean(axis=1)

                team_data_målbare_sidstesæson[team] = pd.concat([team_forward_passes,team_forward_passes_successful, team_passes, team_touches_in_box,team_xg,team_xgpershot,team_dzshots,team_possessionantal,team_possessionmodstandershalvdel,team_possessionmodstandersfelt,team_challenge_intensity,team_recoveries,team_opponenthalfrecoveries,team_ppda], axis=1)
                
            team_df_målbaresidstesæson = pd.concat(team_data_målbare_sidstesæson, axis=0, keys=team_data_målbare_sidstesæson.keys())
            team_df_målbaresidstesæson.columns = ['Forward passes','Forward passes successful', 'Passes', 'Touches in box','xG','xG/shot','Dangerzone shots','Antal possessions','Antal possessions der når modstanders halvdel','Antal possessions der når modstanders felt','Challenge intensity','Recoveries','Opp half recoveries','PPDA']
            team_df_målbaresidstesæson = team_df_målbaresidstesæson.groupby(level=0).mean()
            team_df_målbaresidstesæson['Forward pass %'] = (team_df_målbaresidstesæson['Forward passes successful']/team_df_målbaresidstesæson['Forward passes'])*100
            team_df_målbaresidstesæson['Forward pass share'] = (team_df_målbaresidstesæson['Forward passes']/team_df_målbaresidstesæson['Passes'])*100
            team_df_målbaresidstesæson['Forward pass score'] = team_df_målbaresidstesæson[['Forward pass share','Forward pass %']].mean(axis=1)
            team_df_målbaresidstesæson['Possession to opp box'] = team_df_målbaresidstesæson['Antal possessions der når modstanders felt']
            team_df_målbaresidstesæson['Possession to opp half %'] = (team_df_målbaresidstesæson['Antal possessions der når modstanders halvdel']/team_df_målbaresidstesæson['Antal possessions'])*100
            team_df_målbaresidstesæson['Possession to opp box %'] = (team_df_målbaresidstesæson['Antal possessions der når modstanders felt']/team_df_målbaresidstesæson['Antal possessions'])*100
            team_df_målbaresidstesæson = team_df_målbaresidstesæson[['Forward pass score','Touches in box','xG','xG/shot','Dangerzone shots','Possession to opp box','Possession to opp half %','Possession to opp box %','Challenge intensity','Recoveries','Opp half recoveries','PPDA']]
            team_df_målbaresidstesæson = team_df_målbaresidstesæson.round(decimals=3)

            team_df_målbaresidstesæson['xG against'] = team_df_målbaresidstesæson['xG'].mean()
            team_df_målbaresidstesæson['Danger zone shots against'] = team_df_målbaresidstesæson['Dangerzone shots'].mean()
            team_df_målbaresidstesæson['Touches in box against'] = team_df_målbaresidstesæson['Touches in box'].mean()
            team_df_målbaresidstesæson['Duels won %'] = (team_df_sidstesæson['Duels won']/team_df_sidstesæson['Duels'])*100
            mask = team_df_målbaresidstesæson.index.str.contains('Horsens')
            team_df_målbaresidstesæson = team_df_målbaresidstesæson[mask]
            team_df_målbaresidstesæson = team_df_målbaresidstesæson.round(decimals=2)
            frames = [team_df_målbare_alle,team_df_målbare,team_df_målbaresidstesæson]
            Benchmark = pd.concat(frames)
            st.dataframe(Benchmark)
            import plotly.graph_objs as go
            import numpy as np
            from plotly.subplots import make_subplots

            trace1 = go.Indicator(mode="gauge+number",    value=Benchmark['Forward pass score'][1],domain={'row' : 1, 'column' : 1},title={'text': "Forward pass score"},gauge={'axis': {'range': [min(Benchmark['Forward pass score'][0], Benchmark['Forward pass score'][2]),max(Benchmark['Forward pass score'][0], Benchmark['Forward pass score'][2])]}})
            trace2 = go.Indicator(mode="gauge+number",    value=Benchmark['Touches in box'][1],domain={'row' : 1, 'column' : 2},title={'text': "Touches in box"},gauge={'axis': {'range': [min(Benchmark['Touches in box'][0], Benchmark['Touches in box'][2]),max(Benchmark['Touches in box'][0], Benchmark['Touches in box'][2])]}})
            trace3 = go.Indicator(mode="gauge+number",    value=Benchmark['xG'][1],domain={'row' : 1, 'column' : 3},title={'text': "xG"},gauge={'axis': {'range': [min(Benchmark['xG'][0], Benchmark['xG'][2]),max(Benchmark['xG'][0], Benchmark['xG'][2])]}})
            trace4 = go.Indicator(mode="gauge+number",    value=Benchmark['xG/shot'][1],domain={'row' : 1, 'column' : 4},title={'text': "xG/shot"},gauge={'axis': {'range': [min(Benchmark['xG/shot'][0], Benchmark['xG/shot'][2]),max(Benchmark['xG/shot'][0], Benchmark['xG/shot'][2])]}})
            trace5 = go.Indicator(mode="gauge+number",    value=Benchmark['Dangerzone shots'][1],domain={'row' : 2, 'column' : 1},title={'text': "Dangerzone shots"},gauge={'axis': {'range': [min(Benchmark['Dangerzone shots'][0], Benchmark['Dangerzone shots'][2]),max(Benchmark['Dangerzone shots'][0], Benchmark['Dangerzone shots'][2])]}})
            trace6 = go.Indicator(mode="gauge+number",    value=Benchmark['Possession to opp box'][1],domain={'row' : 2, 'column' : 2},title={'text': "Possession to opp box"},gauge={'axis': {'range': [min(Benchmark['Possession to opp box'][0], Benchmark['Possession to opp box'][2]),max(Benchmark['Possession to opp box'][0], Benchmark['Possession to opp box'][2])]}})
            trace7 = go.Indicator(mode="gauge+number",    value=Benchmark['Possession to opp half %'][1],domain={'row' : 2, 'column' : 3},title={'text': "Possession to opp half %"},gauge={'axis': {'range': [min(Benchmark['Possession to opp half %'][0], Benchmark['Possession to opp half %'][2]),max(Benchmark['Possession to opp half %'][0], Benchmark['Possession to opp half %'][2])]}})
            trace8 = go.Indicator(mode="gauge+number",    value=Benchmark['Possession to opp box %'][1],domain={'row' : 2, 'column' : 4},title={'text': "Possession to opp box %"},gauge={'axis': {'range': [min(Benchmark['Possession to opp box %'][0], Benchmark['Possession to opp box %'][2]),max(Benchmark['Possession to opp box %'][0], Benchmark['Possession to opp box %'][2])]}})
            
            fig = make_subplots(
            rows=2,
            cols=4,
            specs=[[{'type' : 'indicator'},{'type' : 'indicator'},{'type' : 'indicator'},{'type' : 'indicator'}],[{'type' : 'indicator'},{'type' : 'indicator'},{'type' : 'indicator'},{'type' : 'indicator'}]],
            )

            fig.append_trace(trace1, row=1, col=1)
            fig.append_trace(trace2, row=1, col=2)
            fig.append_trace(trace3, row=1, col=3)
            fig.append_trace(trace4, row=1, col=4)
            fig.append_trace(trace5, row=2, col=1)
            fig.append_trace(trace6, row=2, col=2)
            fig.append_trace(trace7, row=2, col=3)
            fig.append_trace(trace8, row=2, col=4)
            
            st.title('Offensive parametre')
            st.write('Skalaen går fra eget gennemsnit i seneste sæson til denne sæsons ligagennemsnit, ved ingen udfyldning er den rød, delvis udfyldning er gul, helt fyldt er grøn')
            st.plotly_chart(fig,use_container_width=True)
            
            trace9 = go.Indicator(mode="gauge+number",    value=Benchmark['xG against'][1],domain={'row' : 1, 'column' : 1},title={'text': "xG against"},gauge={'axis': {'range': [max(Benchmark['xG against'][0], Benchmark['xG against'][2]),min(Benchmark['xG against'][0], Benchmark['xG against'][2])]}})
            trace10 = go.Indicator(mode="gauge+number",    value=Benchmark['PPDA'][1],domain={'row' : 1, 'column' : 2},title={'text': "PPDA"},gauge={'axis': {'range': [max(Benchmark['PPDA'][0], Benchmark['PPDA'][2]),min(Benchmark['PPDA'][0], Benchmark['PPDA'][2])]}})
            trace11 = go.Indicator(mode="gauge+number",    value=Benchmark['Danger zone shots against'][1],domain={'row' : 1, 'column' : 3},title={'text': "Danger zone shots against"},gauge={'axis': {'range': [max(Benchmark['Danger zone shots against'][0], Benchmark['Danger zone shots against'][2]),min(Benchmark['Danger zone shots against'][0], Benchmark['Danger zone shots against'][2])]}})
            trace12 = go.Indicator(mode="gauge+number",    value=Benchmark['Challenge intensity'][1],domain={'row' : 1, 'column' : 4},title={'text': "Challenge intensity"},gauge={'axis': {'range': [min(Benchmark['Challenge intensity'][0], Benchmark['Challenge intensity'][2]),max(Benchmark['Challenge intensity'][0], Benchmark['Challenge intensity'][2])]}})
            trace13 = go.Indicator(mode="gauge+number",    value=Benchmark['Recoveries'][1],domain={'row' : 2, 'column' : 1},title={'text': "Recoveries"},gauge={'axis': {'range': [min(Benchmark['Recoveries'][0], Benchmark['Recoveries'][2]),max(Benchmark['Recoveries'][0], Benchmark['Recoveries'][2])]}})
            trace14 = go.Indicator(mode="gauge+number",    value=Benchmark['Opp half recoveries'][1],domain={'row' : 2, 'column' : 2},title={'text': "Opp half recoveries"},gauge={'axis': {'range': [min(Benchmark['Opp half recoveries'][0], Benchmark['Opp half recoveries'][2]),max(Benchmark['Opp half recoveries'][0], Benchmark['Opp half recoveries'][2])]}})
            trace15 = go.Indicator(mode="gauge+number",    value=Benchmark['Touches in box against'][1],domain={'row' : 2, 'column' : 3},title={'text': "Touches in box against"},gauge={'axis': {'range': [max(Benchmark['Touches in box against'][0], Benchmark['Touches in box against'][2]),min(Benchmark['Touches in box against'][0], Benchmark['Touches in box against'][2])]}})
            trace16 = go.Indicator(mode="gauge+number",    value=Benchmark['Duels won %'][1],domain={'row' : 2, 'column' : 4},title={'text': "Duels won %"},gauge={'axis': {'range': [min(Benchmark['Duels won %'][0], Benchmark['Duels won %'][2]),max(Benchmark['Duels won %'][0], Benchmark['Duels won %'][2])]}})
            fig1 = make_subplots(
            rows=2,
            cols=4,
            specs=[[{'type' : 'indicator'},{'type' : 'indicator'},{'type' : 'indicator'},{'type' : 'indicator'}],[{'type' : 'indicator'},{'type' : 'indicator'},{'type' : 'indicator'},{'type' : 'indicator'}]],
            )

            fig1.append_trace(trace9, row=1, col=1)
            fig1.append_trace(trace10, row=1, col=2)
            fig1.append_trace(trace11, row=1, col=3)
            fig1.append_trace(trace12, row=1, col=4)
            fig1.append_trace(trace13, row=2, col=1)
            fig1.append_trace(trace14, row=2, col=2)
            fig1.append_trace(trace15, row=2, col=3)
            fig1.append_trace(trace16, row=2, col=4)
            st.title('Defensive parametre')
            st.write('Skalaen går fra eget gennemsnit i seneste sæson til denne sæsons ligagennemsnit, ved ingen udfyldning er den rød, delvis udfyldning er gul, helt fyldt er grøn')
            st.plotly_chart(fig1,use_container_width=True)    


        Årgange = {
            'U13':U13,
            'U14':U14,
            'U15':U15,
            'U17':U17,
            'U19':U19,
        }
        rullemenu = st.selectbox('Vælg årgang',Årgange.keys())
        Årgange[rullemenu]()

    def Kampevaluering():
        def U15():
            import json
            import pandas as pd
            import matplotlib.pyplot as plt
            import seaborn as sns
            from mplsoccer.pitch import Pitch
            import numpy as np
            import streamlit as st
            df = pd.read_csv(r'xT/U15 Ligaen 23 24.csv')

            hold = 'Horsens U15'
            df = df[df['label'].str.contains(hold)]
            df['date'] = pd.to_datetime(df['date'])
            df = df.sort_values(by='date',ascending=False)
            valgtekamp = st.multiselect('Vælg kamp', df['label'].unique(),default=df['label'].unique()[0])

            df1 = df.copy()

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

            dfscore = pd.read_csv(r'xT/Zone scores.csv')

            df = df.merge(dfscore[['Start Zone', 'Start zone score']], on='Start Zone', how='left')

            # Merge 'End Zone' scores
            df = df.merge(dfscore[['End Zone', 'End zone score']], on='End Zone', how='left')

            df['xT'] = df['End zone score'] - df['Start zone score']
            xThold = df.groupby(['team.name'])['xT'].agg('sum').reset_index()

            with st.expander('Se xT model'):
                col1,col2 = st.columns(2)
                with col1:
                    from PIL import Image
                    image = Image.open('xT/xT zoner.png')
                    st.image(image,'xT zoner')
                with col2:
                    zoner = pd.read_csv(r'xT/Zone scores.csv')
                    zoner = zoner[['Start Zone','Start zone score']]
                    zoner = zoner.rename(columns={'Start Zone': 'Zone'})
                    zoner = zoner.rename(columns={'Start zone score': 'Zone score'})

                    st.dataframe(zoner,hide_index=True)
                    st.write('xT udregnes som: zonen hvor pasning/dribling slutter - zone hvor pasning/dribling starter')
                    st.write('Zonernes værdi er udregnet på baggrund af de seneste 8 sæsoner i 1. div og Superligaen med udgangspunkt i den gennemsnitlige værdi for en boldbesiddelse i zonen. Den er så vægtet efter hvor mange aktioner der går fra boldbesiddelsen i zonen til en afslutning. Jo flere jo lavere vægtning')

            xgc = df1
            xgchold = xgc.rename(columns={'shot.xg': 'Hold xG i åbent spil'})
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


            col1,col2, col34 = st.columns([1,1,2])
            with col1:  
                xTspiller = df.groupby(['player.name','team.name'])['xT'].agg('sum').reset_index()
                xTspiller = xTspiller[xTspiller['team.name'] == hold]
                xTspiller = xTspiller.sort_values(by='xT', ascending=False)
                xTspiller = xTspiller[['player.name','xT']]
                st.dataframe(xTspiller,hide_index=True)
                samlet = xgcspiller.merge(xTspiller)
            with col2:
                xgcspiller = xgcspiller[['player.name','xGC','xGCC']]
                st.dataframe(xgcspiller,hide_index=True)
            
            with col34:
                xgplacering = df1
                xgplacering = xgplacering[xgplacering['shot.xg'] > 0]
                xgplacering = xgplacering[xgplacering['team.name'] == hold]
                
                x = xgplacering['location.x']
                y = xgplacering['location.y']
                player_names = xgplacering['player.name']  # Extract player names
                label_text = xgplacering.sort_values(by='shot.xg',ascending=False)
                label_text = label_text[['player.name', 'shot.xg']].to_string(index=False,header=False)
                shot_xg = xgplacering['shot.xg'].astype(float)
                min_size = 5  # Minimum dot size
                max_size = 100  # Maximum dot size
                sizes = np.interp(shot_xg, (shot_xg.min(), shot_xg.max()), (min_size, max_size))

                pitch = Pitch(pitch_type='wyscout', pitch_color='grass', line_color='white', stripe=True)
                fig, ax = pitch.draw()
                sc = pitch.scatter(x, y, ax=ax, s=sizes)

                # Add player names as labels using annotate
                for i, txt in enumerate(player_names):
                    ax.annotate(txt, (x.iloc[i], y.iloc[i]), color='white', fontsize=8, ha='center', va='bottom')

                ax.text(0.3, 0.5, label_text, color='black', ha='center', va='center',
                        transform=ax.transAxes, fontsize=10, bbox=dict(facecolor='white', alpha=0.7))


                st.write('Xg plot (Jo større markering, jo større xG)')
                st.pyplot(plt.gcf(), use_container_width=True)
                                
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
                pass_df = pass_df[(pass_df['location.x'] > 33) & (pass_df['location.x'] < 66)]
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

        def U17():
            import json
            import pandas as pd
            import matplotlib.pyplot as plt
            import seaborn as sns
            from mplsoccer.pitch import Pitch
            import numpy as np
            import streamlit as st
            df = pd.read_csv(r'xT/U17 Ligaen 23 24.csv')

            hold = 'Horsens U17'
            df = df[df['label'].str.contains(hold)]
            df['date'] = pd.to_datetime(df['date'])
            df = df.sort_values(by='date',ascending=False)
            valgtekamp = st.multiselect('Vælg kamp', df['label'].unique(),default=df['label'].unique()[0])

            df1 = df.copy()

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

            dfscore = pd.read_csv(r'xT/Zone scores.csv')

            df = df.merge(dfscore[['Start Zone', 'Start zone score']], on='Start Zone', how='left')

            # Merge 'End Zone' scores
            df = df.merge(dfscore[['End Zone', 'End zone score']], on='End Zone', how='left')

            df['xT'] = df['End zone score'] - df['Start zone score']
            xThold = df.groupby(['team.name'])['xT'].agg('sum').reset_index()

            with st.expander('Se xT model'):
                col1,col2 = st.columns(2)
                with col1:
                    from PIL import Image
                    image = Image.open('xT/xT zoner.png')
                    st.image(image,'xT zoner')
                with col2:
                    zoner = pd.read_csv(r'xT/Zone scores.csv')
                    zoner = zoner[['Start Zone','Start zone score']]
                    zoner = zoner.rename(columns={'Start Zone': 'Zone'})
                    zoner = zoner.rename(columns={'Start zone score': 'Zone score'})

                    st.dataframe(zoner,hide_index=True)
                    st.write('xT udregnes som: zonen hvor pasning/dribling slutter - zone hvor pasning/dribling starter')
                    st.write('Zonernes værdi er udregnet på baggrund af de seneste 8 sæsoner i 1. div og Superligaen med udgangspunkt i den gennemsnitlige værdi for en boldbesiddelse i zonen. Den er så vægtet efter hvor mange aktioner der går fra boldbesiddelsen i zonen til en afslutning. Jo flere jo lavere vægtning')

            xgc = df1
            xgchold = xgc.rename(columns={'shot.xg': 'Hold xG i åbent spil'})
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


            col1,col2, col34 = st.columns([1,1,2])
            with col1:  
                xTspiller = df.groupby(['player.name','team.name'])['xT'].agg('sum').reset_index()
                xTspiller = xTspiller[xTspiller['team.name'] == hold]
                xTspiller = xTspiller.sort_values(by='xT', ascending=False)
                xTspiller = xTspiller[['player.name','xT']]
                st.dataframe(xTspiller,hide_index=True)
                samlet = xgcspiller.merge(xTspiller)
            with col2:
                xgcspiller = xgcspiller[['player.name','xGC','xGCC']]
                st.dataframe(xgcspiller,hide_index=True)
            
            with col34:
                xgplacering = df1
                xgplacering = xgplacering[xgplacering['shot.xg'] > 0]
                xgplacering = xgplacering[xgplacering['team.name'] == hold]
                
                x = xgplacering['location.x']
                y = xgplacering['location.y']
                player_names = xgplacering['player.name']  # Extract player names
                label_text = xgplacering.sort_values(by='shot.xg',ascending=False)
                label_text = label_text[['player.name', 'shot.xg']].to_string(index=False,header=False)
                shot_xg = xgplacering['shot.xg'].astype(float)
                min_size = 5  # Minimum dot size
                max_size = 100  # Maximum dot size
                sizes = np.interp(shot_xg, (shot_xg.min(), shot_xg.max()), (min_size, max_size))

                pitch = Pitch(pitch_type='wyscout', pitch_color='grass', line_color='white', stripe=True)
                fig, ax = pitch.draw()
                sc = pitch.scatter(x, y, ax=ax, s=sizes)

                # Add player names as labels using annotate
                for i, txt in enumerate(player_names):
                    ax.annotate(txt, (x.iloc[i], y.iloc[i]), color='white', fontsize=8, ha='center', va='bottom')

                ax.text(0.3, 0.5, label_text, color='black', ha='center', va='center',
                        transform=ax.transAxes, fontsize=10, bbox=dict(facecolor='white', alpha=0.7))


                st.write('Xg plot (Jo større markering, jo større xG)')
                st.pyplot(plt.gcf(), use_container_width=True)
                
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
                pass_df = pass_df[(pass_df['location.x'] > 33) & (pass_df['location.x'] < 66)]
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

        def U19():
            import json
            import pandas as pd
            import matplotlib.pyplot as plt
            import seaborn as sns
            from mplsoccer.pitch import Pitch
            import numpy as np
            import streamlit as st
            from dateutil import parser
            
            df = pd.read_csv(r'xT/U19 Ligaen 23 24.csv')
            hold = 'Horsens U19'
            df = df[df['label'].str.contains(hold)]
            df['date'] = pd.to_datetime(df['date'])
            df = df.sort_values(by='date',ascending=False)
            valgtekamp = st.multiselect('Vælg kamp', df['label'].unique(),default=df['label'].unique()[0])
            df.loc[df['player.id'] == 624663, 'player.name'] = 'Je. Beluli'
            df.loc[df['pass.recipient.id'] == 624663, 'pass.recipient.name'] = 'Je. Beluli'

            df1 = df.copy()

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

            dfscore = pd.read_csv(r'xT/Zone scores.csv')

            df = df.merge(dfscore[['Start Zone', 'Start zone score']], on='Start Zone', how='left')

            # Merge 'End Zone' scores
            df = df.merge(dfscore[['End Zone', 'End zone score']], on='End Zone', how='left')

            df['xT'] = df['End zone score'] - df['Start zone score']
            xThold = df.groupby(['team.name'])['xT'].agg('sum').reset_index()

            with st.expander('Se xT model'):
                col1,col2 = st.columns(2)
                with col1:
                    from PIL import Image
                    image = Image.open('xT/xT zoner.png')
                    st.image(image,'xT zoner')
                with col2:
                    zoner = pd.read_csv('xT/Zone scores.csv')
                    zoner = zoner[['Start Zone','Start zone score']]
                    zoner = zoner.rename(columns={'Start Zone': 'Zone'})
                    zoner = zoner.rename(columns={'Start zone score': 'Zone score'})

                    st.dataframe(zoner,hide_index=True)
                    st.write('xT udregnes som: zonen hvor pasning/dribling slutter - zone hvor pasning/dribling starter')
                    st.write('Zonernes værdi er udregnet på baggrund af de seneste 8 sæsoner i 1. div og Superligaen med udgangspunkt i den gennemsnitlige værdi for en boldbesiddelse i zonen. Den er så vægtet efter hvor mange aktioner der går fra boldbesiddelsen i zonen til en afslutning. Jo flere jo lavere vægtning')

            xgc = df1
            xgchold = xgc.rename(columns={'shot.xg': 'Hold xG i åbent spil'})
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

            col1,col2, col34 = st.columns([1,1,2])
            with col1:  
                xTspiller = df.groupby(['player.name','team.name'])['xT'].agg('sum').reset_index()
                xTspiller = xTspiller[xTspiller['team.name'] == hold]
                xTspiller = xTspiller.sort_values(by='xT', ascending=False)
                xTspiller = xTspiller[['player.name','xT']]
                st.dataframe(xTspiller,hide_index=True)
                samlet = xgcspiller.merge(xTspiller)
            with col2:
                xgcspiller = xgcspiller[['player.name','xGC','xGCC']]
                st.dataframe(xgcspiller,hide_index=True)
            
            with col34:
                xgplacering = df1
                xgplacering = xgplacering[xgplacering['shot.xg'] > 0]
                xgplacering = xgplacering[xgplacering['team.name'] == hold]
                
                x = xgplacering['location.x']
                y = xgplacering['location.y']
                player_names = xgplacering['player.name']  # Extract player names
                label_text = xgplacering.sort_values(by='shot.xg',ascending=False)
                label_text = label_text[['player.name', 'shot.xg']].to_string(index=False,header=False)
                shot_xg = xgplacering['shot.xg'].astype(float)
                min_size = 5  # Minimum dot size
                max_size = 100  # Maximum dot size
                sizes = np.interp(shot_xg, (shot_xg.min(), shot_xg.max()), (min_size, max_size))

                pitch = Pitch(pitch_type='wyscout', pitch_color='grass', line_color='white', stripe=True)
                fig, ax = pitch.draw()
                sc = pitch.scatter(x, y, ax=ax, s=sizes)

                # Add player names as labels using annotate
                for i, txt in enumerate(player_names):
                    ax.annotate(txt, (x.iloc[i], y.iloc[i]), color='white', fontsize=8, ha='center', va='bottom')

                ax.text(0.3, 0.5, label_text, color='black', ha='center', va='center',
                        transform=ax.transAxes, fontsize=10, bbox=dict(facecolor='white', alpha=0.7))


                st.write('Xg plot (Jo større markering, jo større xG)')
                st.pyplot(plt.gcf(), use_container_width=True)
                
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
                pass_df = pass_df[(pass_df['location.x'] > 33) & (pass_df['location.x'] < 66)]
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

        Årgange = {

            'U15':U15,
            'U17':U17,
            'U19':U19,
        }
        rullemenu = st.selectbox('Vælg årgang',Årgange.keys())
        Årgange[rullemenu]()
     
    def Individuelt_dashboard():
        def U13():
            import pandas as pd
            import streamlit as st
            import json
            from pandas import json_normalize
            import ast
            from dateutil import parser
            import plotly.graph_objects as go
            import matplotlib.pyplot as plt
            import matplotlib
            from datetime import datetime, timedelta
            import plotly.express as px
            import numpy as np
            from datetime import date

            navne = pd.read_excel('Navne.xlsx')
            navne = navne[navne['Trup'].str.contains('U13')]
            navneliste = navne['Spillere'].sort_values(ascending=True)
            option2 = st.selectbox('Vælg spiller',navneliste)
            df = pd.read_csv(r'Fysisk data/U13 PHV.csv')
            df = df.drop(df.index[:6])
            df.columns = df.iloc[0]
            df = df.drop(df.index[:1])
            df['Navn'] = df['First Name'] + " " + df['Last Name']
            df = df[['Navn','Age @ PHV','Date of Birth (dd-mm-yy)']]
            df.dropna(subset=['Navn'], inplace=True)
            df['Date of Birth (dd-mm-yy)'] = pd.to_datetime(df['Date of Birth (dd-mm-yy)'])
            df['Fødselsdato'] = df['Date of Birth (dd-mm-yy)'].dt.strftime('%d-%m-%Y')
            today = pd.Timestamp(date.today())
            df['Alder'] = (today- df['Date of Birth (dd-mm-yy)'])/ np.timedelta64(1,'Y')
            df['Alder'] = pd.to_numeric(df['Alder'])
            df['Age @ PHV'] = pd.to_numeric(df['Age @ PHV'])
            df['Modenhed'] = df['Alder'] - df['Age @ PHV']
            df['Modenhed'] = df['Modenhed'].astype(float)
            df = df[df['Navn'] == option2]
            df = df[['Navn','Age @ PHV','Fødselsdato','Modenhed']]
            st.dataframe(df,hide_index=True)

            try:
                with open('træningsregistrering.json', 'r') as json_file:
                    træningsdata = json.load(json_file)
                    træningsdata = pd.DataFrame(træningsdata)
            except FileNotFoundError:
                return pd.DataFrame(columns=['Tidspunkt', 'Dato','Årgang','Rådighed', 'Spillerens navn', 'Træningshold', 'Træningstype', 'Antal minutter trænet'])
            
            date_format = '%d-%m-%Y'  # Specify your date format
            træningsdata['Dato'] = pd.to_datetime(træningsdata['Dato'], format=date_format)

            min_date = træningsdata['Dato'].min()
            max_date = træningsdata['Dato'].max()

            date_range = pd.date_range(start=min_date, end=max_date, freq='D')
            date_options = date_range.strftime(date_format)  # Convert dates to the specified format

            default_end_date = date_options[-1]

            # Calculate the default start date as 14 days before the default end date
            default_start_date = pd.to_datetime(default_end_date, format=date_format) - timedelta(days=14)
            default_start_date = default_start_date.strftime(date_format)

            # Set the default start and end date values for the select_slider
            selected_start_date, selected_end_date = st.select_slider(
                'Vælg datointerval',
                options=date_options,
                value=(default_start_date, default_end_date)
            )

            selected_start_date = pd.to_datetime(selected_start_date, format=date_format)
            selected_end_date = pd.to_datetime(selected_end_date, format=date_format)
            filtered_data = træningsdata[
                (træningsdata['Dato'] >= selected_start_date) & (træningsdata['Dato'] <= selected_end_date)
            ]

            # Sort the filtered data by the 'Dato' column
#            sorted_data = filtered_data.sort_values(by ='Dato')
            sorted_data = filtered_data.copy()
            sorted_data = sorted_data[sorted_data['Spiller'] == option2]
            minutter_columns = sorted_data.filter(regex='.*minutter$').columns.tolist()
            minutter_columns_processed = [col.replace('minutter', '') for col in minutter_columns]

            minutter_df = pd.DataFrame({
                'Træningstype': minutter_columns_processed,
                'Minutter': [sorted_data[col].sum() for col in minutter_columns]
            })
            st.title(option2 + ' Træningsdata')
            minutter_df['Træningstype'] = minutter_df['Træningstype'].str.replace('minutter', '')
            col1, col2 = st.columns([3,1])

            with col2:
                træningsgruppe = sorted_data[['Træningsgruppe']].value_counts()
                træningsgruppe = træningsgruppe.rename_axis('Træningsgruppe').reset_index(name='Antal')
                #træningsgruppe = træningsgruppe.set_index('Træningsgruppe')
                #st.dataframe(træningsgruppe,use_container_width=True,hide_index=True)
                fig = go.Figure()
                fig.add_trace(go.Pie(
                    labels=træningsgruppe['Træningsgruppe'],
                    values=træningsgruppe['Antal'],
                    hole=0.0,
                ))
                fig.update_layout(title='Træningsgrupper')
                st.plotly_chart(fig)       

            with col1:
                fig = go.Figure()
                for idx, label in enumerate(minutter_df['Træningstype']):
                    fig.add_trace(go.Pie(
                        labels=minutter_df['Træningstype'],
                        values=minutter_df['Minutter'],
                    ))

                fig.update_layout(title='Træningstyper og deres tid i minutter',
                )
                st.plotly_chart(fig)

            col1,col2 = st.columns(2)


            fig = go.Figure()
            for idx, col in enumerate(minutter_columns):
                fig.add_trace(go.Bar(
                    x=sorted_data['Dato'],
                    y=sorted_data[col],
                    name=col.replace('minutter', ''),
                ))

            fig.update_layout(
                barmode='stack',
                xaxis=dict(title='Dato'),
                yaxis=dict(title='Minutter'),
                title='Træningsdata over tid'
            )

            st.plotly_chart(fig,use_container_width=True)

         
            afbud_årsag = sorted_data['Afbud årsag'].value_counts()
            afbud_årsag = afbud_årsag.rename_axis('Afbud årsag').reset_index(name='Antal')  # Renaming axis for clarity
            afbud_årsag = afbud_årsag.set_index('Afbud årsag')
            
            col1,col2,col3 = st.columns(3)    
            with col1:
                Individuel_træning_kommentar = sorted_data[['Dato', 'Individuel træning kommentar']]
                Individuel_træning_kommentar = Individuel_træning_kommentar.dropna(subset=['Individuel træning kommentar'])
                st.dataframe(Individuel_træning_kommentar.style.format({'Dato': '{:%d-%m-%Y}'}), hide_index=True,use_container_width=True)
            with col2:    
                Individuel_video_kommentar = sorted_data[['Dato', 'Individuel video kommentar']]
                Individuel_video_kommentar = Individuel_video_kommentar.dropna(subset=['Individuel video kommentar'])
                st.dataframe(Individuel_video_kommentar.style.format({'Dato': '{:%d-%m-%Y}'}), hide_index=True,use_container_width=True)
            with col3:
                st.dataframe(afbud_årsag,use_container_width=True)

            st.title(option2 + ' Kampdata')
            try:
                with open('Kampregistrering.json', 'r') as json_file:
                    Kampdata = json.load(json_file)
                    Kampdata = pd.DataFrame(Kampdata)
            except FileNotFoundError:
                return st.write('Ingen kampdata på den valgte spiller')

            date_format = '%d-%m-%Y'  # Specify your date format
            Kampdata['Dato'] = pd.to_datetime(Kampdata['Dato'], format=date_format)

            filtered_data = Kampdata[
                (Kampdata['Dato'] >= selected_start_date) & (Kampdata['Dato'] <= selected_end_date)
            ]
            sorted_data = filtered_data.sort_values(by ='Dato')
            sorted_data = sorted_data[sorted_data['Spiller'] == option2]
            
            kampminutter_spillet = sorted_data['Minutter spillet'].sum()
            kampminutter_til_rådighed = sorted_data['Minutter til rådighed'].sum()

            minutter_ude = kampminutter_til_rådighed - kampminutter_spillet
            minutter_spillet = kampminutter_spillet

            # Creating a DataFrame with the percentages
            data = {
                'Minutter spillet': [minutter_spillet],
                'Minutter ikke spillet': [minutter_ude]
            }
            kampminutter = pd.DataFrame(data, index=['Kampminutter'])
            
            Starter_inde = {
                'Starter inde' : sorted_data['Starter inde'].sum(),
                'Starter ude' : sorted_data['Starter ude'].sum()
            }
            Starter_inde = pd.DataFrame.from_dict(Starter_inde,orient='index',columns = ['Antal kampe'])
            
            Mål_assist = {
                'Mål': sorted_data['Mål'].sum(),
                'Assist': sorted_data['Assist'].sum(),
            }
            Mål_assist = pd.DataFrame.from_dict(Mål_assist, orient='index', columns=['Antal'])

            # Get unique values from the 'Spillere' column
            spillere_values = sorted_data['Spiller'].unique()

            # Filter columns containing a string from 'Spillere' column
            filtered_columns = [col for col in sorted_data.columns if any(spiller in col for spiller in spillere_values)]

            # Create a new DataFrame with the filtered columns
            filtered_data = sorted_data[filtered_columns]
            
            Kamptype = sorted_data['Kamptype'].value_counts()
            Kamptype = Kamptype.rename_axis('Kamptype').reset_index(name='Antal')  # Renaming axis for clarity
            Kamptype = Kamptype.set_index('Kamptype')

            Rådighed = sorted_data['Rådighed'].value_counts()
            Rådighed = Rådighed.rename_axis('Rådighed').reset_index(name='Antal')  # Renaming axis for clarity
            Rådighed = Rådighed.set_index('Rådighed')
            
            Modstandere = sorted_data['Modstanderhold'].value_counts()
            Modstandere = Modstandere.rename_axis('Modstander').reset_index(name='Antal')  # Renaming axis for clarity
            Modstandere = Modstandere.set_index('Modstander')
            Kampårgang = sorted_data['Kampårgang'].value_counts()
            Kampårgang = Kampårgang.rename_axis('Kampårgang').reset_index(name='Antal')  # Renaming axis for clarity
            Kampårgang = Kampårgang.set_index('Kampårgang')

            def create_pie_chart(data, title):
                fig = go.Figure(data=[go.Pie(labels=data.index, values=data['Antal'], hole=0.0)])
                fig.update_layout(title=title)
                st.plotly_chart(fig)

            
            col1,col2= st.columns([3,1])
            with col1:
                fig = go.Figure(data=[go.Pie(labels=kampminutter.columns, values=kampminutter.iloc[0], hole=0.0)])
                fig.update_layout(title='Fordeling af minutter til rådighed')
                st.plotly_chart(fig)
                create_pie_chart(Kamptype, 'Fordeling af kamptyper')
                
            with col2:
                create_pie_chart(Rådighed,'Fordeling af rådighedsstatus')
                create_pie_chart(Kampårgang, 'Fordeling af Kampårgange')
                
            col1,col2 = st.columns(2)
            with col1:
                st.dataframe(Mål_assist,use_container_width=True)
                
            with col2:
                st.dataframe(Modstandere,use_container_width=True)
                      
        def U14():
            import pandas as pd
            import streamlit as st
            import json
            from pandas import json_normalize
            import ast
            from dateutil import parser
            import plotly.graph_objects as go
            import matplotlib.pyplot as plt
            import matplotlib
            from datetime import datetime, timedelta
            import plotly.express as px
            import numpy as np
            from datetime import date

            navne = pd.read_excel('Navne.xlsx')
            navne = navne[navne['Trup'].str.contains('U14')]
            navneliste = navne['Spillere'].sort_values(ascending=True)
            option2 = st.selectbox('Vælg spiller',navneliste)
            df = pd.read_csv(r'Fysisk data/U14 PHV.csv')
            df = df.drop(df.index[:6])
            df.columns = df.iloc[0]
            df = df.drop(df.index[:1])
            df['Navn'] = df['First Name'] + " " + df['Last Name']
            df = df[['Navn','Age @ PHV','Date of Birth (dd-mm-yy)']]
            df.dropna(subset=['Navn'], inplace=True)
            df['Date of Birth (dd-mm-yy)'] = pd.to_datetime(df['Date of Birth (dd-mm-yy)'])
            df['Fødselsdato'] = df['Date of Birth (dd-mm-yy)'].dt.strftime('%d-%m-%Y')
            today = pd.Timestamp(date.today())
            df['Alder'] = (today- df['Date of Birth (dd-mm-yy)'])/ np.timedelta64(1,'Y')
            df['Alder'] = pd.to_numeric(df['Alder'])
            df['Age @ PHV'] = pd.to_numeric(df['Age @ PHV'])
            df['Modenhed'] = df['Alder'] - df['Age @ PHV']
            df['Modenhed'] = df['Modenhed'].astype(float)
            df = df[df['Navn'] == option2]
            df = df[['Navn','Age @ PHV','Fødselsdato','Modenhed']]
            st.dataframe(df,hide_index=True)
            try:
                with open('træningsregistrering.json', 'r') as json_file:
                    træningsdata = json.load(json_file)
                    træningsdata = pd.DataFrame(træningsdata)
            except FileNotFoundError:
                return pd.DataFrame(columns=['Tidspunkt', 'Dato','Årgang','Rådighed', 'Spillerens navn', 'Træningshold', 'Træningstype', 'Antal minutter trænet'])
            
            date_format = '%d-%m-%Y'  # Specify your date format
            træningsdata['Dato'] = pd.to_datetime(træningsdata['Dato'], format=date_format)

            min_date = træningsdata['Dato'].min()
            max_date = træningsdata['Dato'].max()

            date_range = pd.date_range(start=min_date, end=max_date, freq='D')
            date_options = date_range.strftime(date_format)  # Convert dates to the specified format

            default_end_date = date_options[-1]

            # Calculate the default start date as 14 days before the default end date
            default_start_date = pd.to_datetime(default_end_date, format=date_format) - timedelta(days=14)
            default_start_date = default_start_date.strftime(date_format)

            # Set the default start and end date values for the select_slider
            selected_start_date, selected_end_date = st.select_slider(
                'Vælg datointerval',
                options=date_options,
                value=(default_start_date, default_end_date)
            )

            selected_start_date = pd.to_datetime(selected_start_date, format=date_format)
            selected_end_date = pd.to_datetime(selected_end_date, format=date_format)
            filtered_data = træningsdata[
                (træningsdata['Dato'] >= selected_start_date) & (træningsdata['Dato'] <= selected_end_date)
            ]

            # Sort the filtered data by the 'Dato' column
#            sorted_data = filtered_data.sort_values(by ='Dato')
            sorted_data = filtered_data.copy()
            sorted_data = sorted_data[sorted_data['Spiller'] == option2]
            minutter_columns = sorted_data.filter(regex='.*minutter$').columns.tolist()
            minutter_columns_processed = [col.replace('minutter', '') for col in minutter_columns]

            minutter_df = pd.DataFrame({
                'Træningstype': minutter_columns_processed,
                'Minutter': [sorted_data[col].sum() for col in minutter_columns]
            })
            st.title(option2 + ' Træningsdata')
            minutter_df['Træningstype'] = minutter_df['Træningstype'].str.replace('minutter', '')
            col1, col2 = st.columns([3,1])

            with col2:
                træningsgruppe = sorted_data[['Træningsgruppe']].value_counts()
                træningsgruppe = træningsgruppe.rename_axis('Træningsgruppe').reset_index(name='Antal')
                #træningsgruppe = træningsgruppe.set_index('Træningsgruppe')
                #st.dataframe(træningsgruppe,use_container_width=True,hide_index=True)
                fig = go.Figure()
                fig.add_trace(go.Pie(
                    labels=træningsgruppe['Træningsgruppe'],
                    values=træningsgruppe['Antal'],
                    hole=0.0,
                ))
                fig.update_layout(title='Træningsgrupper')
                st.plotly_chart(fig)       

            with col1:
                fig = go.Figure()
                for idx, label in enumerate(minutter_df['Træningstype']):
                    fig.add_trace(go.Pie(
                        labels=minutter_df['Træningstype'],
                        values=minutter_df['Minutter'],
                    ))

                fig.update_layout(title='Træningstyper og deres tid i minutter',
                )
                st.plotly_chart(fig)

            col1,col2 = st.columns(2)


            fig = go.Figure()
            for idx, col in enumerate(minutter_columns):
                fig.add_trace(go.Bar(
                    x=sorted_data['Dato'],
                    y=sorted_data[col],
                    name=col.replace('minutter', ''),
                ))

            fig.update_layout(
                barmode='stack',
                xaxis=dict(title='Dato'),
                yaxis=dict(title='Minutter'),
                title='Træningsdata over tid'
            )

            st.plotly_chart(fig,use_container_width=True)

         
            afbud_årsag = sorted_data['Afbud årsag'].value_counts()
            afbud_årsag = afbud_årsag.rename_axis('Afbud årsag').reset_index(name='Antal')  # Renaming axis for clarity
            afbud_årsag = afbud_årsag.set_index('Afbud årsag')
            
            col1,col2,col3 = st.columns(3)    
            with col1:
                Individuel_træning_kommentar = sorted_data[['Dato', 'Individuel træning kommentar']]
                Individuel_træning_kommentar = Individuel_træning_kommentar.dropna(subset=['Individuel træning kommentar'])
                st.dataframe(Individuel_træning_kommentar.style.format({'Dato': '{:%d-%m-%Y}'}), hide_index=True,use_container_width=True)
            with col2:    
                Individuel_video_kommentar = sorted_data[['Dato', 'Individuel video kommentar']]
                Individuel_video_kommentar = Individuel_video_kommentar.dropna(subset=['Individuel video kommentar'])
                st.dataframe(Individuel_video_kommentar.style.format({'Dato': '{:%d-%m-%Y}'}), hide_index=True,use_container_width=True)
            with col3:
                st.dataframe(afbud_årsag,use_container_width=True)

            st.title(option2 + ' Kampdata')
            try:
                with open('Kampregistrering.json', 'r') as json_file:
                    Kampdata = json.load(json_file)
                    Kampdata = pd.DataFrame(Kampdata)
            except FileNotFoundError:
                return st.write('Ingen kampdata på den valgte spiller')

            date_format = '%d-%m-%Y'  # Specify your date format
            Kampdata['Dato'] = pd.to_datetime(Kampdata['Dato'], format=date_format)

            filtered_data = Kampdata[
                (Kampdata['Dato'] >= selected_start_date) & (Kampdata['Dato'] <= selected_end_date)
            ]
            sorted_data = filtered_data.sort_values(by ='Dato')
            sorted_data = sorted_data[sorted_data['Spiller'] == option2]
            
            kampminutter_spillet = sorted_data['Minutter spillet'].sum()
            kampminutter_til_rådighed = sorted_data['Minutter til rådighed'].sum()

            minutter_ude = kampminutter_til_rådighed - kampminutter_spillet
            minutter_spillet = kampminutter_spillet

            # Creating a DataFrame with the percentages
            data = {
                'Minutter spillet': [minutter_spillet],
                'Minutter ikke spillet': [minutter_ude]
            }
            kampminutter = pd.DataFrame(data, index=['Kampminutter'])
            
            Starter_inde = {
                'Starter inde' : sorted_data['Starter inde'].sum(),
                'Starter ude' : sorted_data['Starter ude'].sum()
            }
            Starter_inde = pd.DataFrame.from_dict(Starter_inde,orient='index',columns = ['Antal kampe'])
            
            Mål_assist = {
                'Mål': sorted_data['Mål'].sum(),
                'Assist': sorted_data['Assist'].sum(),
            }
            Mål_assist = pd.DataFrame.from_dict(Mål_assist, orient='index', columns=['Antal'])

            # Get unique values from the 'Spillere' column
            spillere_values = sorted_data['Spiller'].unique()

            # Filter columns containing a string from 'Spillere' column
            filtered_columns = [col for col in sorted_data.columns if any(spiller in col for spiller in spillere_values)]

            # Create a new DataFrame with the filtered columns
            filtered_data = sorted_data[filtered_columns]
            
            Kamptype = sorted_data['Kamptype'].value_counts()
            Kamptype = Kamptype.rename_axis('Kamptype').reset_index(name='Antal')  # Renaming axis for clarity
            Kamptype = Kamptype.set_index('Kamptype')

            Rådighed = sorted_data['Rådighed'].value_counts()
            Rådighed = Rådighed.rename_axis('Rådighed').reset_index(name='Antal')  # Renaming axis for clarity
            Rådighed = Rådighed.set_index('Rådighed')
            
            Modstandere = sorted_data['Modstanderhold'].value_counts()
            Modstandere = Modstandere.rename_axis('Modstander').reset_index(name='Antal')  # Renaming axis for clarity
            Modstandere = Modstandere.set_index('Modstander')
            Kampårgang = sorted_data['Kampårgang'].value_counts()
            Kampårgang = Kampårgang.rename_axis('Kampårgang').reset_index(name='Antal')  # Renaming axis for clarity
            Kampårgang = Kampårgang.set_index('Kampårgang')

            def create_pie_chart(data, title):
                fig = go.Figure(data=[go.Pie(labels=data.index, values=data['Antal'], hole=0.0)])
                fig.update_layout(title=title)
                st.plotly_chart(fig)

            
            col1,col2= st.columns([3,1])
            with col1:
                fig = go.Figure(data=[go.Pie(labels=kampminutter.columns, values=kampminutter.iloc[0], hole=0.0)])
                fig.update_layout(title='Fordeling af minutter til rådighed')
                st.plotly_chart(fig)
                create_pie_chart(Kamptype, 'Fordeling af kamptyper')
                
            with col2:
                create_pie_chart(Rådighed,'Fordeling af rådighedsstatus')
                create_pie_chart(Kampårgang, 'Fordeling af Kampårgange')
                
            col1,col2 = st.columns(2)
            with col1:
                st.dataframe(Mål_assist,use_container_width=True)
                
            with col2:
                st.dataframe(Modstandere,use_container_width=True)
         
        def U15():
            import pandas as pd
            import streamlit as st
            import json
            from pandas import json_normalize
            import ast
            from dateutil import parser
            import plotly.graph_objects as go
            import matplotlib.pyplot as plt
            import matplotlib
            from datetime import datetime, timedelta
            import plotly.express as px
            from datetime import date
            import numpy as np
            
            navne = pd.read_excel('Navne.xlsx')
            navne = navne[navne['Trup'].str.contains('U15')]
            navneliste = navne['Spillere'].sort_values(ascending=True)
            

            
            df = pd.read_csv(r'Individuelt dashboard/Individuelt dashboard U15.csv')
            df.rename(columns={'playerId': 'Player id'}, inplace=True)
            df = df.astype(str)
            dfevents = pd.read_csv('U15 eventdata alle.csv',low_memory=False)
            dfevents1 = dfevents[['Player id','Player name','team_name','label','date','matchId']]
            dfspillernavn = df[['Player id','matchId','positions','average','percent','total']]
            dfspillernavn = dfspillernavn.astype(str)
            dfevents1['Player id'] = dfevents1['Player id'].astype(str)
            dfevents1['matchId'] = dfevents1['matchId'].astype(str)
            df = dfspillernavn.merge(dfevents1)

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
            df = df.sort_values('date',ascending=True)

            df_backs = df[df['position_codes'].str.contains('|'.join(['lb', 'rb']))]
            df_backs = df_backs[df_backs['total_minutesOnField'] >= 40]
            df_backsminutter = df_backs[['Player name','Team name','total_minutesOnField']]
            df_backsminutter = df_backsminutter.groupby(['Player id']).sum(numeric_only=True)
            df_backsminutter = df_backsminutter[df_backsminutter['total_minutesOnField'] >= 200]

            df_Stoppere = df[df['position_codes'].str.contains('|'.join(['cb']))]
            df_Stoppere = df_Stoppere[df_Stoppere['total_minutesOnField'] >= 40]
            df_stoppereminutter = df_Stoppere[['Player name','Team name','total_minutesOnField']]
            df_stoppereminutter = df_stoppereminutter.groupby(['Player id']).sum(numeric_only=True)
            df_stoppereminutter = df_stoppereminutter[df_stoppereminutter['total_minutesOnField'] >= 200]

            df_Centrale_midt = df[df['position_codes'].str.contains('|'.join(['cm','amf','dmf']))]
            df_Centrale_midt = df_Centrale_midt[df_Centrale_midt['total_minutesOnField'] >= 40]
            df_centraleminutter = df_Centrale_midt[['Player name','Team name','total_minutesOnField']]
            df_centraleminutter = df_centraleminutter.groupby(['Player id']).sum(numeric_only=True)
            df_centraleminutter = df_centraleminutter[df_centraleminutter['total_minutesOnField'] >= 200]

            df_Kanter = df[df['position_codes'].str.contains('|'.join(['rw','lw','ramf','lamf']))]
            df_Kanter = df_Kanter[df_Kanter['total_minutesOnField'] >=40]
            df_kanterminutter = df_Kanter[['Player name','Team name','total_minutesOnField']]
            df_kanterminutter = df_kanterminutter.groupby(['Player id']).sum(numeric_only=True)
            df_kanterminutter = df_kanterminutter[df_kanterminutter['total_minutesOnField'] >=200]


            df_Angribere = df[df['position_codes'].str.contains('|'.join(['cf','ss']))]
            df_Angribere = df_Angribere[df_Angribere['total_minutesOnField'] >= 40]
            df_angribereminutter = df_Angribere[['Player name','Team name','total_minutesOnField']]
            df_angribereminutter = df_angribereminutter.groupby(['Player id']).sum(numeric_only=True)
            df_angribereminutter = df_angribereminutter[df_angribereminutter['total_minutesOnField'] >= 200]

            df_backs = pd.merge(df_backsminutter,df_backs,on=('Player id'))
            df_backs = df_backs[df_backs['total_minutesOnField_y'] >=40]

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
            df_backssæsonen = df_backs[['Player name','Team name','label','total_minutesOnField_x','total_minutesOnField_y','Number of crosses score','Accurate crosses score','XA score','Passes to final third score','Successful dribbles score','Defensive duels won score','Progressive runs score','Offensive duels won score','Accelerations score','Duels won score','Interceptions score','Successful defensive actions score']]
            df_backssæsonen.rename(columns={'total_minutesOnField_x':'Total minutes'},inplace=True)
            df_backssæsonen = df_backssæsonen.groupby(['Player name','Team name','Total minutes','label']).mean(numeric_only=True)

            df_backssæsonen['Indlægsstærk'] = (df_backssæsonen['Number of crosses score'] + df_backssæsonen['Accurate crosses score'] + df_backssæsonen['XA score'] + df_backssæsonen['Passes to final third score'])/4
            df_backssæsonen['1v1 færdigheder'] = (df_backssæsonen['Successful dribbles score'] + df_backssæsonen['Defensive duels won score'] + df_backssæsonen['Progressive runs score'] + df_backssæsonen['Offensive duels won score'] + df_backssæsonen['Accelerations score'] + df_backssæsonen['Duels won score'])/6
            df_backssæsonen['Spilintelligens defensivt'] = (df_backssæsonen['Interceptions score'] + df_backssæsonen['Successful defensive actions score'] + df_backssæsonen['Duels won score'] + df_backssæsonen['Defensive duels won score'])/4
            df_backssæsonen['Fart'] = (df_backssæsonen['Successful dribbles score'] + df_backssæsonen['Progressive runs score'] + df_backssæsonen['Offensive duels won score'] + df_backssæsonen['Accelerations score'])/4
            df_backssæsonen ['Samlet'] = (df_backssæsonen['Indlægsstærk'] + df_backssæsonen['1v1 færdigheder'] + df_backssæsonen['Spilintelligens defensivt'] + df_backssæsonen['Fart'])/4
            df_backssæsonen = df_backssæsonen[['Indlægsstærk','1v1 færdigheder','Spilintelligens defensivt','Fart','Samlet']]
    #        df_backssæsonen = df_backssæsonen.sort_values(by='Samlet',ascending=False)

            df_backs['Indlægsstærk'] = (df_backs['Number of crosses score'] + df_backs['Accurate crosses score'] + df_backs['XA score'] + df_backs['Passes to final third score'])/4
            df_backs['1v1 færdigheder'] = (df_backs['Successful dribbles score'] + df_backs['Defensive duels won score'] + df_backs['Progressive runs score'] + df_backs['Offensive duels won score'] + df_backs['Accelerations score'] + df_backs['Duels won score'])/6
            df_backs['Spilintelligens defensivt'] = (df_backs['Interceptions score'] + df_backs['Successful defensive actions score'] + df_backs['Duels won score'] + df_backs['Defensive duels won score'])/4
            df_backs['Fart'] = (df_backs['Successful dribbles score'] + df_backs['Progressive runs score'] + df_backs['Offensive duels won score'] + df_backs['Accelerations score'])/4
            df_backs['Samlet'] = (df_backs['Indlægsstærk'] + df_backs['1v1 færdigheder'] + df_backs['Spilintelligens defensivt'] + df_backs['Fart'])/4

            df_backs = df_backs[['Player name','Team name','label','total_minutesOnField_y','Indlægsstærk','1v1 færdigheder','Spilintelligens defensivt','Fart','Samlet']]
    #        df_backs = df_backs.sort_values(by='Samlet',ascending=False)
            
            df_backs = navne.merge(df_backs)
            df_backs = df_backs.drop('Player Name',axis=1)
            df_backs = df_backs.drop('Player name',axis=1)    
            df_backssæsonen = df_backssæsonen.reset_index()
            df_backssæsonen = navne.merge(df_backssæsonen)
            df_backs = navne.merge(df_backs)
            df_backssæsonen = df_backssæsonen.drop('Player Name',axis=1)
            df_backssæsonen = df_backssæsonen.drop('Player name',axis=1)
            df_backssæsonen = df_backssæsonen.drop('label',axis=1)

            df_Stoppere = pd.merge(df_stoppereminutter,df_Stoppere,on=('Player id'))
            df_Stoppere = df_Stoppere[df_Stoppere['total_minutesOnField_y'] >=30]

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
            df_Stopperesæsonen = df_Stoppere.copy()
            df_Stopperesæsonen = df_Stopperesæsonen.rename(columns={'total_minutesOnField_x':'Total minutes'})
            df_Stopperesæsonen = df_Stopperesæsonen.groupby(['Player name','Team name','Total minutes','label']).mean(numeric_only=True)
            
            df_Stopperesæsonen['Pasningssikker'] = (df_Stopperesæsonen['Accurate passes score'] + df_Stopperesæsonen['Accurate long passes score'] + df_Stopperesæsonen['Forward passes score'] + df_Stopperesæsonen['Accurate forward passes score'] + df_Stopperesæsonen['Accurate progressive passes score'] + df_Stopperesæsonen['Accurate vertical passes score'])/6
            df_Stopperesæsonen['Spilintelligens defensivt'] = (df_Stopperesæsonen['Interceptions score'] + df_Stopperesæsonen['Succesful defensive actions score'] + df_Stopperesæsonen['Shots blocked score'] + df_Stopperesæsonen['Succesful defensive actions score'] + df_Stopperesæsonen['Defensive duels won % score']) /5
            df_Stopperesæsonen['Spilintelligens offensivt'] = (df_Stopperesæsonen['Forward passes score'] + df_Stopperesæsonen['Accurate forward passes score'] + df_Stopperesæsonen['Accurate passes to final third'] + df_Stopperesæsonen['Passes to final third'] + df_Stopperesæsonen['Accurate progressive passes score'] + df_Stopperesæsonen['Progressive passes score'] + df_Stopperesæsonen['Through passes'] + df_Stopperesæsonen['Accurate through passes']+ df_Stopperesæsonen['Progressive runs'] + df_Stopperesæsonen['Offensive duels won %'] + df_Stopperesæsonen['Successful dribbles %'])/11
            df_Stopperesæsonen['Nærkamps- og duelstærk'] = (df_Stopperesæsonen['Defensive duels won % score'] + df_Stopperesæsonen['Aerial duels won % score'] + df_Stopperesæsonen['Defensive duels won % score'])/3
            df_Stopperesæsonen['Samlet'] = (df_Stopperesæsonen['Pasningssikker'] + df_Stopperesæsonen['Spilintelligens defensivt'] + df_Stopperesæsonen['Spilintelligens offensivt'] + df_Stopperesæsonen['Nærkamps- og duelstærk'] + df_Stopperesæsonen['Nærkamps- og duelstærk'] + df_Stopperesæsonen['Spilintelligens defensivt'])/6

            df_Stopperesæsonen = df_Stopperesæsonen[['Pasningssikker','Spilintelligens defensivt','Spilintelligens offensivt','Nærkamps- og duelstærk','Samlet']]
    #        df_Stopperesæsonen = df_Stopperesæsonen.sort_values(by='Samlet',ascending=False)

            df_Stoppere = df_Stoppere[df_Stoppere['Team name'].str.contains('Horsens')]
            df_Stoppere['Pasningssikker'] = (df_Stoppere['Accurate passes score'] + df_Stoppere['Accurate long passes score'] + df_Stoppere['Forward passes score'] + df_Stoppere['Accurate forward passes score'] + df_Stoppere['Accurate progressive passes score'] + df_Stoppere['Accurate vertical passes score'])/6    
            df_Stoppere['Spilintelligens defensivt'] = (df_Stoppere['Interceptions score'] + df_Stoppere['Succesful defensive actions score'] + df_Stoppere['Shots blocked score'] + df_Stoppere['Succesful defensive actions score'] + df_Stoppere['Defensive duels won % score']) /5
            df_Stoppere['Spilintelligens offensivt'] = (df_Stoppere['Forward passes score'] + df_Stoppere['Accurate forward passes score'] + df_Stoppere['Accurate passes to final third'] + df_Stoppere['Passes to final third'] + df_Stoppere['Accurate progressive passes score'] + df_Stoppere['Progressive passes score'] + df_Stoppere['Through passes'] + df_Stoppere['Accurate through passes']+ df_Stoppere['Progressive runs'] + df_Stoppere['Offensive duels won %'] + df_Stoppere['Successful dribbles %'])/11
            df_Stoppere['Nærkamps- og duelstærk'] = (df_Stoppere['Defensive duels won % score'] + df_Stoppere['Aerial duels won % score'] + df_Stoppere['Defensive duels won % score'])/3
            df_Stoppere['Samlet'] = (df_Stoppere['Pasningssikker'] + df_Stoppere['Spilintelligens defensivt'] + df_Stoppere['Spilintelligens offensivt'] + df_Stoppere['Nærkamps- og duelstærk'] + df_Stoppere['Spilintelligens defensivt'] + df_Stoppere['Nærkamps- og duelstærk'])/6
            df_Stoppere = df_Stoppere[['Player name','Team name','label','total_minutesOnField_y','Pasningssikker','Spilintelligens defensivt','Spilintelligens offensivt','Nærkamps- og duelstærk','Samlet']]
    #        df_Stoppere = df_Stoppere.sort_values(by='Samlet',ascending=False)


            df_Stoppere = navne.merge(df_Stoppere)
            df_Stoppere = df_Stoppere.drop('Player Name',axis=1)
            df_Stoppere = df_Stoppere.drop('Player name',axis=1)    
            df_Stopperesæsonen = df_Stopperesæsonen.reset_index()
            df_Stopperesæsonen = navne.merge(df_Stopperesæsonen)
            df_Stoppere = navne.merge(df_Stoppere)
            df_Stopperesæsonen = df_Stopperesæsonen.drop('Player Name',axis=1)
            df_Stopperesæsonen = df_Stopperesæsonen.drop('Player name',axis=1)
            df_Stopperesæsonen = df_Stopperesæsonen.drop('label',axis=1)


            df_Centrale_midt = pd.merge(df_centraleminutter,df_Centrale_midt,on=('Player id'))
            df_Centrale_midt = df_Centrale_midt[df_Centrale_midt['total_minutesOnField_y'] >=30]

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

            df_Centrale_midtsæsonen = df_Centrale_midt.copy()
            df_Centrale_midtsæsonen = df_Centrale_midtsæsonen.rename(columns={'total_minutesOnField_x':'Total minutes'})
            df_Centrale_midtsæsonen = df_Centrale_midtsæsonen.groupby(['Player name','Team name','Total minutes','label']).mean(numeric_only=True)
            df_Centrale_midtsæsonen['Pasningssikker/Spilvendinger'] = (df_Centrale_midtsæsonen['Passes %'] + df_Centrale_midtsæsonen['Passes #'] + df_Centrale_midtsæsonen['Forward Passes %'] + df_Centrale_midtsæsonen['Forward Passes #'] + df_Centrale_midtsæsonen['Long Passes %'] + df_Centrale_midtsæsonen['Long Passes #']+ df_Centrale_midtsæsonen['Smart passes %'] + df_Centrale_midtsæsonen['Smart passes #'] + + df_Centrale_midtsæsonen['Key passes %'] + df_Centrale_midtsæsonen['Key passes #'] + df_Centrale_midtsæsonen['Passes to final third %'] + df_Centrale_midtsæsonen['Passes to final third #']+ df_Centrale_midtsæsonen['Vertical passes %'] + df_Centrale_midtsæsonen['Vertical passes #']+ df_Centrale_midtsæsonen['Through passes %'] + df_Centrale_midtsæsonen['Through passes #']+ df_Centrale_midtsæsonen['Progressive passes %'] + df_Centrale_midtsæsonen['Progressive passes #'])/18
            df_Centrale_midtsæsonen['Boldfast'] = (df_Centrale_midtsæsonen['Passes %'] + df_Centrale_midtsæsonen['Passes #']+ df_Centrale_midtsæsonen['Offensive duels %'] + df_Centrale_midtsæsonen['Received passes'] + df_Centrale_midtsæsonen['Succesful dribbles %'] + df_Centrale_midtsæsonen['Succesful dribbles #'])/6
            df_Centrale_midtsæsonen['Spilintelligens defensivt'] = (df_Centrale_midtsæsonen['Duels won %'] + df_Centrale_midtsæsonen['Duels won #'] +df_Centrale_midtsæsonen['Interceptions'] + df_Centrale_midtsæsonen['Counterpressing recoveries #'] + df_Centrale_midtsæsonen['Defensive duels won %'] + df_Centrale_midtsæsonen['Defensive duels won #'])/6
            df_Centrale_midtsæsonen['Samlet'] = (df_Centrale_midtsæsonen['Pasningssikker/Spilvendinger'] + df_Centrale_midtsæsonen['Boldfast'] + df_Centrale_midtsæsonen['Spilintelligens defensivt'])/3
            df_Centrale_midtsæsonen = df_Centrale_midtsæsonen[['Pasningssikker/Spilvendinger','Boldfast','Spilintelligens defensivt','Samlet']]
    #        df_Centrale_midtsæsonen = df_Centrale_midtsæsonen.sort_values(by='Samlet',ascending=False)

            df_Centrale_midt = df_Centrale_midt[df_Centrale_midt['Team name'].str.contains('Horsens')]
            df_Centrale_midt['Pasningssikker/Spilvendinger'] = (df_Centrale_midt['Passes %'] + df_Centrale_midt['Passes #'] + df_Centrale_midt['Forward Passes %'] + df_Centrale_midt['Forward Passes #'] + df_Centrale_midt['Long Passes %'] + df_Centrale_midt['Long Passes #']+ df_Centrale_midt['Smart passes %'] + df_Centrale_midt['Smart passes #'] + + df_Centrale_midt['Key passes %'] + df_Centrale_midt['Key passes #'] + df_Centrale_midt['Passes to final third %'] + df_Centrale_midt['Passes to final third #']+ df_Centrale_midt['Vertical passes %'] + df_Centrale_midt['Vertical passes #']+ df_Centrale_midt['Through passes %'] + df_Centrale_midt['Through passes #']+ df_Centrale_midt['Progressive passes %'] + df_Centrale_midt['Progressive passes #'])/18
            df_Centrale_midt['Boldfast'] = (df_Centrale_midt['Passes %'] + df_Centrale_midt['Passes #']+ df_Centrale_midt['Offensive duels %'] + df_Centrale_midt['Received passes'] + df_Centrale_midt['Succesful dribbles %'] + df_Centrale_midt['Succesful dribbles #'])/6
            df_Centrale_midt['Spilintelligens defensivt'] = (df_Centrale_midt['Duels won %'] + df_Centrale_midt['Duels won #'] +df_Centrale_midt['Interceptions'] + df_Centrale_midt['Counterpressing recoveries #'] + df_Centrale_midt['Defensive duels won %'] + df_Centrale_midt['Defensive duels won #'])/6
            df_Centrale_midt['Samlet'] = (df_Centrale_midt['Pasningssikker/Spilvendinger'] + df_Centrale_midt['Boldfast'] + df_Centrale_midt['Spilintelligens defensivt'])/3
            df_Centrale_midt = df_Centrale_midt[['Player name','Team name','label','total_minutesOnField_y','Pasningssikker/Spilvendinger','Boldfast','Spilintelligens defensivt','Samlet']]
    #        df_Centrale_midt = df_Centrale_midt.sort_values(by='Samlet',ascending=False)

            df_Centrale_midt = navne.merge(df_Centrale_midt)
            df_Centrale_midt = df_Centrale_midt.drop('Player Name',axis=1)
            df_Centrale_midt = df_Centrale_midt.drop('Player name',axis=1)    
            df_Centrale_midtsæsonen = df_Centrale_midtsæsonen.reset_index()
            df_Centrale_midtsæsonen = navne.merge(df_Centrale_midtsæsonen)
            df_Centrale_midt = navne.merge(df_Centrale_midt)
            df_Centrale_midtsæsonen = df_Centrale_midtsæsonen.drop('Player Name',axis=1)
            df_Centrale_midtsæsonen = df_Centrale_midtsæsonen.drop('Player name',axis=1)
            df_Centrale_midtsæsonen = df_Centrale_midtsæsonen.drop('label',axis=1)


            df_Kanter = pd.merge(df_kanterminutter,df_Kanter,on=('Player id'))
            df_Kanter = df_Kanter[df_Kanter['total_minutesOnField_y'] >=30]

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

            df_Kantersæsonen = df_Kanter.copy()
            df_Kantersæsonen = df_Kantersæsonen.rename(columns={'total_minutesOnField_x':'Total minutes'})
        
            df_Kantersæsonen = df_Kantersæsonen.groupby(['Player name','Team name','Total minutes','label']).mean(numeric_only=True)

            df_Kantersæsonen['Sparkefærdigheder'] = (df_Kantersæsonen['Shots on target %'] + df_Kantersæsonen['Shots on target #'] + df_Kantersæsonen['XG'] + df_Kantersæsonen['Passes to final third %'] + df_Kantersæsonen['Forward Passes %'] + df_Kantersæsonen['Vertical passes %'])/6
            df_Kantersæsonen['Kombinationsstærk'] = (df_Kantersæsonen['Passes %'] + df_Kantersæsonen['Passes #'] + df_Kantersæsonen['Forward Passes %'] + df_Kantersæsonen['Forward Passes #'] + df_Kantersæsonen['Passes to final third %'] + df_Kantersæsonen['Passes to final third #'] + df_Kantersæsonen['Through passes %'] + df_Kantersæsonen['Through passes #'] + df_Kantersæsonen['Progressive passes %'] + df_Kantersæsonen['Progressive passes #'] + df_Kantersæsonen['Successful attacking actions'])/11
            df_Kantersæsonen['Spilintelligens offensivt/indlægsstærk'] = (df_Kantersæsonen['XA per 90'] + df_Kantersæsonen['XG per 90'] + df_Kantersæsonen['Through passes %'] + df_Kantersæsonen['Through passes #'] + df_Kantersæsonen['Smart passes %'] + df_Kantersæsonen['Smart passes #'] + df_Kantersæsonen['Progressive passes %'] + df_Kantersæsonen['Progressive passes #'] + df_Kantersæsonen['Key passes %'] + df_Kantersæsonen['Key passes #'] + df_Kantersæsonen['Successful attacking actions'])/11
            df_Kantersæsonen['1v1 offensivt'] = (df_Kantersæsonen['Successful dribbles #'] + df_Kantersæsonen['Successful dribbles %'] + df_Kantersæsonen['Offensive duels #'] + df_Kantersæsonen['Offensive duels %'] + df_Kantersæsonen['Progressive runs'])/5
            df_Kantersæsonen['Fart'] = (df_Kantersæsonen['Progressive runs'] + df_Kantersæsonen['Successful dribbles #'] + df_Kantersæsonen['Successful dribbles %'] + df_Kantersæsonen['Accelerations score'])/4
            df_Kantersæsonen['Samlet'] = (df_Kantersæsonen['Sparkefærdigheder'] + df_Kantersæsonen['Kombinationsstærk'] + df_Kantersæsonen['Spilintelligens offensivt/indlægsstærk'] + df_Kantersæsonen['1v1 offensivt'] + df_Kantersæsonen['Fart'])/5
            df_Kantersæsonen = df_Kantersæsonen[['Sparkefærdigheder','Kombinationsstærk','Spilintelligens offensivt/indlægsstærk','1v1 offensivt','Fart','Samlet']]
    #        df_Kantersæsonen = df_Kantersæsonen.sort_values(by='Samlet',ascending=False)
            df_Kanter = df_Kanter[df_Kanter['Team name'].str.contains('Horsens')]
            df_Kanter['Sparkefærdigheder'] = (df_Kanter['Shots on target %'] + df_Kanter['Shots on target #'] + df_Kanter['XG'] + df_Kanter['Passes to final third %'] + df_Kanter['Forward Passes %'] + df_Kanter['Vertical passes %'])/6
            df_Kanter['Kombinationsstærk'] = (df_Kanter['Passes %'] + df_Kanter['Passes #'] + df_Kanter['Forward Passes %'] + df_Kanter['Forward Passes #'] + df_Kanter['Passes to final third %'] + df_Kanter['Passes to final third #'] + df_Kanter['Through passes %'] + df_Kanter['Through passes #'] + df_Kanter['Progressive passes %'] + df_Kanter['Progressive passes #'] + df_Kanter['Successful attacking actions'])/11
            df_Kanter['Spilintelligens offensivt/indlægsstærk'] = (df_Kanter['XA per 90'] + df_Kanter['XG per 90'] + df_Kanter['Through passes %'] + df_Kanter['Through passes #'] + df_Kanter['Smart passes %'] + df_Kanter['Smart passes #'] + df_Kanter['Progressive passes %'] + df_Kanter['Progressive passes #'] + df_Kanter['Key passes %'] + df_Kanter['Key passes #'] + df_Kanter['Successful attacking actions'])/11
            df_Kanter['1v1 offensivt'] = (df_Kanter['Successful dribbles #'] + df_Kanter['Successful dribbles %'] + df_Kanter['Offensive duels #'] + df_Kanter['Offensive duels %'] + df_Kanter['Progressive runs'])/5
            df_Kanter['Fart'] = (df_Kanter['Progressive runs'] + df_Kanter['Successful dribbles #'] + df_Kanter['Successful dribbles %'] + df_Kanter['Accelerations score'])/4
            df_Kanter['Samlet'] = (df_Kanter['Sparkefærdigheder'] + df_Kanter['Kombinationsstærk'] + df_Kanter['Spilintelligens offensivt/indlægsstærk'] + df_Kanter['1v1 offensivt'] + df_Kanter['Fart'])/5
            df_Kanter = df_Kanter[['Player name','Team name','label','total_minutesOnField_y','Sparkefærdigheder','Kombinationsstærk','Spilintelligens offensivt/indlægsstærk','1v1 offensivt','Fart','Samlet']]
    #        df_Kanter = df_Kanter.sort_values(by='Samlet',ascending=False)

            df_Kanter = navne.merge(df_Kanter)
            df_Kanter = df_Kanter.drop('Player Name',axis=1)
            df_Kanter = df_Kanter.drop('Player name',axis=1)    
            df_Kantersæsonen=df_Kantersæsonen.reset_index()
            df_Kantersæsonen = navne.merge(df_Kantersæsonen)
            df_Kanter = navne.merge(df_Kanter)
            df_Kantersæsonen= df_Kantersæsonen.drop('Player Name',axis=1)
            df_Kantersæsonen = df_Kantersæsonen.drop('Player name',axis=1)
            df_Kantersæsonen = df_Kantersæsonen.drop('label',axis=1)
        
            
            df_Angribere = pd.merge(df_angribereminutter,df_Angribere,on=('Player id'))
            df_Angribere = df_Angribere[df_Angribere['total_minutesOnField_y'] >=30]

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

            df_Angriberesæsonen = df_Angribere.copy()
            df_Angriberesæsonen = df_Angriberesæsonen.rename(columns={'total_minutesOnField_x':'Total minutes'})
            df_Angriberesæsonen = df_Angriberesæsonen.groupby(['Player name','Team name','Total minutes','label']).mean(numeric_only=True)

            df_Angriberesæsonen['Sparkefærdigheder'] = (df_Angriberesæsonen['xG per 90 score'] + df_Angriberesæsonen['xG per 90 score'] + df_Angriberesæsonen['Goals per 90 score'] + df_Angriberesæsonen['Shots on target, % score'])/4
            df_Angriberesæsonen['Boldfast'] = (df_Angriberesæsonen['Offensive duels won, % score'] + df_Angriberesæsonen['Offensive duels won, % score'] + df_Angriberesæsonen['Duels won, % score'] + df_Angriberesæsonen['Accurate passes, % score'] + df_Angriberesæsonen['Successful dribbles, % score'])/5
            df_Angriberesæsonen['Spilintelligens offensivt'] = (df_Angriberesæsonen['xA per 90 score'] + df_Angriberesæsonen['xG per 90 score'] + df_Angriberesæsonen['Touches in box per 90 score'] + df_Angriberesæsonen['Progressive passes per 90 score'] + df_Angriberesæsonen['Successful attacking actions per 90 score'] + df_Angriberesæsonen['Touches in box per 90 score'] + df_Angriberesæsonen['xG per 90 score'])/7
            df_Angriberesæsonen['Målfarlighed'] = (df_Angriberesæsonen['xG per 90 score']+df_Angriberesæsonen['Goals per 90 score']+df_Angriberesæsonen['xG per 90 score'] + df_Angriberesæsonen['Målfarlighed score'])/4
            df_Angriberesæsonen['Fart'] = (df_Angriberesæsonen['Progressive runs']  + df_Angriberesæsonen['Progressive runs'] + df_Angriberesæsonen['Progressive runs'] + df_Angriberesæsonen['Successful dribbles #'] + df_Angriberesæsonen['Successful dribbles, % score'] + df_Angriberesæsonen['Accelerations score'] + df_Angriberesæsonen['Offensive duels won, % score'])/7
            df_Angriberesæsonen = df_Angriberesæsonen[['Sparkefærdigheder','Boldfast','Spilintelligens offensivt','Målfarlighed','Fart']]
            df_Angriberesæsonen['Samlet'] = (df_Angriberesæsonen['Sparkefærdigheder']+df_Angriberesæsonen['Boldfast']+df_Angriberesæsonen['Spilintelligens offensivt']+df_Angriberesæsonen['Målfarlighed']+df_Angriberesæsonen['Målfarlighed']+df_Angriberesæsonen['Målfarlighed']+df_Angriberesæsonen['Fart'])/7
    #        df_Angriberesæsonen = df_Angriberesæsonen.sort_values(by='Samlet',ascending=False)

            df_Angribere = df_Angribere[df_Angribere['Team name'].str.contains('Horsens')]
            df_Angribere['Sparkefærdigheder'] = (df_Angribere['xG per 90 score'] + df_Angribere['xG per 90 score'] + df_Angribere['Goals per 90 score'] + df_Angribere['Shots on target, % score'])/4
            df_Angribere['Boldfast'] = (df_Angribere['Offensive duels won, % score'] + df_Angribere['Offensive duels won, % score'] + df_Angribere['Duels won, % score'] + df_Angribere['Accurate passes, % score'] + df_Angribere['Successful dribbles, % score'])/5
            df_Angribere['Spilintelligens offensivt'] = (df_Angribere['xA per 90 score'] + df_Angribere['xG per 90 score'] + df_Angribere['Touches in box per 90 score'] + df_Angribere['Progressive passes per 90 score'] + df_Angribere['Successful attacking actions per 90 score'] + df_Angribere['Touches in box per 90 score'] + df_Angribere['xG per 90 score'])/7
            df_Angribere['Målfarlighed'] = (df_Angribere['xG per 90 score']+df_Angribere['Goals per 90 score']+df_Angribere['xG per 90 score'] + df_Angribere['Målfarlighed score'])/4
            df_Angribere['Fart'] = (df_Angribere['Progressive runs'] + df_Angribere['Progressive runs'] + df_Angribere['Progressive runs'] + df_Angribere['Successful dribbles #'] + df_Angribere['Successful dribbles, % score'] + df_Angribere['Accelerations score'] + df_Angribere['Offensive duels won, % score'])/7
            df_Angribere = df_Angribere[['Player name','Team name','label','total_minutesOnField_y','Sparkefærdigheder','Boldfast','Spilintelligens offensivt','Målfarlighed','Fart']]
            df_Angribere['Samlet'] = (df_Angribere['Sparkefærdigheder']+df_Angribere['Boldfast']+df_Angribere['Spilintelligens offensivt']+df_Angribere['Målfarlighed']+df_Angribere['Målfarlighed']+df_Angribere['Målfarlighed']+df_Angribere['Fart'])/7
    #        df_Angribere = df_Angribere.sort_values(by='Samlet',ascending=False)
            
            kampe = df['label']
            kampe = kampe[kampe.str.contains('Horsens')]
            kampe = kampe.drop_duplicates(keep='first')  
            
            df_Angribere = navne.merge(df_Angribere)
            df_Angribere = df_Angribere.drop('Player Name',axis=1)
            df_Angribere = df_Angribere.drop('Player name',axis=1)
            df_Angriberesæsonen=df_Angriberesæsonen.reset_index()
            df_Angriberesæsonen = navne.merge(df_Angriberesæsonen)
            df_Angribere = navne.merge(df_Angribere)
            df_Angriberesæsonen= df_Angriberesæsonen.drop('Player Name',axis=1)
            df_Angriberesæsonen = df_Angriberesæsonen.drop('Player name',axis=1)
            df_Angriberesæsonen = df_Angriberesæsonen.drop('label',axis=1)
            col1, col2, col3 = st.columns(3)
            with col1:
                option2 = st.selectbox('Vælg spiller',navneliste)
                df_Angriberesæsonen = df_Angriberesæsonen[df_Angriberesæsonen['Spillere'].str.contains(option2)]
                df_Angribere = df_Angribere[df_Angribere['Spillere'].str.contains(option2)]
                df_Kantersæsonen = df_Kantersæsonen[df_Kantersæsonen['Spillere'].str.contains(option2)]
                df_Kanter = df_Kanter[df_Kanter['Spillere'].str.contains(option2)]
                df_Centrale_midtsæsonen = df_Centrale_midtsæsonen[df_Centrale_midtsæsonen['Spillere'].str.contains(option2)]
                df_Centrale_midt = df_Centrale_midt[df_Centrale_midt['Spillere'].str.contains(option2)]
                df_Stopperesæsonen = df_Stopperesæsonen[df_Stopperesæsonen['Spillere'].str.contains(option2)]
                df_Stoppere = df_Stoppere[df_Stoppere['Spillere'].str.contains(option2)]
                df_backssæsonen = df_backssæsonen[df_backssæsonen['Spillere'].str.contains(option2)]
                df_backs = df_backs[df_backs['Spillere'].str.contains(option2)]

            with col2:
                option = st.multiselect('Vælg kamp(e))',kampe)
                if len(option) > 0:
                    temp_select = option
                else:
                    temp_select = kampe
            df = pd.read_csv(r'Fysisk data/U15 PHV.csv')
            df = df.drop(df.index[:6])
            df.columns = df.iloc[0]
            df = df.drop(df.index[:1])
            df['Navn'] = df['First Name'] + " " + df['Last Name']
            df = df[['Navn','Age @ PHV','Date of Birth (dd-mm-yy)']]
            df.dropna(subset=['Navn'], inplace=True)
            df['Date of Birth (dd-mm-yy)'] = pd.to_datetime(df['Date of Birth (dd-mm-yy)'])
            df['Fødselsdato'] = df['Date of Birth (dd-mm-yy)'].dt.strftime('%d-%m-%Y')
            today = pd.Timestamp(date.today())
            df['Alder'] = (today- df['Date of Birth (dd-mm-yy)'])/ np.timedelta64(1,'Y')
            df['Alder'] = pd.to_numeric(df['Alder'])
            df['Age @ PHV'] = pd.to_numeric(df['Age @ PHV'])
            df['Modenhed'] = df['Alder'] - df['Age @ PHV']
            df['Modenhed'] = df['Modenhed'].astype(float)
            df = df[df['Navn'] == option2]
            df = df[['Navn','Age @ PHV','Fødselsdato','Modenhed']]
            df1 = pd.read_csv(r'Fysisk data/Fysiske test U15.csv')
            df1['Navn'] = df1['Fornavn'] + " " + df1['Efternavn']
            df1 = df1[df1['Navn'] == option2]
            df1['CMJ'] = df1[['CMJ 1 (cm)','CMJ 2 (cm)']].max(axis=1)
            df1['Sprint 5 m'] = df1[['Sprint 5 m','Sprint 5 m2']].min(axis=1)
            df1['Sprint 10 m'] = df1[['Sprint 10 m','Sprint 10 m3']].min(axis=1)
            df1['Sprint 25 m'] = df1[['Sprint 25 m','Sprint 25 m4']].min(axis=1)
            df1['Sprint 30 m'] = df1[['Sprint 30 m','Sprint 30 m5']].min(axis=1)
            df1['Topfart (km/t)'] = df1[['Topfart (km/t)','Topfart (km/t)6']].max(axis=1)
            df1 = df1[['Navn','CMJ','Sprint 5 m','Sprint 10 m','Sprint 25 m','Sprint 30 m','Topfart (km/t)']]
            df = pd.merge(df,df1,how='inner')
            st.dataframe(df,hide_index=True,use_container_width=True)
            
            df_backs = df_backs[df_backs['label'].isin(temp_select)]
            df_backstal = df_backs.copy()
            df_backstal = df_backstal.rename(columns={'total_minutesOnField_y':'Total minutes'},inplace=False)
            df_backstal = df_backstal[['Spillere','label','Total minutes','Indlægsstærk','1v1 færdigheder','Spilintelligens defensivt','Fart','Samlet']]
            df_backstal = df_backstal.set_index('Spillere')
            df_backs = df_backs.drop('label',axis=1)
            df_backssæsonen = df_backssæsonen.groupby(['Spillere','Trup','Team name','Total minutes']).mean()
            
            df_backs = df_backs.groupby(['Spillere','Trup','Team name']).agg({
            'total_minutesOnField_y':'sum',
            'Indlægsstærk':'mean',
            '1v1 færdigheder':'mean',
            'Spilintelligens defensivt':'mean',
            'Fart':'mean',
            'Samlet':'mean'
            })

            df_backs = df_backs.sort_values(by='Samlet',ascending=False)
            df_backs = df_backs.rename(columns={'total_minutesOnField_y':'Total minutes'},inplace=False)
            df_backs = df_backs.reset_index()
            df_backs = df_backs.set_index(['Spillere','Trup','Team name'])
            df_backssæsonen = df_backssæsonen.reset_index()
            df_backssæsonen = df_backssæsonen.set_index(['Spillere','Trup','Team name'])
            df_backs = pd.concat([df_backs,df_backssæsonen],axis=0)        
            df_backs = df_backs.reset_index(drop=True)
            df_backs = df_backs.set_index(['Total minutes'])
            df_backssæsonen = df_backssæsonen.reset_index(drop=True)
            df_backssæsonen = df_backssæsonen.set_index(['Total minutes'])

            
            df_Stoppere = df_Stoppere[df_Stoppere['label'].isin(temp_select)]
            df_Stopperetal = df_Stoppere.copy()
            df_Stopperetal = df_Stopperetal.rename(columns={'total_minutesOnField_y':'Total minutes'},inplace=False)
            df_Stopperetal = df_Stopperetal[['Spillere','label','Total minutes','Pasningssikker','Spilintelligens defensivt','Spilintelligens offensivt','Nærkamps- og duelstærk','Samlet']]
            df_Stopperetal = df_Stopperetal.set_index('Spillere')

            df_Stoppere = df_Stoppere.drop('label',axis=1)
            df_Stopperesæsonen = df_Stopperesæsonen.groupby(['Spillere','Trup','Team name','Total minutes']).mean()
            
            df_Stoppere = df_Stoppere.groupby(['Spillere','Trup','Team name']).agg({
            'total_minutesOnField_y':'sum',
            'Pasningssikker':'mean',
            'Spilintelligens offensivt':'mean',
            'Spilintelligens defensivt':'mean',
            'Nærkamps- og duelstærk':'mean',
            'Samlet':'mean'
            })

            df_Stoppere = df_Stoppere.sort_values(by='Samlet',ascending=False)
            df_Stoppere = df_Stoppere.rename(columns={'total_minutesOnField_y':'Total minutes'},inplace=False)
            df_Stoppere = df_Stoppere.reset_index()
            df_Stoppere = df_Stoppere.set_index(['Spillere','Trup','Team name'])
            df_Stopperesæsonen = df_Stopperesæsonen.reset_index()
            df_Stopperesæsonen = df_Stopperesæsonen.set_index(['Spillere','Trup','Team name'])
            df_Stoppere = pd.concat([df_Stoppere,df_Stopperesæsonen],axis=0)
            df_Stoppere = df_Stoppere.reset_index(drop=True)
            df_Stoppere = df_Stoppere.set_index(['Total minutes'])
            df_Stopperesæsonen = df_Stopperesæsonen.reset_index(drop=True)
            df_Stopperesæsonen = df_Stopperesæsonen.set_index(['Total minutes'])

            df_Centrale_midt = df_Centrale_midt[df_Centrale_midt['label'].isin(temp_select)]
            df_Centraletal = df_Centrale_midt.copy()
            df_Centraletal = df_Centraletal.rename(columns={'total_minutesOnField_y':'Total minutes'},inplace=False)
            df_Centraletal = df_Centraletal[['Spillere','label','Total minutes','Pasningssikker/Spilvendinger','Spilintelligens defensivt','Boldfast','Samlet']]
            df_Centraletal = df_Centraletal.set_index('Spillere')
            
            df_Centrale_midt = df_Centrale_midt.drop('label',axis=1)
            df_Centrale_midtsæsonen = df_Centrale_midtsæsonen.groupby(['Spillere','Trup','Team name','Total minutes']).mean()
            
            df_Centrale_midt = df_Centrale_midt.groupby(['Spillere','Trup','Team name']).agg({
            'total_minutesOnField_y':'sum',
            'Pasningssikker/Spilvendinger':'mean',
            'Boldfast':'mean',
            'Spilintelligens defensivt':'mean',
            'Samlet':'mean'
            })

            df_Centrale_midt = df_Centrale_midt.sort_values(by='Samlet',ascending=False)
            df_Centrale_midt = df_Centrale_midt.rename(columns={'total_minutesOnField_y':'Total minutes'},inplace=False)
            df_Centrale_midt = df_Centrale_midt.reset_index()
            df_Centrale_midt = df_Centrale_midt.set_index(['Spillere','Trup','Team name'])
            df_Centrale_midtsæsonen = df_Centrale_midtsæsonen.reset_index()
            df_Centrale_midtsæsonen = df_Centrale_midtsæsonen.set_index(['Spillere','Trup','Team name'])
            df_Centrale_midt = pd.concat([df_Centrale_midt,df_Centrale_midtsæsonen],axis=0)
            df_Centrale_midt = df_Centrale_midt.reset_index(drop=True)
            df_Centrale_midt = df_Centrale_midt.set_index(['Total minutes'])
            df_Centrale_midtsæsonen = df_Centrale_midtsæsonen.reset_index(drop=True)
            df_Centrale_midtsæsonen = df_Centrale_midtsæsonen.set_index(['Total minutes'])
        
                
            df_Kanter = df_Kanter[df_Kanter['label'].isin(temp_select)]
            df_Kantertal = df_Kanter.copy()
            df_Kantertal = df_Kantertal.rename(columns={'total_minutesOnField_y':'Total minutes'},inplace=False)
            df_Kantertal = df_Kantertal[['Spillere','label','Total minutes','Sparkefærdigheder','Kombinationsstærk','Spilintelligens offensivt/indlægsstærk','1v1 offensivt','Fart','Samlet']]
            df_Kantertal = df_Kantertal.set_index('Spillere')
            df_Kanter = df_Kanter.drop('label',axis=1)
            df_Kantersæsonen = df_Kantersæsonen.groupby(['Spillere','Trup','Team name','Total minutes']).mean()
            
            df_Kanter = df_Kanter.groupby(['Spillere','Trup','Team name']).agg({
            'total_minutesOnField_y':'sum',
            'Sparkefærdigheder':'mean',
            'Kombinationsstærk':'mean',
            'Spilintelligens offensivt/indlægsstærk':'mean',
            '1v1 offensivt':'mean',
            'Fart':'mean',
            'Samlet':'mean'
            })
            
            df_Kanter = df_Kanter.sort_values(by='Samlet',ascending=False)
            df_Kanter = df_Kanter.rename(columns={'total_minutesOnField_y':'Total minutes'},inplace=False)
            df_Kanter = df_Kanter.reset_index()
            df_Kanter = df_Kanter.set_index(['Spillere','Trup','Team name'])
            df_Kantersæsonen = df_Kantersæsonen.reset_index()
            df_Kantersæsonen = df_Kantersæsonen.set_index(['Spillere','Trup','Team name'])
            df_Kanter = pd.concat([df_Kanter,df_Kantersæsonen],axis=0)
            df_Kanter = df_Kanter.reset_index(drop=True)
            df_Kanter = df_Kanter.set_index(['Total minutes'])
            df_Kantersæsonen = df_Kantersæsonen.reset_index(drop=True)
            df_Kantersæsonen = df_Kantersæsonen.set_index(['Total minutes'])
            
            df_Angribere = df_Angribere[df_Angribere['label'].isin(temp_select)]
            df_Angriberetal = df_Angribere.copy()
            df_Angriberetal = df_Angriberetal.rename(columns={'total_minutesOnField_y':'Total minutes'},inplace=False)
            df_Angriberetal = df_Angriberetal[['Spillere','label','Total minutes','Sparkefærdigheder','Boldfast','Spilintelligens offensivt','Målfarlighed','Fart','Samlet']]
            df_Angriberetal = df_Angriberetal.set_index('Spillere')
            df_Angribere = df_Angribere.drop('label',axis=1)
            df_Angriberesæsonen = df_Angriberesæsonen.groupby(['Spillere','Trup','Team name','Total minutes']).mean()

            df_Angribere = df_Angribere.groupby(['Spillere','Trup','Team name']).agg({
            'total_minutesOnField_y':'sum',
            'Sparkefærdigheder': 'mean',
            'Boldfast': 'mean',
            'Spilintelligens offensivt':'mean',
            'Målfarlighed':'mean',
            'Fart':'mean',
            'Samlet':'mean',
            })

            df_Angribere = df_Angribere.sort_values(by = 'Samlet',ascending=False)
            df_Angribere = df_Angribere.rename(columns={'total_minutesOnField_y':'Total minutes'},inplace=False)
            df_Angribere = df_Angribere.reset_index()
            df_Angribere = df_Angribere.set_index(['Spillere','Trup','Team name'])
            df_Angriberesæsonen = df_Angriberesæsonen.reset_index()
            df_Angriberesæsonen = df_Angriberesæsonen.set_index(['Spillere','Trup','Team name'])
            df_Angribere = pd.concat([df_Angribere,df_Angriberesæsonen],axis=0)
            df_Angribere = df_Angribere.reset_index(drop=True)
            df_Angribere = df_Angribere.set_index(['Total minutes'])
            df_Angriberesæsonen = df_Angriberesæsonen.reset_index(drop=True)
            df_Angriberesæsonen = df_Angriberesæsonen.set_index(['Total minutes'])

            dataframe_names = ['Stopper', 'Back', 'Central midt', 'Kant', 'Angriber']

            # Create the selectbox in Streamlit
            with col3:
                selected_dataframe = st.selectbox('Position', options=dataframe_names)
                selected_dftal = None  # Initialize selected_dftal to None before the if-elif block

            # Based on the selected dataframe, retrieve the corresponding dataframe object
            if selected_dataframe == 'Stopper':
                selected_df = df_Stoppere
                selected_dftal = df_Stopperetal
            elif selected_dataframe == 'Back':
                selected_df = df_backs
                selected_dftal = df_backstal
            elif selected_dataframe == 'Central midt':
                selected_df = df_Centrale_midt
                selected_dftal = df_Centraletal
            elif selected_dataframe == 'Kant':
                selected_df = df_Kanter
                selected_dftal = df_Kantertal
            elif selected_dataframe == 'Angriber':
                selected_df = df_Angribere
                selected_dftal = df_Angriberetal
            with st.expander('Wyscout data'):
                st.title(option2 + ' Wyscout data')
                st.dataframe(selected_df,use_container_width=True)
                df_filtered = selected_df.copy()
                st.write('Hver parameter går fra 1-5, hvor 5 er top 20% i ligaen, 4 er top 40% osv. Hvert talent-id punkt er en udregning af flere parametre')
                # Create a scatterpolar plot using plotly
                        
                selected_dftal_columns = None
                if selected_dftal is not None:
                    selected_dftal_columns = selected_dftal.columns[2:]

                # Create two columns for displaying plots side by side
                col1, col2 = st.columns(2)

                # Plot the first plot in the first column
                with col1:
                    fig = go.Figure()
                    try:
                        for _, row in df_filtered.iterrows():
                            fig.add_trace(go.Scatterpolar(
                                r=row.values,
                                theta=df_filtered.columns,
                                fill='toself'
                            ))
                        fig.data[0].name = 'Valgte periode'
                        fig.data[1].name = 'Hele sæsonen'
                        # Set plot title and layout
                        fig.update_layout(
                            title='Talent-id plot',
                            template='plotly_dark',
                            polar=dict(
                                radialaxis=dict(
                                    visible=True,
                                    range=[1, 5],
                                    tickfont=dict(
                                        size=8  # Adjust the font size for radial axis labels
                                    ),
                                ),
                            ),
                            width=400,  # Adjust the width as needed
                            height=500,  # Adjust the height as needed
                            font=dict(
                                size=8
                            )
                        )
                        st.plotly_chart(fig)
                    except IndexError:
                        st.warning(" ")

                # Plot the second plot in the second column
                with col2:
                    if selected_dftal.empty:
                        st.warning('')
                    else:
                        fig = go.Figure()
                        try:
                            for column in selected_dftal_columns:
                                fig.add_trace(go.Scatter(
                                    x=selected_dftal['label'],
                                    y=selected_dftal[column],
                                    mode='lines',
                                    name=column
                                    ))

                                fig.update_layout(
                                    title='Talent id score over tid',
                                    template='plotly_dark',
                                    legend=dict(
                                        orientation="h",  # Set legend orientation to horizontal
                                        font=dict(
                                            size=8
                                        )
                                    ),
                                    xaxis=dict(
                                        tickangle=0,  # Adjust x-axis label rotation angle as needed
                                        tickfont=dict(
                                            size=8,  # Adjust font size for x-axis labels
                                        ),
                                    ),
                                    yaxis=dict(
                                        range=[1, 5],  # Set y-axis range to [1, 5]
                                    ),
                                    width=500,  # Adjust the width as needed
                                )

                            st.plotly_chart(fig)
                        except IndexError:
                            st.warning(" ")

            
                # Display the dataframe
                if selected_dftal is not None:
                    selected_dftal = selected_dftal.reset_index()
                    selected_dftal = selected_dftal.drop(columns=['Spillere'])
                    selected_dftal = selected_dftal.set_index('label')
                    st.dataframe(selected_dftal,use_container_width=True)
            
            try:
                with open('træningsregistrering.json', 'r') as json_file:
                    træningsdata = json.load(json_file)
                    træningsdata = pd.DataFrame(træningsdata)
            except FileNotFoundError:
                return pd.DataFrame(columns=['Tidspunkt', 'Dato','Årgang','Rådighed', 'Spillerens navn', 'Træningshold', 'Træningstype', 'Antal minutter trænet'])
            
            date_format = '%d-%m-%Y'  # Specify your date format
            træningsdata['Dato'] = pd.to_datetime(træningsdata['Dato'], format=date_format)

            min_date = træningsdata['Dato'].min()
            max_date = træningsdata['Dato'].max()

            date_range = pd.date_range(start=min_date, end=max_date, freq='D')
            date_options = date_range.strftime(date_format)  # Convert dates to the specified format

            default_end_date = date_options[-1]

            # Calculate the default start date as 14 days before the default end date
            default_start_date = pd.to_datetime(default_end_date, format=date_format) - timedelta(days=14)
            default_start_date = default_start_date.strftime(date_format)

            # Set the default start and end date values for the select_slider
            selected_start_date, selected_end_date = st.select_slider(
                'Vælg datointerval',
                options=date_options,
                value=(default_start_date, default_end_date)
            )

            selected_start_date = pd.to_datetime(selected_start_date, format=date_format)
            selected_end_date = pd.to_datetime(selected_end_date, format=date_format)
            filtered_data = træningsdata[
                (træningsdata['Dato'] >= selected_start_date) & (træningsdata['Dato'] <= selected_end_date)
            ]

            # Sort the filtered data by the 'Dato' column
#            sorted_data = filtered_data.sort_values(by ='Dato')
            sorted_data = filtered_data.copy()
            sorted_data = sorted_data[sorted_data['Spiller'] == option2]
            minutter_columns = sorted_data.filter(regex='.*minutter$').columns.tolist()
            minutter_columns_processed = [col.replace('minutter', '') for col in minutter_columns]

            minutter_df = pd.DataFrame({
                'Træningstype': minutter_columns_processed,
                'Minutter': [sorted_data[col].sum() for col in minutter_columns]
            })
            st.title(option2 + ' Træningsdata')
            minutter_df['Træningstype'] = minutter_df['Træningstype'].str.replace('minutter', '')
            col1, col2 = st.columns([3,1])

            with col2:
                træningsgruppe = sorted_data[['Træningsgruppe']].value_counts()
                træningsgruppe = træningsgruppe.rename_axis('Træningsgruppe').reset_index(name='Antal')
                #træningsgruppe = træningsgruppe.set_index('Træningsgruppe')
                #st.dataframe(træningsgruppe,use_container_width=True,hide_index=True)
                fig = go.Figure()
                fig.add_trace(go.Pie(
                    labels=træningsgruppe['Træningsgruppe'],
                    values=træningsgruppe['Antal'],
                    hole=0.0,
                ))
                fig.update_layout(title='Træningsgrupper')
                st.plotly_chart(fig)       

            with col1:
                fig = go.Figure()
                for idx, label in enumerate(minutter_df['Træningstype']):
                    fig.add_trace(go.Pie(
                        labels=minutter_df['Træningstype'],
                        values=minutter_df['Minutter'],
                    ))

                fig.update_layout(title='Træningstyper og deres tid i minutter',
                )
                st.plotly_chart(fig)

            col1,col2 = st.columns(2)


            fig = go.Figure()
            for idx, col in enumerate(minutter_columns):
                fig.add_trace(go.Bar(
                    x=sorted_data['Dato'],
                    y=sorted_data[col],
                    name=col.replace('minutter', ''),
                ))

            fig.update_layout(
                barmode='stack',
                xaxis=dict(title='Dato'),
                yaxis=dict(title='Minutter'),
                title='Træningsdata over tid'
            )

            st.plotly_chart(fig,use_container_width=True)

         
            afbud_årsag = sorted_data['Afbud årsag'].value_counts()
            afbud_årsag = afbud_årsag.rename_axis('Afbud årsag').reset_index(name='Antal')  # Renaming axis for clarity
            afbud_årsag = afbud_årsag.set_index('Afbud årsag')
            
            col1,col2,col3 = st.columns(3)    
            with col1:
                Individuel_træning_kommentar = sorted_data[['Dato', 'Individuel træning kommentar']]
                Individuel_træning_kommentar = Individuel_træning_kommentar.dropna(subset=['Individuel træning kommentar'])
                st.dataframe(Individuel_træning_kommentar.style.format({'Dato': '{:%d-%m-%Y}'}), hide_index=True,use_container_width=True)
            with col2:    
                Individuel_video_kommentar = sorted_data[['Dato', 'Individuel video kommentar']]
                Individuel_video_kommentar = Individuel_video_kommentar.dropna(subset=['Individuel video kommentar'])
                st.dataframe(Individuel_video_kommentar.style.format({'Dato': '{:%d-%m-%Y}'}), hide_index=True,use_container_width=True)
            with col3:
                st.dataframe(afbud_årsag,use_container_width=True)

            st.title(option2 + ' Kampdata')
            try:
                with open('Kampregistrering.json', 'r') as json_file:
                    Kampdata = json.load(json_file)
                    Kampdata = pd.DataFrame(Kampdata)
            except FileNotFoundError:
                return st.write('Ingen kampdata på den valgte spiller')

            date_format = '%d-%m-%Y'  # Specify your date format
            Kampdata['Dato'] = pd.to_datetime(Kampdata['Dato'], format=date_format)

            filtered_data = Kampdata[
                (Kampdata['Dato'] >= selected_start_date) & (Kampdata['Dato'] <= selected_end_date)
            ]
            sorted_data = filtered_data.sort_values(by ='Dato')
            sorted_data = sorted_data[sorted_data['Spiller'] == option2]
            
            kampminutter_spillet = sorted_data['Minutter spillet'].sum()
            kampminutter_til_rådighed = sorted_data['Minutter til rådighed'].sum()

            minutter_ude = kampminutter_til_rådighed - kampminutter_spillet
            minutter_spillet = kampminutter_spillet

            # Creating a DataFrame with the percentages
            data = {
                'Minutter spillet': [minutter_spillet],
                'Minutter ikke spillet': [minutter_ude]
            }
            kampminutter = pd.DataFrame(data, index=['Kampminutter'])
            
            Starter_inde = {
                'Starter inde' : sorted_data['Starter inde'].sum(),
                'Starter ude' : sorted_data['Starter ude'].sum()
            }
            Starter_inde = pd.DataFrame.from_dict(Starter_inde,orient='index',columns = ['Antal kampe'])
            
            Mål_assist = {
                'Mål': sorted_data['Mål'].sum(),
                'Assist': sorted_data['Assist'].sum(),
            }
            Mål_assist = pd.DataFrame.from_dict(Mål_assist, orient='index', columns=['Antal'])

            # Get unique values from the 'Spillere' column
            spillere_values = sorted_data['Spiller'].unique()

            # Filter columns containing a string from 'Spillere' column
            filtered_columns = [col for col in sorted_data.columns if any(spiller in col for spiller in spillere_values)]

            # Create a new DataFrame with the filtered columns
            filtered_data = sorted_data[filtered_columns]
            
            Kamptype = sorted_data['Kamptype'].value_counts()
            Kamptype = Kamptype.rename_axis('Kamptype').reset_index(name='Antal')  # Renaming axis for clarity
            Kamptype = Kamptype.set_index('Kamptype')

            Rådighed = sorted_data['Rådighed'].value_counts()
            Rådighed = Rådighed.rename_axis('Rådighed').reset_index(name='Antal')  # Renaming axis for clarity
            Rådighed = Rådighed.set_index('Rådighed')
            
            Modstandere = sorted_data['Modstanderhold'].value_counts()
            Modstandere = Modstandere.rename_axis('Modstander').reset_index(name='Antal')  # Renaming axis for clarity
            Modstandere = Modstandere.set_index('Modstander')
            Kampårgang = sorted_data['Kampårgang'].value_counts()
            Kampårgang = Kampårgang.rename_axis('Kampårgang').reset_index(name='Antal')  # Renaming axis for clarity
            Kampårgang = Kampårgang.set_index('Kampårgang')

            def create_pie_chart(data, title):
                fig = go.Figure(data=[go.Pie(labels=data.index, values=data['Antal'], hole=0.0)])
                fig.update_layout(title=title)
                st.plotly_chart(fig)

            
            col1,col2= st.columns([3,1])
            with col1:
                fig = go.Figure(data=[go.Pie(labels=kampminutter.columns, values=kampminutter.iloc[0], hole=0.0)])
                fig.update_layout(title='Fordeling af minutter til rådighed')
                st.plotly_chart(fig)
                create_pie_chart(Kamptype, 'Fordeling af kamptyper')
                
            with col2:
                create_pie_chart(Rådighed,'Fordeling af rådighedsstatus')
                create_pie_chart(Kampårgang, 'Fordeling af Kampårgange')
                
            col1,col2 = st.columns(2)
            with col1:
                st.dataframe(Mål_assist,use_container_width=True)
                
            with col2:
                st.dataframe(Modstandere,use_container_width=True)
                
            import gspread
            import pandas as pd
            import numpy as np

            gc = gspread.service_account('wellness-1123-178fea106d0a.json')
            sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1haWEtNQdhthKaSQjb2BRHlq2FLexicUOAHbjNFRAUAk/edit#gid=1984878556')
            ws = sh.worksheet('Samlet')
            df = pd.DataFrame(ws.get_all_records())
            
            df['Tidsstempel'] = pd.to_datetime(df['Tidsstempel'], format='%d/%m/%Y %H.%M.%S', errors='coerce').astype('datetime64[ns]')

            df['Hvilken årgang er du?'] = df['Hvilken årgang er du?'].astype(str)
            df['Hvor frisk er du?'] = df['Hvor frisk er du?'].astype(str)
            df['Hvor frisk er du?'] = df['Hvor frisk er du?'].str.extract(r'(\d+)').astype(float)
            df['Hvordan har du det mentalt'] = df['Hvordan har du det mentalt'].astype(str)
            df['Hvordan har du det mentalt'] = df['Hvordan har du det mentalt'].str.extract(r'(\d+)').astype(float)
            df['Hvordan har din søvn været?'] = df['Hvordan har din søvn været?'].astype(str)
            df['Hvordan har din søvn været?'] = df['Hvordan har din søvn været?'].str.extract(r'(\d+)').astype(float)
            df['Hvor hård var træning/kamp? (10 er hårdest)'] = df['Hvor hård var træning/kamp? (10 er hårdest)'].astype(str)
            df['Hvor hård var træning/kamp? (10 er hårdest)'] = df['Hvor hård var træning/kamp? (10 er hårdest)'].str.extract(r'(\d+)').astype(float)
            df['Hvor udmattet er du?'] = df['Hvor udmattet er du?'].astype(str)
            df['Hvor udmattet er du?'] = df['Hvor udmattet er du?'].str.extract(r'(\d+)').astype(float)
            df['Bedøm din muskelømhed'] = df['Bedøm din muskelømhed'].astype(str)
            df['Bedøm din muskelømhed'] = df['Bedøm din muskelømhed'].str.extract(r'(\d+)').astype(float)
            df['Jeg følte mig tilpas udfordret under træning/kamp'] = df['Jeg følte mig tilpas udfordret under træning/kamp'].astype(str)
            df['Jeg følte mig tilpas udfordret under træning/kamp'] = df['Jeg følte mig tilpas udfordret under træning/kamp'].str.extract(r'(\d+)').astype(float)
            df['Min tidsfornemmelse forsvandt under træning/kamp'] = df['Min tidsfornemmelse forsvandt under træning/kamp'].astype(str)
            df['Min tidsfornemmelse forsvandt under træning/kamp'] = df['Min tidsfornemmelse forsvandt under træning/kamp'].str.extract(r'(\d+)').astype(float)
            df['Jeg oplevede at tanker og handlinger var rettet mod træning/kamp'] = df['Jeg oplevede at tanker og handlinger var rettet mod træning/kamp'].astype(str)
            df['Jeg oplevede at tanker og handlinger var rettet mod træning/kamp'] = df['Jeg oplevede at tanker og handlinger var rettet mod træning/kamp'].str.extract(r'(\d+)').astype(float)
            df['Hvordan har du det mentalt?'] = df['Hvordan har du det mentalt?'].astype(str)
            df['Hvordan har du det mentalt?'] = df['Hvordan har du det mentalt?'].str.extract(r'(\d+)').astype(float)

            df.rename(columns={'Hvor mange timer sov i du i nat?':'Hvor mange timer sov du i nat?'},inplace=True)
            df = pd.melt(df,id_vars=['Tidsstempel','Spørgsmål før eller efter træning','Hvor frisk er du?','Hvordan har du det mentalt','Har du fået nok at spise inden træning/kamp?','Hvordan har din søvn været?','Hvor mange timer sov du i nat?','Træning/kamp - tid i minutter?','Hvor hård var træning/kamp? (10 er hårdest)','Hvor udmattet er du?','Bedøm din muskelømhed','Hvordan har du det mentalt?','Jeg følte mig tilpas udfordret under træning/kamp','Min tidsfornemmelse forsvandt under træning/kamp','Jeg oplevede at tanker og handlinger var rettet mod træning/kamp','Hvilken årgang er du?'],value_vars=['Spillere U13','Spillere U14','Spillere U15','Spillere U16','Spillere U17','Spillere U18','Spillere U19','Spillere U20'],value_name='Spiller')
            df = df[df['Spiller'] != '']
            df['Hvilken årgang er du?'] = df['Hvilken årgang er du?'].astype(float)
            df = df[df['Spiller']==option2]
            
            førtræning = df[['Tidsstempel','Spiller','Hvilken årgang er du?','Hvor frisk er du?','Hvordan har du det mentalt','Har du fået nok at spise inden træning/kamp?','Hvordan har din søvn været?','Hvor mange timer sov du i nat?']]
            eftertræning = df[['Tidsstempel','Spiller','Hvilken årgang er du?','Træning/kamp - tid i minutter?','Hvor hård var træning/kamp? (10 er hårdest)','Hvor udmattet er du?','Bedøm din muskelømhed','Hvordan har du det mentalt?','Jeg følte mig tilpas udfordret under træning/kamp','Min tidsfornemmelse forsvandt under træning/kamp','Jeg oplevede at tanker og handlinger var rettet mod træning/kamp']]
            førtræning.dropna(inplace=True)
            eftertræning.dropna(inplace=True)


            #eftertræning.set_index('Tidsstempel', inplace=True)
            #eftertræning.sort_index(ascending=False, inplace=True)
            #førtræning.set_index('Tidsstempel', inplace=True)
            #førtræning.sort_index(ascending=False, inplace=True)
            førtræning['Tidsstempel'] = pd.to_datetime(førtræning['Tidsstempel'])
            eftertræning['Tidsstempel'] = pd.to_datetime(eftertræning['Tidsstempel'])

            førtræning = førtræning[
            (førtræning['Tidsstempel'] >= selected_start_date) & (førtræning['Tidsstempel'] <= selected_end_date)
            ]
            eftertræning= eftertræning[
                (eftertræning['Tidsstempel'] >= selected_start_date) & (eftertræning['Tidsstempel'] <= selected_end_date)
            ]

            col1,col2 = st.columns([3,1])
            with col1:
                fig_førtræning = px.bar(førtræning, x='Tidsstempel', y=['Hvor frisk er du?', 'Hvordan har du det mentalt', 'Hvordan har din søvn været?'],barmode='group')
                fig_førtræning.update_layout(
                    title='Før træning scores over tid',
                    template='plotly_dark',
                    bargap=0.0,  # Adjust the gap between bars
                    bargroupgap=0.0,  # Adjust the gap between groups of bars
                    yaxis=dict(range=[0, 7]))
                st.plotly_chart(fig_førtræning)

            with col2:
                fig_eftertræning = px.bar(eftertræning, x='Tidsstempel', y=['Hvor udmattet er du?','Bedøm din muskelømhed','Hvordan har du det mentalt?'],barmode='group')
                fig_eftertræning.update_layout(
                    title='Efter træning scores over tid',
                    template='plotly_dark',
                    bargap=0.0,  # Adjust the gap between bars
                    bargroupgap=0.0,  # Adjust the gap between groups of bars
                    yaxis=dict(range=[0, 7]))  # Set the y-axis range
                st.plotly_chart(fig_eftertræning)

        def U17():
            import pandas as pd
            import streamlit as st
            import json
            from pandas import json_normalize
            import ast
            from dateutil import parser
            import plotly.graph_objects as go
            import matplotlib.pyplot as plt
            import matplotlib
            from datetime import datetime, timedelta
            import plotly.express as px
            from datetime import date
            import numpy as np
            
            navne = pd.read_excel('Navne.xlsx')
            navne = navne[navne['Trup'].str.contains('U17')]
            navneliste = navne['Spillere'].sort_values(ascending=True)
            
            df = pd.read_csv(r'Individuelt dashboard/Individuelt dashboard U17.csv')
            df.rename(columns={'playerId': 'Player id'}, inplace=True)
            df = df.astype(str)
            dfevents = pd.read_csv('U17 eventdata alle.csv',low_memory=False)
            dfevents1 = dfevents[['Player id','Player name','team_name','label','date','matchId']]
            dfspillernavn = df[['Player id','matchId','positions','average','percent','total']]
            dfspillernavn = dfspillernavn.astype(str)
            dfevents1['Player id'] = dfevents1['Player id'].astype(str)
            dfevents1['matchId'] = dfevents1['matchId'].astype(str)
            df = dfspillernavn.merge(dfevents1)

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
            df = df.sort_values('date',ascending=True)

            df_backs = df[df['position_codes'].str.contains('|'.join(['lb', 'rb']))]
            df_backs = df_backs[df_backs['total_minutesOnField'] >= 40]
            df_backsminutter = df_backs[['Player name','Team name','total_minutesOnField']]
            df_backsminutter = df_backsminutter.groupby(['Player id']).sum(numeric_only=True)
            df_backsminutter = df_backsminutter[df_backsminutter['total_minutesOnField'] >= 200]

            df_Stoppere = df[df['position_codes'].str.contains('|'.join(['cb']))]
            df_Stoppere = df_Stoppere[df_Stoppere['total_minutesOnField'] >= 40]
            df_stoppereminutter = df_Stoppere[['Player name','Team name','total_minutesOnField']]
            df_stoppereminutter = df_stoppereminutter.groupby(['Player id']).sum(numeric_only=True)
            df_stoppereminutter = df_stoppereminutter[df_stoppereminutter['total_minutesOnField'] >= 200]

            df_Centrale_midt = df[df['position_codes'].str.contains('|'.join(['cm','amf','dmf']))]
            df_Centrale_midt = df_Centrale_midt[df_Centrale_midt['total_minutesOnField'] >= 40]
            df_centraleminutter = df_Centrale_midt[['Player name','Team name','total_minutesOnField']]
            df_centraleminutter = df_centraleminutter.groupby(['Player id']).sum(numeric_only=True)
            df_centraleminutter = df_centraleminutter[df_centraleminutter['total_minutesOnField'] >= 200]

            df_Kanter = df[df['position_codes'].str.contains('|'.join(['rw','lw','ramf','lamf']))]
            df_Kanter = df_Kanter[df_Kanter['total_minutesOnField'] >=40]
            df_kanterminutter = df_Kanter[['Player name','Team name','total_minutesOnField']]
            df_kanterminutter = df_kanterminutter.groupby(['Player id']).sum(numeric_only=True)
            df_kanterminutter = df_kanterminutter[df_kanterminutter['total_minutesOnField'] >=200]


            df_Angribere = df[df['position_codes'].str.contains('|'.join(['cf','ss']))]
            df_Angribere = df_Angribere[df_Angribere['total_minutesOnField'] >= 40]
            df_angribereminutter = df_Angribere[['Player name','Team name','total_minutesOnField']]
            df_angribereminutter = df_angribereminutter.groupby(['Player id']).sum(numeric_only=True)
            df_angribereminutter = df_angribereminutter[df_angribereminutter['total_minutesOnField'] >= 200]

            df_backs = pd.merge(df_backsminutter,df_backs,on=('Player id'))
            df_backs = df_backs[df_backs['total_minutesOnField_y'] >=40]

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
            df_backssæsonen = df_backs[['Player name','Team name','label','total_minutesOnField_x','total_minutesOnField_y','Number of crosses score','Accurate crosses score','XA score','Passes to final third score','Successful dribbles score','Defensive duels won score','Progressive runs score','Offensive duels won score','Accelerations score','Duels won score','Interceptions score','Successful defensive actions score']]
            df_backssæsonen.rename(columns={'total_minutesOnField_x':'Total minutes'},inplace=True)
            df_backssæsonen = df_backssæsonen.groupby(['Player name','Team name','Total minutes','label']).mean(numeric_only=True)

            df_backssæsonen['Indlægsstærk'] = (df_backssæsonen['Number of crosses score'] + df_backssæsonen['Accurate crosses score'] + df_backssæsonen['XA score'] + df_backssæsonen['Passes to final third score'])/4
            df_backssæsonen['1v1 færdigheder'] = (df_backssæsonen['Successful dribbles score'] + df_backssæsonen['Defensive duels won score'] + df_backssæsonen['Progressive runs score'] + df_backssæsonen['Offensive duels won score'] + df_backssæsonen['Accelerations score'] + df_backssæsonen['Duels won score'])/6
            df_backssæsonen['Spilintelligens defensivt'] = (df_backssæsonen['Interceptions score'] + df_backssæsonen['Successful defensive actions score'] + df_backssæsonen['Duels won score'] + df_backssæsonen['Defensive duels won score'])/4
            df_backssæsonen['Fart'] = (df_backssæsonen['Successful dribbles score'] + df_backssæsonen['Progressive runs score'] + df_backssæsonen['Offensive duels won score'] + df_backssæsonen['Accelerations score'])/4
            df_backssæsonen ['Samlet'] = (df_backssæsonen['Indlægsstærk'] + df_backssæsonen['1v1 færdigheder'] + df_backssæsonen['Spilintelligens defensivt'] + df_backssæsonen['Fart'])/4
            df_backssæsonen = df_backssæsonen[['Indlægsstærk','1v1 færdigheder','Spilintelligens defensivt','Fart','Samlet']]
    #        df_backssæsonen = df_backssæsonen.sort_values(by='Samlet',ascending=False)

            df_backs['Indlægsstærk'] = (df_backs['Number of crosses score'] + df_backs['Accurate crosses score'] + df_backs['XA score'] + df_backs['Passes to final third score'])/4
            df_backs['1v1 færdigheder'] = (df_backs['Successful dribbles score'] + df_backs['Defensive duels won score'] + df_backs['Progressive runs score'] + df_backs['Offensive duels won score'] + df_backs['Accelerations score'] + df_backs['Duels won score'])/6
            df_backs['Spilintelligens defensivt'] = (df_backs['Interceptions score'] + df_backs['Successful defensive actions score'] + df_backs['Duels won score'] + df_backs['Defensive duels won score'])/4
            df_backs['Fart'] = (df_backs['Successful dribbles score'] + df_backs['Progressive runs score'] + df_backs['Offensive duels won score'] + df_backs['Accelerations score'])/4
            df_backs['Samlet'] = (df_backs['Indlægsstærk'] + df_backs['1v1 færdigheder'] + df_backs['Spilintelligens defensivt'] + df_backs['Fart'])/4

            df_backs = df_backs[['Player name','Team name','label','total_minutesOnField_y','Indlægsstærk','1v1 færdigheder','Spilintelligens defensivt','Fart','Samlet']]
    #        df_backs = df_backs.sort_values(by='Samlet',ascending=False)
            
            df_backs = navne.merge(df_backs)
            df_backs = df_backs.drop('Player Name',axis=1)
            df_backs = df_backs.drop('Player name',axis=1)    
            df_backssæsonen = df_backssæsonen.reset_index()
            df_backssæsonen = navne.merge(df_backssæsonen)
            df_backs = navne.merge(df_backs)
            df_backssæsonen = df_backssæsonen.drop('Player Name',axis=1)
            df_backssæsonen = df_backssæsonen.drop('Player name',axis=1)
            df_backssæsonen = df_backssæsonen.drop('label',axis=1)

            df_Stoppere = pd.merge(df_stoppereminutter,df_Stoppere,on=('Player id'))
            df_Stoppere = df_Stoppere[df_Stoppere['total_minutesOnField_y'] >=30]

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
            df_Stopperesæsonen = df_Stoppere.copy()
            df_Stopperesæsonen = df_Stopperesæsonen.rename(columns={'total_minutesOnField_x':'Total minutes'})
            df_Stopperesæsonen = df_Stopperesæsonen.groupby(['Player name','Team name','Total minutes','label']).mean(numeric_only=True)
            
            df_Stopperesæsonen['Pasningssikker'] = (df_Stopperesæsonen['Accurate passes score'] + df_Stopperesæsonen['Accurate long passes score'] + df_Stopperesæsonen['Forward passes score'] + df_Stopperesæsonen['Accurate forward passes score'] + df_Stopperesæsonen['Accurate progressive passes score'] + df_Stopperesæsonen['Accurate vertical passes score'])/6
            df_Stopperesæsonen['Spilintelligens defensivt'] = (df_Stopperesæsonen['Interceptions score'] + df_Stopperesæsonen['Succesful defensive actions score'] + df_Stopperesæsonen['Shots blocked score'] + df_Stopperesæsonen['Succesful defensive actions score'] + df_Stopperesæsonen['Defensive duels won % score']) /5
            df_Stopperesæsonen['Spilintelligens offensivt'] = (df_Stopperesæsonen['Forward passes score'] + df_Stopperesæsonen['Accurate forward passes score'] + df_Stopperesæsonen['Accurate passes to final third'] + df_Stopperesæsonen['Passes to final third'] + df_Stopperesæsonen['Accurate progressive passes score'] + df_Stopperesæsonen['Progressive passes score'] + df_Stopperesæsonen['Through passes'] + df_Stopperesæsonen['Accurate through passes']+ df_Stopperesæsonen['Progressive runs'] + df_Stopperesæsonen['Offensive duels won %'] + df_Stopperesæsonen['Successful dribbles %'])/11
            df_Stopperesæsonen['Nærkamps- og duelstærk'] = (df_Stopperesæsonen['Defensive duels won % score'] + df_Stopperesæsonen['Aerial duels won % score'] + df_Stopperesæsonen['Defensive duels won % score'])/3
            df_Stopperesæsonen['Samlet'] = (df_Stopperesæsonen['Pasningssikker'] + df_Stopperesæsonen['Spilintelligens defensivt'] + df_Stopperesæsonen['Spilintelligens offensivt'] + df_Stopperesæsonen['Nærkamps- og duelstærk'] + df_Stopperesæsonen['Nærkamps- og duelstærk'] + df_Stopperesæsonen['Spilintelligens defensivt'])/6

            df_Stopperesæsonen = df_Stopperesæsonen[['Pasningssikker','Spilintelligens defensivt','Spilintelligens offensivt','Nærkamps- og duelstærk','Samlet']]
    #        df_Stopperesæsonen = df_Stopperesæsonen.sort_values(by='Samlet',ascending=False)

            df_Stoppere = df_Stoppere[df_Stoppere['Team name'].str.contains('Horsens')]
            df_Stoppere['Pasningssikker'] = (df_Stoppere['Accurate passes score'] + df_Stoppere['Accurate long passes score'] + df_Stoppere['Forward passes score'] + df_Stoppere['Accurate forward passes score'] + df_Stoppere['Accurate progressive passes score'] + df_Stoppere['Accurate vertical passes score'])/6    
            df_Stoppere['Spilintelligens defensivt'] = (df_Stoppere['Interceptions score'] + df_Stoppere['Succesful defensive actions score'] + df_Stoppere['Shots blocked score'] + df_Stoppere['Succesful defensive actions score'] + df_Stoppere['Defensive duels won % score']) /5
            df_Stoppere['Spilintelligens offensivt'] = (df_Stoppere['Forward passes score'] + df_Stoppere['Accurate forward passes score'] + df_Stoppere['Accurate passes to final third'] + df_Stoppere['Passes to final third'] + df_Stoppere['Accurate progressive passes score'] + df_Stoppere['Progressive passes score'] + df_Stoppere['Through passes'] + df_Stoppere['Accurate through passes']+ df_Stoppere['Progressive runs'] + df_Stoppere['Offensive duels won %'] + df_Stoppere['Successful dribbles %'])/11
            df_Stoppere['Nærkamps- og duelstærk'] = (df_Stoppere['Defensive duels won % score'] + df_Stoppere['Aerial duels won % score'] + df_Stoppere['Defensive duels won % score'])/3
            df_Stoppere['Samlet'] = (df_Stoppere['Pasningssikker'] + df_Stoppere['Spilintelligens defensivt'] + df_Stoppere['Spilintelligens offensivt'] + df_Stoppere['Nærkamps- og duelstærk'] + df_Stoppere['Spilintelligens defensivt'] + df_Stoppere['Nærkamps- og duelstærk'])/6
            df_Stoppere = df_Stoppere[['Player name','Team name','label','total_minutesOnField_y','Pasningssikker','Spilintelligens defensivt','Spilintelligens offensivt','Nærkamps- og duelstærk','Samlet']]
    #        df_Stoppere = df_Stoppere.sort_values(by='Samlet',ascending=False)


            df_Stoppere = navne.merge(df_Stoppere)
            df_Stoppere = df_Stoppere.drop('Player Name',axis=1)
            df_Stoppere = df_Stoppere.drop('Player name',axis=1)    
            df_Stopperesæsonen = df_Stopperesæsonen.reset_index()
            df_Stopperesæsonen = navne.merge(df_Stopperesæsonen)
            df_Stoppere = navne.merge(df_Stoppere)
            df_Stopperesæsonen = df_Stopperesæsonen.drop('Player Name',axis=1)
            df_Stopperesæsonen = df_Stopperesæsonen.drop('Player name',axis=1)
            df_Stopperesæsonen = df_Stopperesæsonen.drop('label',axis=1)


            df_Centrale_midt = pd.merge(df_centraleminutter,df_Centrale_midt,on=('Player id'))
            df_Centrale_midt = df_Centrale_midt[df_Centrale_midt['total_minutesOnField_y'] >=30]

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

            df_Centrale_midtsæsonen = df_Centrale_midt.copy()
            df_Centrale_midtsæsonen = df_Centrale_midtsæsonen.rename(columns={'total_minutesOnField_x':'Total minutes'})
            df_Centrale_midtsæsonen = df_Centrale_midtsæsonen.groupby(['Player name','Team name','Total minutes','label']).mean(numeric_only=True)
            df_Centrale_midtsæsonen['Pasningssikker/Spilvendinger'] = (df_Centrale_midtsæsonen['Passes %'] + df_Centrale_midtsæsonen['Passes #'] + df_Centrale_midtsæsonen['Forward Passes %'] + df_Centrale_midtsæsonen['Forward Passes #'] + df_Centrale_midtsæsonen['Long Passes %'] + df_Centrale_midtsæsonen['Long Passes #']+ df_Centrale_midtsæsonen['Smart passes %'] + df_Centrale_midtsæsonen['Smart passes #'] + + df_Centrale_midtsæsonen['Key passes %'] + df_Centrale_midtsæsonen['Key passes #'] + df_Centrale_midtsæsonen['Passes to final third %'] + df_Centrale_midtsæsonen['Passes to final third #']+ df_Centrale_midtsæsonen['Vertical passes %'] + df_Centrale_midtsæsonen['Vertical passes #']+ df_Centrale_midtsæsonen['Through passes %'] + df_Centrale_midtsæsonen['Through passes #']+ df_Centrale_midtsæsonen['Progressive passes %'] + df_Centrale_midtsæsonen['Progressive passes #'])/18
            df_Centrale_midtsæsonen['Boldfast'] = (df_Centrale_midtsæsonen['Passes %'] + df_Centrale_midtsæsonen['Passes #']+ df_Centrale_midtsæsonen['Offensive duels %'] + df_Centrale_midtsæsonen['Received passes'] + df_Centrale_midtsæsonen['Succesful dribbles %'] + df_Centrale_midtsæsonen['Succesful dribbles #'])/6
            df_Centrale_midtsæsonen['Spilintelligens defensivt'] = (df_Centrale_midtsæsonen['Duels won %'] + df_Centrale_midtsæsonen['Duels won #'] +df_Centrale_midtsæsonen['Interceptions'] + df_Centrale_midtsæsonen['Counterpressing recoveries #'] + df_Centrale_midtsæsonen['Defensive duels won %'] + df_Centrale_midtsæsonen['Defensive duels won #'])/6
            df_Centrale_midtsæsonen['Samlet'] = (df_Centrale_midtsæsonen['Pasningssikker/Spilvendinger'] + df_Centrale_midtsæsonen['Boldfast'] + df_Centrale_midtsæsonen['Spilintelligens defensivt'])/3
            df_Centrale_midtsæsonen = df_Centrale_midtsæsonen[['Pasningssikker/Spilvendinger','Boldfast','Spilintelligens defensivt','Samlet']]
    #        df_Centrale_midtsæsonen = df_Centrale_midtsæsonen.sort_values(by='Samlet',ascending=False)

            df_Centrale_midt = df_Centrale_midt[df_Centrale_midt['Team name'].str.contains('Horsens')]
            df_Centrale_midt['Pasningssikker/Spilvendinger'] = (df_Centrale_midt['Passes %'] + df_Centrale_midt['Passes #'] + df_Centrale_midt['Forward Passes %'] + df_Centrale_midt['Forward Passes #'] + df_Centrale_midt['Long Passes %'] + df_Centrale_midt['Long Passes #']+ df_Centrale_midt['Smart passes %'] + df_Centrale_midt['Smart passes #'] + + df_Centrale_midt['Key passes %'] + df_Centrale_midt['Key passes #'] + df_Centrale_midt['Passes to final third %'] + df_Centrale_midt['Passes to final third #']+ df_Centrale_midt['Vertical passes %'] + df_Centrale_midt['Vertical passes #']+ df_Centrale_midt['Through passes %'] + df_Centrale_midt['Through passes #']+ df_Centrale_midt['Progressive passes %'] + df_Centrale_midt['Progressive passes #'])/18
            df_Centrale_midt['Boldfast'] = (df_Centrale_midt['Passes %'] + df_Centrale_midt['Passes #']+ df_Centrale_midt['Offensive duels %'] + df_Centrale_midt['Received passes'] + df_Centrale_midt['Succesful dribbles %'] + df_Centrale_midt['Succesful dribbles #'])/6
            df_Centrale_midt['Spilintelligens defensivt'] = (df_Centrale_midt['Duels won %'] + df_Centrale_midt['Duels won #'] +df_Centrale_midt['Interceptions'] + df_Centrale_midt['Counterpressing recoveries #'] + df_Centrale_midt['Defensive duels won %'] + df_Centrale_midt['Defensive duels won #'])/6
            df_Centrale_midt['Samlet'] = (df_Centrale_midt['Pasningssikker/Spilvendinger'] + df_Centrale_midt['Boldfast'] + df_Centrale_midt['Spilintelligens defensivt'])/3
            df_Centrale_midt = df_Centrale_midt[['Player name','Team name','label','total_minutesOnField_y','Pasningssikker/Spilvendinger','Boldfast','Spilintelligens defensivt','Samlet']]
    #        df_Centrale_midt = df_Centrale_midt.sort_values(by='Samlet',ascending=False)

            df_Centrale_midt = navne.merge(df_Centrale_midt)
            df_Centrale_midt = df_Centrale_midt.drop('Player Name',axis=1)
            df_Centrale_midt = df_Centrale_midt.drop('Player name',axis=1)    
            df_Centrale_midtsæsonen = df_Centrale_midtsæsonen.reset_index()
            df_Centrale_midtsæsonen = navne.merge(df_Centrale_midtsæsonen)
            df_Centrale_midt = navne.merge(df_Centrale_midt)
            df_Centrale_midtsæsonen = df_Centrale_midtsæsonen.drop('Player Name',axis=1)
            df_Centrale_midtsæsonen = df_Centrale_midtsæsonen.drop('Player name',axis=1)
            df_Centrale_midtsæsonen = df_Centrale_midtsæsonen.drop('label',axis=1)


            df_Kanter = pd.merge(df_kanterminutter,df_Kanter,on=('Player id'))
            df_Kanter = df_Kanter[df_Kanter['total_minutesOnField_y'] >=30]

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

            df_Kantersæsonen = df_Kanter.copy()
            df_Kantersæsonen = df_Kantersæsonen.rename(columns={'total_minutesOnField_x':'Total minutes'})
        
            df_Kantersæsonen = df_Kantersæsonen.groupby(['Player name','Team name','Total minutes','label']).mean(numeric_only=True)

            df_Kantersæsonen['Sparkefærdigheder'] = (df_Kantersæsonen['Shots on target %'] + df_Kantersæsonen['Shots on target #'] + df_Kantersæsonen['XG'] + df_Kantersæsonen['Passes to final third %'] + df_Kantersæsonen['Forward Passes %'] + df_Kantersæsonen['Vertical passes %'])/6
            df_Kantersæsonen['Kombinationsstærk'] = (df_Kantersæsonen['Passes %'] + df_Kantersæsonen['Passes #'] + df_Kantersæsonen['Forward Passes %'] + df_Kantersæsonen['Forward Passes #'] + df_Kantersæsonen['Passes to final third %'] + df_Kantersæsonen['Passes to final third #'] + df_Kantersæsonen['Through passes %'] + df_Kantersæsonen['Through passes #'] + df_Kantersæsonen['Progressive passes %'] + df_Kantersæsonen['Progressive passes #'] + df_Kantersæsonen['Successful attacking actions'])/11
            df_Kantersæsonen['Spilintelligens offensivt/indlægsstærk'] = (df_Kantersæsonen['XA per 90'] + df_Kantersæsonen['XG per 90'] + df_Kantersæsonen['Through passes %'] + df_Kantersæsonen['Through passes #'] + df_Kantersæsonen['Smart passes %'] + df_Kantersæsonen['Smart passes #'] + df_Kantersæsonen['Progressive passes %'] + df_Kantersæsonen['Progressive passes #'] + df_Kantersæsonen['Key passes %'] + df_Kantersæsonen['Key passes #'] + df_Kantersæsonen['Successful attacking actions'])/11
            df_Kantersæsonen['1v1 offensivt'] = (df_Kantersæsonen['Successful dribbles #'] + df_Kantersæsonen['Successful dribbles %'] + df_Kantersæsonen['Offensive duels #'] + df_Kantersæsonen['Offensive duels %'] + df_Kantersæsonen['Progressive runs'])/5
            df_Kantersæsonen['Fart'] = (df_Kantersæsonen['Progressive runs'] + df_Kantersæsonen['Successful dribbles #'] + df_Kantersæsonen['Successful dribbles %'] + df_Kantersæsonen['Accelerations score'])/4
            df_Kantersæsonen['Samlet'] = (df_Kantersæsonen['Sparkefærdigheder'] + df_Kantersæsonen['Kombinationsstærk'] + df_Kantersæsonen['Spilintelligens offensivt/indlægsstærk'] + df_Kantersæsonen['1v1 offensivt'] + df_Kantersæsonen['Fart'])/5
            df_Kantersæsonen = df_Kantersæsonen[['Sparkefærdigheder','Kombinationsstærk','Spilintelligens offensivt/indlægsstærk','1v1 offensivt','Fart','Samlet']]
    #        df_Kantersæsonen = df_Kantersæsonen.sort_values(by='Samlet',ascending=False)
            df_Kanter = df_Kanter[df_Kanter['Team name'].str.contains('Horsens')]
            df_Kanter['Sparkefærdigheder'] = (df_Kanter['Shots on target %'] + df_Kanter['Shots on target #'] + df_Kanter['XG'] + df_Kanter['Passes to final third %'] + df_Kanter['Forward Passes %'] + df_Kanter['Vertical passes %'])/6
            df_Kanter['Kombinationsstærk'] = (df_Kanter['Passes %'] + df_Kanter['Passes #'] + df_Kanter['Forward Passes %'] + df_Kanter['Forward Passes #'] + df_Kanter['Passes to final third %'] + df_Kanter['Passes to final third #'] + df_Kanter['Through passes %'] + df_Kanter['Through passes #'] + df_Kanter['Progressive passes %'] + df_Kanter['Progressive passes #'] + df_Kanter['Successful attacking actions'])/11
            df_Kanter['Spilintelligens offensivt/indlægsstærk'] = (df_Kanter['XA per 90'] + df_Kanter['XG per 90'] + df_Kanter['Through passes %'] + df_Kanter['Through passes #'] + df_Kanter['Smart passes %'] + df_Kanter['Smart passes #'] + df_Kanter['Progressive passes %'] + df_Kanter['Progressive passes #'] + df_Kanter['Key passes %'] + df_Kanter['Key passes #'] + df_Kanter['Successful attacking actions'])/11
            df_Kanter['1v1 offensivt'] = (df_Kanter['Successful dribbles #'] + df_Kanter['Successful dribbles %'] + df_Kanter['Offensive duels #'] + df_Kanter['Offensive duels %'] + df_Kanter['Progressive runs'])/5
            df_Kanter['Fart'] = (df_Kanter['Progressive runs'] + df_Kanter['Successful dribbles #'] + df_Kanter['Successful dribbles %'] + df_Kanter['Accelerations score'])/4
            df_Kanter['Samlet'] = (df_Kanter['Sparkefærdigheder'] + df_Kanter['Kombinationsstærk'] + df_Kanter['Spilintelligens offensivt/indlægsstærk'] + df_Kanter['1v1 offensivt'] + df_Kanter['Fart'])/5
            df_Kanter = df_Kanter[['Player name','Team name','label','total_minutesOnField_y','Sparkefærdigheder','Kombinationsstærk','Spilintelligens offensivt/indlægsstærk','1v1 offensivt','Fart','Samlet']]
    #        df_Kanter = df_Kanter.sort_values(by='Samlet',ascending=False)

            df_Kanter = navne.merge(df_Kanter)
            df_Kanter = df_Kanter.drop('Player Name',axis=1)
            df_Kanter = df_Kanter.drop('Player name',axis=1)    
            df_Kantersæsonen=df_Kantersæsonen.reset_index()
            df_Kantersæsonen = navne.merge(df_Kantersæsonen)
            df_Kanter = navne.merge(df_Kanter)
            df_Kantersæsonen= df_Kantersæsonen.drop('Player Name',axis=1)
            df_Kantersæsonen = df_Kantersæsonen.drop('Player name',axis=1)
            df_Kantersæsonen = df_Kantersæsonen.drop('label',axis=1)
        
            
            df_Angribere = pd.merge(df_angribereminutter,df_Angribere,on=('Player id'))
            df_Angribere = df_Angribere[df_Angribere['total_minutesOnField_y'] >=30]

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

            df_Angriberesæsonen = df_Angribere.copy()
            df_Angriberesæsonen = df_Angriberesæsonen.rename(columns={'total_minutesOnField_x':'Total minutes'})
            df_Angriberesæsonen = df_Angriberesæsonen.groupby(['Player name','Team name','Total minutes','label']).mean(numeric_only=True)

            df_Angriberesæsonen['Sparkefærdigheder'] = (df_Angriberesæsonen['xG per 90 score'] + df_Angriberesæsonen['xG per 90 score'] + df_Angriberesæsonen['Goals per 90 score'] + df_Angriberesæsonen['Shots on target, % score'])/4
            df_Angriberesæsonen['Boldfast'] = (df_Angriberesæsonen['Offensive duels won, % score'] + df_Angriberesæsonen['Offensive duels won, % score'] + df_Angriberesæsonen['Duels won, % score'] + df_Angriberesæsonen['Accurate passes, % score'] + df_Angriberesæsonen['Successful dribbles, % score'])/5
            df_Angriberesæsonen['Spilintelligens offensivt'] = (df_Angriberesæsonen['xA per 90 score'] + df_Angriberesæsonen['xG per 90 score'] + df_Angriberesæsonen['Touches in box per 90 score'] + df_Angriberesæsonen['Progressive passes per 90 score'] + df_Angriberesæsonen['Successful attacking actions per 90 score'] + df_Angriberesæsonen['Touches in box per 90 score'] + df_Angriberesæsonen['xG per 90 score'])/7
            df_Angriberesæsonen['Målfarlighed'] = (df_Angriberesæsonen['xG per 90 score']+df_Angriberesæsonen['Goals per 90 score']+df_Angriberesæsonen['xG per 90 score'] + df_Angriberesæsonen['Målfarlighed score'])/4
            df_Angriberesæsonen['Fart'] = (df_Angriberesæsonen['Progressive runs']  + df_Angriberesæsonen['Progressive runs'] + df_Angriberesæsonen['Progressive runs'] + df_Angriberesæsonen['Successful dribbles #'] + df_Angriberesæsonen['Successful dribbles, % score'] + df_Angriberesæsonen['Accelerations score'] + df_Angriberesæsonen['Offensive duels won, % score'])/7
            df_Angriberesæsonen = df_Angriberesæsonen[['Sparkefærdigheder','Boldfast','Spilintelligens offensivt','Målfarlighed','Fart']]
            df_Angriberesæsonen['Samlet'] = (df_Angriberesæsonen['Sparkefærdigheder']+df_Angriberesæsonen['Boldfast']+df_Angriberesæsonen['Spilintelligens offensivt']+df_Angriberesæsonen['Målfarlighed']+df_Angriberesæsonen['Målfarlighed']+df_Angriberesæsonen['Målfarlighed']+df_Angriberesæsonen['Fart'])/7
    #        df_Angriberesæsonen = df_Angriberesæsonen.sort_values(by='Samlet',ascending=False)

            df_Angribere = df_Angribere[df_Angribere['Team name'].str.contains('Horsens')]
            df_Angribere['Sparkefærdigheder'] = (df_Angribere['xG per 90 score'] + df_Angribere['xG per 90 score'] + df_Angribere['Goals per 90 score'] + df_Angribere['Shots on target, % score'])/4
            df_Angribere['Boldfast'] = (df_Angribere['Offensive duels won, % score'] + df_Angribere['Offensive duels won, % score'] + df_Angribere['Duels won, % score'] + df_Angribere['Accurate passes, % score'] + df_Angribere['Successful dribbles, % score'])/5
            df_Angribere['Spilintelligens offensivt'] = (df_Angribere['xA per 90 score'] + df_Angribere['xG per 90 score'] + df_Angribere['Touches in box per 90 score'] + df_Angribere['Progressive passes per 90 score'] + df_Angribere['Successful attacking actions per 90 score'] + df_Angribere['Touches in box per 90 score'] + df_Angribere['xG per 90 score'])/7
            df_Angribere['Målfarlighed'] = (df_Angribere['xG per 90 score']+df_Angribere['Goals per 90 score']+df_Angribere['xG per 90 score'] + df_Angribere['Målfarlighed score'])/4
            df_Angribere['Fart'] = (df_Angribere['Progressive runs'] + df_Angribere['Progressive runs'] + df_Angribere['Progressive runs'] + df_Angribere['Successful dribbles #'] + df_Angribere['Successful dribbles, % score'] + df_Angribere['Accelerations score'] + df_Angribere['Offensive duels won, % score'])/7
            df_Angribere = df_Angribere[['Player name','Team name','label','total_minutesOnField_y','Sparkefærdigheder','Boldfast','Spilintelligens offensivt','Målfarlighed','Fart']]
            df_Angribere['Samlet'] = (df_Angribere['Sparkefærdigheder']+df_Angribere['Boldfast']+df_Angribere['Spilintelligens offensivt']+df_Angribere['Målfarlighed']+df_Angribere['Målfarlighed']+df_Angribere['Målfarlighed']+df_Angribere['Fart'])/7
    #        df_Angribere = df_Angribere.sort_values(by='Samlet',ascending=False)
            
            kampe = df['label']
            kampe = kampe[kampe.str.contains('Horsens')]
            kampe = kampe.drop_duplicates(keep='first')  
            
            df_Angribere = navne.merge(df_Angribere)
            df_Angribere = df_Angribere.drop('Player Name',axis=1)
            df_Angribere = df_Angribere.drop('Player name',axis=1)
            df_Angriberesæsonen=df_Angriberesæsonen.reset_index()
            df_Angriberesæsonen = navne.merge(df_Angriberesæsonen)
            df_Angribere = navne.merge(df_Angribere)
            df_Angriberesæsonen= df_Angriberesæsonen.drop('Player Name',axis=1)
            df_Angriberesæsonen = df_Angriberesæsonen.drop('Player name',axis=1)
            df_Angriberesæsonen = df_Angriberesæsonen.drop('label',axis=1)
            col1, col2, col3 = st.columns(3)
            with col1:
                option2 = st.selectbox('Vælg spiller',navneliste)
                df_Angriberesæsonen = df_Angriberesæsonen[df_Angriberesæsonen['Spillere'].str.contains(option2)]
                df_Angribere = df_Angribere[df_Angribere['Spillere'].str.contains(option2)]
                df_Kantersæsonen = df_Kantersæsonen[df_Kantersæsonen['Spillere'].str.contains(option2)]
                df_Kanter = df_Kanter[df_Kanter['Spillere'].str.contains(option2)]
                df_Centrale_midtsæsonen = df_Centrale_midtsæsonen[df_Centrale_midtsæsonen['Spillere'].str.contains(option2)]
                df_Centrale_midt = df_Centrale_midt[df_Centrale_midt['Spillere'].str.contains(option2)]
                df_Stopperesæsonen = df_Stopperesæsonen[df_Stopperesæsonen['Spillere'].str.contains(option2)]
                df_Stoppere = df_Stoppere[df_Stoppere['Spillere'].str.contains(option2)]
                df_backssæsonen = df_backssæsonen[df_backssæsonen['Spillere'].str.contains(option2)]
                df_backs = df_backs[df_backs['Spillere'].str.contains(option2)]

            with col2:
                option = st.multiselect('Vælg kamp(e))',kampe)
                if len(option) > 0:
                    temp_select = option
                else:
                    temp_select = kampe
            df = pd.read_csv(r'Fysisk data/Fysiske test U17.csv')
            df['Navn'] = df['Fornavn'] + " " + df['Efternavn']
            df = df[df['Navn'] == option2]
            df['CMJ'] = df[['CMJ 1 (cm)','CMJ 2 (cm)']].max(axis=1)
            df['Sprint 5 m'] = df[['Sprint 5 m','Sprint 5 m2']].min(axis=1)
            df['Sprint 10 m'] = df[['Sprint 10 m','Sprint 10 m3']].min(axis=1)
            df['Sprint 25 m'] = df[['Sprint 25 m','Sprint 25 m4']].min(axis=1)
            df['Sprint 30 m'] = df[['Sprint 30 m','Sprint 30 m5']].min(axis=1)
            df['Topfart (km/t)'] = df[['Topfart (km/t)','Topfart (km/t)6']].max(axis=1)
            df = df[['Navn','CMJ','Sprint 5 m','Sprint 10 m','Sprint 25 m','Sprint 30 m','Topfart (km/t)']]
            st.dataframe(df,hide_index=True,use_container_width=True)
            
            df_backs = df_backs[df_backs['label'].isin(temp_select)]
            df_backstal = df_backs.copy()
            df_backstal = df_backstal.rename(columns={'total_minutesOnField_y':'Total minutes'},inplace=False)
            df_backstal = df_backstal[['Spillere','label','Total minutes','Indlægsstærk','1v1 færdigheder','Spilintelligens defensivt','Fart','Samlet']]
            df_backstal = df_backstal.set_index('Spillere')
            df_backs = df_backs.drop('label',axis=1)
            df_backssæsonen = df_backssæsonen.groupby(['Spillere','Trup','Team name','Total minutes']).mean()
            
            df_backs = df_backs.groupby(['Spillere','Trup','Team name']).agg({
            'total_minutesOnField_y':'sum',
            'Indlægsstærk':'mean',
            '1v1 færdigheder':'mean',
            'Spilintelligens defensivt':'mean',
            'Fart':'mean',
            'Samlet':'mean'
            })

            df_backs = df_backs.sort_values(by='Samlet',ascending=False)
            df_backs = df_backs.rename(columns={'total_minutesOnField_y':'Total minutes'},inplace=False)
            df_backs = df_backs.reset_index()
            df_backs = df_backs.set_index(['Spillere','Trup','Team name'])
            df_backssæsonen = df_backssæsonen.reset_index()
            df_backssæsonen = df_backssæsonen.set_index(['Spillere','Trup','Team name'])
            df_backs = pd.concat([df_backs,df_backssæsonen],axis=0)        
            df_backs = df_backs.reset_index(drop=True)
            df_backs = df_backs.set_index(['Total minutes'])
            df_backssæsonen = df_backssæsonen.reset_index(drop=True)
            df_backssæsonen = df_backssæsonen.set_index(['Total minutes'])

            
            df_Stoppere = df_Stoppere[df_Stoppere['label'].isin(temp_select)]
            df_Stopperetal = df_Stoppere.copy()
            df_Stopperetal = df_Stopperetal.rename(columns={'total_minutesOnField_y':'Total minutes'},inplace=False)
            df_Stopperetal = df_Stopperetal[['Spillere','label','Total minutes','Pasningssikker','Spilintelligens defensivt','Spilintelligens offensivt','Nærkamps- og duelstærk','Samlet']]
            df_Stopperetal = df_Stopperetal.set_index('Spillere')

            df_Stoppere = df_Stoppere.drop('label',axis=1)
            df_Stopperesæsonen = df_Stopperesæsonen.groupby(['Spillere','Trup','Team name','Total minutes']).mean()
            
            df_Stoppere = df_Stoppere.groupby(['Spillere','Trup','Team name']).agg({
            'total_minutesOnField_y':'sum',
            'Pasningssikker':'mean',
            'Spilintelligens offensivt':'mean',
            'Spilintelligens defensivt':'mean',
            'Nærkamps- og duelstærk':'mean',
            'Samlet':'mean'
            })

            df_Stoppere = df_Stoppere.sort_values(by='Samlet',ascending=False)
            df_Stoppere = df_Stoppere.rename(columns={'total_minutesOnField_y':'Total minutes'},inplace=False)
            df_Stoppere = df_Stoppere.reset_index()
            df_Stoppere = df_Stoppere.set_index(['Spillere','Trup','Team name'])
            df_Stopperesæsonen = df_Stopperesæsonen.reset_index()
            df_Stopperesæsonen = df_Stopperesæsonen.set_index(['Spillere','Trup','Team name'])
            df_Stoppere = pd.concat([df_Stoppere,df_Stopperesæsonen],axis=0)
            df_Stoppere = df_Stoppere.reset_index(drop=True)
            df_Stoppere = df_Stoppere.set_index(['Total minutes'])
            df_Stopperesæsonen = df_Stopperesæsonen.reset_index(drop=True)
            df_Stopperesæsonen = df_Stopperesæsonen.set_index(['Total minutes'])

            df_Centrale_midt = df_Centrale_midt[df_Centrale_midt['label'].isin(temp_select)]
            df_Centraletal = df_Centrale_midt.copy()
            df_Centraletal = df_Centraletal.rename(columns={'total_minutesOnField_y':'Total minutes'},inplace=False)
            df_Centraletal = df_Centraletal[['Spillere','label','Total minutes','Pasningssikker/Spilvendinger','Spilintelligens defensivt','Boldfast','Samlet']]
            df_Centraletal = df_Centraletal.set_index('Spillere')
            
            df_Centrale_midt = df_Centrale_midt.drop('label',axis=1)
            df_Centrale_midtsæsonen = df_Centrale_midtsæsonen.groupby(['Spillere','Trup','Team name','Total minutes']).mean()
            
            df_Centrale_midt = df_Centrale_midt.groupby(['Spillere','Trup','Team name']).agg({
            'total_minutesOnField_y':'sum',
            'Pasningssikker/Spilvendinger':'mean',
            'Boldfast':'mean',
            'Spilintelligens defensivt':'mean',
            'Samlet':'mean'
            })

            df_Centrale_midt = df_Centrale_midt.sort_values(by='Samlet',ascending=False)
            df_Centrale_midt = df_Centrale_midt.rename(columns={'total_minutesOnField_y':'Total minutes'},inplace=False)
            df_Centrale_midt = df_Centrale_midt.reset_index()
            df_Centrale_midt = df_Centrale_midt.set_index(['Spillere','Trup','Team name'])
            df_Centrale_midtsæsonen = df_Centrale_midtsæsonen.reset_index()
            df_Centrale_midtsæsonen = df_Centrale_midtsæsonen.set_index(['Spillere','Trup','Team name'])
            df_Centrale_midt = pd.concat([df_Centrale_midt,df_Centrale_midtsæsonen],axis=0)
            df_Centrale_midt = df_Centrale_midt.reset_index(drop=True)
            df_Centrale_midt = df_Centrale_midt.set_index(['Total minutes'])
            df_Centrale_midtsæsonen = df_Centrale_midtsæsonen.reset_index(drop=True)
            df_Centrale_midtsæsonen = df_Centrale_midtsæsonen.set_index(['Total minutes'])
        
                
            df_Kanter = df_Kanter[df_Kanter['label'].isin(temp_select)]
            df_Kantertal = df_Kanter.copy()
            df_Kantertal = df_Kantertal.rename(columns={'total_minutesOnField_y':'Total minutes'},inplace=False)
            df_Kantertal = df_Kantertal[['Spillere','label','Total minutes','Sparkefærdigheder','Kombinationsstærk','Spilintelligens offensivt/indlægsstærk','1v1 offensivt','Fart','Samlet']]
            df_Kantertal = df_Kantertal.set_index('Spillere')
            df_Kanter = df_Kanter.drop('label',axis=1)
            df_Kantersæsonen = df_Kantersæsonen.groupby(['Spillere','Trup','Team name','Total minutes']).mean()
            
            df_Kanter = df_Kanter.groupby(['Spillere','Trup','Team name']).agg({
            'total_minutesOnField_y':'sum',
            'Sparkefærdigheder':'mean',
            'Kombinationsstærk':'mean',
            'Spilintelligens offensivt/indlægsstærk':'mean',
            '1v1 offensivt':'mean',
            'Fart':'mean',
            'Samlet':'mean'
            })
            
            df_Kanter = df_Kanter.sort_values(by='Samlet',ascending=False)
            df_Kanter = df_Kanter.rename(columns={'total_minutesOnField_y':'Total minutes'},inplace=False)
            df_Kanter = df_Kanter.reset_index()
            df_Kanter = df_Kanter.set_index(['Spillere','Trup','Team name'])
            df_Kantersæsonen = df_Kantersæsonen.reset_index()
            df_Kantersæsonen = df_Kantersæsonen.set_index(['Spillere','Trup','Team name'])
            df_Kanter = pd.concat([df_Kanter,df_Kantersæsonen],axis=0)
            df_Kanter = df_Kanter.reset_index(drop=True)
            df_Kanter = df_Kanter.set_index(['Total minutes'])
            df_Kantersæsonen = df_Kantersæsonen.reset_index(drop=True)
            df_Kantersæsonen = df_Kantersæsonen.set_index(['Total minutes'])
            
            df_Angribere = df_Angribere[df_Angribere['label'].isin(temp_select)]
            df_Angriberetal = df_Angribere.copy()
            df_Angriberetal = df_Angriberetal.rename(columns={'total_minutesOnField_y':'Total minutes'},inplace=False)
            df_Angriberetal = df_Angriberetal[['Spillere','label','Total minutes','Sparkefærdigheder','Boldfast','Spilintelligens offensivt','Målfarlighed','Fart','Samlet']]
            df_Angriberetal = df_Angriberetal.set_index('Spillere')
            df_Angribere = df_Angribere.drop('label',axis=1)
            df_Angriberesæsonen = df_Angriberesæsonen.groupby(['Spillere','Trup','Team name','Total minutes']).mean()

            df_Angribere = df_Angribere.groupby(['Spillere','Trup','Team name']).agg({
            'total_minutesOnField_y':'sum',
            'Sparkefærdigheder': 'mean',
            'Boldfast': 'mean',
            'Spilintelligens offensivt':'mean',
            'Målfarlighed':'mean',
            'Fart':'mean',
            'Samlet':'mean',
            })

            df_Angribere = df_Angribere.sort_values(by = 'Samlet',ascending=False)
            df_Angribere = df_Angribere.rename(columns={'total_minutesOnField_y':'Total minutes'},inplace=False)
            df_Angribere = df_Angribere.reset_index()
            df_Angribere = df_Angribere.set_index(['Spillere','Trup','Team name'])
            df_Angriberesæsonen = df_Angriberesæsonen.reset_index()
            df_Angriberesæsonen = df_Angriberesæsonen.set_index(['Spillere','Trup','Team name'])
            df_Angribere = pd.concat([df_Angribere,df_Angriberesæsonen],axis=0)
            df_Angribere = df_Angribere.reset_index(drop=True)
            df_Angribere = df_Angribere.set_index(['Total minutes'])
            df_Angriberesæsonen = df_Angriberesæsonen.reset_index(drop=True)
            df_Angriberesæsonen = df_Angriberesæsonen.set_index(['Total minutes'])

            dataframe_names = ['Stopper', 'Back', 'Central midt', 'Kant', 'Angriber']

            # Create the selectbox in Streamlit
            with col3:
                selected_dataframe = st.selectbox('Position', options=dataframe_names)
                selected_dftal = None  # Initialize selected_dftal to None before the if-elif block

            # Based on the selected dataframe, retrieve the corresponding dataframe object
            if selected_dataframe == 'Stopper':
                selected_df = df_Stoppere
                selected_dftal = df_Stopperetal
            elif selected_dataframe == 'Back':
                selected_df = df_backs
                selected_dftal = df_backstal
            elif selected_dataframe == 'Central midt':
                selected_df = df_Centrale_midt
                selected_dftal = df_Centraletal
            elif selected_dataframe == 'Kant':
                selected_df = df_Kanter
                selected_dftal = df_Kantertal
            elif selected_dataframe == 'Angriber':
                selected_df = df_Angribere
                selected_dftal = df_Angriberetal
            with st.expander('Wyscout data'):
                st.title(option2 + ' Wyscout data')
                st.dataframe(selected_df,use_container_width=True)
                df_filtered = selected_df.copy()
                st.write('Hver parameter går fra 1-5, hvor 5 er top 20% i ligaen, 4 er top 40% osv. Hvert talent-id punkt er en udregning af flere parametre')
                # Create a scatterpolar plot using plotly
                        
                selected_dftal_columns = None
                if selected_dftal is not None:
                    selected_dftal_columns = selected_dftal.columns[2:]

                # Create two columns for displaying plots side by side
                col1, col2 = st.columns(2)

                # Plot the first plot in the first column
                with col1:
                    fig = go.Figure()
                    try:
                        for _, row in df_filtered.iterrows():
                            fig.add_trace(go.Scatterpolar(
                                r=row.values,
                                theta=df_filtered.columns,
                                fill='toself'
                            ))
                        fig.data[0].name = 'Valgte periode'
                        fig.data[1].name = 'Hele sæsonen'
                        # Set plot title and layout
                        fig.update_layout(
                            title='Talent-id plot',
                            template='plotly_dark',
                            polar=dict(
                                radialaxis=dict(
                                    visible=True,
                                    range=[1, 5],
                                    tickfont=dict(
                                        size=8  # Adjust the font size for radial axis labels
                                    ),
                                ),
                            ),
                            width=400,  # Adjust the width as needed
                            height=500,  # Adjust the height as needed
                            font=dict(
                                size=8
                            )
                        )
                        st.plotly_chart(fig)
                    except IndexError:
                        st.warning(" ")

                # Plot the second plot in the second column
                with col2:
                    if selected_dftal.empty:
                        st.warning('')
                    else:
                        fig = go.Figure()
                        try:
                            for column in selected_dftal_columns:
                                fig.add_trace(go.Scatter(
                                    x=selected_dftal['label'],
                                    y=selected_dftal[column],
                                    mode='lines',
                                    name=column
                                    ))

                                fig.update_layout(
                                    title='Talent id score over tid',
                                    template='plotly_dark',
                                    legend=dict(
                                        orientation="h",  # Set legend orientation to horizontal
                                        font=dict(
                                            size=8
                                        )
                                    ),
                                    xaxis=dict(
                                        tickangle=0,  # Adjust x-axis label rotation angle as needed
                                        tickfont=dict(
                                            size=8,  # Adjust font size for x-axis labels
                                        ),
                                    ),
                                    yaxis=dict(
                                        range=[1, 5],  # Set y-axis range to [1, 5]
                                    ),
                                    width=500,  # Adjust the width as needed
                                )

                            st.plotly_chart(fig)
                        except IndexError:
                            st.warning(" ")

            
                # Display the dataframe
                if selected_dftal is not None:
                    selected_dftal = selected_dftal.reset_index()
                    selected_dftal = selected_dftal.drop(columns=['Spillere'])
                    selected_dftal = selected_dftal.set_index('label')
                    st.dataframe(selected_dftal,use_container_width=True)
            
            try:
                with open('træningsregistrering.json', 'r') as json_file:
                    træningsdata = json.load(json_file)
                    træningsdata = pd.DataFrame(træningsdata)
            except FileNotFoundError:
                return pd.DataFrame(columns=['Tidspunkt', 'Dato','Årgang','Rådighed', 'Spillerens navn', 'Træningshold', 'Træningstype', 'Antal minutter trænet'])
            
            date_format = '%d-%m-%Y'  # Specify your date format
            træningsdata['Dato'] = pd.to_datetime(træningsdata['Dato'], format=date_format)

            min_date = træningsdata['Dato'].min()
            max_date = træningsdata['Dato'].max()

            date_range = pd.date_range(start=min_date, end=max_date, freq='D')
            date_options = date_range.strftime(date_format)  # Convert dates to the specified format

            default_end_date = date_options[-1]

            # Calculate the default start date as 14 days before the default end date
            default_start_date = pd.to_datetime(default_end_date, format=date_format) - timedelta(days=14)
            default_start_date = default_start_date.strftime(date_format)

            # Set the default start and end date values for the select_slider
            selected_start_date, selected_end_date = st.select_slider(
                'Vælg datointerval',
                options=date_options,
                value=(default_start_date, default_end_date)
            )

            selected_start_date = pd.to_datetime(selected_start_date, format=date_format)
            selected_end_date = pd.to_datetime(selected_end_date, format=date_format)
            filtered_data = træningsdata[
                (træningsdata['Dato'] >= selected_start_date) & (træningsdata['Dato'] <= selected_end_date)
            ]

            # Sort the filtered data by the 'Dato' column
#            sorted_data = filtered_data.sort_values(by ='Dato')
            sorted_data = filtered_data.copy()
            sorted_data = sorted_data[sorted_data['Spiller'] == option2]
            minutter_columns = sorted_data.filter(regex='.*minutter$').columns.tolist()
            minutter_columns_processed = [col.replace('minutter', '') for col in minutter_columns]

            minutter_df = pd.DataFrame({
                'Træningstype': minutter_columns_processed,
                'Minutter': [sorted_data[col].sum() for col in minutter_columns]
            })
            st.title(option2 + ' Træningsdata')
            minutter_df['Træningstype'] = minutter_df['Træningstype'].str.replace('minutter', '')
            col1, col2 = st.columns([3,1])

            with col2:
                træningsgruppe = sorted_data[['Træningsgruppe']].value_counts()
                træningsgruppe = træningsgruppe.rename_axis('Træningsgruppe').reset_index(name='Antal')
                #træningsgruppe = træningsgruppe.set_index('Træningsgruppe')
                #st.dataframe(træningsgruppe,use_container_width=True,hide_index=True)
                fig = go.Figure()
                fig.add_trace(go.Pie(
                    labels=træningsgruppe['Træningsgruppe'],
                    values=træningsgruppe['Antal'],
                    hole=0.0,
                ))
                fig.update_layout(title='Træningsgrupper')
                st.plotly_chart(fig)       

            with col1:
                fig = go.Figure()
                for idx, label in enumerate(minutter_df['Træningstype']):
                    fig.add_trace(go.Pie(
                        labels=minutter_df['Træningstype'],
                        values=minutter_df['Minutter'],
                    ))

                fig.update_layout(title='Træningstyper og deres tid i minutter',
                )
                st.plotly_chart(fig)

            col1,col2 = st.columns(2)


            fig = go.Figure()
            for idx, col in enumerate(minutter_columns):
                fig.add_trace(go.Bar(
                    x=sorted_data['Dato'],
                    y=sorted_data[col],
                    name=col.replace('minutter', ''),
                ))

            fig.update_layout(
                barmode='stack',
                xaxis=dict(title='Dato'),
                yaxis=dict(title='Minutter'),
                title='Træningsdata over tid'
            )

            st.plotly_chart(fig,use_container_width=True)

         
            afbud_årsag = sorted_data['Afbud årsag'].value_counts()
            afbud_årsag = afbud_årsag.rename_axis('Afbud årsag').reset_index(name='Antal')  # Renaming axis for clarity
            afbud_årsag = afbud_årsag.set_index('Afbud årsag')
            
            col1,col2,col3 = st.columns(3)    
            with col1:
                Individuel_træning_kommentar = sorted_data[['Dato', 'Individuel træning kommentar']]
                Individuel_træning_kommentar = Individuel_træning_kommentar.dropna(subset=['Individuel træning kommentar'])
                st.dataframe(Individuel_træning_kommentar.style.format({'Dato': '{:%d-%m-%Y}'}), hide_index=True,use_container_width=True)
            with col2:    
                Individuel_video_kommentar = sorted_data[['Dato', 'Individuel video kommentar']]
                Individuel_video_kommentar = Individuel_video_kommentar.dropna(subset=['Individuel video kommentar'])
                st.dataframe(Individuel_video_kommentar.style.format({'Dato': '{:%d-%m-%Y}'}), hide_index=True,use_container_width=True)
            with col3:
                st.dataframe(afbud_årsag,use_container_width=True)

            st.title(option2 + ' Kampdata')
            try:
                with open('Kampregistrering.json', 'r') as json_file:
                    Kampdata = json.load(json_file)
                    Kampdata = pd.DataFrame(Kampdata)
            except FileNotFoundError:
                return st.write('Ingen kampdata på den valgte spiller')

            date_format = '%d-%m-%Y'  # Specify your date format
            Kampdata['Dato'] = pd.to_datetime(Kampdata['Dato'], format=date_format)

            filtered_data = Kampdata[
                (Kampdata['Dato'] >= selected_start_date) & (Kampdata['Dato'] <= selected_end_date)
            ]
            sorted_data = filtered_data.sort_values(by ='Dato')
            sorted_data = sorted_data[sorted_data['Spiller'] == option2]
            
            kampminutter_spillet = sorted_data['Minutter spillet'].sum()
            kampminutter_til_rådighed = sorted_data['Minutter til rådighed'].sum()

            minutter_ude = kampminutter_til_rådighed - kampminutter_spillet
            minutter_spillet = kampminutter_spillet

            # Creating a DataFrame with the percentages
            data = {
                'Minutter spillet': [minutter_spillet],
                'Minutter ikke spillet': [minutter_ude]
            }
            kampminutter = pd.DataFrame(data, index=['Kampminutter'])
            
            Starter_inde = {
                'Starter inde' : sorted_data['Starter inde'].sum(),
                'Starter ude' : sorted_data['Starter ude'].sum()
            }
            Starter_inde = pd.DataFrame.from_dict(Starter_inde,orient='index',columns = ['Antal kampe'])
            
            Mål_assist = {
                'Mål': sorted_data['Mål'].sum(),
                'Assist': sorted_data['Assist'].sum(),
            }
            Mål_assist = pd.DataFrame.from_dict(Mål_assist, orient='index', columns=['Antal'])

            # Get unique values from the 'Spillere' column
            spillere_values = sorted_data['Spiller'].unique()

            # Filter columns containing a string from 'Spillere' column
            filtered_columns = [col for col in sorted_data.columns if any(spiller in col for spiller in spillere_values)]

            # Create a new DataFrame with the filtered columns
            filtered_data = sorted_data[filtered_columns]
            
            Kamptype = sorted_data['Kamptype'].value_counts()
            Kamptype = Kamptype.rename_axis('Kamptype').reset_index(name='Antal')  # Renaming axis for clarity
            Kamptype = Kamptype.set_index('Kamptype')

            Rådighed = sorted_data['Rådighed'].value_counts()
            Rådighed = Rådighed.rename_axis('Rådighed').reset_index(name='Antal')  # Renaming axis for clarity
            Rådighed = Rådighed.set_index('Rådighed')
            
            Modstandere = sorted_data['Modstanderhold'].value_counts()
            Modstandere = Modstandere.rename_axis('Modstander').reset_index(name='Antal')  # Renaming axis for clarity
            Modstandere = Modstandere.set_index('Modstander')
            Kampårgang = sorted_data['Kampårgang'].value_counts()
            Kampårgang = Kampårgang.rename_axis('Kampårgang').reset_index(name='Antal')  # Renaming axis for clarity
            Kampårgang = Kampårgang.set_index('Kampårgang')

            def create_pie_chart(data, title):
                fig = go.Figure(data=[go.Pie(labels=data.index, values=data['Antal'], hole=0.0)])
                fig.update_layout(title=title)
                st.plotly_chart(fig)

            
            col1,col2= st.columns([3,1])
            with col1:
                fig = go.Figure(data=[go.Pie(labels=kampminutter.columns, values=kampminutter.iloc[0], hole=0.0)])
                fig.update_layout(title='Fordeling af minutter til rådighed')
                st.plotly_chart(fig)
                create_pie_chart(Kamptype, 'Fordeling af kamptyper')
                
            with col2:
                create_pie_chart(Rådighed,'Fordeling af rådighedsstatus')
                create_pie_chart(Kampårgang, 'Fordeling af Kampårgange')
                
            col1,col2 = st.columns(2)
            with col1:
                st.dataframe(Mål_assist,use_container_width=True)
                
            with col2:
                st.dataframe(Modstandere,use_container_width=True)
                
            import gspread
            import pandas as pd
            import numpy as np

            gc = gspread.service_account('wellness-1123-178fea106d0a.json')
            sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1haWEtNQdhthKaSQjb2BRHlq2FLexicUOAHbjNFRAUAk/edit#gid=1984878556')
            ws = sh.worksheet('Samlet')
            df = pd.DataFrame(ws.get_all_records())
            
            df['Tidsstempel'] = pd.to_datetime(df['Tidsstempel'], format='%d/%m/%Y %H.%M.%S', errors='coerce').astype('datetime64[ns]')

            df['Hvilken årgang er du?'] = df['Hvilken årgang er du?'].astype(str)
            df['Hvor frisk er du?'] = df['Hvor frisk er du?'].astype(str)
            df['Hvor frisk er du?'] = df['Hvor frisk er du?'].str.extract(r'(\d+)').astype(float)
            df['Hvordan har du det mentalt'] = df['Hvordan har du det mentalt'].astype(str)
            df['Hvordan har du det mentalt'] = df['Hvordan har du det mentalt'].str.extract(r'(\d+)').astype(float)
            df['Hvordan har din søvn været?'] = df['Hvordan har din søvn været?'].astype(str)
            df['Hvordan har din søvn været?'] = df['Hvordan har din søvn været?'].str.extract(r'(\d+)').astype(float)
            df['Hvor hård var træning/kamp? (10 er hårdest)'] = df['Hvor hård var træning/kamp? (10 er hårdest)'].astype(str)
            df['Hvor hård var træning/kamp? (10 er hårdest)'] = df['Hvor hård var træning/kamp? (10 er hårdest)'].str.extract(r'(\d+)').astype(float)
            df['Hvor udmattet er du?'] = df['Hvor udmattet er du?'].astype(str)
            df['Hvor udmattet er du?'] = df['Hvor udmattet er du?'].str.extract(r'(\d+)').astype(float)
            df['Bedøm din muskelømhed'] = df['Bedøm din muskelømhed'].astype(str)
            df['Bedøm din muskelømhed'] = df['Bedøm din muskelømhed'].str.extract(r'(\d+)').astype(float)
            df['Jeg følte mig tilpas udfordret under træning/kamp'] = df['Jeg følte mig tilpas udfordret under træning/kamp'].astype(str)
            df['Jeg følte mig tilpas udfordret under træning/kamp'] = df['Jeg følte mig tilpas udfordret under træning/kamp'].str.extract(r'(\d+)').astype(float)
            df['Min tidsfornemmelse forsvandt under træning/kamp'] = df['Min tidsfornemmelse forsvandt under træning/kamp'].astype(str)
            df['Min tidsfornemmelse forsvandt under træning/kamp'] = df['Min tidsfornemmelse forsvandt under træning/kamp'].str.extract(r'(\d+)').astype(float)
            df['Jeg oplevede at tanker og handlinger var rettet mod træning/kamp'] = df['Jeg oplevede at tanker og handlinger var rettet mod træning/kamp'].astype(str)
            df['Jeg oplevede at tanker og handlinger var rettet mod træning/kamp'] = df['Jeg oplevede at tanker og handlinger var rettet mod træning/kamp'].str.extract(r'(\d+)').astype(float)
            df['Hvordan har du det mentalt?'] = df['Hvordan har du det mentalt?'].astype(str)
            df['Hvordan har du det mentalt?'] = df['Hvordan har du det mentalt?'].str.extract(r'(\d+)').astype(float)

            df.rename(columns={'Hvor mange timer sov i du i nat?':'Hvor mange timer sov du i nat?'},inplace=True)
            df = pd.melt(df,id_vars=['Tidsstempel','Spørgsmål før eller efter træning','Hvor frisk er du?','Hvordan har du det mentalt','Har du fået nok at spise inden træning/kamp?','Hvordan har din søvn været?','Hvor mange timer sov du i nat?','Træning/kamp - tid i minutter?','Hvor hård var træning/kamp? (10 er hårdest)','Hvor udmattet er du?','Bedøm din muskelømhed','Hvordan har du det mentalt?','Jeg følte mig tilpas udfordret under træning/kamp','Min tidsfornemmelse forsvandt under træning/kamp','Jeg oplevede at tanker og handlinger var rettet mod træning/kamp','Hvilken årgang er du?'],value_vars=['Spillere U13','Spillere U14','Spillere U15','Spillere U16','Spillere U17','Spillere U18','Spillere U19','Spillere U20'],value_name='Spiller')
            df = df[df['Spiller'] != '']
            df['Hvilken årgang er du?'] = df['Hvilken årgang er du?'].astype(float)
            df = df[df['Spiller']==option2]
            
            førtræning = df[['Tidsstempel','Spiller','Hvilken årgang er du?','Hvor frisk er du?','Hvordan har du det mentalt','Har du fået nok at spise inden træning/kamp?','Hvordan har din søvn været?','Hvor mange timer sov du i nat?']]
            eftertræning = df[['Tidsstempel','Spiller','Hvilken årgang er du?','Træning/kamp - tid i minutter?','Hvor hård var træning/kamp? (10 er hårdest)','Hvor udmattet er du?','Bedøm din muskelømhed','Hvordan har du det mentalt?','Jeg følte mig tilpas udfordret under træning/kamp','Min tidsfornemmelse forsvandt under træning/kamp','Jeg oplevede at tanker og handlinger var rettet mod træning/kamp']]
            førtræning.dropna(inplace=True)
            eftertræning.dropna(inplace=True)


            #eftertræning.set_index('Tidsstempel', inplace=True)
            #eftertræning.sort_index(ascending=False, inplace=True)
            #førtræning.set_index('Tidsstempel', inplace=True)
            #førtræning.sort_index(ascending=False, inplace=True)
            førtræning['Tidsstempel'] = pd.to_datetime(førtræning['Tidsstempel'])
            eftertræning['Tidsstempel'] = pd.to_datetime(eftertræning['Tidsstempel'])

            førtræning = førtræning[
            (førtræning['Tidsstempel'] >= selected_start_date) & (førtræning['Tidsstempel'] <= selected_end_date)
            ]
            eftertræning= eftertræning[
                (eftertræning['Tidsstempel'] >= selected_start_date) & (eftertræning['Tidsstempel'] <= selected_end_date)
            ]

            col1,col2 = st.columns([3,1])
            with col1:
                fig_førtræning = px.bar(førtræning, x='Tidsstempel', y=['Hvor frisk er du?', 'Hvordan har du det mentalt', 'Hvordan har din søvn været?'],barmode='group')
                fig_førtræning.update_layout(
                    title='Før træning scores over tid',
                    template='plotly_dark',
                    bargap=0.0,  # Adjust the gap between bars
                    bargroupgap=0.0,  # Adjust the gap between groups of bars
                    yaxis=dict(range=[0, 7]))
                st.plotly_chart(fig_førtræning)

            with col2:
                fig_eftertræning = px.bar(eftertræning, x='Tidsstempel', y=['Hvor udmattet er du?','Bedøm din muskelømhed','Hvordan har du det mentalt?'],barmode='group')
                fig_eftertræning.update_layout(
                    title='Efter træning scores over tid',
                    template='plotly_dark',
                    bargap=0.0,  # Adjust the gap between bars
                    bargroupgap=0.0,  # Adjust the gap between groups of bars
                    yaxis=dict(range=[0, 7]))  # Set the y-axis range
                st.plotly_chart(fig_eftertræning)
                
        def U19():
            import pandas as pd
            import streamlit as st
            import json
            from pandas import json_normalize
            import ast
            from dateutil import parser
            import plotly.graph_objects as go
            import matplotlib.pyplot as plt
            import matplotlib
            from datetime import datetime, timedelta
            import plotly.express as px
            from datetime import date
            import numpy as np
            
            navne = pd.read_excel('Navne.xlsx')
            navne = navne[navne['Trup'].str.contains('U19')]
            navneliste = navne['Spillere'].sort_values(ascending=True)
            
            df = pd.read_csv(r'Individuelt dashboard/Individuelt dashboard U19.csv')
            df.rename(columns={'playerId': 'Player id'}, inplace=True)
            df = df.astype(str)
            dfevents = pd.read_csv('U19 eventdata alle.csv',low_memory=False)
            dfevents1 = dfevents[['Player id','Player name','team_name','label','date','matchId']]
            dfspillernavn = df[['Player id','matchId','positions','average','percent','total']]
            dfspillernavn = dfspillernavn.astype(str)
            dfevents1['Player id'] = dfevents1['Player id'].astype(str)
            dfevents1['matchId'] = dfevents1['matchId'].astype(str)
            df = dfspillernavn.merge(dfevents1)

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
            df = df.sort_values('date',ascending=True)

            df_backs = df[df['position_codes'].str.contains('|'.join(['lb', 'rb']))]
            df_backs = df_backs[df_backs['total_minutesOnField'] >= 40]
            df_backsminutter = df_backs[['Player name','Team name','total_minutesOnField']]
            df_backsminutter = df_backsminutter.groupby(['Player id']).sum(numeric_only=True)
            df_backsminutter = df_backsminutter[df_backsminutter['total_minutesOnField'] >= 200]

            df_Stoppere = df[df['position_codes'].str.contains('|'.join(['cb']))]
            df_Stoppere = df_Stoppere[df_Stoppere['total_minutesOnField'] >= 40]
            df_stoppereminutter = df_Stoppere[['Player name','Team name','total_minutesOnField']]
            df_stoppereminutter = df_stoppereminutter.groupby(['Player id']).sum(numeric_only=True)
            df_stoppereminutter = df_stoppereminutter[df_stoppereminutter['total_minutesOnField'] >= 200]

            df_Centrale_midt = df[df['position_codes'].str.contains('|'.join(['cm','amf','dmf']))]
            df_Centrale_midt = df_Centrale_midt[df_Centrale_midt['total_minutesOnField'] >= 40]
            df_centraleminutter = df_Centrale_midt[['Player name','Team name','total_minutesOnField']]
            df_centraleminutter = df_centraleminutter.groupby(['Player id']).sum(numeric_only=True)
            df_centraleminutter = df_centraleminutter[df_centraleminutter['total_minutesOnField'] >= 200]

            df_Kanter = df[df['position_codes'].str.contains('|'.join(['rw','lw','ramf','lamf']))]
            df_Kanter = df_Kanter[df_Kanter['total_minutesOnField'] >=40]
            df_kanterminutter = df_Kanter[['Player name','Team name','total_minutesOnField']]
            df_kanterminutter = df_kanterminutter.groupby(['Player id']).sum(numeric_only=True)
            df_kanterminutter = df_kanterminutter[df_kanterminutter['total_minutesOnField'] >=200]


            df_Angribere = df[df['position_codes'].str.contains('|'.join(['cf','ss']))]
            df_Angribere = df_Angribere[df_Angribere['total_minutesOnField'] >= 40]
            df_angribereminutter = df_Angribere[['Player name','Team name','total_minutesOnField']]
            df_angribereminutter = df_angribereminutter.groupby(['Player id']).sum(numeric_only=True)
            df_angribereminutter = df_angribereminutter[df_angribereminutter['total_minutesOnField'] >= 200]

            df_backs = pd.merge(df_backsminutter,df_backs,on=('Player id'))
            df_backs = df_backs[df_backs['total_minutesOnField_y'] >=40]

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
            df_backssæsonen = df_backs[['Player name','Team name','label','total_minutesOnField_x','total_minutesOnField_y','Number of crosses score','Accurate crosses score','XA score','Passes to final third score','Successful dribbles score','Defensive duels won score','Progressive runs score','Offensive duels won score','Accelerations score','Duels won score','Interceptions score','Successful defensive actions score']]
            df_backssæsonen.rename(columns={'total_minutesOnField_x':'Total minutes'},inplace=True)
            df_backssæsonen = df_backssæsonen.groupby(['Player name','Team name','Total minutes','label']).mean(numeric_only=True)

            df_backssæsonen['Indlægsstærk'] = (df_backssæsonen['Number of crosses score'] + df_backssæsonen['Accurate crosses score'] + df_backssæsonen['XA score'] + df_backssæsonen['Passes to final third score'])/4
            df_backssæsonen['1v1 færdigheder'] = (df_backssæsonen['Successful dribbles score'] + df_backssæsonen['Defensive duels won score'] + df_backssæsonen['Progressive runs score'] + df_backssæsonen['Offensive duels won score'] + df_backssæsonen['Accelerations score'] + df_backssæsonen['Duels won score'])/6
            df_backssæsonen['Spilintelligens defensivt'] = (df_backssæsonen['Interceptions score'] + df_backssæsonen['Successful defensive actions score'] + df_backssæsonen['Duels won score'] + df_backssæsonen['Defensive duels won score'])/4
            df_backssæsonen['Fart'] = (df_backssæsonen['Successful dribbles score'] + df_backssæsonen['Progressive runs score'] + df_backssæsonen['Offensive duels won score'] + df_backssæsonen['Accelerations score'])/4
            df_backssæsonen ['Samlet'] = (df_backssæsonen['Indlægsstærk'] + df_backssæsonen['1v1 færdigheder'] + df_backssæsonen['Spilintelligens defensivt'] + df_backssæsonen['Fart'])/4
            df_backssæsonen = df_backssæsonen[['Indlægsstærk','1v1 færdigheder','Spilintelligens defensivt','Fart','Samlet']]
    #        df_backssæsonen = df_backssæsonen.sort_values(by='Samlet',ascending=False)

            df_backs['Indlægsstærk'] = (df_backs['Number of crosses score'] + df_backs['Accurate crosses score'] + df_backs['XA score'] + df_backs['Passes to final third score'])/4
            df_backs['1v1 færdigheder'] = (df_backs['Successful dribbles score'] + df_backs['Defensive duels won score'] + df_backs['Progressive runs score'] + df_backs['Offensive duels won score'] + df_backs['Accelerations score'] + df_backs['Duels won score'])/6
            df_backs['Spilintelligens defensivt'] = (df_backs['Interceptions score'] + df_backs['Successful defensive actions score'] + df_backs['Duels won score'] + df_backs['Defensive duels won score'])/4
            df_backs['Fart'] = (df_backs['Successful dribbles score'] + df_backs['Progressive runs score'] + df_backs['Offensive duels won score'] + df_backs['Accelerations score'])/4
            df_backs['Samlet'] = (df_backs['Indlægsstærk'] + df_backs['1v1 færdigheder'] + df_backs['Spilintelligens defensivt'] + df_backs['Fart'])/4

            df_backs = df_backs[['Player name','Team name','label','total_minutesOnField_y','Indlægsstærk','1v1 færdigheder','Spilintelligens defensivt','Fart','Samlet']]
    #        df_backs = df_backs.sort_values(by='Samlet',ascending=False)
            
            df_backs = navne.merge(df_backs)
            df_backs = df_backs.drop('Player Name',axis=1)
            df_backs = df_backs.drop('Player name',axis=1)    
            df_backssæsonen = df_backssæsonen.reset_index()
            df_backssæsonen = navne.merge(df_backssæsonen)
            df_backs = navne.merge(df_backs)
            df_backssæsonen = df_backssæsonen.drop('Player Name',axis=1)
            df_backssæsonen = df_backssæsonen.drop('Player name',axis=1)
            df_backssæsonen = df_backssæsonen.drop('label',axis=1)

            df_Stoppere = pd.merge(df_stoppereminutter,df_Stoppere,on=('Player id'))
            df_Stoppere = df_Stoppere[df_Stoppere['total_minutesOnField_y'] >=30]

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
            df_Stopperesæsonen = df_Stoppere.copy()
            df_Stopperesæsonen = df_Stopperesæsonen.rename(columns={'total_minutesOnField_x':'Total minutes'})
            df_Stopperesæsonen = df_Stopperesæsonen.groupby(['Player name','Team name','Total minutes','label']).mean(numeric_only=True)
            
            df_Stopperesæsonen['Pasningssikker'] = (df_Stopperesæsonen['Accurate passes score'] + df_Stopperesæsonen['Accurate long passes score'] + df_Stopperesæsonen['Forward passes score'] + df_Stopperesæsonen['Accurate forward passes score'] + df_Stopperesæsonen['Accurate progressive passes score'] + df_Stopperesæsonen['Accurate vertical passes score'])/6
            df_Stopperesæsonen['Spilintelligens defensivt'] = (df_Stopperesæsonen['Interceptions score'] + df_Stopperesæsonen['Succesful defensive actions score'] + df_Stopperesæsonen['Shots blocked score'] + df_Stopperesæsonen['Succesful defensive actions score'] + df_Stopperesæsonen['Defensive duels won % score']) /5
            df_Stopperesæsonen['Spilintelligens offensivt'] = (df_Stopperesæsonen['Forward passes score'] + df_Stopperesæsonen['Accurate forward passes score'] + df_Stopperesæsonen['Accurate passes to final third'] + df_Stopperesæsonen['Passes to final third'] + df_Stopperesæsonen['Accurate progressive passes score'] + df_Stopperesæsonen['Progressive passes score'] + df_Stopperesæsonen['Through passes'] + df_Stopperesæsonen['Accurate through passes']+ df_Stopperesæsonen['Progressive runs'] + df_Stopperesæsonen['Offensive duels won %'] + df_Stopperesæsonen['Successful dribbles %'])/11
            df_Stopperesæsonen['Nærkamps- og duelstærk'] = (df_Stopperesæsonen['Defensive duels won % score'] + df_Stopperesæsonen['Aerial duels won % score'] + df_Stopperesæsonen['Defensive duels won % score'])/3
            df_Stopperesæsonen['Samlet'] = (df_Stopperesæsonen['Pasningssikker'] + df_Stopperesæsonen['Spilintelligens defensivt'] + df_Stopperesæsonen['Spilintelligens offensivt'] + df_Stopperesæsonen['Nærkamps- og duelstærk'] + df_Stopperesæsonen['Nærkamps- og duelstærk'] + df_Stopperesæsonen['Spilintelligens defensivt'])/6

            df_Stopperesæsonen = df_Stopperesæsonen[['Pasningssikker','Spilintelligens defensivt','Spilintelligens offensivt','Nærkamps- og duelstærk','Samlet']]
    #        df_Stopperesæsonen = df_Stopperesæsonen.sort_values(by='Samlet',ascending=False)

            df_Stoppere = df_Stoppere[df_Stoppere['Team name'].str.contains('Horsens')]
            df_Stoppere['Pasningssikker'] = (df_Stoppere['Accurate passes score'] + df_Stoppere['Accurate long passes score'] + df_Stoppere['Forward passes score'] + df_Stoppere['Accurate forward passes score'] + df_Stoppere['Accurate progressive passes score'] + df_Stoppere['Accurate vertical passes score'])/6    
            df_Stoppere['Spilintelligens defensivt'] = (df_Stoppere['Interceptions score'] + df_Stoppere['Succesful defensive actions score'] + df_Stoppere['Shots blocked score'] + df_Stoppere['Succesful defensive actions score'] + df_Stoppere['Defensive duels won % score']) /5
            df_Stoppere['Spilintelligens offensivt'] = (df_Stoppere['Forward passes score'] + df_Stoppere['Accurate forward passes score'] + df_Stoppere['Accurate passes to final third'] + df_Stoppere['Passes to final third'] + df_Stoppere['Accurate progressive passes score'] + df_Stoppere['Progressive passes score'] + df_Stoppere['Through passes'] + df_Stoppere['Accurate through passes']+ df_Stoppere['Progressive runs'] + df_Stoppere['Offensive duels won %'] + df_Stoppere['Successful dribbles %'])/11
            df_Stoppere['Nærkamps- og duelstærk'] = (df_Stoppere['Defensive duels won % score'] + df_Stoppere['Aerial duels won % score'] + df_Stoppere['Defensive duels won % score'])/3
            df_Stoppere['Samlet'] = (df_Stoppere['Pasningssikker'] + df_Stoppere['Spilintelligens defensivt'] + df_Stoppere['Spilintelligens offensivt'] + df_Stoppere['Nærkamps- og duelstærk'] + df_Stoppere['Spilintelligens defensivt'] + df_Stoppere['Nærkamps- og duelstærk'])/6
            df_Stoppere = df_Stoppere[['Player name','Team name','label','total_minutesOnField_y','Pasningssikker','Spilintelligens defensivt','Spilintelligens offensivt','Nærkamps- og duelstærk','Samlet']]
    #        df_Stoppere = df_Stoppere.sort_values(by='Samlet',ascending=False)


            df_Stoppere = navne.merge(df_Stoppere)
            df_Stoppere = df_Stoppere.drop('Player Name',axis=1)
            df_Stoppere = df_Stoppere.drop('Player name',axis=1)    
            df_Stopperesæsonen = df_Stopperesæsonen.reset_index()
            df_Stopperesæsonen = navne.merge(df_Stopperesæsonen)
            df_Stoppere = navne.merge(df_Stoppere)
            df_Stopperesæsonen = df_Stopperesæsonen.drop('Player Name',axis=1)
            df_Stopperesæsonen = df_Stopperesæsonen.drop('Player name',axis=1)
            df_Stopperesæsonen = df_Stopperesæsonen.drop('label',axis=1)


            df_Centrale_midt = pd.merge(df_centraleminutter,df_Centrale_midt,on=('Player id'))
            df_Centrale_midt = df_Centrale_midt[df_Centrale_midt['total_minutesOnField_y'] >=30]

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

            df_Centrale_midtsæsonen = df_Centrale_midt.copy()
            df_Centrale_midtsæsonen = df_Centrale_midtsæsonen.rename(columns={'total_minutesOnField_x':'Total minutes'})
            df_Centrale_midtsæsonen = df_Centrale_midtsæsonen.groupby(['Player name','Team name','Total minutes','label']).mean(numeric_only=True)
            df_Centrale_midtsæsonen['Pasningssikker/Spilvendinger'] = (df_Centrale_midtsæsonen['Passes %'] + df_Centrale_midtsæsonen['Passes #'] + df_Centrale_midtsæsonen['Forward Passes %'] + df_Centrale_midtsæsonen['Forward Passes #'] + df_Centrale_midtsæsonen['Long Passes %'] + df_Centrale_midtsæsonen['Long Passes #']+ df_Centrale_midtsæsonen['Smart passes %'] + df_Centrale_midtsæsonen['Smart passes #'] + + df_Centrale_midtsæsonen['Key passes %'] + df_Centrale_midtsæsonen['Key passes #'] + df_Centrale_midtsæsonen['Passes to final third %'] + df_Centrale_midtsæsonen['Passes to final third #']+ df_Centrale_midtsæsonen['Vertical passes %'] + df_Centrale_midtsæsonen['Vertical passes #']+ df_Centrale_midtsæsonen['Through passes %'] + df_Centrale_midtsæsonen['Through passes #']+ df_Centrale_midtsæsonen['Progressive passes %'] + df_Centrale_midtsæsonen['Progressive passes #'])/18
            df_Centrale_midtsæsonen['Boldfast'] = (df_Centrale_midtsæsonen['Passes %'] + df_Centrale_midtsæsonen['Passes #']+ df_Centrale_midtsæsonen['Offensive duels %'] + df_Centrale_midtsæsonen['Received passes'] + df_Centrale_midtsæsonen['Succesful dribbles %'] + df_Centrale_midtsæsonen['Succesful dribbles #'])/6
            df_Centrale_midtsæsonen['Spilintelligens defensivt'] = (df_Centrale_midtsæsonen['Duels won %'] + df_Centrale_midtsæsonen['Duels won #'] +df_Centrale_midtsæsonen['Interceptions'] + df_Centrale_midtsæsonen['Counterpressing recoveries #'] + df_Centrale_midtsæsonen['Defensive duels won %'] + df_Centrale_midtsæsonen['Defensive duels won #'])/6
            df_Centrale_midtsæsonen['Samlet'] = (df_Centrale_midtsæsonen['Pasningssikker/Spilvendinger'] + df_Centrale_midtsæsonen['Boldfast'] + df_Centrale_midtsæsonen['Spilintelligens defensivt'])/3
            df_Centrale_midtsæsonen = df_Centrale_midtsæsonen[['Pasningssikker/Spilvendinger','Boldfast','Spilintelligens defensivt','Samlet']]
    #        df_Centrale_midtsæsonen = df_Centrale_midtsæsonen.sort_values(by='Samlet',ascending=False)

            df_Centrale_midt = df_Centrale_midt[df_Centrale_midt['Team name'].str.contains('Horsens')]
            df_Centrale_midt['Pasningssikker/Spilvendinger'] = (df_Centrale_midt['Passes %'] + df_Centrale_midt['Passes #'] + df_Centrale_midt['Forward Passes %'] + df_Centrale_midt['Forward Passes #'] + df_Centrale_midt['Long Passes %'] + df_Centrale_midt['Long Passes #']+ df_Centrale_midt['Smart passes %'] + df_Centrale_midt['Smart passes #'] + + df_Centrale_midt['Key passes %'] + df_Centrale_midt['Key passes #'] + df_Centrale_midt['Passes to final third %'] + df_Centrale_midt['Passes to final third #']+ df_Centrale_midt['Vertical passes %'] + df_Centrale_midt['Vertical passes #']+ df_Centrale_midt['Through passes %'] + df_Centrale_midt['Through passes #']+ df_Centrale_midt['Progressive passes %'] + df_Centrale_midt['Progressive passes #'])/18
            df_Centrale_midt['Boldfast'] = (df_Centrale_midt['Passes %'] + df_Centrale_midt['Passes #']+ df_Centrale_midt['Offensive duels %'] + df_Centrale_midt['Received passes'] + df_Centrale_midt['Succesful dribbles %'] + df_Centrale_midt['Succesful dribbles #'])/6
            df_Centrale_midt['Spilintelligens defensivt'] = (df_Centrale_midt['Duels won %'] + df_Centrale_midt['Duels won #'] +df_Centrale_midt['Interceptions'] + df_Centrale_midt['Counterpressing recoveries #'] + df_Centrale_midt['Defensive duels won %'] + df_Centrale_midt['Defensive duels won #'])/6
            df_Centrale_midt['Samlet'] = (df_Centrale_midt['Pasningssikker/Spilvendinger'] + df_Centrale_midt['Boldfast'] + df_Centrale_midt['Spilintelligens defensivt'])/3
            df_Centrale_midt = df_Centrale_midt[['Player name','Team name','label','total_minutesOnField_y','Pasningssikker/Spilvendinger','Boldfast','Spilintelligens defensivt','Samlet']]
    #        df_Centrale_midt = df_Centrale_midt.sort_values(by='Samlet',ascending=False)

            df_Centrale_midt = navne.merge(df_Centrale_midt)
            df_Centrale_midt = df_Centrale_midt.drop('Player Name',axis=1)
            df_Centrale_midt = df_Centrale_midt.drop('Player name',axis=1)    
            df_Centrale_midtsæsonen = df_Centrale_midtsæsonen.reset_index()
            df_Centrale_midtsæsonen = navne.merge(df_Centrale_midtsæsonen)
            df_Centrale_midt = navne.merge(df_Centrale_midt)
            df_Centrale_midtsæsonen = df_Centrale_midtsæsonen.drop('Player Name',axis=1)
            df_Centrale_midtsæsonen = df_Centrale_midtsæsonen.drop('Player name',axis=1)
            df_Centrale_midtsæsonen = df_Centrale_midtsæsonen.drop('label',axis=1)


            df_Kanter = pd.merge(df_kanterminutter,df_Kanter,on=('Player id'))
            df_Kanter = df_Kanter[df_Kanter['total_minutesOnField_y'] >=30]

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

            df_Kantersæsonen = df_Kanter.copy()
            df_Kantersæsonen = df_Kantersæsonen.rename(columns={'total_minutesOnField_x':'Total minutes'})
        
            df_Kantersæsonen = df_Kantersæsonen.groupby(['Player name','Team name','Total minutes','label']).mean(numeric_only=True)

            df_Kantersæsonen['Sparkefærdigheder'] = (df_Kantersæsonen['Shots on target %'] + df_Kantersæsonen['Shots on target #'] + df_Kantersæsonen['XG'] + df_Kantersæsonen['Passes to final third %'] + df_Kantersæsonen['Forward Passes %'] + df_Kantersæsonen['Vertical passes %'])/6
            df_Kantersæsonen['Kombinationsstærk'] = (df_Kantersæsonen['Passes %'] + df_Kantersæsonen['Passes #'] + df_Kantersæsonen['Forward Passes %'] + df_Kantersæsonen['Forward Passes #'] + df_Kantersæsonen['Passes to final third %'] + df_Kantersæsonen['Passes to final third #'] + df_Kantersæsonen['Through passes %'] + df_Kantersæsonen['Through passes #'] + df_Kantersæsonen['Progressive passes %'] + df_Kantersæsonen['Progressive passes #'] + df_Kantersæsonen['Successful attacking actions'])/11
            df_Kantersæsonen['Spilintelligens offensivt/indlægsstærk'] = (df_Kantersæsonen['XA per 90'] + df_Kantersæsonen['XG per 90'] + df_Kantersæsonen['Through passes %'] + df_Kantersæsonen['Through passes #'] + df_Kantersæsonen['Smart passes %'] + df_Kantersæsonen['Smart passes #'] + df_Kantersæsonen['Progressive passes %'] + df_Kantersæsonen['Progressive passes #'] + df_Kantersæsonen['Key passes %'] + df_Kantersæsonen['Key passes #'] + df_Kantersæsonen['Successful attacking actions'])/11
            df_Kantersæsonen['1v1 offensivt'] = (df_Kantersæsonen['Successful dribbles #'] + df_Kantersæsonen['Successful dribbles %'] + df_Kantersæsonen['Offensive duels #'] + df_Kantersæsonen['Offensive duels %'] + df_Kantersæsonen['Progressive runs'])/5
            df_Kantersæsonen['Fart'] = (df_Kantersæsonen['Progressive runs'] + df_Kantersæsonen['Successful dribbles #'] + df_Kantersæsonen['Successful dribbles %'] + df_Kantersæsonen['Accelerations score'])/4
            df_Kantersæsonen['Samlet'] = (df_Kantersæsonen['Sparkefærdigheder'] + df_Kantersæsonen['Kombinationsstærk'] + df_Kantersæsonen['Spilintelligens offensivt/indlægsstærk'] + df_Kantersæsonen['1v1 offensivt'] + df_Kantersæsonen['Fart'])/5
            df_Kantersæsonen = df_Kantersæsonen[['Sparkefærdigheder','Kombinationsstærk','Spilintelligens offensivt/indlægsstærk','1v1 offensivt','Fart','Samlet']]
    #        df_Kantersæsonen = df_Kantersæsonen.sort_values(by='Samlet',ascending=False)
            df_Kanter = df_Kanter[df_Kanter['Team name'].str.contains('Horsens')]
            df_Kanter['Sparkefærdigheder'] = (df_Kanter['Shots on target %'] + df_Kanter['Shots on target #'] + df_Kanter['XG'] + df_Kanter['Passes to final third %'] + df_Kanter['Forward Passes %'] + df_Kanter['Vertical passes %'])/6
            df_Kanter['Kombinationsstærk'] = (df_Kanter['Passes %'] + df_Kanter['Passes #'] + df_Kanter['Forward Passes %'] + df_Kanter['Forward Passes #'] + df_Kanter['Passes to final third %'] + df_Kanter['Passes to final third #'] + df_Kanter['Through passes %'] + df_Kanter['Through passes #'] + df_Kanter['Progressive passes %'] + df_Kanter['Progressive passes #'] + df_Kanter['Successful attacking actions'])/11
            df_Kanter['Spilintelligens offensivt/indlægsstærk'] = (df_Kanter['XA per 90'] + df_Kanter['XG per 90'] + df_Kanter['Through passes %'] + df_Kanter['Through passes #'] + df_Kanter['Smart passes %'] + df_Kanter['Smart passes #'] + df_Kanter['Progressive passes %'] + df_Kanter['Progressive passes #'] + df_Kanter['Key passes %'] + df_Kanter['Key passes #'] + df_Kanter['Successful attacking actions'])/11
            df_Kanter['1v1 offensivt'] = (df_Kanter['Successful dribbles #'] + df_Kanter['Successful dribbles %'] + df_Kanter['Offensive duels #'] + df_Kanter['Offensive duels %'] + df_Kanter['Progressive runs'])/5
            df_Kanter['Fart'] = (df_Kanter['Progressive runs'] + df_Kanter['Successful dribbles #'] + df_Kanter['Successful dribbles %'] + df_Kanter['Accelerations score'])/4
            df_Kanter['Samlet'] = (df_Kanter['Sparkefærdigheder'] + df_Kanter['Kombinationsstærk'] + df_Kanter['Spilintelligens offensivt/indlægsstærk'] + df_Kanter['1v1 offensivt'] + df_Kanter['Fart'])/5
            df_Kanter = df_Kanter[['Player name','Team name','label','total_minutesOnField_y','Sparkefærdigheder','Kombinationsstærk','Spilintelligens offensivt/indlægsstærk','1v1 offensivt','Fart','Samlet']]
    #        df_Kanter = df_Kanter.sort_values(by='Samlet',ascending=False)

            df_Kanter = navne.merge(df_Kanter)
            df_Kanter = df_Kanter.drop('Player Name',axis=1)
            df_Kanter = df_Kanter.drop('Player name',axis=1)    
            df_Kantersæsonen=df_Kantersæsonen.reset_index()
            df_Kantersæsonen = navne.merge(df_Kantersæsonen)
            df_Kanter = navne.merge(df_Kanter)
            df_Kantersæsonen= df_Kantersæsonen.drop('Player Name',axis=1)
            df_Kantersæsonen = df_Kantersæsonen.drop('Player name',axis=1)
            df_Kantersæsonen = df_Kantersæsonen.drop('label',axis=1)
        
            
            df_Angribere = pd.merge(df_angribereminutter,df_Angribere,on=('Player id'))
            df_Angribere = df_Angribere[df_Angribere['total_minutesOnField_y'] >=30]

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

            df_Angriberesæsonen = df_Angribere.copy()
            df_Angriberesæsonen = df_Angriberesæsonen.rename(columns={'total_minutesOnField_x':'Total minutes'})
            df_Angriberesæsonen = df_Angriberesæsonen.groupby(['Player name','Team name','Total minutes','label']).mean(numeric_only=True)

            df_Angriberesæsonen['Sparkefærdigheder'] = (df_Angriberesæsonen['xG per 90 score'] + df_Angriberesæsonen['xG per 90 score'] + df_Angriberesæsonen['Goals per 90 score'] + df_Angriberesæsonen['Shots on target, % score'])/4
            df_Angriberesæsonen['Boldfast'] = (df_Angriberesæsonen['Offensive duels won, % score'] + df_Angriberesæsonen['Offensive duels won, % score'] + df_Angriberesæsonen['Duels won, % score'] + df_Angriberesæsonen['Accurate passes, % score'] + df_Angriberesæsonen['Successful dribbles, % score'])/5
            df_Angriberesæsonen['Spilintelligens offensivt'] = (df_Angriberesæsonen['xA per 90 score'] + df_Angriberesæsonen['xG per 90 score'] + df_Angriberesæsonen['Touches in box per 90 score'] + df_Angriberesæsonen['Progressive passes per 90 score'] + df_Angriberesæsonen['Successful attacking actions per 90 score'] + df_Angriberesæsonen['Touches in box per 90 score'] + df_Angriberesæsonen['xG per 90 score'])/7
            df_Angriberesæsonen['Målfarlighed'] = (df_Angriberesæsonen['xG per 90 score']+df_Angriberesæsonen['Goals per 90 score']+df_Angriberesæsonen['xG per 90 score'] + df_Angriberesæsonen['Målfarlighed score'])/4
            df_Angriberesæsonen['Fart'] = (df_Angriberesæsonen['Progressive runs']  + df_Angriberesæsonen['Progressive runs'] + df_Angriberesæsonen['Progressive runs'] + df_Angriberesæsonen['Successful dribbles #'] + df_Angriberesæsonen['Successful dribbles, % score'] + df_Angriberesæsonen['Accelerations score'] + df_Angriberesæsonen['Offensive duels won, % score'])/7
            df_Angriberesæsonen = df_Angriberesæsonen[['Sparkefærdigheder','Boldfast','Spilintelligens offensivt','Målfarlighed','Fart']]
            df_Angriberesæsonen['Samlet'] = (df_Angriberesæsonen['Sparkefærdigheder']+df_Angriberesæsonen['Boldfast']+df_Angriberesæsonen['Spilintelligens offensivt']+df_Angriberesæsonen['Målfarlighed']+df_Angriberesæsonen['Målfarlighed']+df_Angriberesæsonen['Målfarlighed']+df_Angriberesæsonen['Fart'])/7
    #        df_Angriberesæsonen = df_Angriberesæsonen.sort_values(by='Samlet',ascending=False)

            df_Angribere = df_Angribere[df_Angribere['Team name'].str.contains('Horsens')]
            df_Angribere['Sparkefærdigheder'] = (df_Angribere['xG per 90 score'] + df_Angribere['xG per 90 score'] + df_Angribere['Goals per 90 score'] + df_Angribere['Shots on target, % score'])/4
            df_Angribere['Boldfast'] = (df_Angribere['Offensive duels won, % score'] + df_Angribere['Offensive duels won, % score'] + df_Angribere['Duels won, % score'] + df_Angribere['Accurate passes, % score'] + df_Angribere['Successful dribbles, % score'])/5
            df_Angribere['Spilintelligens offensivt'] = (df_Angribere['xA per 90 score'] + df_Angribere['xG per 90 score'] + df_Angribere['Touches in box per 90 score'] + df_Angribere['Progressive passes per 90 score'] + df_Angribere['Successful attacking actions per 90 score'] + df_Angribere['Touches in box per 90 score'] + df_Angribere['xG per 90 score'])/7
            df_Angribere['Målfarlighed'] = (df_Angribere['xG per 90 score']+df_Angribere['Goals per 90 score']+df_Angribere['xG per 90 score'] + df_Angribere['Målfarlighed score'])/4
            df_Angribere['Fart'] = (df_Angribere['Progressive runs'] + df_Angribere['Progressive runs'] + df_Angribere['Progressive runs'] + df_Angribere['Successful dribbles #'] + df_Angribere['Successful dribbles, % score'] + df_Angribere['Accelerations score'] + df_Angribere['Offensive duels won, % score'])/7
            df_Angribere = df_Angribere[['Player name','Team name','label','total_minutesOnField_y','Sparkefærdigheder','Boldfast','Spilintelligens offensivt','Målfarlighed','Fart']]
            df_Angribere['Samlet'] = (df_Angribere['Sparkefærdigheder']+df_Angribere['Boldfast']+df_Angribere['Spilintelligens offensivt']+df_Angribere['Målfarlighed']+df_Angribere['Målfarlighed']+df_Angribere['Målfarlighed']+df_Angribere['Fart'])/7
    #        df_Angribere = df_Angribere.sort_values(by='Samlet',ascending=False)
            
            kampe = df['label']
            kampe = kampe[kampe.str.contains('Horsens')]
            kampe = kampe.drop_duplicates(keep='first')  
            
            df_Angribere = navne.merge(df_Angribere)
            df_Angribere = df_Angribere.drop('Player Name',axis=1)
            df_Angribere = df_Angribere.drop('Player name',axis=1)
            df_Angriberesæsonen=df_Angriberesæsonen.reset_index()
            df_Angriberesæsonen = navne.merge(df_Angriberesæsonen)
            df_Angribere = navne.merge(df_Angribere)
            df_Angriberesæsonen= df_Angriberesæsonen.drop('Player Name',axis=1)
            df_Angriberesæsonen = df_Angriberesæsonen.drop('Player name',axis=1)
            df_Angriberesæsonen = df_Angriberesæsonen.drop('label',axis=1)
            col1, col2, col3 = st.columns(3)
            with col1:
                option2 = st.selectbox('Vælg spiller',navneliste)
                df_Angriberesæsonen = df_Angriberesæsonen[df_Angriberesæsonen['Spillere'].str.contains(option2)]
                df_Angribere = df_Angribere[df_Angribere['Spillere'].str.contains(option2)]
                df_Kantersæsonen = df_Kantersæsonen[df_Kantersæsonen['Spillere'].str.contains(option2)]
                df_Kanter = df_Kanter[df_Kanter['Spillere'].str.contains(option2)]
                df_Centrale_midtsæsonen = df_Centrale_midtsæsonen[df_Centrale_midtsæsonen['Spillere'].str.contains(option2)]
                df_Centrale_midt = df_Centrale_midt[df_Centrale_midt['Spillere'].str.contains(option2)]
                df_Stopperesæsonen = df_Stopperesæsonen[df_Stopperesæsonen['Spillere'].str.contains(option2)]
                df_Stoppere = df_Stoppere[df_Stoppere['Spillere'].str.contains(option2)]
                df_backssæsonen = df_backssæsonen[df_backssæsonen['Spillere'].str.contains(option2)]
                df_backs = df_backs[df_backs['Spillere'].str.contains(option2)]

            with col2:
                option = st.multiselect('Vælg kamp(e))',kampe)
                if len(option) > 0:
                    temp_select = option
                else:
                    temp_select = kampe
            df = pd.read_csv(r'Fysisk data/Fysiske test U19.csv')
            df['Navn'] = df['Fornavn'] + " " + df['Efternavn']
            df = df[df['Navn'] == option2]
            df['CMJ'] = df[['CMJ 1 (cm)','CMJ 2 (cm)']].max(axis=1)
            df['Sprint 5 m'] = df[['Sprint 5 m','Sprint 5 m2']].min(axis=1)
            df['Sprint 10 m'] = df[['Sprint 10 m','Sprint 10 m3']].min(axis=1)
            df['Sprint 25 m'] = df[['Sprint 25 m','Sprint 25 m4']].min(axis=1)
            df['Sprint 30 m'] = df[['Sprint 30 m','Sprint 30 m5']].min(axis=1)
            df['Topfart (km/t)'] = df[['Topfart (km/t)','Topfart (km/t)6']].max(axis=1)
            df = df[['Navn','CMJ','Sprint 5 m','Sprint 10 m','Sprint 25 m','Sprint 30 m','Topfart (km/t)']]
            st.dataframe(df,hide_index=True,use_container_width=True)
            
            df_backs = df_backs[df_backs['label'].isin(temp_select)]
            df_backstal = df_backs.copy()
            df_backstal = df_backstal.rename(columns={'total_minutesOnField_y':'Total minutes'},inplace=False)
            df_backstal = df_backstal[['Spillere','label','Total minutes','Indlægsstærk','1v1 færdigheder','Spilintelligens defensivt','Fart','Samlet']]
            df_backstal = df_backstal.set_index('Spillere')
            df_backs = df_backs.drop('label',axis=1)
            df_backssæsonen = df_backssæsonen.groupby(['Spillere','Trup','Team name','Total minutes']).mean()
            
            df_backs = df_backs.groupby(['Spillere','Trup','Team name']).agg({
            'total_minutesOnField_y':'sum',
            'Indlægsstærk':'mean',
            '1v1 færdigheder':'mean',
            'Spilintelligens defensivt':'mean',
            'Fart':'mean',
            'Samlet':'mean'
            })

            df_backs = df_backs.sort_values(by='Samlet',ascending=False)
            df_backs = df_backs.rename(columns={'total_minutesOnField_y':'Total minutes'},inplace=False)
            df_backs = df_backs.reset_index()
            df_backs = df_backs.set_index(['Spillere','Trup','Team name'])
            df_backssæsonen = df_backssæsonen.reset_index()
            df_backssæsonen = df_backssæsonen.set_index(['Spillere','Trup','Team name'])
            df_backs = pd.concat([df_backs,df_backssæsonen],axis=0)        
            df_backs = df_backs.reset_index(drop=True)
            df_backs = df_backs.set_index(['Total minutes'])
            df_backssæsonen = df_backssæsonen.reset_index(drop=True)
            df_backssæsonen = df_backssæsonen.set_index(['Total minutes'])

            
            df_Stoppere = df_Stoppere[df_Stoppere['label'].isin(temp_select)]
            df_Stopperetal = df_Stoppere.copy()
            df_Stopperetal = df_Stopperetal.rename(columns={'total_minutesOnField_y':'Total minutes'},inplace=False)
            df_Stopperetal = df_Stopperetal[['Spillere','label','Total minutes','Pasningssikker','Spilintelligens defensivt','Spilintelligens offensivt','Nærkamps- og duelstærk','Samlet']]
            df_Stopperetal = df_Stopperetal.set_index('Spillere')

            df_Stoppere = df_Stoppere.drop('label',axis=1)
            df_Stopperesæsonen = df_Stopperesæsonen.groupby(['Spillere','Trup','Team name','Total minutes']).mean()
            
            df_Stoppere = df_Stoppere.groupby(['Spillere','Trup','Team name']).agg({
            'total_minutesOnField_y':'sum',
            'Pasningssikker':'mean',
            'Spilintelligens offensivt':'mean',
            'Spilintelligens defensivt':'mean',
            'Nærkamps- og duelstærk':'mean',
            'Samlet':'mean'
            })

            df_Stoppere = df_Stoppere.sort_values(by='Samlet',ascending=False)
            df_Stoppere = df_Stoppere.rename(columns={'total_minutesOnField_y':'Total minutes'},inplace=False)
            df_Stoppere = df_Stoppere.reset_index()
            df_Stoppere = df_Stoppere.set_index(['Spillere','Trup','Team name'])
            df_Stopperesæsonen = df_Stopperesæsonen.reset_index()
            df_Stopperesæsonen = df_Stopperesæsonen.set_index(['Spillere','Trup','Team name'])
            df_Stoppere = pd.concat([df_Stoppere,df_Stopperesæsonen],axis=0)
            df_Stoppere = df_Stoppere.reset_index(drop=True)
            df_Stoppere = df_Stoppere.set_index(['Total minutes'])
            df_Stopperesæsonen = df_Stopperesæsonen.reset_index(drop=True)
            df_Stopperesæsonen = df_Stopperesæsonen.set_index(['Total minutes'])

            df_Centrale_midt = df_Centrale_midt[df_Centrale_midt['label'].isin(temp_select)]
            df_Centraletal = df_Centrale_midt.copy()
            df_Centraletal = df_Centraletal.rename(columns={'total_minutesOnField_y':'Total minutes'},inplace=False)
            df_Centraletal = df_Centraletal[['Spillere','label','Total minutes','Pasningssikker/Spilvendinger','Spilintelligens defensivt','Boldfast','Samlet']]
            df_Centraletal = df_Centraletal.set_index('Spillere')
            
            df_Centrale_midt = df_Centrale_midt.drop('label',axis=1)
            df_Centrale_midtsæsonen = df_Centrale_midtsæsonen.groupby(['Spillere','Trup','Team name','Total minutes']).mean()
            
            df_Centrale_midt = df_Centrale_midt.groupby(['Spillere','Trup','Team name']).agg({
            'total_minutesOnField_y':'sum',
            'Pasningssikker/Spilvendinger':'mean',
            'Boldfast':'mean',
            'Spilintelligens defensivt':'mean',
            'Samlet':'mean'
            })

            df_Centrale_midt = df_Centrale_midt.sort_values(by='Samlet',ascending=False)
            df_Centrale_midt = df_Centrale_midt.rename(columns={'total_minutesOnField_y':'Total minutes'},inplace=False)
            df_Centrale_midt = df_Centrale_midt.reset_index()
            df_Centrale_midt = df_Centrale_midt.set_index(['Spillere','Trup','Team name'])
            df_Centrale_midtsæsonen = df_Centrale_midtsæsonen.reset_index()
            df_Centrale_midtsæsonen = df_Centrale_midtsæsonen.set_index(['Spillere','Trup','Team name'])
            df_Centrale_midt = pd.concat([df_Centrale_midt,df_Centrale_midtsæsonen],axis=0)
            df_Centrale_midt = df_Centrale_midt.reset_index(drop=True)
            df_Centrale_midt = df_Centrale_midt.set_index(['Total minutes'])
            df_Centrale_midtsæsonen = df_Centrale_midtsæsonen.reset_index(drop=True)
            df_Centrale_midtsæsonen = df_Centrale_midtsæsonen.set_index(['Total minutes'])
        
                
            df_Kanter = df_Kanter[df_Kanter['label'].isin(temp_select)]
            df_Kantertal = df_Kanter.copy()
            df_Kantertal = df_Kantertal.rename(columns={'total_minutesOnField_y':'Total minutes'},inplace=False)
            df_Kantertal = df_Kantertal[['Spillere','label','Total minutes','Sparkefærdigheder','Kombinationsstærk','Spilintelligens offensivt/indlægsstærk','1v1 offensivt','Fart','Samlet']]
            df_Kantertal = df_Kantertal.set_index('Spillere')
            df_Kanter = df_Kanter.drop('label',axis=1)
            df_Kantersæsonen = df_Kantersæsonen.groupby(['Spillere','Trup','Team name','Total minutes']).mean()
            
            df_Kanter = df_Kanter.groupby(['Spillere','Trup','Team name']).agg({
            'total_minutesOnField_y':'sum',
            'Sparkefærdigheder':'mean',
            'Kombinationsstærk':'mean',
            'Spilintelligens offensivt/indlægsstærk':'mean',
            '1v1 offensivt':'mean',
            'Fart':'mean',
            'Samlet':'mean'
            })
            
            df_Kanter = df_Kanter.sort_values(by='Samlet',ascending=False)
            df_Kanter = df_Kanter.rename(columns={'total_minutesOnField_y':'Total minutes'},inplace=False)
            df_Kanter = df_Kanter.reset_index()
            df_Kanter = df_Kanter.set_index(['Spillere','Trup','Team name'])
            df_Kantersæsonen = df_Kantersæsonen.reset_index()
            df_Kantersæsonen = df_Kantersæsonen.set_index(['Spillere','Trup','Team name'])
            df_Kanter = pd.concat([df_Kanter,df_Kantersæsonen],axis=0)
            df_Kanter = df_Kanter.reset_index(drop=True)
            df_Kanter = df_Kanter.set_index(['Total minutes'])
            df_Kantersæsonen = df_Kantersæsonen.reset_index(drop=True)
            df_Kantersæsonen = df_Kantersæsonen.set_index(['Total minutes'])
            
            df_Angribere = df_Angribere[df_Angribere['label'].isin(temp_select)]
            df_Angriberetal = df_Angribere.copy()
            df_Angriberetal = df_Angriberetal.rename(columns={'total_minutesOnField_y':'Total minutes'},inplace=False)
            df_Angriberetal = df_Angriberetal[['Spillere','label','Total minutes','Sparkefærdigheder','Boldfast','Spilintelligens offensivt','Målfarlighed','Fart','Samlet']]
            df_Angriberetal = df_Angriberetal.set_index('Spillere')
            df_Angribere = df_Angribere.drop('label',axis=1)
            df_Angriberesæsonen = df_Angriberesæsonen.groupby(['Spillere','Trup','Team name','Total minutes']).mean()

            df_Angribere = df_Angribere.groupby(['Spillere','Trup','Team name']).agg({
            'total_minutesOnField_y':'sum',
            'Sparkefærdigheder': 'mean',
            'Boldfast': 'mean',
            'Spilintelligens offensivt':'mean',
            'Målfarlighed':'mean',
            'Fart':'mean',
            'Samlet':'mean',
            })

            df_Angribere = df_Angribere.sort_values(by = 'Samlet',ascending=False)
            df_Angribere = df_Angribere.rename(columns={'total_minutesOnField_y':'Total minutes'},inplace=False)
            df_Angribere = df_Angribere.reset_index()
            df_Angribere = df_Angribere.set_index(['Spillere','Trup','Team name'])
            df_Angriberesæsonen = df_Angriberesæsonen.reset_index()
            df_Angriberesæsonen = df_Angriberesæsonen.set_index(['Spillere','Trup','Team name'])
            df_Angribere = pd.concat([df_Angribere,df_Angriberesæsonen],axis=0)
            df_Angribere = df_Angribere.reset_index(drop=True)
            df_Angribere = df_Angribere.set_index(['Total minutes'])
            df_Angriberesæsonen = df_Angriberesæsonen.reset_index(drop=True)
            df_Angriberesæsonen = df_Angriberesæsonen.set_index(['Total minutes'])

            dataframe_names = ['Stopper', 'Back', 'Central midt', 'Kant', 'Angriber']

            # Create the selectbox in Streamlit
            with col3:
                selected_dataframe = st.selectbox('Position', options=dataframe_names)
                selected_dftal = None  # Initialize selected_dftal to None before the if-elif block

            # Based on the selected dataframe, retrieve the corresponding dataframe object
            if selected_dataframe == 'Stopper':
                selected_df = df_Stoppere
                selected_dftal = df_Stopperetal
            elif selected_dataframe == 'Back':
                selected_df = df_backs
                selected_dftal = df_backstal
            elif selected_dataframe == 'Central midt':
                selected_df = df_Centrale_midt
                selected_dftal = df_Centraletal
            elif selected_dataframe == 'Kant':
                selected_df = df_Kanter
                selected_dftal = df_Kantertal
            elif selected_dataframe == 'Angriber':
                selected_df = df_Angribere
                selected_dftal = df_Angriberetal
            with st.expander('Wyscout data'):
                st.title(option2 + ' Wyscout data')
                st.dataframe(selected_df,use_container_width=True)
                df_filtered = selected_df.copy()
                st.write('Hver parameter går fra 1-5, hvor 5 er top 20% i ligaen, 4 er top 40% osv. Hvert talent-id punkt er en udregning af flere parametre')
                # Create a scatterpolar plot using plotly
                        
                selected_dftal_columns = None
                if selected_dftal is not None:
                    selected_dftal_columns = selected_dftal.columns[2:]

                # Create two columns for displaying plots side by side
                col1, col2 = st.columns(2)

                # Plot the first plot in the first column
                with col1:
                    fig = go.Figure()
                    try:
                        for _, row in df_filtered.iterrows():
                            fig.add_trace(go.Scatterpolar(
                                r=row.values,
                                theta=df_filtered.columns,
                                fill='toself'
                            ))
                        fig.data[0].name = 'Valgte periode'
                        fig.data[1].name = 'Hele sæsonen'
                        # Set plot title and layout
                        fig.update_layout(
                            title='Talent-id plot',
                            template='plotly_dark',
                            polar=dict(
                                radialaxis=dict(
                                    visible=True,
                                    range=[1, 5],
                                    tickfont=dict(
                                        size=8  # Adjust the font size for radial axis labels
                                    ),
                                ),
                            ),
                            width=400,  # Adjust the width as needed
                            height=500,  # Adjust the height as needed
                            font=dict(
                                size=8
                            )
                        )
                        st.plotly_chart(fig)
                    except IndexError:
                        st.warning(" ")

                # Plot the second plot in the second column
                with col2:
                    if selected_dftal.empty:
                        st.warning('')
                    else:
                        fig = go.Figure()
                        try:
                            for column in selected_dftal_columns:
                                fig.add_trace(go.Scatter(
                                    x=selected_dftal['label'],
                                    y=selected_dftal[column],
                                    mode='lines',
                                    name=column
                                    ))

                                fig.update_layout(
                                    title='Talent id score over tid',
                                    template='plotly_dark',
                                    legend=dict(
                                        orientation="h",  # Set legend orientation to horizontal
                                        font=dict(
                                            size=8
                                        )
                                    ),
                                    xaxis=dict(
                                        tickangle=0,  # Adjust x-axis label rotation angle as needed
                                        tickfont=dict(
                                            size=8,  # Adjust font size for x-axis labels
                                        ),
                                    ),
                                    yaxis=dict(
                                        range=[1, 5],  # Set y-axis range to [1, 5]
                                    ),
                                    width=500,  # Adjust the width as needed
                                )

                            st.plotly_chart(fig)
                        except IndexError:
                            st.warning(" ")

            
                # Display the dataframe
                if selected_dftal is not None:
                    selected_dftal = selected_dftal.reset_index()
                    selected_dftal = selected_dftal.drop(columns=['Spillere'])
                    selected_dftal = selected_dftal.set_index('label')
                    st.dataframe(selected_dftal,use_container_width=True)
            
            try:
                with open('træningsregistrering.json', 'r') as json_file:
                    træningsdata = json.load(json_file)
                    træningsdata = pd.DataFrame(træningsdata)
            except FileNotFoundError:
                return pd.DataFrame(columns=['Tidspunkt', 'Dato','Årgang','Rådighed', 'Spillerens navn', 'Træningshold', 'Træningstype', 'Antal minutter trænet'])
            
            date_format = '%d-%m-%Y'  # Specify your date format
            træningsdata['Dato'] = pd.to_datetime(træningsdata['Dato'], format=date_format)

            min_date = træningsdata['Dato'].min()
            max_date = træningsdata['Dato'].max()

            date_range = pd.date_range(start=min_date, end=max_date, freq='D')
            date_options = date_range.strftime(date_format)  # Convert dates to the specified format

            default_end_date = date_options[-1]

            # Calculate the default start date as 14 days before the default end date
            default_start_date = pd.to_datetime(default_end_date, format=date_format) - timedelta(days=14)
            default_start_date = default_start_date.strftime(date_format)

            # Set the default start and end date values for the select_slider
            selected_start_date, selected_end_date = st.select_slider(
                'Vælg datointerval',
                options=date_options,
                value=(default_start_date, default_end_date)
            )

            selected_start_date = pd.to_datetime(selected_start_date, format=date_format)
            selected_end_date = pd.to_datetime(selected_end_date, format=date_format)
            filtered_data = træningsdata[
                (træningsdata['Dato'] >= selected_start_date) & (træningsdata['Dato'] <= selected_end_date)
            ]

            # Sort the filtered data by the 'Dato' column
#            sorted_data = filtered_data.sort_values(by ='Dato')
            sorted_data = filtered_data.copy()
            sorted_data = sorted_data[sorted_data['Spiller'] == option2]
            minutter_columns = sorted_data.filter(regex='.*minutter$').columns.tolist()
            minutter_columns_processed = [col.replace('minutter', '') for col in minutter_columns]

            minutter_df = pd.DataFrame({
                'Træningstype': minutter_columns_processed,
                'Minutter': [sorted_data[col].sum() for col in minutter_columns]
            })
            st.title(option2 + ' Træningsdata')
            minutter_df['Træningstype'] = minutter_df['Træningstype'].str.replace('minutter', '')
            col1, col2 = st.columns([3,1])

            with col2:
                træningsgruppe = sorted_data[['Træningsgruppe']].value_counts()
                træningsgruppe = træningsgruppe.rename_axis('Træningsgruppe').reset_index(name='Antal')
                #træningsgruppe = træningsgruppe.set_index('Træningsgruppe')
                #st.dataframe(træningsgruppe,use_container_width=True,hide_index=True)
                fig = go.Figure()
                fig.add_trace(go.Pie(
                    labels=træningsgruppe['Træningsgruppe'],
                    values=træningsgruppe['Antal'],
                    hole=0.0,
                ))
                fig.update_layout(title='Træningsgrupper')
                st.plotly_chart(fig)       

            with col1:
                fig = go.Figure()
                for idx, label in enumerate(minutter_df['Træningstype']):
                    fig.add_trace(go.Pie(
                        labels=minutter_df['Træningstype'],
                        values=minutter_df['Minutter'],
                    ))

                fig.update_layout(title='Træningstyper og deres tid i minutter',
                )
                st.plotly_chart(fig)

            col1,col2 = st.columns(2)


            fig = go.Figure()
            for idx, col in enumerate(minutter_columns):
                fig.add_trace(go.Bar(
                    x=sorted_data['Dato'],
                    y=sorted_data[col],
                    name=col.replace('minutter', ''),
                ))

            fig.update_layout(
                barmode='stack',
                xaxis=dict(title='Dato'),
                yaxis=dict(title='Minutter'),
                title='Træningsdata over tid'
            )

            st.plotly_chart(fig,use_container_width=True)

         
            afbud_årsag = sorted_data['Afbud årsag'].value_counts()
            afbud_årsag = afbud_årsag.rename_axis('Afbud årsag').reset_index(name='Antal')  # Renaming axis for clarity
            afbud_årsag = afbud_årsag.set_index('Afbud årsag')
            
            col1,col2,col3 = st.columns(3)    
            with col1:
                Individuel_træning_kommentar = sorted_data[['Dato', 'Individuel træning kommentar']]
                Individuel_træning_kommentar = Individuel_træning_kommentar.dropna(subset=['Individuel træning kommentar'])
                st.dataframe(Individuel_træning_kommentar.style.format({'Dato': '{:%d-%m-%Y}'}), hide_index=True,use_container_width=True)
            with col2:    
                Individuel_video_kommentar = sorted_data[['Dato', 'Individuel video kommentar']]
                Individuel_video_kommentar = Individuel_video_kommentar.dropna(subset=['Individuel video kommentar'])
                st.dataframe(Individuel_video_kommentar.style.format({'Dato': '{:%d-%m-%Y}'}), hide_index=True,use_container_width=True)
            with col3:
                st.dataframe(afbud_årsag,use_container_width=True)

            st.title(option2 + ' Kampdata')
            try:
                with open('Kampregistrering.json', 'r') as json_file:
                    Kampdata = json.load(json_file)
                    Kampdata = pd.DataFrame(Kampdata)
            except FileNotFoundError:
                return st.write('Ingen kampdata på den valgte spiller')

            date_format = '%d-%m-%Y'  # Specify your date format
            Kampdata['Dato'] = pd.to_datetime(Kampdata['Dato'], format=date_format)

            filtered_data = Kampdata[
                (Kampdata['Dato'] >= selected_start_date) & (Kampdata['Dato'] <= selected_end_date)
            ]
            sorted_data = filtered_data.sort_values(by ='Dato')
            sorted_data = sorted_data[sorted_data['Spiller'] == option2]
            
            kampminutter_spillet = sorted_data['Minutter spillet'].sum()
            kampminutter_til_rådighed = sorted_data['Minutter til rådighed'].sum()

            minutter_ude = kampminutter_til_rådighed - kampminutter_spillet
            minutter_spillet = kampminutter_spillet

            # Creating a DataFrame with the percentages
            data = {
                'Minutter spillet': [minutter_spillet],
                'Minutter ikke spillet': [minutter_ude]
            }
            kampminutter = pd.DataFrame(data, index=['Kampminutter'])
            
            Starter_inde = {
                'Starter inde' : sorted_data['Starter inde'].sum(),
                'Starter ude' : sorted_data['Starter ude'].sum()
            }
            Starter_inde = pd.DataFrame.from_dict(Starter_inde,orient='index',columns = ['Antal kampe'])
            
            Mål_assist = {
                'Mål': sorted_data['Mål'].sum(),
                'Assist': sorted_data['Assist'].sum(),
            }
            Mål_assist = pd.DataFrame.from_dict(Mål_assist, orient='index', columns=['Antal'])

            # Get unique values from the 'Spillere' column
            spillere_values = sorted_data['Spiller'].unique()

            # Filter columns containing a string from 'Spillere' column
            filtered_columns = [col for col in sorted_data.columns if any(spiller in col for spiller in spillere_values)]

            # Create a new DataFrame with the filtered columns
            filtered_data = sorted_data[filtered_columns]
            
            Kamptype = sorted_data['Kamptype'].value_counts()
            Kamptype = Kamptype.rename_axis('Kamptype').reset_index(name='Antal')  # Renaming axis for clarity
            Kamptype = Kamptype.set_index('Kamptype')

            Rådighed = sorted_data['Rådighed'].value_counts()
            Rådighed = Rådighed.rename_axis('Rådighed').reset_index(name='Antal')  # Renaming axis for clarity
            Rådighed = Rådighed.set_index('Rådighed')
            
            Modstandere = sorted_data['Modstanderhold'].value_counts()
            Modstandere = Modstandere.rename_axis('Modstander').reset_index(name='Antal')  # Renaming axis for clarity
            Modstandere = Modstandere.set_index('Modstander')
            Kampårgang = sorted_data['Kampårgang'].value_counts()
            Kampårgang = Kampårgang.rename_axis('Kampårgang').reset_index(name='Antal')  # Renaming axis for clarity
            Kampårgang = Kampårgang.set_index('Kampårgang')

            def create_pie_chart(data, title):
                fig = go.Figure(data=[go.Pie(labels=data.index, values=data['Antal'], hole=0.0)])
                fig.update_layout(title=title)
                st.plotly_chart(fig)

            
            col1,col2= st.columns([3,1])
            with col1:
                fig = go.Figure(data=[go.Pie(labels=kampminutter.columns, values=kampminutter.iloc[0], hole=0.0)])
                fig.update_layout(title='Fordeling af minutter til rådighed')
                st.plotly_chart(fig)
                create_pie_chart(Kamptype, 'Fordeling af kamptyper')
                
            with col2:
                create_pie_chart(Rådighed,'Fordeling af rådighedsstatus')
                create_pie_chart(Kampårgang, 'Fordeling af Kampårgange')
                
            col1,col2 = st.columns(2)
            with col1:
                st.dataframe(Mål_assist,use_container_width=True)
                
            with col2:
                st.dataframe(Modstandere,use_container_width=True)
                
            import gspread
            import pandas as pd
            import numpy as np

            gc = gspread.service_account('wellness-1123-178fea106d0a.json')
            sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1haWEtNQdhthKaSQjb2BRHlq2FLexicUOAHbjNFRAUAk/edit#gid=1984878556')
            ws = sh.worksheet('Samlet')
            df = pd.DataFrame(ws.get_all_records())
            
            df['Tidsstempel'] = pd.to_datetime(df['Tidsstempel'], format='%d/%m/%Y %H.%M.%S', errors='coerce').astype('datetime64[ns]')

            df['Hvilken årgang er du?'] = df['Hvilken årgang er du?'].astype(str)
            df['Hvor frisk er du?'] = df['Hvor frisk er du?'].astype(str)
            df['Hvor frisk er du?'] = df['Hvor frisk er du?'].str.extract(r'(\d+)').astype(float)
            df['Hvordan har du det mentalt'] = df['Hvordan har du det mentalt'].astype(str)
            df['Hvordan har du det mentalt'] = df['Hvordan har du det mentalt'].str.extract(r'(\d+)').astype(float)
            df['Hvordan har din søvn været?'] = df['Hvordan har din søvn været?'].astype(str)
            df['Hvordan har din søvn været?'] = df['Hvordan har din søvn været?'].str.extract(r'(\d+)').astype(float)
            df['Hvor hård var træning/kamp? (10 er hårdest)'] = df['Hvor hård var træning/kamp? (10 er hårdest)'].astype(str)
            df['Hvor hård var træning/kamp? (10 er hårdest)'] = df['Hvor hård var træning/kamp? (10 er hårdest)'].str.extract(r'(\d+)').astype(float)
            df['Hvor udmattet er du?'] = df['Hvor udmattet er du?'].astype(str)
            df['Hvor udmattet er du?'] = df['Hvor udmattet er du?'].str.extract(r'(\d+)').astype(float)
            df['Bedøm din muskelømhed'] = df['Bedøm din muskelømhed'].astype(str)
            df['Bedøm din muskelømhed'] = df['Bedøm din muskelømhed'].str.extract(r'(\d+)').astype(float)
            df['Jeg følte mig tilpas udfordret under træning/kamp'] = df['Jeg følte mig tilpas udfordret under træning/kamp'].astype(str)
            df['Jeg følte mig tilpas udfordret under træning/kamp'] = df['Jeg følte mig tilpas udfordret under træning/kamp'].str.extract(r'(\d+)').astype(float)
            df['Min tidsfornemmelse forsvandt under træning/kamp'] = df['Min tidsfornemmelse forsvandt under træning/kamp'].astype(str)
            df['Min tidsfornemmelse forsvandt under træning/kamp'] = df['Min tidsfornemmelse forsvandt under træning/kamp'].str.extract(r'(\d+)').astype(float)
            df['Jeg oplevede at tanker og handlinger var rettet mod træning/kamp'] = df['Jeg oplevede at tanker og handlinger var rettet mod træning/kamp'].astype(str)
            df['Jeg oplevede at tanker og handlinger var rettet mod træning/kamp'] = df['Jeg oplevede at tanker og handlinger var rettet mod træning/kamp'].str.extract(r'(\d+)').astype(float)
            df['Hvordan har du det mentalt?'] = df['Hvordan har du det mentalt?'].astype(str)
            df['Hvordan har du det mentalt?'] = df['Hvordan har du det mentalt?'].str.extract(r'(\d+)').astype(float)

            df.rename(columns={'Hvor mange timer sov i du i nat?':'Hvor mange timer sov du i nat?'},inplace=True)
            df = pd.melt(df,id_vars=['Tidsstempel','Spørgsmål før eller efter træning','Hvor frisk er du?','Hvordan har du det mentalt','Har du fået nok at spise inden træning/kamp?','Hvordan har din søvn været?','Hvor mange timer sov du i nat?','Træning/kamp - tid i minutter?','Hvor hård var træning/kamp? (10 er hårdest)','Hvor udmattet er du?','Bedøm din muskelømhed','Hvordan har du det mentalt?','Jeg følte mig tilpas udfordret under træning/kamp','Min tidsfornemmelse forsvandt under træning/kamp','Jeg oplevede at tanker og handlinger var rettet mod træning/kamp','Hvilken årgang er du?'],value_vars=['Spillere U13','Spillere U14','Spillere U15','Spillere U16','Spillere U17','Spillere U18','Spillere U19','Spillere U20'],value_name='Spiller')
            df = df[df['Spiller'] != '']
            df['Hvilken årgang er du?'] = df['Hvilken årgang er du?'].astype(float)
            df = df[df['Spiller']==option2]
            
            førtræning = df[['Tidsstempel','Spiller','Hvilken årgang er du?','Hvor frisk er du?','Hvordan har du det mentalt','Har du fået nok at spise inden træning/kamp?','Hvordan har din søvn været?','Hvor mange timer sov du i nat?']]
            eftertræning = df[['Tidsstempel','Spiller','Hvilken årgang er du?','Træning/kamp - tid i minutter?','Hvor hård var træning/kamp? (10 er hårdest)','Hvor udmattet er du?','Bedøm din muskelømhed','Hvordan har du det mentalt?','Jeg følte mig tilpas udfordret under træning/kamp','Min tidsfornemmelse forsvandt under træning/kamp','Jeg oplevede at tanker og handlinger var rettet mod træning/kamp']]
            førtræning.dropna(inplace=True)
            eftertræning.dropna(inplace=True)


            #eftertræning.set_index('Tidsstempel', inplace=True)
            #eftertræning.sort_index(ascending=False, inplace=True)
            #førtræning.set_index('Tidsstempel', inplace=True)
            #førtræning.sort_index(ascending=False, inplace=True)
            førtræning['Tidsstempel'] = pd.to_datetime(førtræning['Tidsstempel'])
            eftertræning['Tidsstempel'] = pd.to_datetime(eftertræning['Tidsstempel'])

            førtræning = førtræning[
            (førtræning['Tidsstempel'] >= selected_start_date) & (førtræning['Tidsstempel'] <= selected_end_date)
            ]
            eftertræning= eftertræning[
                (eftertræning['Tidsstempel'] >= selected_start_date) & (eftertræning['Tidsstempel'] <= selected_end_date)
            ]

            col1,col2 = st.columns([3,1])
            with col1:
                fig_førtræning = px.bar(førtræning, x='Tidsstempel', y=['Hvor frisk er du?', 'Hvordan har du det mentalt', 'Hvordan har din søvn været?'],barmode='group')
                fig_førtræning.update_layout(
                    title='Før træning scores over tid',
                    template='plotly_dark',
                    bargap=0.0,  # Adjust the gap between bars
                    bargroupgap=0.0,  # Adjust the gap between groups of bars
                    yaxis=dict(range=[0, 7]))
                st.plotly_chart(fig_førtræning)

            with col2:
                fig_eftertræning = px.bar(eftertræning, x='Tidsstempel', y=['Hvor udmattet er du?','Bedøm din muskelømhed','Hvordan har du det mentalt?'],barmode='group')
                fig_eftertræning.update_layout(
                    title='Efter træning scores over tid',
                    template='plotly_dark',
                    bargap=0.0,  # Adjust the gap between bars
                    bargroupgap=0.0,  # Adjust the gap between groups of bars
                    yaxis=dict(range=[0, 7]))  # Set the y-axis range
                st.plotly_chart(fig_eftertræning)
                
        Årgange = {
                'U13':U13,
                'U14':U14,
                'U15':U15,
                'U17':U17,
                'U19':U19}
        rullemenu = st.selectbox('Vælg årgang',Årgange.keys())
        Årgange[rullemenu]()

    def modstanderanalyse():
        def U15 ():
            import pandas as pd
            import streamlit as st
            import plotly.express as px
            from mplsoccer import Pitch
            import matplotlib.pyplot as plt
            import numpy as np

            dfteamstats = pd.read_csv(r'Teamsheet alle kampe U15.csv')
            df = pd.read_csv(r'xT/U15 Ligaen 23 24.csv')
            holdnavne = df['team.name'].drop_duplicates(keep= 'first')
            modstander = st.selectbox('Vælg modstander',holdnavne)

            columns_after_first_3 = dfteamstats.columns[3:]
            dfteamstatsmodstander = dfteamstats.iloc[:, :3].join(dfteamstats.loc[:, columns_after_first_3[dfteamstats.columns[3:].str.contains(modstander)]])
            df = df[df['team.name'].str.contains(modstander)]

            kampe = df['opponentTeam.name'].drop_duplicates(keep='first')
            kampe = kampe.dropna()
            kampe = sorted(kampe)
            option4 = st.multiselect('Vælg modstanderens modstander (Hvis ingen er valgt, vises alle)',kampe)
            if len(option4) > 0:
                filtreretdfkamp = option4
            else:
                filtreretdfkamp = kampe

            df = df[df['opponentTeam.name'].isin(filtreretdfkamp)]
            dfteamstatsmodstander = dfteamstatsmodstander[dfteamstatsmodstander['label'].str.contains('|'.join(filtreretdfkamp))]
            #st.dataframe(dfteamstatsmodstander)
            ppda_columns = dfteamstatsmodstander.columns[dfteamstatsmodstander.columns.str.endswith('.ppda')]
            passes_columns = dfteamstatsmodstander.columns[
                dfteamstatsmodstander.columns.str.endswith('.passes') |
                dfteamstatsmodstander.columns.str.endswith('.passesSuccessful') |
                dfteamstatsmodstander.columns.str.endswith('longPasses')
            ]
            challenge_intensity_columns = dfteamstatsmodstander.columns[dfteamstatsmodstander.columns.str.endswith('.challengeIntensity')]
                

            average_passes = dfteamstatsmodstander.loc[:, passes_columns].mean()
            average_passes_df = average_passes.to_frame(name='Pasninger')
            columns = average_passes_df.columns
            long_pass_share = average_passes_df.values[2]/average_passes_df.values[0]
            long_pass_share = pd.DataFrame([long_pass_share],columns = columns,index=['Long pass share'])
            values = average_passes_df.values[1]/average_passes_df.values[0]
            values = pd.DataFrame([values],columns = columns,index=['Procent'])
            frames = [average_passes_df,values,long_pass_share]
            average_passes_df = pd.concat(frames)

            average_passes_df = average_passes_df.reset_index(drop=True)

            average_passes_df.index = ['Antal', 'Succesfulde','Lange', 'Procent','Long pass %']

            average_passes_df.loc['Procent', :] = average_passes_df.loc['Procent', :].apply(lambda x: f"{x:.2%}" if isinstance(x, float) else x)
            average_passes_df.loc['Long pass %', :] = average_passes_df.loc['Long pass %', :].apply(lambda x: f"{x:.2%}" if isinstance(x, float) else x)

            #st.dataframe(average_passes_df)
            average_challengeintensity = dfteamstatsmodstander.loc[:,challenge_intensity_columns].mean()
            average_challengeintensity_df = average_challengeintensity.to_frame(name='Challenge intensity')
            average_ppda = dfteamstatsmodstander.loc[:, ppda_columns].mean()
            average_ppda_df = average_ppda.to_frame(name='PPDA')

            team_formation_counts = df['team.formation'].value_counts()
            total_rows = len(df)
            team_formation_percentages = (team_formation_counts / total_rows) * 100
            top_formations = team_formation_percentages.head(3)
            top_formations = top_formations.round(2)
            st.write('Formationer spillet')
            st.write(top_formations)

            Deep_completion = df.copy()

            Deep_completion = Deep_completion[Deep_completion['type.secondary'].str.contains('deep_completion|deep_completed_cross')]

            Assists = df.copy()

            # Create a boolean mask for rows to remove
            strings_to_remove = ['second_assist', 'third_assist']
            rows_to_remove = Assists['type.secondary'].str.contains('|'.join(strings_to_remove))

            # Apply the mask to remove rows
            Assists = Assists[~rows_to_remove]

            # Replace 'shot_assist' string in the 'type_secondary' column
            Assists['type.secondary'] = Assists['type.secondary'].str.replace('shot_assist', '')

            # Filter rows that contain 'assist' in the modified 'type_secondary' column
            Assists = Assists[Assists['type.secondary'].str.contains('assist')]

            Målscorer = df.copy()
            strings_to_remove = ['goal_kick', 'goalkeeper_exit','conceded_goal']
            rows_to_remove = Målscorer['type.secondary'].str.contains('|'.join(strings_to_remove))
            Målscorer = Målscorer[~rows_to_remove]
            Målscorer = Målscorer[Målscorer['type.secondary'].str.contains('goal')]


            col1, col2, col3, col4 = st.columns(4)
            with col1:
                
                Shotxg = df[['player.name','shot.xg']]
                Shotxg = Shotxg.groupby('player.name')['shot.xg'].sum()
                Shotxg = Shotxg.nlargest(3)
                st.write('Xg')
                st.dataframe(Shotxg)

            with col2:
                
                Postshotxg = df[['player.name','shot.postShotXg']]
                Postshotxg = Postshotxg.groupby('player.name')['shot.postShotXg'].sum()
                Postshotxg = Postshotxg.nlargest(3)
                st.write('Postshot xG')
                st.dataframe(Postshotxg)

            with col3:
                top_player_names = Assists['player.name'].value_counts().head(3)
                top_player_names = top_player_names.rename_axis("Spiller navn").reset_index()
                top_player_names.columns = ["Player name", "Assists"]
                top_player_names = top_player_names.set_index('Player name')
                st.write('Assists')
                st.dataframe(top_player_names)

            with col4:
                top_player_names = Målscorer['player.name'].value_counts().head(3)
                top_player_names = top_player_names.rename_axis("Spiller navn").reset_index()
                top_player_names.columns = ["player.name", "Mål"]
                top_player_names = top_player_names.set_index('player.name')
                st.write('Mål')
                st.dataframe(top_player_names)


            col1, col2, col34 = st.columns([1,1,2])

            with col1:
                st.write("Pasninger")
                average_passes_df.columns = ['Antal']
                st.dataframe(average_passes_df)

            with col2:
                st.write('PPDA')
                average_ppda_df.index.values[0] = modstander
                st.dataframe(average_ppda_df)
                st.write('Challenge intensity')
                average_challengeintensity_df.index.values[0] = modstander
                st.dataframe(average_challengeintensity_df)

            with col34:
                xgplacering = df.copy()
                xgplacering = df[df['shot.xg'].astype(float) > 0]
                spillere = xgplacering['player.name'].drop_duplicates(keep='first')
                spillere = spillere.dropna()
                spillere = sorted(spillere)
                option4 = st.multiselect('Vælg spiller (hvis ingen vælges vises alle)',spillere)
                if len(option4) > 0:
                    filtreretdfkamp = option4
                else:
                    filtreretdfkamp = spillere

                xgplacering = xgplacering[xgplacering['player.name'].isin(filtreretdfkamp)]

                x = xgplacering['location.x']
                y = xgplacering['location.y']
                shot_xg = xgplacering['shot.xg'].astype(float)
                min_size = 1  # Minimum dot size
                max_size = 50  # Maximum dot size
                sizes = np.interp(shot_xg, (shot_xg.min(), shot_xg.max()), (min_size, max_size))

                pitch = Pitch(pitch_type='wyscout', pitch_color='grass', line_color='white', stripe=True)
                fig, ax = pitch.draw()
                sc = pitch.scatter(x, y, ax=ax, s=sizes)
                st.write('Xg plot (Jo større markering, jo større xG)')
                st.pyplot(plt.gcf(), use_container_width=True)

                

            col1, col2 = st.columns(2)
            with col1:
                
                pitch = Pitch(pitch_type = 'wyscout',pitch_color='grass', line_color='white', stripe=True)
                fig, ax = pitch.draw()

                for _, row in Deep_completion.iterrows():
                    start_x = row['location.x']
                    start_y = row['location.y']
                    end_x = row['pass.endLocation.x']
                    end_y = row['pass.endLocation.y']
                    
                    arrow_dx = end_x - start_x
                    arrow_dy = end_y - start_y

                    plt.arrow(
                        start_x, start_y,
                        arrow_dx, arrow_dy,
                        head_width=0.5, head_length=0.5,
                        fc='blue', ec='blue', alpha=0.5
                    )

                st.write('Deep completions')
                st.pyplot(fig)

            with col2:
                pitch = Pitch(pitch_type='wyscout', pitch_color='grass', line_color='white', stripe=True)
                fig, ax = pitch.draw()

                for _, row in Assists.iterrows():
                    start_x = row['location.x']
                    start_y = row['location.y']
                    end_x = row['pass.endLocation.x']
                    end_y = row['pass.endLocation.y']
                    
                    arrow_dx = end_x - start_x
                    arrow_dy = end_y - start_y

                    plt.arrow(
                        start_x, start_y,
                        arrow_dx, arrow_dy,
                        head_width=0.5, head_length=0.5,
                        fc='blue', ec='blue', alpha=0.5
                    )

                st.write('Assists')
                st.pyplot(fig)

            col1, col2, col3, col4 = st.columns(4)
            with col1:
                top_player_names = Deep_completion['player.name'].value_counts().head(3)
                st.write('Top 3 spillere på Deep completions')
                top_player_df = top_player_names.to_frame(name='Antal')
                st.dataframe(top_player_df)

            with col2:    
                top_player_positions = Deep_completion['player.position'].value_counts().head(3)
                st.write('Top 3 positioner for Deep completions')
                top_player_df = top_player_positions.to_frame(name='Antal')
                st.dataframe(top_player_df)

            with col3:
                top_player_names = Assists['player.name'].value_counts().head(3)
                st.write('Top 3 spillere på Assists')
                top_player_df = top_player_names.to_frame(name='Antal')
                st.dataframe(top_player_df)
            with col4:    
                top_player_positions = Assists['player.position'].value_counts().head(3)
                st.write('Top 3 positioner for Assists')
                top_player_df = top_player_positions.to_frame(name='Antal')
                st.dataframe(top_player_df)



            Forward_passes = df
            Forward_passes = Forward_passes[
                (Forward_passes['type.primary'].str.contains('pass')) &
                (Forward_passes['location.x'].astype(float) <= 50) &
                (Forward_passes['location.x'] + 10 <= Forward_passes['pass.endLocation.x']) &
                (Forward_passes['pass.accurate'] ==True)
            ]
            top_combinationsf = Forward_passes.groupby(['player.name', 'pass.recipient.name']).agg({
                'player.position': 'first',
                'pass.recipient.position': 'first',
                'player.name': 'count'
            }).nlargest(5, 'player.name')

            top_combinationsf = top_combinationsf.rename(columns={'player.name':'Antal'})

            st.write("Top 5 mest frekvente fremadrettede pasninger på mere end 10 meter")
            st.dataframe(top_combinationsf)

            Losses = df
            Losses = Losses[
                (Losses['type.secondary'].str.contains('loss')) &
                (Losses['location.x'].astype(float) <= 50)
            ]
            top_combinations = Losses.groupby(['player.name']).agg({
                'player.position': 'first',
                'player.name': 'count'
            }).nlargest(5, 'player.name')

            top_combinations = top_combinations.rename(columns={'player.name':'Antal'})


            # Create two columns using st.beta_columns()
            col1, col2 = st.columns(2)

            # Plot the first figure in the first column
            with col1:
                pitch = Pitch(pitch_type='wyscout', pitch_color='grass', line_color='white', stripe=True)
                fig, ax = pitch.draw()

                for _, row in Forward_passes.iterrows():
                    start_x = row['location.x']
                    start_y = row['location.y']
                    end_x = row['pass.endLocation.x']
                    end_y = row['pass.endLocation.y']

                    arrow_dx = end_x - start_x
                    arrow_dy = end_y - start_y

                    plt.arrow(
                        start_x, start_y,
                        arrow_dx, arrow_dy,
                        head_width=0.5, head_length=0.5,
                        fc='blue', ec='blue', alpha=0.5
                    )

                ax.set_title('Forward Passes med succes fra egen halvdel på mere end 10 meter')
                st.pyplot(fig)

            # Plot the second figure in the second column
            with col2:
                pitch = Pitch(pitch_type='wyscout', pitch_color='grass', line_color='white', stripe=True)
                fig, ax = pitch.draw()

                for _, row in Losses.iterrows():
                    start_x = row['location.x']
                    start_y = row['location.y']
                    end_x = row['pass.endLocation.x']
                    end_y = row['pass.endLocation.y']

                    arrow_dx = end_x - start_x
                    arrow_dy = end_y - start_y

                    plt.arrow(
                        start_x, start_y,
                        arrow_dx, arrow_dy,
                        head_width=0.5, head_length=0.5,
                        fc='red', ec='red', alpha=0.5
                    )

                ax.set_title('Boldtab på egen banehalvdel')
                st.pyplot(fig)

            st.write("Top 5 mest frekvente boldtab")
            st.dataframe(top_combinations)

            # Show the DataFrame
            st.title('Boldtab')

            col1, col2 = st.columns(2)
            with col1:
                st.write('Boldtab højde på banen')
                plot = px.histogram(data_frame=Losses,x=Losses['location.x'],nbins=10)
                st.plotly_chart(plot,use_container_width=True)

            with col2:
                st.write('Boldtab bredde på banen')
                plot = px.histogram(data_frame=Losses,x=Losses['location.y'],nbins=10)
                plot.update_xaxes(range=[0, 100])
                st.plotly_chart(plot,use_container_width=True) 

        def U17 ():
            import pandas as pd
            import streamlit as st
            import plotly.express as px
            from mplsoccer import Pitch
            import matplotlib.pyplot as plt
            import numpy as np

            dfteamstats = pd.read_csv(r'Teamsheet alle kampe U17.csv')
            df = pd.read_csv(r'xT/U17 Ligaen 23 24.csv')
            holdnavne = df['team.name'].drop_duplicates(keep= 'first')
            modstander = st.selectbox('Vælg modstander',holdnavne)

            columns_after_first_3 = dfteamstats.columns[3:]
            dfteamstatsmodstander = dfteamstats.iloc[:, :3].join(dfteamstats.loc[:, columns_after_first_3[dfteamstats.columns[3:].str.contains(modstander)]])
            df = df[df['team.name'].str.contains(modstander)]

            kampe = df['opponentTeam.name'].drop_duplicates(keep='first')
            kampe = kampe.dropna()
            kampe = sorted(kampe)
            option4 = st.multiselect('Vælg modstanderens modstander (Hvis ingen er valgt, vises alle)',kampe)
            if len(option4) > 0:
                filtreretdfkamp = option4
            else:
                filtreretdfkamp = kampe

            df = df[df['opponentTeam.name'].isin(filtreretdfkamp)]
            dfteamstatsmodstander = dfteamstatsmodstander[dfteamstatsmodstander['label'].str.contains('|'.join(filtreretdfkamp))]
            #st.dataframe(dfteamstatsmodstander)
            ppda_columns = dfteamstatsmodstander.columns[dfteamstatsmodstander.columns.str.endswith('.ppda')]
            passes_columns = dfteamstatsmodstander.columns[
                dfteamstatsmodstander.columns.str.endswith('.passes') |
                dfteamstatsmodstander.columns.str.endswith('.passesSuccessful') |
                dfteamstatsmodstander.columns.str.endswith('longPasses')
            ]
            challenge_intensity_columns = dfteamstatsmodstander.columns[dfteamstatsmodstander.columns.str.endswith('.challengeIntensity')]
                

            average_passes = dfteamstatsmodstander.loc[:, passes_columns].mean()
            average_passes_df = average_passes.to_frame(name='Pasninger')
            columns = average_passes_df.columns
            long_pass_share = average_passes_df.values[2]/average_passes_df.values[0]
            long_pass_share = pd.DataFrame([long_pass_share],columns = columns,index=['Long pass share'])
            values = average_passes_df.values[1]/average_passes_df.values[0]
            values = pd.DataFrame([values],columns = columns,index=['Procent'])
            frames = [average_passes_df,values,long_pass_share]
            average_passes_df = pd.concat(frames)

            average_passes_df = average_passes_df.reset_index(drop=True)

            average_passes_df.index = ['Antal', 'Succesfulde','Lange', 'Procent','Long pass %']

            average_passes_df.loc['Procent', :] = average_passes_df.loc['Procent', :].apply(lambda x: f"{x:.2%}" if isinstance(x, float) else x)
            average_passes_df.loc['Long pass %', :] = average_passes_df.loc['Long pass %', :].apply(lambda x: f"{x:.2%}" if isinstance(x, float) else x)

            #st.dataframe(average_passes_df)
            average_challengeintensity = dfteamstatsmodstander.loc[:,challenge_intensity_columns].mean()
            average_challengeintensity_df = average_challengeintensity.to_frame(name='Challenge intensity')
            average_ppda = dfteamstatsmodstander.loc[:, ppda_columns].mean()
            average_ppda_df = average_ppda.to_frame(name='PPDA')

            team_formation_counts = df['team.formation'].value_counts()
            total_rows = len(df)
            team_formation_percentages = (team_formation_counts / total_rows) * 100
            top_formations = team_formation_percentages.head(3)
            top_formations = top_formations.round(2)
            st.write('Formationer spillet')
            st.write(top_formations)

            Deep_completion = df.copy()

            Deep_completion = Deep_completion[Deep_completion['type.secondary'].str.contains('deep_completion|deep_completed_cross')]

            Assists = df.copy()

            # Create a boolean mask for rows to remove
            strings_to_remove = ['second_assist', 'third_assist']
            rows_to_remove = Assists['type.secondary'].str.contains('|'.join(strings_to_remove))

            # Apply the mask to remove rows
            Assists = Assists[~rows_to_remove]

            # Replace 'shot_assist' string in the 'type_secondary' column
            Assists['type.secondary'] = Assists['type.secondary'].str.replace('shot_assist', '')

            # Filter rows that contain 'assist' in the modified 'type_secondary' column
            Assists = Assists[Assists['type.secondary'].str.contains('assist')]

            Målscorer = df.copy()
            strings_to_remove = ['goal_kick', 'goalkeeper_exit','conceded_goal']
            rows_to_remove = Målscorer['type.secondary'].str.contains('|'.join(strings_to_remove))
            Målscorer = Målscorer[~rows_to_remove]
            Målscorer = Målscorer[Målscorer['type.secondary'].str.contains('goal')]


            col1, col2, col3, col4 = st.columns(4)
            with col1:
                
                Shotxg = df[['player.name','shot.xg']]
                Shotxg = Shotxg.groupby('player.name')['shot.xg'].sum()
                Shotxg = Shotxg.nlargest(3)
                st.write('Xg')
                st.dataframe(Shotxg)

            with col2:
                
                Postshotxg = df[['player.name','shot.postShotXg']]
                Postshotxg = Postshotxg.groupby('player.name')['shot.postShotXg'].sum()
                Postshotxg = Postshotxg.nlargest(3)
                st.write('Postshot xG')
                st.dataframe(Postshotxg)

            with col3:
                top_player_names = Assists['player.name'].value_counts().head(3)
                top_player_names = top_player_names.rename_axis("Spiller navn").reset_index()
                top_player_names.columns = ["Player name", "Assists"]
                top_player_names = top_player_names.set_index('Player name')
                st.write('Assists')
                st.dataframe(top_player_names)

            with col4:
                top_player_names = Målscorer['player.name'].value_counts().head(3)
                top_player_names = top_player_names.rename_axis("Spiller navn").reset_index()
                top_player_names.columns = ["player.name", "Mål"]
                top_player_names = top_player_names.set_index('player.name')
                st.write('Mål')
                st.dataframe(top_player_names)


            col1, col2, col34 = st.columns([1,1,2])

            with col1:
                st.write("Pasninger")
                average_passes_df.columns = ['Antal']
                st.dataframe(average_passes_df)

            with col2:
                st.write('PPDA')
                average_ppda_df.index.values[0] = modstander
                st.dataframe(average_ppda_df)
                st.write('Challenge intensity')
                average_challengeintensity_df.index.values[0] = modstander
                st.dataframe(average_challengeintensity_df)

            with col34:
                xgplacering = df.copy()
                xgplacering = df[df['shot.xg'].astype(float) > 0]
                spillere = xgplacering['player.name'].drop_duplicates(keep='first')
                spillere = spillere.dropna()
                spillere = sorted(spillere)
                option4 = st.multiselect('Vælg spiller (hvis ingen vælges vises alle)',spillere)
                if len(option4) > 0:
                    filtreretdfkamp = option4
                else:
                    filtreretdfkamp = spillere

                xgplacering = xgplacering[xgplacering['player.name'].isin(filtreretdfkamp)]

                x = xgplacering['location.x']
                y = xgplacering['location.y']
                shot_xg = xgplacering['shot.xg'].astype(float)
                min_size = 1  # Minimum dot size
                max_size = 50  # Maximum dot size
                sizes = np.interp(shot_xg, (shot_xg.min(), shot_xg.max()), (min_size, max_size))

                pitch = Pitch(pitch_type='wyscout', pitch_color='grass', line_color='white', stripe=True)
                fig, ax = pitch.draw()
                sc = pitch.scatter(x, y, ax=ax, s=sizes)
                st.write('Xg plot (Jo større markering, jo større xG)')
                st.pyplot(plt.gcf(), use_container_width=True)

                

            col1, col2 = st.columns(2)
            with col1:
                
                pitch = Pitch(pitch_type = 'wyscout',pitch_color='grass', line_color='white', stripe=True)
                fig, ax = pitch.draw()

                for _, row in Deep_completion.iterrows():
                    start_x = row['location.x']
                    start_y = row['location.y']
                    end_x = row['pass.endLocation.x']
                    end_y = row['pass.endLocation.y']
                    
                    arrow_dx = end_x - start_x
                    arrow_dy = end_y - start_y

                    plt.arrow(
                        start_x, start_y,
                        arrow_dx, arrow_dy,
                        head_width=0.5, head_length=0.5,
                        fc='blue', ec='blue', alpha=0.5
                    )

                st.write('Deep completions')
                st.pyplot(fig)

            with col2:
                pitch = Pitch(pitch_type='wyscout', pitch_color='grass', line_color='white', stripe=True)
                fig, ax = pitch.draw()

                for _, row in Assists.iterrows():
                    start_x = row['location.x']
                    start_y = row['location.y']
                    end_x = row['pass.endLocation.x']
                    end_y = row['pass.endLocation.y']
                    
                    arrow_dx = end_x - start_x
                    arrow_dy = end_y - start_y

                    plt.arrow(
                        start_x, start_y,
                        arrow_dx, arrow_dy,
                        head_width=0.5, head_length=0.5,
                        fc='blue', ec='blue', alpha=0.5
                    )

                st.write('Assists')
                st.pyplot(fig)

            col1, col2, col3, col4 = st.columns(4)
            with col1:
                top_player_names = Deep_completion['player.name'].value_counts().head(3)
                st.write('Top 3 spillere på Deep completions')
                top_player_df = top_player_names.to_frame(name='Antal')
                st.dataframe(top_player_df)

            with col2:    
                top_player_positions = Deep_completion['player.position'].value_counts().head(3)
                st.write('Top 3 positioner for Deep completions')
                top_player_df = top_player_positions.to_frame(name='Antal')
                st.dataframe(top_player_df)

            with col3:
                top_player_names = Assists['player.name'].value_counts().head(3)
                st.write('Top 3 spillere på Assists')
                top_player_df = top_player_names.to_frame(name='Antal')
                st.dataframe(top_player_df)
            with col4:    
                top_player_positions = Assists['player.position'].value_counts().head(3)
                st.write('Top 3 positioner for Assists')
                top_player_df = top_player_positions.to_frame(name='Antal')
                st.dataframe(top_player_df)



            Forward_passes = df
            Forward_passes = Forward_passes[
                (Forward_passes['type.primary'].str.contains('pass')) &
                (Forward_passes['location.x'].astype(float) <= 50) &
                (Forward_passes['location.x'] + 10 <= Forward_passes['pass.endLocation.x']) &
                (Forward_passes['pass.accurate'] ==True)
            ]
            top_combinationsf = Forward_passes.groupby(['player.name', 'pass.recipient.name']).agg({
                'player.position': 'first',
                'pass.recipient.position': 'first',
                'player.name': 'count'
            }).nlargest(5, 'player.name')

            top_combinationsf = top_combinationsf.rename(columns={'player.name':'Antal'})

            st.write("Top 5 mest frekvente fremadrettede pasninger på mere end 10 meter")
            st.dataframe(top_combinationsf)

            Losses = df
            Losses = Losses[
                (Losses['type.secondary'].str.contains('loss')) &
                (Losses['location.x'].astype(float) <= 50)
            ]
            top_combinations = Losses.groupby(['player.name']).agg({
                'player.position': 'first',
                'player.name': 'count'
            }).nlargest(5, 'player.name')

            top_combinations = top_combinations.rename(columns={'player.name':'Antal'})


            # Create two columns using st.beta_columns()
            col1, col2 = st.columns(2)

            # Plot the first figure in the first column
            with col1:
                pitch = Pitch(pitch_type='wyscout', pitch_color='grass', line_color='white', stripe=True)
                fig, ax = pitch.draw()

                for _, row in Forward_passes.iterrows():
                    start_x = row['location.x']
                    start_y = row['location.y']
                    end_x = row['pass.endLocation.x']
                    end_y = row['pass.endLocation.y']

                    arrow_dx = end_x - start_x
                    arrow_dy = end_y - start_y

                    plt.arrow(
                        start_x, start_y,
                        arrow_dx, arrow_dy,
                        head_width=0.5, head_length=0.5,
                        fc='blue', ec='blue', alpha=0.5
                    )

                ax.set_title('Forward Passes med succes fra egen halvdel på mere end 10 meter')
                st.pyplot(fig)

            # Plot the second figure in the second column
            with col2:
                pitch = Pitch(pitch_type='wyscout', pitch_color='grass', line_color='white', stripe=True)
                fig, ax = pitch.draw()

                for _, row in Losses.iterrows():
                    start_x = row['location.x']
                    start_y = row['location.y']
                    end_x = row['pass.endLocation.x']
                    end_y = row['pass.endLocation.y']

                    arrow_dx = end_x - start_x
                    arrow_dy = end_y - start_y

                    plt.arrow(
                        start_x, start_y,
                        arrow_dx, arrow_dy,
                        head_width=0.5, head_length=0.5,
                        fc='red', ec='red', alpha=0.5
                    )

                ax.set_title('Boldtab på egen banehalvdel')
                st.pyplot(fig)

            st.write("Top 5 mest frekvente boldtab")
            st.dataframe(top_combinations)

            # Show the DataFrame
            st.title('Boldtab')

            col1, col2 = st.columns(2)
            with col1:
                st.write('Boldtab højde på banen')
                plot = px.histogram(data_frame=Losses,x=Losses['location.x'],nbins=10)
                st.plotly_chart(plot,use_container_width=True)

            with col2:
                st.write('Boldtab bredde på banen')
                plot = px.histogram(data_frame=Losses,x=Losses['location.y'],nbins=10)
                plot.update_xaxes(range=[0, 100])
                st.plotly_chart(plot,use_container_width=True) 

        def U19 ():
            import pandas as pd
            import streamlit as st
            import plotly.express as px
            from mplsoccer import Pitch
            import matplotlib.pyplot as plt
            import numpy as np

            dfteamstats = pd.read_csv(r'Teamsheet alle kampe U19.csv')
            df = pd.read_csv(r'xT/U19 Ligaen 23 24.csv')
            df.loc[df['player.id'] == 624663, 'player.name'] = 'Je. Beluli'
            holdnavne = df['team.name'].drop_duplicates(keep= 'first')
            modstander = st.selectbox('Vælg modstander',holdnavne)

            columns_after_first_3 = dfteamstats.columns[3:]
            dfteamstatsmodstander = dfteamstats.iloc[:, :3].join(dfteamstats.loc[:, columns_after_first_3[dfteamstats.columns[3:].str.contains(modstander)]])
            df = df[df['team.name'].str.contains(modstander)]

            kampe = df['opponentTeam.name'].drop_duplicates(keep='first')
            kampe = kampe.dropna()
            kampe = sorted(kampe)
            option4 = st.multiselect('Vælg modstanderens modstander (Hvis ingen er valgt, vises alle)',kampe)
            if len(option4) > 0:
                filtreretdfkamp = option4
            else:
                filtreretdfkamp = kampe

            df = df[df['opponentTeam.name'].isin(filtreretdfkamp)]
            dfteamstatsmodstander = dfteamstatsmodstander[dfteamstatsmodstander['label'].str.contains('|'.join(filtreretdfkamp))]
            #st.dataframe(dfteamstatsmodstander)
            ppda_columns = dfteamstatsmodstander.columns[dfteamstatsmodstander.columns.str.endswith('.ppda')]
            passes_columns = dfteamstatsmodstander.columns[
                dfteamstatsmodstander.columns.str.endswith('.passes') |
                dfteamstatsmodstander.columns.str.endswith('.passesSuccessful') |
                dfteamstatsmodstander.columns.str.endswith('longPasses')
            ]
            challenge_intensity_columns = dfteamstatsmodstander.columns[dfteamstatsmodstander.columns.str.endswith('.challengeIntensity')]
                

            average_passes = dfteamstatsmodstander.loc[:, passes_columns].mean()
            average_passes_df = average_passes.to_frame(name='Pasninger')
            columns = average_passes_df.columns
            long_pass_share = average_passes_df.values[2]/average_passes_df.values[0]
            long_pass_share = pd.DataFrame([long_pass_share],columns = columns,index=['Long pass share'])
            values = average_passes_df.values[1]/average_passes_df.values[0]
            values = pd.DataFrame([values],columns = columns,index=['Procent'])
            frames = [average_passes_df,values,long_pass_share]
            average_passes_df = pd.concat(frames)

            average_passes_df = average_passes_df.reset_index(drop=True)

            average_passes_df.index = ['Antal', 'Succesfulde','Lange', 'Procent','Long pass %']

            average_passes_df.loc['Procent', :] = average_passes_df.loc['Procent', :].apply(lambda x: f"{x:.2%}" if isinstance(x, float) else x)
            average_passes_df.loc['Long pass %', :] = average_passes_df.loc['Long pass %', :].apply(lambda x: f"{x:.2%}" if isinstance(x, float) else x)

            #st.dataframe(average_passes_df)
            average_challengeintensity = dfteamstatsmodstander.loc[:,challenge_intensity_columns].mean()
            average_challengeintensity_df = average_challengeintensity.to_frame(name='Challenge intensity')
            average_ppda = dfteamstatsmodstander.loc[:, ppda_columns].mean()
            average_ppda_df = average_ppda.to_frame(name='PPDA')

            team_formation_counts = df['team.formation'].value_counts()
            total_rows = len(df)
            team_formation_percentages = (team_formation_counts / total_rows) * 100
            top_formations = team_formation_percentages.head(3)
            top_formations = top_formations.round(2)
            st.write('Formationer spillet')
            st.write(top_formations)

            Deep_completion = df.copy()

            Deep_completion = Deep_completion[Deep_completion['type.secondary'].str.contains('deep_completion|deep_completed_cross')]

            Assists = df.copy()

            # Create a boolean mask for rows to remove
            strings_to_remove = ['second_assist', 'third_assist']
            rows_to_remove = Assists['type.secondary'].str.contains('|'.join(strings_to_remove))

            # Apply the mask to remove rows
            Assists = Assists[~rows_to_remove]

            # Replace 'shot_assist' string in the 'type_secondary' column
            Assists['type.secondary'] = Assists['type.secondary'].str.replace('shot_assist', '')

            # Filter rows that contain 'assist' in the modified 'type_secondary' column
            Assists = Assists[Assists['type.secondary'].str.contains('assist')]

            Målscorer = df.copy()
            strings_to_remove = ['goal_kick', 'goalkeeper_exit','conceded_goal']
            rows_to_remove = Målscorer['type.secondary'].str.contains('|'.join(strings_to_remove))
            Målscorer = Målscorer[~rows_to_remove]
            Målscorer = Målscorer[Målscorer['type.secondary'].str.contains('goal')]


            col1, col2, col3, col4 = st.columns(4)
            with col1:
                
                Shotxg = df[['player.id','player.name','shot.xg']]
                Shotxg = Shotxg.groupby(['player.id', 'player.name'])['shot.xg'].sum()
                Shotxg = Shotxg.nlargest(3)
                st.write('Xg')
                Shotxg = Shotxg.reset_index()
                Shotxg = Shotxg[['player.name','shot.xg']]
                st.dataframe(Shotxg,hide_index=True)

            with col2:
                
                Postshotxg = df[['player.id','player.name','shot.postShotXg']]
                Postshotxg = Postshotxg.groupby(['player.id', 'player.name'])['shot.postShotXg'].sum()
                Postshotxg = Postshotxg.nlargest(3)
                st.write('Postshot xG')
                Postshotxg = Postshotxg.reset_index()
                Postshotxg = Postshotxg[['player.name','shot.postShotXg']]
                st.dataframe(Postshotxg,hide_index=True)

            with col3:
                top_player_names = Assists.groupby(['player.id', 'player.name']).size().sort_values(ascending=False).head(3)
                st.write('Assist')
                top_player_names = top_player_names.reset_index()
                top_player_names.columns = ["player.id", "player.name", "Assists"]
                top_player_names = top_player_names[['player.name','Assists']]
                st.dataframe(top_player_names,hide_index=True)

            with col4:
                top_player_names = Målscorer.groupby(['player.id', 'player.name']).size().sort_values(ascending=False).head(3)
                st.write('Mål')
                top_player_names = top_player_names.reset_index()
                top_player_names.columns = ["player.id", "player.name", "Mål"]
                top_player_names = top_player_names[['player.name','Mål']]
                st.dataframe(top_player_names,hide_index=True)

            col1, col2, col34 = st.columns([1,1,2])

            with col1:
                st.write("Pasninger")
                average_passes_df.columns = ['Antal']
                st.dataframe(average_passes_df)

            with col2:
                st.write('PPDA')
                average_ppda_df.index.values[0] = modstander
                st.dataframe(average_ppda_df)
                st.write('Challenge intensity')
                average_challengeintensity_df.index.values[0] = modstander
                st.dataframe(average_challengeintensity_df)

            with col34:
                xgplacering = df.copy()
                xgplacering = df[df['shot.xg'].astype(float) > 0]
                spillere = xgplacering['player.name'].drop_duplicates(keep='first').dropna()
                spillere = sorted(spillere)
                option4 = st.multiselect('Vælg spiller (hvis ingen vælges vises alle)',spillere)
                if len(option4) > 0:
                    filtreretdfkamp = option4
                else:
                    filtreretdfkamp = spillere

                xgplacering = xgplacering[xgplacering['player.name'].isin(filtreretdfkamp)]

                x = xgplacering['location.x']
                y = xgplacering['location.y']
                shot_xg = xgplacering['shot.xg'].astype(float)
                min_size = 1  # Minimum dot size
                max_size = 50  # Maximum dot size
                sizes = np.interp(shot_xg, (shot_xg.min(), shot_xg.max()), (min_size, max_size))

                pitch = Pitch(pitch_type='wyscout', pitch_color='grass', line_color='white', stripe=True)
                fig, ax = pitch.draw()
                sc = pitch.scatter(x, y, ax=ax, s=sizes)
                st.write('Xg plot (Jo større markering, jo større xG)')
                st.pyplot(plt.gcf(), use_container_width=True)

                

            col1, col2 = st.columns(2)
            with col1:
                
                pitch = Pitch(pitch_type = 'wyscout',pitch_color='grass', line_color='white', stripe=True)
                fig, ax = pitch.draw()

                for _, row in Deep_completion.iterrows():
                    start_x = row['location.x']
                    start_y = row['location.y']
                    end_x = row['pass.endLocation.x']
                    end_y = row['pass.endLocation.y']
                    
                    arrow_dx = end_x - start_x
                    arrow_dy = end_y - start_y

                    plt.arrow(
                        start_x, start_y,
                        arrow_dx, arrow_dy,
                        head_width=0.5, head_length=0.5,
                        fc='blue', ec='blue', alpha=0.5
                    )

                st.write('Deep completions')
                st.pyplot(fig)

            with col2:
                pitch = Pitch(pitch_type='wyscout', pitch_color='grass', line_color='white', stripe=True)
                fig, ax = pitch.draw()

                for _, row in Assists.iterrows():
                    start_x = row['location.x']
                    start_y = row['location.y']
                    end_x = row['pass.endLocation.x']
                    end_y = row['pass.endLocation.y']
                    
                    arrow_dx = end_x - start_x
                    arrow_dy = end_y - start_y

                    plt.arrow(
                        start_x, start_y,
                        arrow_dx, arrow_dy,
                        head_width=0.5, head_length=0.5,
                        fc='blue', ec='blue', alpha=0.5
                    )

                st.write('Assists')
                st.pyplot(fig)

            col1, col2, col3, col4 = st.columns(4)
            with col1:
                top_player_names = Deep_completion.groupby(['player.id', 'player.name']).size().sort_values(ascending=False).head(3)
                st.write('Top 3 spillere på Deep completions')
                top_player_df = top_player_names.to_frame(name='Antal')
                top_player_df = top_player_df.reset_index()
                top_player_df = top_player_df[['player.name','Antal']]
                st.dataframe(top_player_df,hide_index=True)

            with col2:    
                top_player_positions = Deep_completion['player.position'].value_counts().head(3)
                st.write('Top 3 positioner for Deep completions')
                top_player_df = top_player_positions.to_frame(name='Antal')
                st.dataframe(top_player_df)

            with col3:
                top_player_names = Assists.groupby(['player.id', 'player.name']).size().sort_values(ascending=False).head(3)
                st.write('Top 3 spillere på Assists')
                top_player_df = top_player_names.to_frame(name='Antal')
                top_player_df = top_player_df.reset_index()
                top_player_names = top_player_names[['player.name','Antal']]
                st.dataframe(top_player_df,hide_index=True)
            
            with col4:    
                top_player_positions = Assists['player.position'].value_counts().head(3)
                st.write('Top 3 positioner for Assists')
                top_player_df = top_player_positions.to_frame(name='Antal')
                st.dataframe(top_player_df)

            Forward_passes = df
            Forward_passes = Forward_passes[
                (Forward_passes['type.primary'].str.contains('pass')) &
                (Forward_passes['location.x'].astype(float) <= 50) &
                (Forward_passes['location.x'] + 10 <= Forward_passes['pass.endLocation.x']) &
                (Forward_passes['pass.accurate'] ==True)
            ]
            top_combinationsf = Forward_passes.groupby(['player.name', 'pass.recipient.name']).agg({
                'player.position': 'first',
                'pass.recipient.position': 'first',
                'player.name': 'count'
            }).nlargest(5, 'player.name')

            top_combinationsf = top_combinationsf.rename(columns={'player.name':'Antal'})

            st.write("Top 5 mest frekvente fremadrettede pasninger på mere end 10 meter")
            st.dataframe(top_combinationsf)

            Losses = df
            Losses = Losses[
                (Losses['type.secondary'].str.contains('loss')) &
                (Losses['location.x'].astype(float) <= 50)
            ]
            top_combinations = Losses.groupby(['player.id','player.name']).agg({
                'player.position': 'first',
                'player.name': 'count'
            }).nlargest(5, 'player.name')

            top_combinations = top_combinations.rename(columns={'player.name':'Antal'})


            # Create two columns using st.beta_columns()
            col1, col2 = st.columns(2)

            # Plot the first figure in the first column
            with col1:
                pitch = Pitch(pitch_type='wyscout', pitch_color='grass', line_color='white', stripe=True)
                fig, ax = pitch.draw()

                for _, row in Forward_passes.iterrows():
                    start_x = row['location.x']
                    start_y = row['location.y']
                    end_x = row['pass.endLocation.x']
                    end_y = row['pass.endLocation.y']

                    arrow_dx = end_x - start_x
                    arrow_dy = end_y - start_y

                    plt.arrow(
                        start_x, start_y,
                        arrow_dx, arrow_dy,
                        head_width=0.5, head_length=0.5,
                        fc='blue', ec='blue', alpha=0.5
                    )

                ax.set_title('Forward Passes med succes fra egen halvdel på mere end 10 meter')
                st.pyplot(fig)

            # Plot the second figure in the second column
            with col2:
                pitch = Pitch(pitch_type='wyscout', pitch_color='grass', line_color='white', stripe=True)
                fig, ax = pitch.draw()

                for _, row in Losses.iterrows():
                    start_x = row['location.x']
                    start_y = row['location.y']
                    end_x = row['pass.endLocation.x']
                    end_y = row['pass.endLocation.y']

                    arrow_dx = end_x - start_x
                    arrow_dy = end_y - start_y

                    plt.arrow(
                        start_x, start_y,
                        arrow_dx, arrow_dy,
                        head_width=0.5, head_length=0.5,
                        fc='red', ec='red', alpha=0.5
                    )

                ax.set_title('Boldtab på egen banehalvdel')
                st.pyplot(fig)

            st.write("Top 5 mest frekvente boldtab")
            st.dataframe(top_combinations)

            # Show the DataFrame
            st.title('Boldtab')

            col1, col2 = st.columns(2)
            with col1:
                st.write('Boldtab højde på banen')
                plot = px.histogram(data_frame=Losses,x=Losses['location.x'],nbins=10)
                st.plotly_chart(plot,use_container_width=True)

            with col2:
                st.write('Boldtab bredde på banen')
                plot = px.histogram(data_frame=Losses,x=Losses['location.y'],nbins=10)
                plot.update_xaxes(range=[0, 100])
                st.plotly_chart(plot,use_container_width=True) 

        Årgange = {'U15':U15,
                'U17':U17,
                'U19':U19}
        rullemenu = st.selectbox('Vælg årgang',Årgange.keys())
        Årgange[rullemenu]()

    def forklaring():
        st.title('Wellness Data')
        st.write('Alle skalaer går fra 1 til 7, 1 er bedst 7 er værst')
        st.write('Linjen bliver rød hvis der er en værdi på 6 eller derover, samt hvis der ikke er spist nok eller sovet under 7 timer')
        st.write('Linjen bliver gul ved en værdi på 5, ved ikke ved om de har spise nok eller hvis søvnen er på 7-8 timer')
    
        st.title('GPS Data')
        st.write('Ved afvigelserne er spilleren på 1.0 hvis han rammer trupgennemsnittet og 0.8 hvis han er 20% under trupgennemsnittet')
        
        st.title('Teamsheet')
        st.write('Skalaen i teamsheet er fra årgangens gennemsnit i den seneste sæson og til ligaens gennemsnit i denne sæson. Omvendt hvis vi præsterede bedre i den seneste sæson end hvad gennemsnittet er i den nuværende sæson')

        st.title('Individuelt dashboard')
        st.write('Forudsætningen for at der vises spillere i det individuelle dashboard er at de har spillet mere end 30 minutter på den valgte position i en kamp')
        st.write('Skalaen går fra 1-5 og er vurderet fra kamp til kamp, så de 20% bedste kampe der er spillet i sæsonen på eksempelvis duels won % giver et 5-tal. Spillerens score er så regnet ud ved et gennemsnit af sine kampe og så er talent-id parametrene regnet ud ved at tage et gennemsnit af flere valgte parametre. For at en kamp tæller med i regnestykket skal spilleren have spillet minimum 30 minutter i kampen')
        st.write('Forklaring af de forskellige talent id parametre:')
        st.header('Stoppere')
        st.write('Pasningssikker: Accurate passes, accurate long passes, forward passes, accurate forward passes, accurate progressive passes, accurate vertical passes')
        st.write('Spilintelligens defensivt: Interceptions, successful defensive actions, shots blocked, defensive duels won %')
        st.write('Spilintelligens offensivt: Forward passes, accurate forward passes, accurate passes to final third, passes to final third, accurate progressive passes, progressive passes, through passes, accurate through passes, progressive runs, offensive duels won %, successful dribbles %')
        st.write('Nærkamps- og duelstærk: Defensive duels won %, Aerial duels won %')
        st.header('Backs')
        st.write('Indlægsstærk: Number of crosses, Accurate crosses, XA, Passes to final third')
        st.write('1v1 færdigheder: successful dribbles, defensive duels won, progressive runs, Offensive duels won, accelerations, duels won')
        st.write('Spilintelligens defensivt: Interceptions, successful defensive actions, duels won, defensive duels won')
        st.write('Fart: Successful dribbles, progressive runs, offensive duels won, accelerations')
        st.header('Centrale midt')
        st.write('Pasningssikker/spilvendinger: Accurate passes %, Number of passes, accurate forward passes, number of forward passes, accurate long passes %, number of long passes, accurate smart passes %, number of smart passes, accurate key passes %, number of key passes, accurate passes to final third %, number of passes to final third, accurate vertical passes, number of vertical passes, accurate through passes %, number of through passes, accurate progressive passes %, number of progressive passes')
        st.write('Boldfast: accurate passes %, number of passes, offensive duels won %, received passes, successful dribbles %, number of successful dribbles')
        st.write('Spilintelligens defensivt: Duels won %, number of duels won, interceptions, number of counterpressing recoveries, defensive duels won %, number of defensive duels won')
        st.header('Kanter')
        st.write('Sparkefærdigheder: Shots on target %, Shots on target #, XG,Passes to final third %, Forward Passes %, Vertical passes %')
        st.write('Kombinationsstærk: Passes %,Passes antal,Forward Passes %, Forward Passes antal,Passes to final third %, Passes to final third antal, Through passes %, Through passes antal, Progressive passes %, Progressive passes antal, Successful attacking actions')
        st.write('Spilintelligens offensivt/indlægsstærk: XA per 90, XG per 90, Through passes %, Through passes antal, Smart passes %, Smart passes antal, Progressive passes %, Progressive passes antal, Key passes %, Key passes antal, Successful attacking actions')
        st.write('1v1 offensivt: Successful dribbles antal, Successful dribbles %, Offensive duels antal, Offensive duels %, Progressive runs')
        st.write('Fart: Progressive runs, Successful dribbles antal, Successful dribbles %, Accelerations score')
        st.header('Angriber')
        st.write('Sparkefærdigheder: xG per 90, xG per 90 score, Goals per 90, Shots on target, % score')
        st.write('Boldfast: Offensive duels won, %, Offensive duels won, %, Duels won, %, Accurate passes, %, Successful dribbles, %')
        st.write('Spilintelligens offensivt: xA per 90 score, xG per 90 score, Touches in box per 90 score, Progressive passes per 90 score, Successful attacking actions per 90 score, Touches in box per 90 score,xG per 90 score')
        st.write('Målfarlighed: xG per 90, Goals per 90, xG per 90, Målfarlighed (goals-xg)')
        st.write('Fart: Progressive runs, Progressive runs, Progressive runs, Successful dribbles antal, Successful dribbles, %, Accelerations, Offensive duels won, %')

    overskrifter_til_menu = {
        'Wellness Data':Wellness_data,
        'Kampregistrering':Kampregistrering,
        'Træningsregistrering':Træningsregistrering,
        'Fysisk data': Fysisk_træning,
        'Teamsheet': Teamsheet,
        'Kampevaluering': Kampevaluering,
        'Individuelt dashboard': Individuelt_dashboard,
        'Modstanderanalyse': modstanderanalyse,
        'Forklaring af data':forklaring}

    selected_tab = st.sidebar.radio("Vælg dataform", list(overskrifter_til_menu.keys()))

    overskrifter_til_menu[selected_tab]()

    from PIL import Image

    image = Image.open('Logo.png')
    st.sidebar.image(image)

else:
    st.error('Forkert brugernavn eller kode')