
def run_predictions_elective_subjects_selection(language_index):
    import streamlit as st
    import pandas as pd
    import google.generativeai as genai
    from dotenv import load_dotenv
    import os
    from pathlib import Path
    from sentence_transformers import SentenceTransformer
    from sklearn.metrics.pairwise import cosine_similarity
    import Background_Style as bs
    import Predictions_Jobs_Showing
    import Process_Button_Styling as pbs


    # Hintergrundstyle hinzufügen
    bs.run_background_styl()

    # Erstelle eine dicke Linie Funktion
    def draw_line(groesse):
        st.markdown(f"<hr style='border: {groesse}px solid black;'>", unsafe_allow_html=True)


    # Metric für die Top 4 Wahlpflichtfächer erstellen
    def make_metric(rank, modul, score):
        import streamlit as st

        if score % 1 != 0:
            score  = f'{score:.3f}'
        st.markdown(
            f"""
            <div style='border: 1px solid black; box-shadow: 0px 0px 25px 3px black; padding: 10px; background-color: #f8f8f8; display: flex; flex-direction: column; justify-content: center;'>
                <h1 style='text-align: center; background-color:#d5d5d5; margin: 0; padding: 5px; flex: 1;'>
                    {rank}  
                </h1>
                <h1 style='text-align: center; background-color:#eeeeee; margin: 0; padding: 5px; flex: 1;min-height:370px;'>
                    <span style='color:#FFD700;'>
                    <span style='color:#FFD700; '>‎ </span>
                    {modul}
                    </span>
                </h1>
                <h1 style='text-align: center; background-color:#d5d5d5; color:#009999; margin: 0; padding: 5px; flex: 1;'>{score}</h1>
            </div>
            """, unsafe_allow_html=True)

        st.write('')
        st.write('')
        st.write('')
        st.write('')

    # Fragen erstellen, um die Kompetenzen festzustellen.
    @st.cache_resource
    def give_me_top_four_elective_modules(elective_modules, preferences_description):
        elective_modules = elective_modules.iloc[:,2:]
        elective_modules.columns = ['Wahlpflichtmodul', 'Voraussetzungen (Stärken)', 'Semester (Sommer- oder Winter-Semester)', 'Sprache (z. B. Englisch, Deutsch, etc.)',
                                    'Lesitungsart (z. B. Klausur, Projekt, Seminar, etc.)', 'Berufliche Ziele', 'Inhalt','Dozent']



        env_path = Path(__file__).resolve().parent.parent / '.env'
        load_dotenv(dotenv_path=env_path)
        API_KEY = os.getenv("GOOGLE_GEMINI_API_KEY")

        genai.configure(api_key=API_KEY)

        prompt = f"""
        Du bist ein hochentwickelter KI-Assistent und unterstützt einen Studenten im Bachelorstudiengang Wirtschaftsinformatik an der Technischen Hcohschule Mittelhessen bei der Auswahl der vier am besten geeigneten Wahlpflichtmodule.

        Die verfügbaren Wahlpflichtmodule sind in der ersten Spalte der folgenden Tabelle aufgeführt: {elective_modules}. Die übrigen Spalten der Tabelle enthalten beschreibende Merkmale zu jedem Modul (z. B. Inhalte, Anforderungen, Kompetenzen, Relevanz für bestimmte Berufsfelder etc.).

        Die Präferenzen des Studenten sind wie folgt beschrieben: {preferences_description}.

        Deine Aufgabe:
        1. Vergleiche die Präferenzen  {preferences_description} des Studenten mit den Informationen aus der Tabelle {elective_modules}.
        
        2. Formatiere das Ergebnis exakt wie folgt ohne zusätzliche Infos, also das Ergebnis soll genau so aussehen:
        [Modulname]<<<>>>[Modulname]<<<>>>[Modulname]<<<>>>[Modulname]"""

        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)

        return response.text


    @st.cache_data
    def load_data_from_database():
        import sqlite3
        import pandas as pd

        connection = sqlite3.connect(r'../Databases/Elective Modules Info (Module Handbook) Database.db')
        elective_modules_from_module_handbook_data = pd.read_sql_query(f'''
                select *
                from elective_modules_from_module_handbook_data
                ''', connection)
        connection.close()
        return elective_modules_from_module_handbook_data

    # WPF Infos laden
    loaded_data = load_data_from_database()

    data = loaded_data

    data.columns = ['id', 'Ladedatum', 'Modul', 'Vorraussetzungen', 'Häufigkeit', 'Sprache', 'Leistungsart',
                    'Berufliche Perspektive', 'Inhalt', 'Betreuer']

    data = data.loc[:,
           ['Modul', 'Vorraussetzungen', 'Häufigkeit', 'Sprache', 'Leistungsart', 'Berufliche Perspektive', 'Inhalt',
            'Betreuer']]

    show_data_elective_subjects_selection = st.checkbox(label='Möchten Sie die Infos der Wahlpflichtmodule einsehen?',
                                                        key='show_data_elective_subjects_selection')

    if show_data_elective_subjects_selection:
        st.dataframe(data,
                     use_container_width=True)

    # Eine horizontale zwei Pixel Linie hinzufügen
    draw_line(2)

    answer_type = st.radio('Bevorzugen Sie es, Ihre Präferenzen bezüglich der Wahlpflichtfächer frei zu formulieren oder strukturierte Fragen zu beantworten?',
                           options=['Freier Text', 'Fragen und Antworten'],
                           horizontal=True,
                           key='answer_type')



    if answer_type == 'Freier Text':
        # Eine horizontale zwei Pixel Linie hinzufügen
        draw_line(2)
        placeholder = """✔️ Bitte beschreiben Sie Ihre Stärken, in welchem Semester (Sommer- oder Winter-Semester) und in welcher Sprache Sie das Wahlpflichtfach (WPF) belegen möchten. \n\n✔️ Geben Sie außerdem an, in welcher Form (Klausur, Seminar, Projekt, etc.) Sie die Leistung erbringen wollen.\n\n✔️Teilen Sie uns mit, welche beruflichen Ziele Sie verfolgen und für welche fachlichen Inhalte Sie sich besonders interessieren.\n\n✔️Falls Sie bestimmte Dozierende bevorzugen, bei denen Sie das Wahlpflichtmodul absolvieren möchten, nennen Sie diese bitte ebenfalls.
        """

        default_value = """Ich bringe folgende Stärken mit: strukturiertes und analytisches Denken, hohe Motivation, Teamfähigkeit sowie fundierte Kenntnisse in Python und Datenanalyse.

Ich möchte das Wahlpflichtfach im Sommer Semester belegen.

Ich bevorzuge es, das Modul in Deutsch zu absolvieren.

Ich möchte die Leistung in Form einer Projektarbeit erbringen, da ich gerne praxisnah arbeite und eigene Ideen umsetze.

Beruflich strebe ich eine Position im Bereich Data Science oder Business Intelligence an, idealerweise in einem technologieorientierten Unternehmen.

Besonders interessiere ich mich für Inhalte aus den Bereichen Künstliche Intelligenz, maschinelles Lernen und datengetriebene Entscheidungsprozesse.

Falls möglich, würde ich das Modul gerne bei Prof. Dr. Breitenstein oder Falkenberg belegen, da er einen starken Praxisbezug bietet und ich seine Lehrveranstaltungen als sehr gut strukturiert und verständlich erlebt habe."""
        preferences_description = st.text_area(label= f'Erläutern Sie Ihre Präferenzen ausführlich und nachvollziehbar (mindestens 150 Zeichen)',
                                               height =450,
                                               placeholder=placeholder,
                                               value=default_value,
                                               key= f'preferences_description')


        # Eine horizontale zwei Pixel Linie hinzufügen
        draw_line(2)

    if answer_type =='Fragen und Antworten':

        # Hole aus jeder Spalte die Punkte und speichere die als Liste (Eindeutig)
        def get_under_potints(column):
            column_rows = data[column]
            options = []
            for parts in column_rows:
                for part in parts.split(', '):
                    options.append(part)
            return set(options)

        # Lade Modelle
        @st.cache_resource
        def get_model():
            model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
            return model

        # Hole die Ähnlichkeit %
        def get_similarity(column, selected_options,weights):
            selected_options = ', '.join(selected_options)
            user_vector = model.encode(selected_options)
            data[f"{column}_Vektor"] = data[column].apply(model.encode)

            # Ähnlichkeiten berechnen
            data[f"{column}_Ähnlichkeit"] = data[f"{column}_Vektor"].apply(
                lambda x: cosine_similarity([user_vector], [x])[0][0]) * weights[column]








        # Eine horizontale zwei Pixel Linie hinzufügen
        draw_line(2)



        # INHALT
        options_col, importance_col = st.columns([10,4])
        # Optionen aus jeder Spalte holen (eindeuitg) Inhalt-Spalte
        with options_col:
            content_options = get_under_potints('Inhalt')
            selected_contents = st.multiselect(label='Welche Inhalte sind Ihnen im Wahlpflichtmodul besonders wichtig?',
                                               options=content_options,
                                               key='selected_contents')

        with importance_col:
            content_importance = st.number_input(label='Wie relevant ist dieses Kriterium für Sie? (Skala von 0.25 bis 3)',
                                                 min_value=0.25,
                                                 max_value=3.0,
                                                 value=1.0,
                                                 step=0.25,
                                                 key='content_importance')

        ########################################################################################
        ########################################################################################
        ########################################################################################


        # Eine horizontale zwei Pixel Linie hinzufügen
        draw_line(2)
        options_col, importance_col = st.columns([10,4])
        # Optionen aus jeder Spalte holen (eindeuitg) Vorraussetzungen-Spalte
        with options_col:
            requirements_options = get_under_potints('Vorraussetzungen')
            selected_requirements = st.multiselect(label='Über welche Fähigkeiten verfügen Sie bereits?',
                                                   options=requirements_options,
                                                   key='selected_requirements')

        with importance_col:
            requirements_importance = st.number_input(label='Wie relevant ist dieses Kriterium für Sie? (Skala von 0.25 bis 3)',
                                                 min_value=0.25,
                                                 max_value=3.0,
                                                 value=1.0,
                                                 step=0.25,
                                                 key='requirements_importance')


        ########################################################################################
        ########################################################################################
        ########################################################################################

        # Eine horizontale zwei Pixel Linie hinzufügen
        draw_line(2)


        options_col, importance_col = st.columns([10,4])
        # Optionen aus jeder Spalte holen (eindeuitg) Häufigkeit-Spalte
        with options_col:
            frequency_options = get_under_potints('Häufigkeit')
            selected_frequency = st.multiselect(label='In welchem Semester möchten Sie das Wahlpflichtmodul belegen? ',
                                                options=frequency_options,
                                                key='selected_frequency')


        with importance_col:
            frequency_importance = st.number_input(label='Wie relevant ist dieses Kriterium für Sie? (Skala von 0.25 bis 3)',
                                                 min_value=0.25,
                                                 max_value=3.0,
                                                 value=1.0,
                                                 step=0.25,
                                                 key='frequency_importance')


        ########################################################################################
        ########################################################################################
        ########################################################################################

        # Eine horizontale zwei Pixel Linie hinzufügen
        draw_line(2)

        options_col, importance_col = st.columns([10,4])
        # Optionen aus jeder Spalte holen (eindeuitg) Sprache-Spalte
        with options_col:
            language_options = get_under_potints('Sprache')
            selected_language = st.multiselect(label='In welcher Sprache bevorzugen Sie das Wahlpflichtmodul?',
                                               options=language_options,
                                               key='selected_language')

        with importance_col:
            language_importance = st.number_input(label='Wie relevant ist dieses Kriterium für Sie? (Skala von 0.25 bis 3)',
                                                 min_value=0.25,
                                                 max_value=3.0,
                                                 value=1.0,
                                                 step=0.25,
                                                 key='language_importance')


        ########################################################################################
        ########################################################################################
        ########################################################################################

        # Eine horizontale zwei Pixel Linie hinzufügen
        draw_line(2)

        options_col, importance_col = st.columns([10,4])
        # Optionen aus jeder Spalte holen (eindeuitg) Berufliche Perspektive-Spalte
        with options_col:
            career_perspectives_options = get_under_potints('Berufliche Perspektive')
            selected_career_perspectives = st.multiselect(label='Welche beruflichen Ziele möchten Sie durch das Wahlpflichtmodul erreichen?',
                                                          options=career_perspectives_options,
                                                          key='selected_career_perspectives')

        with importance_col:
            career_perspectives_importance = st.number_input(label='Wie relevant ist dieses Kriterium für Sie? (Skala von 0.25 bis 3)',
                                                 min_value=0.25,
                                                 max_value=3.0,
                                                 value=1.0,
                                                 step=0.25,
                                                 key='career_perspectives_importance')


        ########################################################################################
        ########################################################################################
        ########################################################################################


        # Eine horizontale zwei Pixel Linie hinzufügen
        draw_line(2)

        options_col, importance_col = st.columns([10,4])
        # Optionen aus jeder Spalte holen (eindeuitg) Berufliche Leistungsart-Spalte
        with options_col:

            type_of_performance_options = get_under_potints('Leistungsart')
            selected_type_of_performance = st.multiselect(label='In welcher Form möchten Sie das Wahlpflichtmodul absolvieren?',
                                                          options=type_of_performance_options,
                                                          key='selected_type_of_performance')

        with importance_col:
            type_of_performance_importance = st.number_input(label='Wie relevant ist dieses Kriterium für Sie? (Skala von 0.25 bis 3)',
                                                         min_value=0.25,
                                                         max_value=3.0,
                                                         value=1.0,
                                                         step=0.25,
                                                         key='type_of_performance_importance')


        ########################################################################################
        ########################################################################################
        ########################################################################################

        # Eine horizontale zwei Pixel Linie hinzufügen
        draw_line(2)

        # Betreuer
        options_col, importance_col = st.columns([10,4])
        # Optionen aus jeder Spalte holen (eindeuitg) Inhalt-Spalte
        with options_col:
            responsible_persons_options = get_under_potints('Betreuer')
            selected_responsible_persons = st.multiselect(label='Bei welchem Betreuer möchten Sie das Wahlpflichtmodul gerne belegen?',
                                               options= responsible_persons_options,
                                               key='selected_responsible_persons')

        with importance_col:
            responsible_persons_importance = st.number_input(label='Wichtigkeit:',
                                                 min_value=0.25,
                                                 max_value=3.0,
                                                 value=1.0,
                                                 step=0.25,
                                                 key='selected_responsible_importance')

        ########################################################################################
        ########################################################################################
        ########################################################################################


        # Gewichte Festlegen
        weights = {'Vorraussetzungen': requirements_importance,
                   'Häufigkeit': frequency_importance,
                   'Sprache': language_importance,
                   'Leistungsart': type_of_performance_importance,
                   'Berufliche Perspektive': career_perspectives_importance,
                   'Inhalt': content_importance,
                   'Betreuer': responsible_persons_importance}



        model = get_model()
        # Eine horizontale zwei Pixel Linie hinzufügen
        draw_line(2)

    ########################################################################################
    ########################################################################################
    ########################################################################################



    selected_city_hesse_col, selected_posted_time_col= st.columns([10,4])
    with selected_city_hesse_col:
        big_german_city_options = [
                "Berlin",
                "Hamburg",
                "München",
                "Köln",
                "Frankfurt am Main",
                "Stuttgart",
                "Düsseldorf",
                "Dortmund",
                "Essen",
                "Leipzig",
                "Bremen",
                "Dresden",
                "Hannover",
                "Nürnberg",
                "Duisburg",
                "Bochum",
                "Wuppertal",
                "Bielefeld",
                "Bonn",
                "Mannheim",
                "Karlsruhe",
                "Wiesbaden",
                "Münster",
                "Aachen",
                "Kiel"
        ]

        selected_german_city = st.selectbox('In welcher Stadt in Deutschland möchten Sie nach Jobs suchen, die Ihren Präferenzen entsprechen?',
                                           options=big_german_city_options,
                                           key='selected_german_city')
    with selected_posted_time_col:
        posted_time_dict = {
            'Letzte 24 Stunden': 'r86400',  # 86400 Sekunden = 1 Tag
            'Letzte Woche': 'r604800',  # 604800 Sekunden = 7 Tage
            'Letzte 2 Wochen': 'r1209600',  # 1209600 Sekunden = 14 Tage
            'Letzte 30 Tage': 'r2592000'  # 2592000 Sekunden = 30 Tage
        }

        selected_posted_time = st.selectbox('Für welchen Zeitraum möchten Sie nach den Jobs suchen?',
                                           options=posted_time_dict.keys(),
                                           key='selected_posted_time')

    # Eine horizontale drei Pixel Linie hinzufügen
    draw_line(3)
    sorted_subjects = pd.DataFrame()

    pbs.run_process_button_style()
    if st.button('Top 4 Wahlpflichtfächer bestimmen und passende Jobs Anzeigen'):
        try:
            if answer_type == 'Fragen und Antworten':
                if selected_requirements and selected_frequency and selected_language and selected_contents and selected_career_perspectives and selected_type_of_performance and selected_responsible_persons:

                    # Alle Selektionen in einer Liste speichern
                    selections = selected_requirements,selected_frequency,selected_language,selected_contents,selected_career_perspectives,selected_type_of_performance, selected_responsible_persons

                    # Berechne die Ähnlichkeit für alle Spalten außer der der Spalte Modulname
                    iteration = 0
                    for column  in data.iloc[:,1:]:
                        get_similarity(column=column,
                                       selected_options=selections[iteration],
                                       weights=weights)

                        iteration = iteration +1

                    # Vectoren addieren und in einer neuen Spalte "Score" speichern
                    data['Score'] = data.iloc[:, 1:].select_dtypes(include='number').sum(axis=1)

                    # Ergebnisse nach Score sortieren
                    sorted_subjects = data.sort_values(by='Score', ascending=False)

                    # Benötigte Spalten auswählen
                    sorted_subjects = sorted_subjects[['Modul',
                                                       'Vorraussetzungen_Ähnlichkeit', 'Häufigkeit_Ähnlichkeit','Sprache_Ähnlichkeit',
                                                       'Leistungsart_Ähnlichkeit', 'Berufliche Perspektive_Ähnlichkeit','Inhalt_Ähnlichkeit','Betreuer_Ähnlichkeit',
                                                       'Score']]
                    # Ähnlichkeiten anzeigen
                    #st.write(sorted_subjects)

                    # Rank-Spalte hinzufügen
                    # Index von 1 zu n numerieren
                    sorted_subjects = sorted_subjects.reset_index(drop=True)
                    sorted_subjects.insert(0,'Rank',sorted_subjects.index +1)
                    #st.write('Sorted Data', sorted_subjects)


                    # Filtern nach den besten vier Wahlpflichtfächer
                    top_four_subjects = sorted_subjects[sorted_subjects['Rank']<=4]
                    top_four_subjects= top_four_subjects.loc[:, ['Rank', 'Modul', 'Score']]


                else:
                    st.warning(
                        # "Please complete your details and check them for accuracy"
                        f'Bitte vervollständigen')

            if answer_type == 'Freier Text':
                if len(preferences_description) >= 150:
                    top_four_subjects_data_list = []
                    count_of_elective_subjects = len(loaded_data)


                    top_four_subjects_raw = give_me_top_four_elective_modules(loaded_data,preferences_description)
                    for module in top_four_subjects_raw.split('<<<>>>'):
                        top_four_subjects_data_list.append(module[:-1] if module.endswith('\n') else module)

                    top_four_subjects = pd.DataFrame({
                            'Rank': [1,2,3,4],
                            'Modul': top_four_subjects_data_list,
                            'Score': [count_of_elective_subjects, count_of_elective_subjects-1,count_of_elective_subjects-2,count_of_elective_subjects-3]
                            })



                else:
                    st.warning('Mind. 150 Zeichen')





            # Eine horizontale zwei Pixel Linie hinzufügen
            draw_line(2)

            subjects_col_one, subjects_col_two, subjects_col_three, subjects_col_four = st.columns(4)

            with subjects_col_one:
                iteration = 1

                for index, row in top_four_subjects.iterrows():
                    rank, modul, score = row['Rank'], row['Modul'], row['Score']

                    if iteration % 4 == 1:
                        make_metric(rank, modul, score)
                    iteration += 1

            with subjects_col_two:
                iteration = 1
                for index, row in top_four_subjects.iterrows():
                    rank, modul, score = row['Rank'], row['Modul'], row['Score']

                    if iteration % 4 == 2:
                        make_metric(rank, modul, score)
                    iteration += 1

            with subjects_col_three:
                iteration = 1
                for index, row in top_four_subjects.iterrows():
                    rank, modul, score = row['Rank'], row['Modul'], row['Score']

                    if iteration % 4 == 3:
                        make_metric(rank, modul, score)
                    iteration += 1

            with subjects_col_four:
                iteration = 1
                for index, row in top_four_subjects.iterrows():
                    rank, modul, score = row['Rank'], row['Modul'], row['Score']
                    if iteration % 4 != 1 and iteration % 4 != 2 and iteration % 4 != 3:
                        make_metric(rank, modul, score)
                    iteration += 1

            # Eine horizontale drei Pixel Linie hinzufügen
            draw_line(3)

            st.markdown(
                f"""
                               <div style='text-align: center; font-weight: bold; font-size: 2.0vw;'>
                                   Aktuelle Jobs
                               </div>
                                   """,
                unsafe_allow_html=True
            )


            # JOBS
            top_four_subjects_list = list(top_four_subjects['Modul'])

            top_four_subjects_jobs = data[data['Modul'].isin(top_four_subjects_list)]['Berufliche Perspektive']
            top_four_subjects_jobs = list(top_four_subjects_jobs)

            all_unique_jobs = []

            for parts in top_four_subjects_jobs:
                for part in parts.split(', '):
                    all_unique_jobs.append(part)

            all_unique_jobs = list(set(all_unique_jobs))



            Predictions_Jobs_Showing.run_predictions_jobs_showing(language_index, all_unique_jobs, selected_german_city, posted_time_dict,selected_posted_time)

            st.write('')
            st.write('')
            st.success('Alles geklappt')

        except Exception as e:
            st.error(f'Fehler: {e}')


    # Footer importieren
    import Footer as ft
    ft.run_footer(language_index=language_index)
