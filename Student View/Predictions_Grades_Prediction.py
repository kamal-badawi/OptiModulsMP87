def run_predictions_grades_prediction(language_index, sidebar_button, student_date_of_birth, student_matriculation_number):
    import streamlit as st
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

    # Score visualisieren
    def make_result_metric(rank, module, grad):
        import math
        st.markdown(
            f"""
            <div style='border: 1px solid black; box-shadow: 0px 0px 25px 3px black; padding: 10px; background-color: #f8f8f8; display: flex; flex-direction: column; justify-content: center;'>
                <h1 style='text-align: center; background-color:#d5d5d5; margin: 0; padding: 5px; flex: 1;'>
                    {rank}  
                </h1>
                <h1 style='text-align: center; background-color:#eeeeee; margin: 0; padding: 5px; flex: 1;min-height:370px;'>
                    <span style='color:#FFD700;'>
                    <span style='color:#FFD700; '>‎ </span>
                    {module}
                    </span>
                </h1>
                <h1 style='text-align: center; background-color:#d5d5d5; color:#009999; margin: 0; padding: 5px; flex: 1;'>{math.ceil(grad)}</h1>
            </div>
            """, unsafe_allow_html=True)

        st.write('')
        st.write('')
        st.write('')
        st.write('')

    @st.cache_resource
    def get_imputers_and_scaler_and_best_model():
        # Lade die Imputer
        imputer_X = joblib.load(r'../Imputers/Grades-Prediction/imputer_X_grades_prediction.pkl')
        imputer_y = joblib.load(r'../Imputers/Grades-Prediction/imputer_y_grades_prediction.pkl')

        # Lade die Scaler
        scaler_X = joblib.load(r'../Scalers/Grades-Prediction/scaler_X_grades_prediction.pkl')
        scaler_y = joblib.load(r'../Scalers/Grades-Prediction/scaler_y_grades_prediction.pkl')

        # Lade das best trainierte Modell
        bestes_trainiertes_model_grades_prediction = joblib.load(
            r'../ML-Model/bestes_xgboost_modell_grades_prediction.pkl')

        return imputer_X, imputer_y, scaler_X, scaler_y, bestes_trainiertes_model_grades_prediction

    @st.cache_data
    def get_columns_info():
        connection_columns_info = sqlite3.connect(r'../Databases/Columns Info Database.db')

        columns_info_data = pd.read_sql('Select * from columns_info_data',
                                        connection_columns_info)

        columns_info_data.columns = ['id', 'Datum', 'Spalte', 'Beschreibung']
        mandatory_modules_info = list(columns_info_data[columns_info_data['Beschreibung'] == 'Pflichtmodul']['Spalte'])
        elective_modules_info = list(
            columns_info_data[columns_info_data['Beschreibung'] == 'Wahlpflichtmodul']['Spalte'])
        return mandatory_modules_info, elective_modules_info



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
    if sidebar_button == 'grades_prediction':
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

            mandatory_modules_columns, elective_modules_columns = get_columns_info()

            model_X_data = student_mandatory_modules_grades_data.loc[:, mandatory_modules_columns]

            # Lade die Imputers, Scalers und das beste Modell
            imputer_X, imputer_y, scaler_X, scaler_y, bestes_trainiertes_model_grades_prediction = get_imputers_and_scaler_and_best_model()

            # Features und Target Spalten festlegen
            X_columns = mandatory_modules_columns
            y_columns_grades_prediction = elective_modules_columns

            X_y_columns_grades_prediction = X_columns + y_columns_grades_prediction

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

            # Noten (Wahlpflichfächer)
            y_grades_predicted_row = pd.DataFrame(bestes_trainiertes_model_grades_prediction.predict(X_scaled),
                                                  columns=y_columns_grades_prediction)

            y_grades_predicted = pd.DataFrame(scaler_y.inverse_transform(y_grades_predicted_row),
                                              columns=y_columns_grades_prediction)

            # Ergebnis-Daten transponieren
            y_grades_predicted = y_grades_predicted.transpose().reset_index()

            y_grades_predicted.columns = ['Wahlpflichtmodul', 'Note']

            # st.write(y_grades_predicted)

            y_grades_predicted = y_grades_predicted.sort_values(by=['Note'],
                                                                ascending=False).reset_index()

            y_grades_predicted['rank'] = y_grades_predicted.index + 1
            # st.write(y_grades_predicted)

            # Eine horizontale ein Pixel Linie hinzufügen
            draw_line(1)

            # Pflichtfächer Noten (Prognose)
            st.markdown(
                f"""
                 <div style='text-align: center; font-weight: bold; font-size: 1.2vw;'>
                     Prognose für Ihre Wahlpflichtfächernoten
                 </div>
                 """,
                unsafe_allow_html=True
            )
            st.write('')
            st.write('')

            modules_col_one, modules_col_two, modules_col_three, modules_col_four = st.columns(4)
            with modules_col_one:
                iteration = 1
                for index, row in y_grades_predicted.loc[:, ['rank', 'Wahlpflichtmodul', 'Note']].iterrows():
                    if iteration % 4 == 1:
                        rank, module, grad = row['rank'], row['Wahlpflichtmodul'], row['Note']
                        make_result_metric(rank, module, grad)
                    iteration += 1

            with modules_col_two:
                iteration = 1
                for index, row in y_grades_predicted.loc[:, ['rank', 'Wahlpflichtmodul', 'Note']].iterrows():
                    if iteration % 4 == 2:
                        rank, module, grad = row['rank'], row['Wahlpflichtmodul'], row['Note']
                        make_result_metric(rank, module, grad)
                    iteration += 1

            with modules_col_three:
                iteration = 1
                for index, row in y_grades_predicted.loc[:, ['rank', 'Wahlpflichtmodul', 'Note']].iterrows():
                    if iteration % 4 == 3:
                        rank, module, grad = row['rank'], row['Wahlpflichtmodul'], row['Note']
                        make_result_metric(rank, module, grad)
                    iteration += 1

            with modules_col_four:

                iteration = 1
                for index, row in y_grades_predicted.loc[:, ['rank', 'Wahlpflichtmodul', 'Note']].iterrows():
                    if iteration % 4 != 1 and iteration % 4 != 2 and iteration % 4 != 3:
                        rank, module, grad = row['rank'], row['Wahlpflichtmodul'], row['Note']
                        make_result_metric(rank, module, grad)
                    iteration += 1

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
