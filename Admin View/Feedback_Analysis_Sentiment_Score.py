def run_feedback_sentiment_score(language_index,feedbacks):
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



    # Score visualisieren
    def make_sentiment_analysis_metric(score_value, count_of_scores, count_of_all_scores):
        import streamlit as st
        percent_of_scores = (count_of_scores / count_of_all_scores) * 100
        st.markdown(
            f"""
                          <div style='border: 1px solid black; box-shadow: 0px 0px 25px 3px black; padding: 10px; background-color: #f8f8f8; display: flex; flex-direction: column; justify-content: center;'>
                              <h1 style='text-align: center; background-color:#d5d5d5; margin: 0; padding: 5px; flex: 1;'>
                                  {count_of_scores}  
                              </h1>
                              <h1 style='text-align: center; background-color:#eeeeee; margin: 0; padding: 5px; flex: 1;'>
                                  <span style='color:#FFD700;'>
                                  <span style='color:#FFD700; '>‎ 
                                  </span>
                                  {score_value}
                                  </span>
                              </h1>
                              <h1 style='text-align: center; background-color:#d5d5d5; color:#009999; margin: 0; padding: 5px; flex: 1;'>{percent_of_scores:.1f} %</h1>
                          </div>
                          """, unsafe_allow_html=True)

        st.write('')
        st.write('')
        st.write('')
        st.write('')

    def create_line_chart(data, x, y, z, title):
        import plotly.express as px

        # Interaktives Liniendiagramm mit Plotly und Streamlit
        fig = px.line(data,
                      x=x,
                      y=y)

        # Hintergrund und Layout anpassen
        fig.update_layout(
            plot_bgcolor='#eeeeee',  # Hintergrundfarbe des Plots
            paper_bgcolor='#d5d5d5',  # Hintergrundfarbe der gesamten Figur
            font=dict(color='#009999'),  # Schriftfarbe
            title=dict(
                text=title,
                # Titeltext
                x=0.5,  # Zentriert den Titel
                xanchor='center',  # Verankert den Titel in der Mitte
                font=dict(size=25)  # Schriftgröße des Titels
            )

        )

        # Achsenfarben anpassen
        fig.update_xaxes(title_font=dict(color='black'), tickfont=dict(color='black'))
        fig.update_yaxes(title_font=dict(color='black'), tickfont=dict(color='black'))

        # Change the line color
        fig.update_traces(line=dict(color='#009999'))

        # Diagramm in Streamlit anzeigen
        st.plotly_chart(fig, use_container_width=True)



    try:
        feedbacks['date_converted'] = pd.to_datetime(feedbacks['date'])
        count_all_feedback = len(feedbacks['date'])
        feedbacks['sentiment_text_value'] = feedbacks['sentiment_text'].apply(
            lambda x: 1 if x == 'Positive' else (0 if x == 'Neutral' else -1))

        # Berechne den durchschnitllichen Sentiment-Score pro Datum
        grouped_avg_sentiment_Score_over_date = feedbacks.groupby('date').agg(
            avg_sentiment_scores=('sentiment_text_value', 'mean') ).reset_index()

        grouped_avg_sentiment_Score_over_date = grouped_avg_sentiment_Score_over_date.rename(columns={'date': 'Date',
                                                                                  'avg_sentiment_scores': 'Sentiment Scores (AVG)'})




        # Visualisieren
        create_line_chart(grouped_avg_sentiment_Score_over_date,
                          x='Date',
                          y='Sentiment Scores (AVG)',
                          z=False,
                          title=f'Durchschnittlicher Sentiment-Score nach Datum ({count_all_feedback} Feedbacks)')

        #############################################################################
        #############################################################################
        #############################################################################

        # Eine horizontale ein Pixel Linie hinzufügen
        draw_line(1)

        # Berechne den die Anzahl der Feedbacks pro Wochentag
        feedbacks['weekday'] = feedbacks['date_converted'].dt.weekday


        grouped_avg_sentiment_Score_over_weekday = feedbacks.groupby('weekday').agg(
            avg_sentiment_scores=('sentiment_text_value', 'mean')).reset_index()

        grouped_avg_sentiment_Score_over_weekday = grouped_avg_sentiment_Score_over_weekday.rename(columns={'weekday': 'Weekday',
                                                                                                      'avg_sentiment_scores': 'Sentiment Scores (AVG)'})

        # Visualisieren
        create_line_chart(grouped_avg_sentiment_Score_over_weekday,
                          x='Weekday',
                          y='Sentiment Scores (AVG)',
                          z=False,
                          title=f'Durchschnittlicher Sentiment-Score nach Wochentag ({count_all_feedback} Feedbacks)')


        #############################################################################
        #############################################################################
        #############################################################################

        # Eine horizontale ein Pixel Linie hinzufügen
        draw_line(1)

        # Berechne den durchschnitllichen Sentiment-Score pro Stunde
        feedbacks['hour'] = pd.to_datetime(feedbacks['date'].astype(str)+' '+feedbacks['time'].astype(str)).dt.hour

        grouped_avg_sentiment_Score_over_hour = feedbacks.groupby('hour').agg(
            avg_sentiment_scores=('sentiment_text_value', 'mean')).reset_index()

        grouped_avg_sentiment_Score_over_hour = grouped_avg_sentiment_Score_over_hour.rename(columns={'hour': 'Hour',
                                                                                  'avg_sentiment_scores': 'Sentiment Scores (AVG)'})

        # Visualisieren
        create_line_chart(grouped_avg_sentiment_Score_over_hour,
                          x='Hour',
                          y='Sentiment Scores (AVG)',
                          z=False,
                          title=f'Durchschnittlicher Sentiment-Score nach Uhrzeit ({count_all_feedback} Feedbacks)')



        #############################################################################
        #############################################################################
        #############################################################################

        # Eine horizontale ein Pixel Linie hinzufügen
        draw_line(1)

        # Sentimentergebnis analysieren
        # Sentiment Text
        st.markdown(
            f"""
                 <div style='text-align: center; font-weight: bold; font-size: 1.2vw;'>
                     Sentimentergebnis-Analyse
                 </div>
                     """,
            unsafe_allow_html=True
        )
        st.write('')
        st.write('')
        st.write('')

        sentiment_text_analysis = feedbacks['sentiment_text'].value_counts().reset_index()

        sentiment_text_analysis = sentiment_text_analysis.rename(columns={'index': 'Result',
                                                                          'sentiment_text': 'Count'})

        # Data Frame in diese Reihenfolge sortieren  'Negative' -> 'Neutral' -> 'Positive'
        order_values = ['Negative', 'Neutral', 'Positive']
        sentiment_text_analysis['Result'] = pd.Categorical(sentiment_text_analysis['Result'],
                                                           categories=order_values,
                                                           ordered=True)
        sentiment_text_analysis = sentiment_text_analysis.sort_values('Result')

        count_all_sentiment_texts = sentiment_text_analysis['Count'].sum()

        postive_sentiment_text_col, neutral_sentiment_text_col, negative_sentiment_text_col = st.columns(3)

        with postive_sentiment_text_col:
            iteration = 1
            for index, row in sentiment_text_analysis.loc[:, ['Result', 'Count']].iterrows():

                result, count = row['Result'], row['Count']
                if iteration % 3 == 1:
                    make_sentiment_analysis_metric(result, count, count_all_feedback)
                iteration += 1

        with neutral_sentiment_text_col:
            iteration = 1
            for index, row in sentiment_text_analysis.loc[:, ['Result', 'Count']].iterrows():

                result, count = row['Result'], row['Count']
                if iteration % 3 == 2:
                    make_sentiment_analysis_metric(result, count,count_all_feedback)
                iteration += 1

        with negative_sentiment_text_col:
            iteration = 1
            for index, row in sentiment_text_analysis.loc[:, ['Result', 'Count']].iterrows():

                result, count = row['Result'], row['Count']
                if iteration % 3 != 1 and iteration % 3 != 2:
                    make_sentiment_analysis_metric(result, count,count_all_feedback)
                iteration += 1

        #############################################################################
        #############################################################################
        #############################################################################

        # Probability analysieren

        # Eine horizontale ein Pixel Linie hinzufügen
        draw_line(1)
        # Scores
        st.markdown(
            f"""
                                 <div style='text-align: center; font-weight: bold; font-size: 1.2vw;'>
                                     Probability-Analyse
                                 </div>
                                     """,
            unsafe_allow_html=True
        )

        st.write('')
        st.write('')
        st.write('')

        scores_bins = [0.0, 0.60, 0.70, 0.80, 0.90, 2]
        scores_labels = ['50-60 %', '60-70 %', '70-80 %', '80-90 %', '90-100 %']

        score = feedbacks
        score['sentiment_probability_group'] = pd.cut(score['sentiment_probability'],
                                                      bins=scores_bins,
                                                      labels=scores_labels,
                                                      right=False)

        probability_analysis = score['sentiment_probability_group'].value_counts().reset_index()

        probability_analysis = probability_analysis.rename(columns={'index': 'Probability (Group)',
                                                                    'sentiment_probability_group': 'Count'})

        # Data Frame  nach sortieren Probability (Group) aufsteigend sortieren
        probability_analysis = probability_analysis.sort_values(by='Probability (Group)',
                                                                ascending=True)

        count_all_probability = probability_analysis['Count'].sum()

        score_group_one_col, score_group_two_col, score_group_three_col, score_group_four_col, score_group_five_col = st.columns(
            5)

        with score_group_one_col:
            iteration = 1
            for index, row in probability_analysis.loc[:, ['Probability (Group)', 'Count']].iterrows():
                group, count = row['Probability (Group)'], row['Count']
                if iteration % 5 == 1:
                    make_sentiment_analysis_metric(group, count,count_all_feedback)
                iteration += 1

        with score_group_two_col:
            iteration = 1
            for index, row in probability_analysis.loc[:, ['Probability (Group)', 'Count']].iterrows():
                group, count = row['Probability (Group)'], row['Count']
                if iteration % 5 == 2:
                    make_sentiment_analysis_metric(group, count,count_all_feedback)
                iteration += 1

        with score_group_three_col:
            iteration = 1
            for index, row in probability_analysis.loc[:, ['Probability (Group)', 'Count']].iterrows():
                group, count = row['Probability (Group)'], row['Count']
                if iteration % 5 == 3:
                    make_sentiment_analysis_metric(group, count,count_all_feedback)
                iteration += 1

        with score_group_four_col:
            iteration = 1
            for index, row in probability_analysis.loc[:, ['Probability (Group)', 'Count']].iterrows():
                group, count = row['Probability (Group)'], row['Count']
                if iteration % 5 == 4:
                    make_sentiment_analysis_metric(group, count,count_all_feedback)
                iteration += 1

        with score_group_five_col:
            iteration = 1
            for index, row in probability_analysis.loc[:, ['Probability (Group)', 'Count']].iterrows():
                group, count = row['Probability (Group)'], row['Count']
                if iteration % 5 != 1 and iteration % 5 != 2 and iteration % 5 != 3 and iteration % 5 != 4:
                    make_sentiment_analysis_metric(group, count,count_all_feedback)
                iteration += 1


    except:
        st.warning('Keine Feedbacks')

    #  Eine horizontale drei Pixel Linie hinzufügen
    draw_line(3)

    # Footer importieren
    import Footer as ft
    ft.run_footer(language_index=language_index)
