def run_predictions_strengths_prediction(language_index,sidebar_button,student_date_of_birth,student_matriculation_number,selected_tipps):
    import streamlit as st
    import google.generativeai as genai
    import sqlite3
    import pandas as pd
    import joblib
    import Process_Button_Styling
    import Background_Style
    Process_Button_Styling.run_process_button_style()
    Background_Style.run_background_styl()

    # Erstelle eine dicke Linie Funktion
    def draw_line(groesse):
        st.markdown(f"<hr style='border: {groesse}px solid black;'>", unsafe_allow_html=True)

    # Pie-Chart für Stärken
    def create_pie_chart(data):
        import plotly.express as px
        # Erstellen des Kreisdiagramms mit Plotly
        data = data.reset_index()
        data.columns = ['column_name', 'column_value']

        data = data.T
        data.columns = ['Stärke', 'Vorhanden in %', 'is_available']
        data = data[1:]

        strength_name = data['Stärke'][0]
        strength_name_available = data['is_available'][0]
        strength_percent_value = data['Vorhanden in %'][0] * 100

        data['Vorhanden in %'] = data['Vorhanden in %'].astype('float')
        data['Nicht vorhanden in %'] = 1 - data['Vorhanden in %']

        data = data.loc[:, ['Vorhanden in %', 'Nicht vorhanden in %']]
        data = data.T

        data = data.reset_index()

        data.columns = ['Exp', 'Value']

        # Farben basierend auf den Werten zuweisen: grün für positiv, rot für negativ
        color_map = {'Vorhanden in %': '#4CAF50', 'Nicht vorhanden in %': '#D1001C'}

        # Kuchendiagramm mit Plotly Express erstellen
        fig = px.pie(
            data,
            values='Value',
            names='Exp',
            title='Verteilung in %',
            color='Exp',  # Farbschema basierend auf den Kategorien
            color_discrete_map=color_map,  # Farben explizit festlegen
            hole=0.3  # Optional für Donut-Style
        )

        # Layout des Diagramms anpassen
        fig.update_layout(
            height=600,  # Höhe des Diagramms
            title={
                'text': f'{strength_name} ({strength_percent_value:.2f} %)',
                'x': 0.5,  # Zentrieren des Titels
                'xanchor': 'center',
                'yanchor': 'top'
            },
            title_font_size=24,  # Titelgröße
            plot_bgcolor='#eeeeee',  # Hintergrundfarbe des Plots
            paper_bgcolor='#d5d5d5',  # Hintergrundfarbe der gesamten Figur
            font=dict(color='#009999'),
            margin=dict(l=50, r=50, t=100, b=50)  # Ränder anpassen
        )

        # Darstellung des Diagramms mit Streamlit
        st.plotly_chart(fig, use_container_width=True)

    # Tipps geben, um meine Kenntnisse zu erweitern.
    @st.cache_resource
    def give_me_tipps(y_strengths_predicted_row,selected_tipps):
        # Lese den Key aus der Lokalen-Datei
        with open(r'../Google Gemini Key/API_KEY.txt', mode='r', encoding='utf-8') as file:
            API_KEY = file.read()

        genai.configure(api_key=API_KEY)

        prompt = f"""
                            Meine Stärken sind: {y_strengths_predicted_row}.
                            schreibe mir die vorhandenen Stärken in Texten.
                            Gib mir Tipps, um mich bei nicht vorhandenen Stärken zu verbessern. Bitte {selected_tipps}. 
                            """

        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)

        return response.text

    @st.cache_resource
    def get_imputers_and_scaler_and_best_model():
        # Lade die Imputer
        imputer_X = joblib.load(r'../Imputers/Strengths-Prediction/imputer_X_strengths_prediction.pkl')
        imputer_y = joblib.load(r'../Imputers/Strengths-Prediction/imputer_y_strengths_prediction.pkl')

        # Lade die Scaler
        scaler_X = joblib.load(r'../Scalers/Strengths-Prediction/scaler_X_strengths_prediction.pkl')
        scaler_y = joblib.load(r'../Scalers/Strengths-Prediction/scaler_y_strengths_prediction.pkl')

        bestes_trainiertes_model_strengths_prediction = joblib.load(
            r'../ML-Model/bestes_xgboost_modell_strengths_prediction.pkl')

        return imputer_X, imputer_y, scaler_X, scaler_y, bestes_trainiertes_model_strengths_prediction


    @st.cache_data
    def get_columns_info():
        connection_columns_info = sqlite3.connect(r'../Databases/Columns Info Database.db')

        columns_info_data = pd.read_sql('Select * from columns_info_data',
                                        connection_columns_info)

        columns_info_data.columns = ['id', 'Datum', 'Spalte', 'Beschreibung']
        preferences_info = list(columns_info_data[columns_info_data['Beschreibung'] == 'Stärke']['Spalte'])
        mandatory_modules_info = list(columns_info_data[columns_info_data['Beschreibung'] == 'Pflichtmodul']['Spalte'])

        return preferences_info, mandatory_modules_info

    @st.cache_data
    def get_student_data():
        connection_mandatory_modules_grades = sqlite3.connect(r'../Databases/Student Mandatory Modules Grades Database.db')

        mandatory_modules_grades_data = pd.read_sql('Select * from mandatory_modules_grades_data',
                                                    connection_mandatory_modules_grades)
        mandatory_modules_grades_data.columns = needed_columns

        # Spalten ab Vorname bis Ende
        mandatory_modules_grades_data = mandatory_modules_grades_data[needed_columns[2:]]

        # Matrikelnummer formatieren
        mandatory_modules_grades_data['Matrikelnummer'] = mandatory_modules_grades_data['Matrikelnummer'].astype(str)

        return mandatory_modules_grades_data

    @st.cache_data
    def get_prefrence_options():
        connection_columns_info = sqlite3.connect(r'../Databases/Columns Info Database.db')

        columns_info_data = pd.read_sql('Select * from columns_info_data',
                                        connection_columns_info)

        columns_info_data.columns = ['id', 'Datum', 'Spalte', 'Beschreibung']
        preferences_options = columns_info_data[columns_info_data['Beschreibung'] == 'Präferenz']['Spalte'].values

        return preferences_options

    needed_columns = [
        'id',
        'Datum',
        "Vorname",
        "Nachname",
        "Geburtsdatum",
        "Matrikelnummer",
        "Einführung in die Wirtschaftsinformatik",
        "Einführung in die Programmierung",
        "Einführung in die Wirtschaftswissenschaften",
        "Mathematik für Wirtschaftsinformatiker 1",
        "Wissenschaftliches Arbeiten",
        "Entwicklung grafischer Bedienoberflächen",
        "Datenbanksysteme",
        "Algorithmen und Datenstrukturen",
        "Rechnungswesen",
        "Mathematik für Wirtschaftsinformatiker 2",
        "Operations Management",
        "Wirtschaftsinformatik-Seminar I (Proseminar)",
        "Softwaretechnik",
        "Grundlagen der Informationssicherheit",
        "Projektmanagement - Planspiel und Fallstudie",
        "Organisationslehre",
        "Wirtschaftsstatistik",
        "Kommerzielle Standardsoftware",
        "Wirtschaftsinformatik-Projekt 1 (Softwaretechnik)",
        "Business Intelligence",
        "Entwicklung betrieblicher Informationssysteme",
        "Wirtschaftsinformatik-Seminar 2 (Hauptseminar)",
        "Wirtschaftsinformatik-Projekt 2",
        "IT-Management",
        "Digitale Geschäftsprozesse",
        "Privat- und Arbeitsrecht sowie Rechtliche Aspekte der Informatik"
    ]

    mandatory_modules_grades_data = get_student_data()
    # st.dataframe(mandatory_modules_grades_data)

    # Datentypen konvertieren in richtiges Foramt
    mandatory_modules_grades_data['Geburtsdatum'] = pd.to_datetime(
        mandatory_modules_grades_data['Geburtsdatum']).dt.date
    mandatory_modules_grades_data['Matrikelnummer'] = mandatory_modules_grades_data['Matrikelnummer'].astype(int)

    # Studenten daten holen (filtern nach Matrikelnummer und Geburtsdatum)
    student_mandatory_modules_grades_data = mandatory_modules_grades_data[
        (mandatory_modules_grades_data['Geburtsdatum'] == student_date_of_birth) & (
                mandatory_modules_grades_data['Matrikelnummer'] == student_matriculation_number)]

    # Matrikelnummer formatieren
    student_mandatory_modules_grades_data['Matrikelnummer'] = student_mandatory_modules_grades_data[
        'Matrikelnummer'].astype(str)
    try:
        first_name = student_mandatory_modules_grades_data['Vorname'].values[0]
        last_name = student_mandatory_modules_grades_data['Nachname'].values[0]


    except:
        first_name = ''
        last_name = ''

    # Wenn der Sidebar-Button gedrückt wurde
    if sidebar_button == 'strengths_prediction':
        if len(first_name) > 1:
            # Hallo  Vorname Nachname
            st.markdown(
                f"""
                                        <div style='text-align: center; font-weight: bold; font-size: 2.7vw; color:#B8860B;'> Hallo 
                                        <div style='text-align: center; font-weight: bold; font-size: 3.7vw; color:black;text-shadow: 2px 2px 15px #B8860B;'>
                                        {first_name} {last_name}
                                        </div>
                                        </div>
                                         """,
                unsafe_allow_html=True
            )
            # Eine horizontale zwei Pixel Linie hinzufügen
            draw_line(2)

            # Pflichtfächer Noten (Prognose)
            st.markdown(
                f"""
                                     <div style='text-align: center; font-weight: bold; font-size: 1.2vw;'>
                                         Ihre bisherigen Noten in Pflichtfächern
                                     </div>
                                     """,
                unsafe_allow_html=True
            )
            st.write('')
            st.write('')

            st.dataframe(student_mandatory_modules_grades_data)

            preferences_columns, mandatory_modules_columns = get_columns_info()

            # Lade den Datensatz für den ausgewählten Studenten
            model_X_data = student_mandatory_modules_grades_data.loc[:, mandatory_modules_columns]

            # Lade die Imputers, Scalers und das beste Modell
            imputer_X, imputer_y, scaler_X, scaler_y, bestes_trainiertes_model_strength_prediction = get_imputers_and_scaler_and_best_model()

            # Features und Target Spalten festlegen
            X_columns = mandatory_modules_columns
            y_columns_strengths_prediction = preferences_columns

            X_y_columns_strengths_prediction = X_columns + y_columns_strengths_prediction

            # Features und Target Daten
            X = model_X_data[X_columns]

            # X Imputed
            X_imputed = pd.DataFrame(imputer_X.transform(X),
                                     columns=X_columns)

            # X Scaled
            X_scaled = pd.DataFrame(scaler_X.transform(X_imputed),
                                    columns=X_columns)

            # st.write(X_imputed)
            # st.write(X_scaled)

            # Eine horizontale ein Pixel Linie hinzufügen
            draw_line(1)

            y_strengths_predicted_row = pd.DataFrame(bestes_trainiertes_model_strength_prediction.predict(X_scaled),
                                                     columns=y_columns_strengths_prediction)

            # Ergebnis-Daten transponieren
            y_strengths_predicted_row = y_strengths_predicted_row.transpose().reset_index()
            y_strengths_predicted_row.columns = ['Stärke', 'Prozentwert']

            y_strengths_predicted_row['Vorhanden'] = y_strengths_predicted_row['Prozentwert'].apply(
                lambda x: 'Ja' if x >= 0.5 else 'Nein')

            # Stärken (Prognose)
            st.markdown(
                f"""
                                     <div style='text-align: center; font-weight: bold; font-size: 1.2vw;'>
                                         Prognose für Ihre Stärken
                                     </div>
                                     """,
                unsafe_allow_html=True
            )
            st.write('')
            st.write('')

            y_strengths_predicted_row = y_strengths_predicted_row.sort_values(by='Prozentwert',
                                                                              ascending=False)
            strengths_col_one, strengths_col_two, strengths_col_three = st.columns(3)
            with strengths_col_one:
                iteration = 1
                for index, row in y_strengths_predicted_row.loc[:, ['Stärke', 'Prozentwert', 'Vorhanden']].iterrows():
                    if iteration % 3 == 1:
                        create_pie_chart(row)
                    iteration += 1

            with strengths_col_two:
                iteration = 1
                for index, row in y_strengths_predicted_row.loc[:, ['Stärke', 'Prozentwert', 'Vorhanden']].iterrows():
                    if iteration % 3 == 2:
                        create_pie_chart(row)
                    iteration += 1

            with strengths_col_three:
                iteration = 1
                for index, row in y_strengths_predicted_row.loc[:, ['Stärke', 'Prozentwert', 'Vorhanden']].iterrows():
                    if iteration % 3 != 1 and iteration % 3 != 2:
                        create_pie_chart(row)
                    iteration += 1

            # st.write(y_strengths_predicted_row)

            # Eine horizontale ein Pixel Linie hinzufügen
            draw_line(1)

            # Vorhandene Stärken (Google Gemini)
            st.markdown(
                f"""
                                         <div style='text-align: center; font-weight: bold; font-size: 1.2vw;'>
                                             {(str(selected_tipps)+'e').capitalize()} Tipps von Google Gemini, um Schwächen gezielt zu verbessern
                                         </div>
                                         """,
                unsafe_allow_html=True
            )
            st.write('')
            st.write('')

            #st.write(y_strengths_predicted_row)
            try:
                result = give_me_tipps(y_strengths_predicted_row,selected_tipps)
                st.write(result)

            except:
                st.warning('Google Gemini braucht einen neuen API-Key 😜')

            # Eine horizontale ein Pixel Linie hinzufügen
            draw_line(1)

            st.write('')
            st.write('')

            st.success('Erfolgreich 😊😊')



        else:
            # Fehlermedlung (Eingaben korrigieren)
            st.markdown(
                f"""
                                <div style='text-align: center; font-weight: bold; font-size: 1.2vw; color:#B8860B;'> Keine Daten vorhanden 
                                <div style='text-align: center; font-weight: bold; font-size: 2.2vw; color:black;text-shadow: 2px 2px 15px #B8860B;'>
                                Bitte überprüfen Sie Ihre Eingaben 😊😊
                                </div>
                                </div>
                                 """,
                unsafe_allow_html=True
            )

            # Eine horizontale drei Pixel Linie hinzufügen
            draw_line(3)

    # Footer importieren
    import Footer as ft
    ft.run_footer(language_index=language_index)
