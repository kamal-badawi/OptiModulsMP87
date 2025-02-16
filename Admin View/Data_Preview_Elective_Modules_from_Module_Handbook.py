def run_preview_loading_elective_modules_from_module_handbook(language_index,data_type):
    import streamlit as st
    import sqlite3
    import pandas as pd

    # Erstelle eine dicke Linie Funktion
    def draw_line(groesse):
        st.markdown(f"<hr style='border: {groesse}px solid black;'>", unsafe_allow_html=True)

    # Lade die Daten aus der Datenbank
    @st.cache_data
    def get_sql_data(database_name, table_name):
        connection = sqlite3.connect(rf'../Databases/{database_name}.db')

        data = pd.read_sql(rf'Select * from {table_name}',
                           connection)

        return data

    # Daten aus der Datenbank laden und in einer DataFrame speichern
    data = get_sql_data('Elective Modules Info (Module Handbook) Database',
                        'elective_modules_from_module_handbook_data')

    # Daten auf der Maske ausgeben
    st.dataframe(data, use_container_width=True)

    #  Eine horizontale drei Pixel Linie hinzufügen
    draw_line(3)

    st.success(f'{data_type} wurden erfolgreich geladen')

    # Footer importieren
    import Footer as ft
    ft.run_footer(language_index=language_index)
