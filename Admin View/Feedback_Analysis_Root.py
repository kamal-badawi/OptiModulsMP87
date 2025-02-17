


def run_feedback_analysis_root(language_index,title):
    import Feedback_Analysis_Comments
    import Feedback_Analysis_Questions
    import Feedback_Analysis_Rating_Stars
    import Feedback_Analysis_Sentiment_Score
    import Feedback_Analysis_NPS_Score
    import Feedback_Analysis_General_Information
    import streamlit as st
    import sqlite3
    import pandas as pd
    import Centred_Title
    import Process_Button_Styling
    import Background_Style
    Process_Button_Styling.run_process_button_style()
    Background_Style.run_background_styl()

    # Erstelle eine dicke Linie Funktion (Sidebar)
    def draw_line_sidebar(width):
        st.sidebar.markdown(f"<hr style='border: {width}px dashed #009999;'>",
                            unsafe_allow_html=True)

    # Lade die Feedbacks
    def load_feedbacks(feedback_date_from, feedback_date_to):
        try:

            connection = sqlite3.connect(r'../Databases/Students Feedbacks Database.db')
            feedbacks = pd.read_sql_query(f'''
                    select  * from students_feedback_data
                    ''', connection)

            feedbacks['date'] = pd.to_datetime(feedbacks['date']).dt.date

            feedbacks = feedbacks[
                (feedbacks['date'] >= feedback_date_from) & (feedbacks['date'] <= feedback_date_to)]
            return feedbacks
        except:
            return pd.DataFrame(columns=[
                'id' 'date' 'time' 'count_of_feedback_stars' 'feedback_text' 'sentiment_text' 'sentiment_probability' 'nps_score' 'app_support_subjects' 'forecast_accuracy' 'strengths_awareness' 'strength_tips_effectiveness' 'subject_selection_ease' 'subject_relevance' 'career_match_helpfulness' 'ui_evaluation' 'navigation_ease' 'feature_gap' 'decision_influence' 'subject_career_link' 'recommendation_likelihood' 'forecast_reliability' 'tips_personalization_importance'],
            )

    # Lade das kleinste Datum
    def load_min_date():
        try:
            connection = sqlite3.connect(r'../Databases/Students Feedbacks Database.db')
            min_date = pd.read_sql_query('select  min(date) from students_feedback_data', connection)
            return min_date
        except:
            return ''

    # Page Title
    Centred_Title.run_centred_title(title)

    # Logo sidebar
    st.sidebar.image("../Images/OptiModuls Logo.png",
                     use_column_width=True)

    # Draw Line for the sidebar (3 Pixel)
    draw_line_sidebar(3)

    feedback_options = [
        'Allgemeine Info',
        'Sternebewertung der App durch Nutzer',
        'Sentiment-Analyse: Bewertung der Stimmung (positiv, neutral, negativ)',
        'Net Promoter Score (NPS) auf einer Skala von 1 bis 10',
        'Analyse spezifischer Fragen: Aspekte, die gefallen oder missfallen',
        'Alle Fragen zur Beurteilung'
    ]

    feedback_option = st.sidebar.selectbox(label='Welches Feedback-Art wollen Sie analysieren?',
                                      options=feedback_options)

    from datetime import datetime

    current_date = datetime.today().date()
    current_time = datetime.now().time().replace(microsecond=0)
    load_min_date = load_min_date()

    # Freitext-Kommentare der Nutzer als Feedback
    if feedback_option == feedback_options[5]:
        from datetime import datetime, timedelta
        min_feedback_date = current_date - timedelta(days=2)
    else:
        min_feedback_date = datetime.strptime(load_min_date['min(date)'].values[0], '%Y-%m-%d')
    max_feedback_date = current_date








    feedback_date_from_col, feedback_date_to_col = st.sidebar.columns(2)
    with feedback_date_from_col:
        feedback_date_from = st.date_input(label='Date (Von):',
                        min_value=min_feedback_date,
                        value=min_feedback_date,
                        key='feedback_date_from')

    with feedback_date_to_col:
        feedback_date_to = st.date_input(label='Date (Bis):',
                                         max_value=max_feedback_date,
                                         value=max_feedback_date,
                                         key='feedback_date_to')

    feedbacks = load_feedbacks(feedback_date_from=feedback_date_from,
                               feedback_date_to=feedback_date_to
                               )






    # Konvertiere die Spalten in das richtige Format
    feedbacks['date'] = pd.to_datetime(feedbacks['date']).dt.date  # Nur das Datum extrahieren
    feedbacks['time'] = pd.to_datetime(feedbacks['time']).dt.time  # Nur die Uhrzeit extrahieren


    # Filtere nach Datum und Uhrzeit
    feedbacks = feedbacks[
        (feedbacks['date'] < current_date) |  # Vorherige Tage immer einschließen
        ((feedbacks['date'] == current_date) & (feedbacks['time'] <= current_time))  # Heute bis zur aktuellen Zeit
        ]

    st.write(feedbacks)
    

    # Allgemeine Info
    if feedback_option == feedback_options[0]:
        # Title festlegen
        st.sidebar.write('')
        st.sidebar.write('')
        st.sidebar.markdown(
            f"""
            <div style='text-align: center; font-weight: bold; font-size: 1.0vw;'>
                {feedback_option}
            </div>
                """,
            unsafe_allow_html=True
        )

        # Seite aufrufen
        Feedback_Analysis_General_Information.run_feedback_analysis_general_information(language_index, feedbacks)

    # Sternebewertung der App durch Nutzer
    if feedback_option == feedback_options[1]:
        # Title festlegen
        st.sidebar.write('')
        st.sidebar.write('')
        st.sidebar.markdown(
            f"""
                    <div style='text-align: center; font-weight: bold; font-size: 1.0vw;'>
                        {feedback_option}
                    </div>
                        """,
            unsafe_allow_html=True
        )

        # Seite aufrufen
        Feedback_Analysis_Rating_Stars.run_feedback_rating_stars(language_index,feedbacks)



    # Sentiment-Analyse: Bewertung der Stimmung (positiv, neutral, negativ)
    elif feedback_option == feedback_options[2]:
        # Title festlegen
        st.sidebar.write('')
        st.sidebar.write('')
        st.sidebar.markdown(
            f"""
                    <div style='text-align: center; font-weight: bold; font-size: 1.0vw;'>
                        {feedback_option}
                    </div>
                        """,
            unsafe_allow_html=True
        )

        # Seite aufrufen
        Feedback_Analysis_Sentiment_Score.run_feedback_sentiment_score(language_index,feedbacks)







    # Net Promoter Score (NPS) auf einer Skala von 1 bis 10
    elif feedback_option == feedback_options[3]:
        # Title festlegen
        st.sidebar.write('')
        st.sidebar.write('')
        st.sidebar.markdown(
            f"""
                    <div style='text-align: center; font-weight: bold; font-size: 1.0vw;'>
                        {feedback_option}
                    </div>
                        """,
            unsafe_allow_html=True
        )

        # Seite aufrufen
        Feedback_Analysis_NPS_Score.run_feedback_nps_score(language_index, feedbacks)



    # Analyse spezifischer Fragen: Aspekte, die gefallen oder missfallen
    elif feedback_option == feedback_options[4]:
        # Title festlegen
        st.sidebar.write('')
        st.sidebar.write('')
        selected_question_analysis_options_dictionary = {
            "Verständnis der Wahlpflichtfächer": "app_support_subjects",
            "Genauigkeit der Notenprognose": "forecast_accuracy",
            "Stärkenbewusstsein durch die OptiModuls-App": "strengths_awareness",
            "Hilfreichkeit der Stärkentipps": "strength_tips_effectiveness",
            "Einfachheit der Fächerwahl": "subject_selection_ease",
            "Relevanz der Wahlpflichtfächer": "subject_relevance",
            "Berufsübersicht zu Fächern": "career_match_helpfulness",
            "Bewertung der Benutzeroberfläche": "ui_evaluation",
            "Intuitivität der Navigation": "navigation_ease",
            "Vollständigkeit der OptModuls-App": "feature_gap",
            "Einfluss auf die Fachwahl": "decision_influence",
            "Verbindung von Fach und Beruf": "subject_career_link",
            "Wahrscheinlichkeit der Empfehlung": "recommendation_likelihood",
            "Zuverlässigkeit der Prognosen": "forecast_reliability",
            "Wichtigkeit der Personalisierung": "tips_personalization_importance"
        }

        selected_question_analysis_options = selected_question_analysis_options_dictionary.keys()
        selected_question = st.sidebar.selectbox('Welche Frage wollen Sie untersuchen?',
                                                 options=selected_question_analysis_options,
                                                 key='selected_question_feedback_analysis')

        st.sidebar.write('')
        st.sidebar.write('')
        st.sidebar.markdown(
            f"""
                    <div style='text-align: center; font-weight: bold; font-size: 1.0vw;'>
                        {feedback_option} ({selected_question})
                    </div>
                        """,
            unsafe_allow_html=True
        )

        # Seite aufrufen
        Feedback_Analysis_Questions.run_feedback_questions(language_index, feedbacks,selected_question_analysis_options_dictionary,selected_question)

    # Freitext-Kommentare der Nutzer als Feedback
    elif feedback_option == feedback_options[5]:
        # Title festlegen
        st.sidebar.write('')
        st.sidebar.write('')
        st.sidebar.markdown(
            f"""
                        <div style='text-align: center; font-weight: bold; font-size: 1.0vw;'>
                            {feedback_option}
                        </div>
                            """,
            unsafe_allow_html=True
        )

        # Seite aufrufen
        Feedback_Analysis_Comments.run_feedback_comments(language_index, feedbacks)

