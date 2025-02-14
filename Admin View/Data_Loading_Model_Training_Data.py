def run_data_loading_model_training_data(language_index,data_type):
    import streamlit as st
    import pandas as pd



    # Erstelle eine dicke Linie Funktion
    def draw_line(groesse):
        st.markdown(f"<hr style='border: {groesse}px solid black;'>", unsafe_allow_html=True)

    # Datenbanktabelle erstellen
    def create_database_table():
        import sqlite3

        connection = sqlite3.connect(r'../Databases/Model Training Database.db')

        cursor = connection.cursor()
        # Tabelle löschen

        try:
            cursor.execute('delete from model_training_data')
        except:
            pass

        cursor.execute('''
        create table if not exists model_training_data (
        id integer primary key autoincrement,
        date text,
        introduction_to_business_informatics,
        introduction_to_programming integer,
        introduction_to_economics,
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
        private_and_labor_law_and_legal_aspects_of_computer_science integer,
        
        
        analytical_thinking integer,
        problem_solving_skills integer,
        programming_knowledge integer,
        database_management integer,
        communication_skills integer,
        it_security_awareness integer,
        organizational_and_project_management integer,
        teamwork_and_collaboration integer,
        business_acumen integer,
        technological_innovation integer,
        legal_understanding integer,
        mathematical_competence integer,
   
        
        business_process_management_with_sap integer,
        predictive_analytics_with_python integer,
        web_technology integer,
        agile_methods_in_practice integer,
        auditing_it_audit integer,
        applied_software_engineering_with_lego_mindstorm integer,
        system_and_software_development_for_driver_assistance_systems integer,
        automotive_data_driven_business integer,
        cyber_security_threat_modelling_lecture integer,
        standards_and_regulations_for_it_security integer,
        requirements_engineering integer,
        big_data integer,
        fundamentals_of_ai integer,
        devops integer
        )  
        ''')
        connection.commit()

        return connection



    upload_file_load_model_training_data = st.file_uploader('Lade die Training Daten hoch',
                                                         type=['xlsx', 'xls'],
                                                         key='upload_file_load_model_training_data')

    if upload_file_load_model_training_data:
        # Eine horizontale zwei Pixel Linie hinzufügen
        draw_line(2)
        loaded_model_training_data_show = pd.read_excel(upload_file_load_model_training_data)
        st.dataframe(loaded_model_training_data_show)

    #  Eine horizontale drei Pixel Linie hinzufügen
    draw_line(3)

    if st.button("Daten in die Datenbank hochladen"):

        if upload_file_load_model_training_data:
            loaded_elective_modules = pd.read_excel(upload_file_load_model_training_data)

            modules_de = [
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
                "Privat- und Arbeitsrecht sowie Rechtliche Aspekte der Informatik",

                "Analytisches Denken",
                "Problemlösungsfähigkeit",
                "Programmierkenntnisse",
                "Datenbankmanagement",
                "Kommunikationsfähigkeit",
                "IT-Sicherheitsbewusstsein",
                "Organisations- und Projektmanagement",
                "Teamarbeit und Kollaboration",
                "Wirtschaftliches Verständnis",
                "Technologische Innovation",
                "Rechtliches Verständnis",
                "Mathematische Kompetenz",

                "Geschäftsprozessmanagement mit SAP",
                "Predictive Analytics mit Python",
                "Web-Technologie",
                "Agile Methoden in der Praxis",
                "Wirtschaftsprüfung / IT-Prüfung",
                "Angewandte Softwaretechnik mit LEGO Mindstorm",
                "System- und Softwareentwicklung für Fahrerassistenzsysteme",
                "Automotive Data Driven Business",
                "Cyber Security Threat Modelling - VL",
                "Standards und Vorschriften zur IT-Sicherheit",
                "Requirements Engineering",
                "Big Data",
                "Grundlagen der KI",
                "DevOps"
            ]


            if list(loaded_elective_modules.columns) == modules_de:
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
                    # Zuweisung von Variablen mit den Werten aus `data`
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

                    analytical_thinking = data["Analytisches Denken"]
                    problem_solving_skills = data["Problemlösungsfähigkeit"]
                    programming_knowledge = data["Programmierkenntnisse"]
                    database_management  = data["Datenbankmanagement"]
                    communication_skills = data["Kommunikationsfähigkeit"]
                    it_security_awareness = data["IT-Sicherheitsbewusstsein"]
                    organizational_and_project_management = data["Organisations- und Projektmanagement"]
                    teamwork_and_collaboration = data["Teamarbeit und Kollaboration"]
                    business_acumen = data["Wirtschaftliches Verständnis"]
                    technological_innovation = data["Technologische Innovation"]
                    legal_understanding = data["Rechtliches Verständnis"]
                    mathematical_competence = data["Mathematische Kompetenz"]

                    business_process_management_with_sap = data["Geschäftsprozessmanagement mit SAP"]
                    predictive_analytics_with_python = data["Predictive Analytics mit Python"]
                    web_technology = data["Web-Technologie"]
                    agile_methods_in_practice = data["Agile Methoden in der Praxis"]
                    auditing_it_audit = data["Wirtschaftsprüfung / IT-Prüfung"]
                    applied_software_engineering_with_lego_mindstorm = data[
                        "Angewandte Softwaretechnik mit LEGO Mindstorm"]
                    system_and_software_development_for_driver_assistance_systems = data[
                        "System- und Softwareentwicklung für Fahrerassistenzsysteme"]
                    automotive_data_driven_business = data["Automotive Data Driven Business"]
                    cyber_security_threat_modelling_lecture = data["Cyber Security Threat Modelling - VL"]
                    standards_and_regulations_for_it_security = data["Standards und Vorschriften zur IT-Sicherheit"]
                    requirements_engineering = data["Requirements Engineering"]
                    big_data = data["Big Data"]
                    fundamentals_of_ai = data["Grundlagen der KI"]
                    devops = data["DevOps"]
                    # Verbindung zur SQLite-Datenbank herstellen (oder Datenbank erstellen)

                    cursor.execute('''
                                        INSERT INTO model_training_data (date, 
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
                                    private_and_labor_law_and_legal_aspects_of_computer_science,
                                    
                                    analytical_thinking,
                                    problem_solving_skills,
                                    programming_knowledge,
                                    database_management,
                                    communication_skills,
                                    it_security_awareness,
                                    organizational_and_project_management,
                                    teamwork_and_collaboration,
                                    business_acumen,
                                    technological_innovation,
                                    legal_understanding,
                                    mathematical_competence,
        
                                    business_process_management_with_sap,
                                    predictive_analytics_with_python,
                                    web_technology,
                                    agile_methods_in_practice,
                                    auditing_it_audit,
                                    applied_software_engineering_with_lego_mindstorm,
                                    system_and_software_development_for_driver_assistance_systems,
                                    automotive_data_driven_business,
                                    cyber_security_threat_modelling_lecture,
                                    standards_and_regulations_for_it_security,
                                    requirements_engineering,
                                    big_data,
                                    fundamentals_of_ai,
                                    devops) VALUES ( ?, ?, ?, ?,?, ?, ?, ?, ?,?, ?, ?, ?, ?,?, ?, ?, ?, ?,?, ?, ?, ?, ?,?, ?, ?, ?, ?,?, ?, ?, ?, ?,?, ?, ?, ?, ?,?, ?, ?, ?, ?,?, ?, ?, ?, ?,?, ?, ?, ? )
                                            ''',
                                   (current_date,introduction_to_business_informatics,
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
                                    private_and_labor_law_and_legal_aspects_of_computer_science,
                                    analytical_thinking,
                                    problem_solving_skills,
                                    programming_knowledge,
                                    database_management,
                                    communication_skills,
                                    it_security_awareness,
                                    organizational_and_project_management,
                                    teamwork_and_collaboration,
                                    business_acumen,
                                    technological_innovation,
                                    legal_understanding,
                                    mathematical_competence ,
                                    business_process_management_with_sap,
                                    predictive_analytics_with_python,
                                    web_technology,
                                    agile_methods_in_practice,
                                    auditing_it_audit,
                                    applied_software_engineering_with_lego_mindstorm,
                                    system_and_software_development_for_driver_assistance_systems,
                                    automotive_data_driven_business,
                                    cyber_security_threat_modelling_lecture,
                                    standards_and_regulations_for_it_security,
                                    requirements_engineering,
                                    big_data,
                                    fundamentals_of_ai,
                                    devops ))

                # Änderungen speichern und Verbindung schließen
                connection.commit()
                connection.close()

                st.success(f'{data_type} wurden erfolgreich in die Datenbank hochgeladen')



            else:
                st.warning(f'Datenstruktur muss wie folgt sein: \n \n {modules_de}')

        else:
            st.warning('Excel-Datei auswählen')