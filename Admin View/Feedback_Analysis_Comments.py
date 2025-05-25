def run_feedback_comments(language_index,feedbacks,  feedback_date_from, feedback_date_to):
    import streamlit as st
    import google.generativeai as genai
    from dotenv import load_dotenv
    import os
    from pathlib import Path
    import pandas as pd
    import sqlite3
    import Process_Button_Styling
    import Background_Style
    Process_Button_Styling.run_process_button_style()
    Background_Style.run_background_styl()

    # Erstelle eine dicke Linie Funktion
    def draw_line(groesse):
        st.markdown(f"<hr style='border: {groesse}px solid black;'>", unsafe_allow_html=True)

    # Erstelle eine dicke Linie Funktion (dashed)
    def draw_dashed_line(groesse):
        st.markdown(f"<hr style='border: {groesse}px dashed black;'>", unsafe_allow_html=True)

        # Fragen erstellen, um die Kompetenzen festzustellen.

    @st.cache_resource
    def create_action_recommendations(comments,  feedback_date_from, feedback_date_to):
        env_path = Path(__file__).resolve().parent.parent / '.env'
        load_dotenv(dotenv_path=env_path)
        API_KEY = os.getenv("GOOGLE_GEMINI_API_KEY")

        genai.configure(api_key=API_KEY)

        prompt = f"""
        Du bist ein erfahrener Data Analyst und unterstützt die Technische Hochschule Mittelhessen bei der Weiterentwicklung des KI-gestützten Systems "OptiModuls".

        Deine Aufgabe besteht darin, die folgenden Kommentare von Studierenden aus dem Zeitraum {feedback_date_from} bis {feedback_date_to} zu analysieren:
        {comments}

        Leite auf Basis dieser Kommentare konkrete Handlungsempfehlungen für die Hochschule ab.

        Hintergrund zu OptiModuls:
        OptiModuls ist ein KI-gestütztes System, das Studierende bei der Auswahl geeigneter Wahlpflichtfächer unterstützt. 
        Es kann auf Basis der bisherigen Leistungen in Pflichtfächern die Noten in Wahlpflichtfächern prognostizieren sowie individuelle Stärken erkennen.
        Darüber hinaus schlägt es passende Stellenangebote (z. B. über LinkedIn) vor und identifiziert Kompetenzen der Studierenden durch gezielte Fragen.

        Bitte analysiere die Kommentare sorgfältig und gib praxisnahe Empfehlungen zur Verbesserung von OptiModuls sowie zur Steigerung der Zufriedenheit der Studierenden.
        """

        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)

        return response.text

    try:

        # feedbacks nach dem Datum absteigend sortieren
        feedbacks = feedbacks.sort_values(by=['date','time'],
                                   ascending=[False,False])

        df_length = len(feedbacks['date'])

        # Header definieren
        date_col, time_col, comment_col, rating_col, nps_col, sentiment_col, answers_col = st.columns([1,1,2,1,1.5,0.5,1])
        with date_col:
            st.markdown(f"**Datum**")

        with time_col:
            st.markdown(f"**Uhrzeit**")

        with comment_col:
            st.markdown(f"**Kommentar**")

        with rating_col:
            st.markdown(f"**Bewertung**")

        with nps_col:
            st.markdown(f"**Net Promoter Score**")

        with sentiment_col:
            st.markdown(f"**Stimmung**")

        with answers_col:
            st.markdown(f"**Antworten-Score**")

        #  Eine horizontale 1-Pixel Linie hinzufügen
        draw_line(1)


        # Feedback-Werte auf der Maske ausgeben
        counter = 0
        for index, row in feedbacks.iterrows():
            counter = counter + 1
            sentiment_score  = '😊' if row['sentiment_text'] == 'Positive' else ('😐' if row['sentiment_text'] == 'Neutral' else '☹️')

            answers_score = (
                row['app_support_subjects'] +
                row['forecast_accuracy'] +
                row['strengths_awareness'] +
                row['strength_tips_effectiveness'] +
                row['subject_selection_ease'] +
                row['subject_relevance'] +
                row['career_match_helpfulness'] +
                row['ui_evaluation'] +
                row['navigation_ease'] +
                row['feature_gap'] +
                row['decision_influence'] +
                row['subject_career_link'] +
                row['recommendation_likelihood'] +
                row['forecast_reliability'] +
                row['tips_personalization_importance']
            )

            date_col, time_col, comment_col, rating_col, nps_col, sentiment_col, answers_col = st.columns([1,1,2,1,1.5,0.5,1])
            with date_col:
                st.markdown(f"{row['date']}")

            with time_col:
                st.markdown(f"{row['time']}")

            with comment_col:
                st.markdown(f"{row['feedback_text']}")


            with rating_col:
                st.markdown(f" <span style='color: gold;'>{row['count_of_feedback_stars'] * '★'}</span>{(5- row['count_of_feedback_stars']) * '★'}", unsafe_allow_html=True)

            with nps_col:
                st.markdown(f"<span style='color: gold;'>{row['nps_score'] * '⬤'}</span> {(10- row['nps_score']) * '⬤'}", unsafe_allow_html=True)

            with sentiment_col:
                st.markdown(f"{sentiment_score}")

            with answers_col:
                answers_value = f'👍 ✖ {answers_score} '+f' 👎 ✖ {(15- answers_score)}'
                st.markdown(answers_value)



            #st.markdown(f"**{row['date']}   {row['time']}:** {row['feedback_text']} (**Bewertung:** <span style='color: gold;'>{row['count_of_feedback_stars'] * '★'}</span>{(5- row['count_of_feedback_stars']) * '★'} | **NPS:** <span style='color: gold;'>{row['nps_score'] * '⬤'}</span> {(10- row['nps_score']) * '⬤'} | **Stimmungs-Score:** {sentiment_score} | **Antworten-Score:** 👍 ✖ {answers_score}  👎 ✖ {(15- answers_score)})", unsafe_allow_html=True)

            if counter < df_length:
                #  Eine horizontale 1-Pixel Linie hinzufügen (dashed)
                draw_dashed_line(1)


        # Gemini Handlungsempfehlungen
        #  Eine horizontale 1-Pixel Linie hinzufügen
        draw_line(1)
        # Handlungsempfehlungen
        st.markdown(
            f"""
             <div style='text-align: center; font-weight: bold; font-size: 1.2vw;'>
                 Handlungsempfehlungen
             </div>
                 """,
            unsafe_allow_html=True
        )
        st.write('')
        st.write('')
        st.write('')

        comments = feedbacks['feedback_text'].to_list()
        action_recommendations = create_action_recommendations(comments,  feedback_date_from, feedback_date_to)
        st.write(action_recommendations)


    except:
        st.warning('Keine Feedbacks')

    #  Eine horizontale drei Pixel Linie hinzufügen
    draw_line(3)

    st.success('Erfolgreich')
    # Footer importieren
    import Footer as ft
    ft.run_footer(language_index=language_index)
