def run_data_loading_student_mandatory_modules_grades_data(language_index,data_type):
    import streamlit as st
    import pandas as pd

    # Erstelle eine dicke Linie Funktion
    def draw_line(groesse):
        st.markdown(f"<hr style='border: {groesse}px solid black;'>", unsafe_allow_html=True)

    # Datenbanktabelle erstellen
    def create_database_table():
        import sqlite3

        connection = sqlite3.connect(r'../Databases/Student Mandatory Modules Grades Database.db')

        cursor = connection.cursor()
        # Tabelle löschen

        try:
            cursor.execute('delete from mandatory_modules_grades_data')
        except:
            pass

        cursor.execute('''
               create table if not exists mandatory_modules_grades_data (
               id integer primary key autoincrement,
               date text,
               first_name text,
               last_name text,
               date_of_birth text,
               matriculation_number integer,
               introduction_to_business_informatics integer,
               introduction_to_programming integer,
               introduction_to_economics integer,
               mathematics_for_business_informatics_1 integer,
               scientific_work integer,
               development_of_graphical_user_interfaces integer,
               database_systems integer,
               algorithms_and_data_structures integer,
               accounting integer,
               mathematics_for_business_informatics_2 integer,
               operations_management integer,
               business_informatics_seminar_i_proseminar integer,
               software_engineering integer,
               fundamentals_of_information_security integer,
               project_management_simulation_and_case_study integer,
               organizational_theory integer,
               business_statistics integer,
               commercial_standard_software integer,
               business_informatics_project_1_software_engineering integer,
               business_intelligence integer,
               development_of_enterprise_information_systems integer,
               business_informatics_seminar_2_advanced_seminar integer,
               business_informatics_project_2 integer,
               it_management integer,
               digital_business_processes integer,
               private_and_labor_law_and_legal_aspects_of_computer_science integer
              
               )  
               ''')
        connection.commit()

        return connection

    upload_file_load_mandatory_modules_grades = st.file_uploader('Lade die Pflichtfäcehrnoten hoch',
                                                     type=['xlsx', 'xls'],
                                                     key='upload_file_load_mandatory_modules_grades')

    if upload_file_load_mandatory_modules_grades:
        # Eine horizontale zwei Pixel Linie hinzufügen
        draw_line(2)
        loaded_mandatory_modules_grades_show = pd.read_excel(upload_file_load_mandatory_modules_grades)
        st.dataframe(loaded_mandatory_modules_grades_show)

    #  Eine horizontale drei Pixel Linie hinzufügen
    draw_line(3)

    if st.button("Daten in die Datenbank hochladen"):

        if upload_file_load_mandatory_modules_grades:
            loaded_mandatory_modules_grades = pd.read_excel(upload_file_load_mandatory_modules_grades)

            needed_columns =  [
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
            if list(loaded_mandatory_modules_grades.columns) == needed_columns:
                # erstelle die Datenbanktabelle

                # Leere die Datenbanktabelle
                import sqlite3
                import datetime

                # Aktuelles Datum
                current_date =  datetime.datetime.now().strftime('%Y-%m-%d')

                connection = create_database_table()

                cursor = connection.cursor()

                # Neue Daten eingeben
                for index, data in loaded_mandatory_modules_grades.iterrows():
                    # Zuweisung von Variablen mit den Werten aus `data`
                    first_name = data['Vorname']
                    last_name = data['Nachname']
                    date_of_birth = pd.to_datetime(data['Geburtsdatum'], format='%Y-%m-%d').date()
                    matriculation_number = data['Matrikelnummer']
                    introduction_to_business_informatics = data["Einführung in die Wirtschaftsinformatik"]
                    introduction_to_programming = data["Einführung in die Programmierung"]
                    introduction_to_economics = data["Einführung in die Wirtschaftswissenschaften"]
                    mathematics_for_business_informatics_1 = data["Mathematik für Wirtschaftsinformatiker 1"]
                    scientific_work = data["Wissenschaftliches Arbeiten"]
                    development_of_graphical_user_interfaces = data["Entwicklung grafischer Bedienoberflächen"]
                    database_systems = data["Datenbanksysteme"]
                    algorithms_and_data_structures = data["Algorithmen und Datenstrukturen"]
                    accounting = data["Rechnungswesen"]
                    mathematics_for_business_informatics_2 = data["Mathematik für Wirtschaftsinformatiker 2"]
                    operations_management = data["Operations Management"]
                    business_informatics_seminar_i_proseminar = data["Wirtschaftsinformatik-Seminar I (Proseminar)"]
                    software_engineering = data["Softwaretechnik"]
                    fundamentals_of_information_security = data["Grundlagen der Informationssicherheit"]
                    project_management_simulation_and_case_study = data["Projektmanagement - Planspiel und Fallstudie"]
                    organizational_theory = data["Organisationslehre"]
                    business_statistics = data["Wirtschaftsstatistik"]
                    commercial_standard_software = data["Kommerzielle Standardsoftware"]
                    business_informatics_project_1_software_engineering = data[
                        "Wirtschaftsinformatik-Projekt 1 (Softwaretechnik)"]
                    business_intelligence = data["Business Intelligence"]
                    development_of_enterprise_information_systems = data[
                        "Entwicklung betrieblicher Informationssysteme"]
                    business_informatics_seminar_2_advanced_seminar = data[
                        "Wirtschaftsinformatik-Seminar 2 (Hauptseminar)"]
                    business_informatics_project_2 = data["Wirtschaftsinformatik-Projekt 2"]
                    it_management = data["IT-Management"]
                    digital_business_processes = data["Digitale Geschäftsprozesse"]
                    private_and_labor_law_and_legal_aspects_of_computer_science = data[
                        "Privat- und Arbeitsrecht sowie Rechtliche Aspekte der Informatik"]

                    # Verbindung zur SQLite-Datenbank herstellen (oder Datenbank erstellen)

                    cursor.execute('''
                                    INSERT INTO mandatory_modules_grades_data (date,
                                first_name,
                                last_name,
                                date_of_birth,
                                matriculation_number, 
                                introduction_to_business_informatics,
                                introduction_to_programming,
                                introduction_to_economics,
                                mathematics_for_business_informatics_1,
                                scientific_work,
                                development_of_graphical_user_interfaces,
                                database_systems,
                                algorithms_and_data_structures,
                                accounting,
                                mathematics_for_business_informatics_2,
                                operations_management,
                                business_informatics_seminar_i_proseminar,
                                software_engineering,
                                fundamentals_of_information_security,
                                project_management_simulation_and_case_study,
                                organizational_theory,
                                business_statistics,
                                commercial_standard_software,
                                business_informatics_project_1_software_engineering,
                                business_intelligence,
                                development_of_enterprise_information_systems,
                                business_informatics_seminar_2_advanced_seminar,
                                business_informatics_project_2,
                                it_management,
                                digital_business_processes,
                                private_and_labor_law_and_legal_aspects_of_computer_science
                               ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
                                   (current_date,
                                    first_name,
                                    last_name,
                                    date_of_birth,
                                    matriculation_number,
                                    introduction_to_business_informatics,
                                    introduction_to_programming,
                                    introduction_to_economics,
                                    mathematics_for_business_informatics_1,
                                    scientific_work,
                                    development_of_graphical_user_interfaces,
                                    database_systems,
                                    algorithms_and_data_structures,
                                    accounting,
                                    mathematics_for_business_informatics_2,
                                    operations_management,
                                    business_informatics_seminar_i_proseminar,
                                    software_engineering,
                                    fundamentals_of_information_security,
                                    project_management_simulation_and_case_study,
                                    organizational_theory,
                                    business_statistics,
                                    commercial_standard_software,
                                    business_informatics_project_1_software_engineering,
                                    business_intelligence,
                                    development_of_enterprise_information_systems,
                                    business_informatics_seminar_2_advanced_seminar,
                                    business_informatics_project_2,
                                    it_management,
                                    digital_business_processes,
                                    private_and_labor_law_and_legal_aspects_of_computer_science))

                # Änderungen speichern und Verbindung schließen
                connection.commit()
                connection.close()

                st.success(f'{data_type} wurden erfolgreich in die Datenbank hochgeladen')



            else:
                st.warning(f'Datenstruktur muss wie folgt sein: \n \n {needed_columns}')

        else:
            st.warning('Excel-Datei auswählen')