def run_feedback_comments(language_index,feedbacks):
    import streamlit as st
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

    try:

        feedbacks = feedbacks.sort_values(by=['date','time'],
                                   ascending=[False,False])

        df_length = len(feedbacks['date'])

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





    except:
        st.warning('Keine Feedbacks')

    #  Eine horizontale drei Pixel Linie hinzufügen
    draw_line(3)

    st.success('Erfolgreich')
    # Footer importieren
    import Footer as ft
    ft.run_footer(language_index=language_index)
