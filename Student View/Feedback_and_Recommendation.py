

def run_feedback_and_recommendation(language_index,title):
    from transformers import pipeline, MarianMTModel, MarianTokenizer
    import streamlit as st
    from streamlit_star_rating import st_star_rating
    from streamlit_text_rating.st_text_rater import st_text_rater
    import datetime
    import Centred_Title
    import Background_Style
    import Process_Button_Styling

    Process_Button_Styling.run_process_button_style()
    Background_Style.run_background_styl()

    # Erstelle eine dicke Linie Funktion
    def draw_line(groesse):
        st.markdown(f"<hr style='border: {groesse}px solid black;'>", unsafe_allow_html=True)

    def create_database_table():
        import sqlite3

        connection = sqlite3.connect(r'../Databases/Students Feedbacks Database.db')
        cursor = connection.cursor()

        cursor.execute('''
        create table if not exists students_feedback_data (
        id integer primary key autoincrement,
        date text,
        time text,
        count_of_feedback_stars integer,
        feedback_text text,
        sentiment_text text,
        sentiment_probability real,
        nps_score integer,
        app_support_subjects integer,
        forecast_accuracy integer,
        strengths_awareness integer,
        strength_tips_effectiveness integer,
        subject_selection_ease integer,
        subject_relevance integer,
        career_match_helpfulness integer,
        ui_evaluation integer,
        navigation_ease integer,
        feature_gap integer,
        decision_influence integer,
        subject_career_link integer,
        recommendation_likelihood integer,
        forecast_reliability integer,
        tips_personalization_importance integer)  
        ''')
        connection.commit()
        return  connection

    create_database_table()





    # Wahrscheinlichkeiten Erklärungen visualisieren
    def make_probability_metric(probability_text, probability_value):

        if probability_text == 'Sehr sicher':
            text_color = 'green'
        elif probability_text == 'Moderat sicher':
            text_color = '#FFD700'
        elif probability_text == 'Unsicher':
            text_color = '#871614'

        st.markdown(
            f"""
               <div style='border: 1px solid black; box-shadow: 0px 0px 25px 3px black; padding: 10px; background-color: #f8f8f8; height: 100%; display: flex; flex-direction: column; justify-content: center;'>
                    <h1 style='text-align: center; background-color:#eeeeee; margin: 0; padding: 5px; height: 50%;color:{text_color};'> {probability_text}</h1>
                   <h1 style='text-align: center; background-color:#d5d5d5; margin: 0; padding: 5px; height: 50%;'>
                       <span style='color:black; '>
                       {probability_value} 
                       </span>
                   </h1>

               </div>
               """, unsafe_allow_html=True
        )

        st.write('')
        st.write('')

    # Sentiment Score visualisieren
    def make_result_score_metric(score_text, score_value):

        if score_text == 'Positive':
            text_color = 'green'
        elif score_text == 'Neutral':
            text_color = '#FFD700'
        elif score_text == 'Negative':
            text_color = '#871614'

        st.markdown(
            f"""
               <div style='border: 1px solid black; box-shadow: 0px 0px 25px 3px black; padding: 10px; background-color: #f8f8f8; height: 100%; display: flex; flex-direction: column; justify-content: center;'>
                    <h1 style='text-align: center; background-color:#eeeeee; margin: 0; padding: 5px; height: 50%;color:{text_color};'> {score_text}</h1>
                   <h1 style='text-align: center; background-color:#d5d5d5; margin: 0; padding: 5px; height: 50%;'>
                       <span style='color:black;'>
                       {score_value * 100:.2f}%
                       </span>
                   </h1>

               </div>
               """, unsafe_allow_html=True
        )

        st.write('')
        st.write('')

    # Keywords metrics visualisieren
    def make_result_keywords_metric(keyword_type, keyword_value):

        st.markdown(
            f"""
               <div style='border: 1px solid black; box-shadow: 0px 0px 25px 3px black; padding: 10px; background-color: #f8f8f8; height: 100%; display: flex; flex-direction: column; justify-content: center;'>
                    <h1 style='text-align: center; background-color:#eeeeee; margin: 0; padding: 5px; height: 50%;'> {keyword_type}</h1>
                   <h1 style='text-align: center; background-color:#d5d5d5; margin: 0; padding: 5px; height: 50%;'>
                       <span style='color:black;'>
                       {keyword_value} 
                       </span>
                   </h1>

               </div>
               """, unsafe_allow_html=True
        )

        st.write('')
        st.write('')

    # Lade Modelle
    @st.cache_resource
    def load_translation_model():
        model_name = "Helsinki-NLP/opus-mt-de-en"
        tokenizer = MarianTokenizer.from_pretrained(model_name)
        model = MarianMTModel.from_pretrained(model_name)
        return pipeline("translation", model=model, tokenizer=tokenizer)

    @st.cache_resource
    def load_finbert():
        return pipeline("sentiment-analysis", model="yiyanghkust/finbert-tone")

    @st.cache_resource
    def load_ner_model():
        return pipeline("ner", model="dbmdz/bert-large-cased-finetuned-conll03-english", aggregation_strategy="simple")

    translator = load_translation_model()
    finbert = load_finbert()
    ner_model = load_ner_model()






    # Page Title
    Centred_Title.run_centred_title(title)

    count_of_feedback_stars = 5
    count_of_feedback_stars = st_star_rating('Wie gefällt Ihnen unsere App?',
                           maxValue=5,
                           defaultValue=5,
                           key='feedback_rating',
                           dark_theme=True,
                           emoticons=True,
                           customCSS='div {background-color: #FFFCF4;}')



    # Eine horizontale zwei Pixel Linie hinzufügen
    draw_line(2)

    nps_score = st_star_rating('Würden Sie unsere App weiterempfehlen?',
                                             maxValue=10,
                                             defaultValue=10,
                                             key='count_of_nps_value',
                                             dark_theme=True,
                                             emoticons=False,
                                             customCSS='div {background-color: #FFFCF4;}')


    # Eine horizontale zwei Pixel Linie hinzufügen
    draw_line(2)
    questions = [
        "Hat die App Ihnen geholfen, Ihre Wahlpflichtfächer besser zu verstehen?",
        "Wie gut finden Sie die Prognosen für Ihre Wahlpflichtfächernoten?",
        "Fühlen Sie sich besser informiert über Ihre Stärken durch die App?",
        "Sind die Tipps zur Verbesserung Ihrer Stärken hilfreich?",
        "Wie einfach ist es, mit der App die geeigneten Wahlpflichtfächer auszuwählen?",
        "Sind die vorgeschlagenen Wahlpflichtfächer relevant für Ihre Interessen und Fähigkeiten?",
        "Wie hilfreich finden Sie die Übersicht über Berufe, die zu den gewählten Wahlpflichtfächern passen?",
        "Wie bewerten Sie die Benutzeroberfläche der App?",
        "Finden Sie die Navigation in der App intuitiv?",
        "Bietet die App alle Funktionen, die Sie benötigen?",
        "Hat die App Ihre Entscheidungen über Wahlpflichtfächer beeinflusst?",
        "Wie nützlich finden Sie die Verbindung zwischen Wahlpflichtfächern und Berufen?",
        "Würden Sie die App Ihren Freunden oder Klassenkameraden empfehlen?",
        "Wie zufrieden sind Sie mit der Genauigkeit der Notenprognosen?",
        "Wie wichtig ist Ihnen die Personalisierung der Tipps zur Verbesserung Ihrer Stärken?"
    ]

    answers = []
    for question in questions:
        answer = st_text_rater(text=question,
                               color_background='#FFFCF4',
                               font_size='26px',
                               font_weight=500,
                               default=1,
                               key=question)
        if answer == 'liked':
            answer = 1
        elif answer =='disliked':
            answer = 0
        answers.append(answer)



    # Eine horizontale zwei Pixel Linie hinzufügen
    draw_line(2)


    user_input = st.text_area("Feedback (Deutsch):",
                              height=200)

    probability_col_one, probability_col_two, probability_col_three = st.columns(3)
    with probability_col_one:
        make_probability_metric('Sehr sicher', '86% – 100%')

    with probability_col_two:
        make_probability_metric('Moderat sicher', '66% – 85%')

    with probability_col_three:
        make_probability_metric('Unsicher', '50% – 65%')
        
    # Eine horizontale drei Pixel Linie hinzufügen
    draw_line(3)

    if st.button("Feedback abschicken"):

        if user_input.strip() and (None not in answers):  #

            translated_text = translator(user_input)[0]['translation_text']

            # Eine horizontale ein Pixel Linie hinzufügen
            draw_line(1)
            # Übersetzung
            st.markdown(
                f"""
                              <div style='text-align: center; font-weight: bold; font-size: 1.2vw;'>
                                  Übersetzung ins Englische
                              </div>
                              """,
                unsafe_allow_html=True
            )
            st.write('')
            st.write('')

            st.write(translated_text)

            # Eine horizontale ein Pixel Linie hinzufügen
            draw_line(1)

            # Sentiment-Analyse
            st.markdown(
                f"""
                  <div style='text-align: center; font-weight: bold; font-size: 1.2vw;'>
                     Sentiment-Score und Keywords
                  </div>
                  """,
                unsafe_allow_html=True
            )
            st.write('')

            # Übersetzung
            sentiment = finbert(translated_text)

            for result in sentiment:
                sentiment_text = result['label']
                sentiment_probability = result['score']
                make_result_score_metric(sentiment_text, sentiment_probability)

            st.write('')
            st.write('')

            # NER KEWWORDS
            entities = ner_model(translated_text)

            keywords_col_one, keywords_col_two, keywords_col_three, keywords_col_four = st.columns(4)
            with keywords_col_one:
                iteration = 1
                for entity in entities:
                    if iteration % 4 == 1:
                        keyword_type = entity['entity_group']
                        keyword_value = entity['word']
                        make_result_keywords_metric(keyword_type, keyword_value)
                    iteration += 1

            with keywords_col_two:
                iteration = 1
                for entity in entities:
                    if iteration % 4 == 2:
                        keyword_type = entity['entity_group']
                        keyword_value = entity['word']
                        make_result_keywords_metric(keyword_type, keyword_value)
                    iteration += 1

            with keywords_col_three:
                iteration = 1
                for entity in entities:
                    if iteration % 4 == 3:
                        keyword_type = entity['entity_group']
                        keyword_value = entity['word']
                        make_result_keywords_metric(keyword_type, keyword_value)
                    iteration += 1

            with keywords_col_four:

                iteration = 1
                for entity in entities:
                    if iteration % 4 != 1 and iteration % 4 != 2 and iteration % 4 != 3:
                        keyword_type = entity['entity_group']
                        keyword_value = entity['word']
                        make_result_keywords_metric(keyword_type, keyword_value)
                    iteration += 1

            # Verbindung zur SQLite-Datenbank herstellen (oder Datenbank erstellen)
            import sqlite3
            current_date = datetime.datetime.now().date()
            current_time = datetime.datetime.now().time().strftime('%H:%M:%S')

          

            connection = sqlite3.connect(r'../Databases/Students Feedbacks Database.db')
            cursor = connection.cursor()
            cursor.execute('''
                                   INSERT INTO students_feedback_data (
                                    date,
                                    time,
                                    count_of_feedback_stars,
                                    feedback_text,
                                    sentiment_text,
                                    sentiment_probability,
                                    nps_score,
                                    app_support_subjects,
                                    forecast_accuracy,
                                    strengths_awareness,
                                    strength_tips_effectiveness,
                                    subject_selection_ease,
                                    subject_relevance,
                                    career_match_helpfulness,
                                    ui_evaluation,
                                    navigation_ease,
                                    feature_gap,
                                    decision_influence,
                                    subject_career_link,
                                    recommendation_likelihood,
                                    forecast_reliability,
                                    tips_personalization_importance) 
                                    VALUES (?, ?, ?, ?,?,?, ?, ?, ?,?, ?, ?, ?,?, ?, ?, ?,?, ?, ?, ?,?)
                                   ''', (
                                    current_date,
                                    current_time,
                                    count_of_feedback_stars,
                                    user_input,
                                    sentiment_text,
                                    sentiment_probability,
                                    nps_score,
                                    answers[0],
                                    answers[1],
                                    answers[2],
                                    answers[3],
                                    answers[4],
                                    answers[5],
                                    answers[6],
                                    answers[7],
                                    answers[8],
                                    answers[9],
                                    answers[10],
                                    answers[11],
                                    answers[12],
                                    answers[13],
                                    answers[14],


            ))

            # Änderungen speichern und Verbindung schließen
            connection.commit()
            connection.close()
            st.success('Vielen Dank für Ihr Feedback 😊😊')


        else:
            st.warning("Bitte gib einen Text ein und antworten Sie auf die Fragen.")


    # Footer importieren
    import Footer as ft
    ft.run_footer(language_index=language_index)
