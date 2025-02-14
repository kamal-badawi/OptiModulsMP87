
def run_feedback_questions(language_index,feedbacks,selected_question_analysis_options_dictionary,selected_question):
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

    # Anazhl der jeweiligen Question mit % visualsiieren
    def make_question_metric(question_value, count_of_question_values, count_of_all_questions_values):
        import streamlit as st

        percent_of_question = (count_of_question_values / count_of_all_questions_values) * 100
        st.markdown(
            f"""
                           <div style='border: 1px solid black; box-shadow: 0px 0px 25px 3px black; padding: 10px; background-color: #f8f8f8; display: flex; flex-direction: column; justify-content: center;'>
                               <h1 style='text-align: center; background-color:#d5d5d5; margin: 0; padding: 5px; flex: 1;'>
                                   {count_of_question_values}  
                               </h1>
                               <h1 style='text-align: center; background-color:#eeeeee; margin: 0; padding: 5px; flex: 1;'>
                                   <span style='color:#FFD700;'>
                                   <span style='color:#FFD700; '>‎ 
                                   </span>
                                   {question_value}
                                   </span>
                               </h1>
                               <h1 style='text-align: center; background-color:#d5d5d5; color:#009999; margin: 0; padding: 5px; flex: 1;'>{percent_of_question:.1f} %</h1>
                           </div>
                           """, unsafe_allow_html=True)

        st.write('')
        st.write('')
        st.write('')
        st.write('')

    # Pie-Chart für Stärken
    def create_pie_chart(postive_percent,data,selected_question):
        import plotly.express as px
        # Farben basierend auf den Werten zuweisen: grün für positiv, rot für negativ
        color_map = {'Positive': '#4CAF50', 'Negative': '#D1001C'}

        # Kuchendiagramm mit Plotly Express erstellen
        fig = px.pie(
            data,
            values='Value',
            names='Score',
            title='Verteilung in %',
            color='Score',  # Farbschema basierend auf den Kategorien
            color_discrete_map=color_map,  # Farben explizit festlegen
            hole=0.3  # Optional für Donut-Style
        )

        # Layout des Diagramms anpassen
        fig.update_layout(
            height=600,  # Höhe des Diagramms
            title={
                'text': f'{selected_question} ({postive_percent*100:.2f} %)',
                'x': 0.5,  # Zentrieren des Titels
                'xanchor': 'center',
                'yanchor': 'top'
            },
            title_font_size=24,  # Titelgröße
            plot_bgcolor='#eeeeee',  # Hintergrundfarbe des Plots
            paper_bgcolor='#d5d5d5',  # Hintergrundfarbe der gesamten Figur
            font=dict(color='#009999'),
            margin=dict(l=50, r=50, t=100, b=50)  # Ränder anpassen
        )

        # Darstellung des Diagramms mit Streamlit
        st.plotly_chart(fig, use_container_width=True)


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




        question_column = selected_question_analysis_options_dictionary.get(selected_question)
        answers_df = feedbacks[['date',question_column]]
        answers_df['dummy'] = 1



        answers_df = answers_df.rename(columns={question_column:'Answer'})


        answers_df['date_converted'] = pd.to_datetime(answers_df['date'])

        count_all_feedback = len(answers_df['date'])

        # Berechne den Mittelwert für die Anzahl der NPS pro Tag
        grouped_avg_count_of_nps_over_date = answers_df.groupby('date').agg(
            avg_answer_score=('Answer', 'mean')).reset_index()


        grouped_avg_count_of_nps_over_date = grouped_avg_count_of_nps_over_date.rename(columns={'date': 'Date',
                                                                                                'avg_answer_score': 'Avg Answer Score'})

        # Visualisieren
        create_line_chart(grouped_avg_count_of_nps_over_date,
                          x='Date',
                          y='Avg Answer Score',
                          z=False,
                          title=f'Durchschnittlicher Antwort-Score nach Datum für {selected_question} ({count_all_feedback} Feedbacks)')

        #############################################################################
        #############################################################################
        #############################################################################

        # Eine horizontale ein Pixel Linie hinzufügen
        draw_line(1)

        # Berechne den durschnitlichen NPS pro Wochentag
        answers_df['weekday'] = answers_df['date_converted'].dt.weekday

        grouped_avg_count_of_nps_over_weekday = answers_df.groupby('weekday').agg(
            avg_answer_score=('Answer', 'mean')).reset_index()

        grouped_avg_count_of_nps_over_weekday = grouped_avg_count_of_nps_over_weekday.rename(columns={'weekday': 'Weekday',
                                                                                                'avg_answer_score': 'Avg Answer Score'})

        # Visualisieren
        create_line_chart(grouped_avg_count_of_nps_over_weekday,
                          x='Weekday',
                          y='Avg Answer Score',
                          z=False,
                          title=f'Durchschnittlicher Antwort-Score nach Wochentag für {selected_question} ({count_all_feedback} Feedbacks)')

        #############################################################################
        #############################################################################
        #############################################################################
        # Eine horizontale ein Pixel Linie hinzufügen
        draw_line(1)

        # Berechne den durschnitlichen NPS pro pro Stunde
        answers_df['hour'] = pd.to_datetime(feedbacks['date'].astype(str)+' '+feedbacks['time'].astype(str)).dt.hour

        grouped_avg_count_of_nps_over_hour = answers_df.groupby('hour').agg(
            avg_answer_score=('Answer', 'mean')).reset_index()

        grouped_avg_count_of_nps_over_hour = grouped_avg_count_of_nps_over_hour.rename(columns={'hour': 'Hour',
                                                                                                'avg_answer_score': 'Avg Answer Score'})

        # Visualisieren
        create_line_chart(grouped_avg_count_of_nps_over_hour,
                          x='Hour',
                          y='Avg Answer Score',
                          z=False,
                          title=f'Durchschnittlicher Antwort-Score nach Uhrzeit für {selected_question} ({count_all_feedback} Feedbacks)')

        #############################################################################
        #############################################################################
        #############################################################################

        # Eine horizontale ein Pixel Linie hinzufügen
        draw_line(1)




        count_of_all_answers = len(answers_df['Answer'])
        #st.write(answers_df,count_of_all_answers)


        positive_answers_df = answers_df[answers_df['Answer'] == 1]
        count_of_positive_answers = len(positive_answers_df['Answer'])
        #st.write(positive_answers_df, count_of_positive_answers)

        negative_answers_df = answers_df[answers_df['Answer']==0]
        count_of_negative_answers =  len(negative_answers_df['Answer'])
        #st.write(negative_answers_df,count_of_negative_answers)

        piechart_df = pd.DataFrame({'Score':['Positive','Negative'],
                                    'Value':[count_of_positive_answers,count_of_negative_answers]
                                    }
                                   )

        # st.write(piechart_df)

        # Piechart erstellen
        create_pie_chart((count_of_positive_answers/count_of_all_answers),piechart_df, selected_question)
        st.write('')
        st.write('')

        answers_col_one , answers_col_two = st.columns(2)
        with answers_col_one:
            make_question_metric('Positiv',count_of_positive_answers,count_of_all_answers)

        with answers_col_two:
            make_question_metric('Negativ',count_of_negative_answers,count_of_all_answers)

        #############################################################################
        #############################################################################
        #############################################################################





    except:
        st.warning('Keine Feedbacks')

    #  Eine horizontale drei Pixel Linie hinzufügen
    draw_line(3)

    # Footer importieren
    import Footer as ft
    ft.run_footer(language_index=language_index)
