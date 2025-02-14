def run_data_loading_columns_info(language_index,data_type):
    import streamlit as st
    import pandas as pd


    # Erstelle eine dicke Linie Funktion
    def draw_line(groesse):
        st.markdown(f"<hr style='border: {groesse}px solid black;'>", unsafe_allow_html=True)

    # Datenbanktabelle erstellen
    def create_database_table():
        import sqlite3

        connection = sqlite3.connect(r'../Databases/Columns Info Database.db')

        cursor = connection.cursor()
        # Tabelle löschen

        try:
            cursor.execute('delete from columns_info_data')
        except:
            pass

        cursor.execute('''
            create table if not exists columns_info_data (
            id integer primary key autoincrement,
            date text,
            column text,
            description text
            )  
            ''')
        connection.commit()

        return connection

    upload_file_load_columns_info = st.file_uploader('Lade die Spalteninformationen hoch',
                                                         type=['xlsx', 'xls'],
                                                         key='upload_file_load_columns_info')

    if upload_file_load_columns_info:
        # Eine horizontale zwei Pixel Linie hinzufügen
        draw_line(2)
        loaded_columns_info_show = pd.read_excel(upload_file_load_columns_info)
        st.dataframe(loaded_columns_info_show)

    #  Eine horizontale drei Pixel Linie hinzufügen
    draw_line(3)

    if st.button("Daten in die Datenbank hochladen"):

        if upload_file_load_columns_info:
            loaded_columns_info = pd.read_excel(upload_file_load_columns_info)

            needed_columns = ['Spalte', 'Beschreibung']
            if list(loaded_columns_info.columns) == needed_columns:
                # erstelle die Datenbanktabelle

                # Leere die Datenbanktabelle
                import sqlite3
                import datetime

                # Aktuelles Datum
                current_date = datetime.datetime.now().date()

                connection = create_database_table()

                cursor = connection.cursor()

                # Neue Daten eingeben
                for index, data in loaded_columns_info.iterrows():
                    column = data['Spalte']
                    description = data['Beschreibung']

                    # Verbindung zur SQLite-Datenbank herstellen (oder Datenbank erstellen)

                    cursor.execute('''
                                            INSERT INTO columns_info_data (date, column,description) VALUES (?, ?,?)
                                                ''',
                                   (current_date,column,description))

                # Änderungen speichern und Verbindung schließen
                connection.commit()
                connection.close()

                st.success(f'{data_type} wurden erfolgreich in die Datenbank hochgeladen')



            else:
                st.warning(f'Datenstruktur muss wie folgt sein: \n \n {needed_columns}')

        else:
            st.warning('Excel-Datei auswählen')