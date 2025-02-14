def run_data_loading_elective_modules_from_module_handbook(language_index,data_type):
    import streamlit as st
    import pandas as pd


    # Erstelle eine dicke Linie Funktion
    def draw_line(groesse):
        st.markdown(f"<hr style='border: {groesse}px solid black;'>", unsafe_allow_html=True)


    # Datenbanktabelle erstellen
    def create_database_table():
        import sqlite3

        connection = sqlite3.connect(r'../Databases/Elective Modules Info (Module Handbook) Database.db')

        cursor = connection.cursor()
        # Tabelle löschen

        try:
            cursor.execute('delete from elective_modules_from_module_handbook_data')
        except:
            pass


        cursor.execute('''
        create table if not exists elective_modules_from_module_handbook_data (
        id integer primary key autoincrement,
        date text,
        module text,
        prerequisites text,
        frequency text,
        language text,
        performance_type text,
        career_perspective text,
        content text,
        responsible_person text
        )  
        ''')
        connection.commit()

        return  connection







    upload_file_load_elective_modules = st.file_uploader('Lade das Modulhandbuch (Wahlpflichtfächer) hoch',
                                                         type=['xlsx','xls'],
                                                         key='upload_file_Load_Elective_Modules')

    if upload_file_load_elective_modules:
        # Eine horizontale zwei Pixel Linie hinzufügen
        draw_line(2)
        loaded_elective_modules_show = pd.read_excel(upload_file_load_elective_modules)
        st.dataframe(loaded_elective_modules_show)


    #  Eine horizontale drei Pixel Linie hinzufügen
    draw_line(3)

    if st.button("Daten in die Datenbank hochladen"):

        if upload_file_load_elective_modules:
            loaded_elective_modules = pd.read_excel(upload_file_load_elective_modules)

            needed_columns= ['Modul', 'Vorraussetzungen', 'Häufigkeit', 'Sprache', 'Leistungsart', 'Berufliche Perspektive', 'Inhalt', 'Betreuer']
            if list(loaded_elective_modules.columns) == needed_columns:
                # erstelle die Datenbanktabelle


                # Leere die Datenbanktabelle
                import sqlite3
                import datetime

                # Aktuelles Datum
                current_date = datetime.datetime.now().date()

                connection = create_database_table()

                cursor = connection.cursor()

                # Neue Daten eingeben
                for index, data in loaded_elective_modules.iterrows():
                    module = data['Modul']
                    prerequisites = data['Vorraussetzungen']
                    frequency = data['Häufigkeit']
                    language = data['Sprache']
                    performance_type = data['Leistungsart']
                    career_perspective = data['Berufliche Perspektive']
                    content = data['Inhalt']
                    responsible_person = data['Betreuer']
                    # Verbindung zur SQLite-Datenbank herstellen (oder Datenbank erstellen)
                    cursor.execute('''
                                        INSERT INTO elective_modules_from_module_handbook_data (date, module, prerequisites, frequency,language, performance_type,career_perspective,content,responsible_person) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                                            ''',
                                   (current_date, module, prerequisites, frequency, language, performance_type,
                                    career_perspective, content, responsible_person))

                # Änderungen speichern und Verbindung schließen
                connection.commit()
                connection.close()



                st.success(f'{data_type} wurden erfolgreich in die Datenbank hochgeladen')



            else:
                st.warning(f'Datenstruktur muss wie folgt sein: \n \n {needed_columns}')

        else:
            st.warning('Excel-Datei auswählen')