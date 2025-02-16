def run_feedback_rating_stars(language_index,feedbacks):
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



    # Anazhl der jeweiligen Sterne mit % visualsiieren
    def make_stars_metric(stars_value, count_of_stars, count_of_all_stars):
        import streamlit as st

        percent_of_stars = (count_of_stars / count_of_all_stars )*100
        st.markdown(
            f"""
                    <div style='border: 1px solid black; box-shadow: 0px 0px 25px 3px black; padding: 10px; background-color: #f8f8f8; display: flex; flex-direction: column; justify-content: center;'>
                        <h1 style='text-align: center; background-color:#d5d5d5; margin: 0; padding: 5px; flex: 1;'>
                            {count_of_stars}  
                        </h1>
                        <h1 style='text-align: center; background-color:#eeeeee; margin: 0; padding: 5px; flex: 1;'>
                            <span style='color:#FFD700;'>
                            <span style='color:#FFD700; '>‎ 
                            </span>
                            {stars_value}
                            </span>
                        </h1>
                        <h1 style='text-align: center; background-color:#d5d5d5; color:#009999; margin: 0; padding: 5px; flex: 1;'>{percent_of_stars:.1f} %</h1>
                    </div>
                    """, unsafe_allow_html=True)

        st.write('')
        st.write('')
        st.write('')
        st.write('')

    # Ein Linien-Diagramm erstellen
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

        # Berechne den Mittelwert für die Anzahl der Sterne pro Tag
        grouped_avg_count_over_date = feedbacks.groupby('date').agg(
            avg_count_of_stars=('count_of_feedback_stars', 'mean')).reset_index()


        grouped_avg_count_over_date = grouped_avg_count_over_date.rename(columns={'date': 'Date',
                                                                                  'avg_count_of_stars': 'Avg Count of Stars'})




        # Visualisieren
        create_line_chart(grouped_avg_count_over_date,
                          x='Date',
                          y='Avg Count of Stars',
                          z=False,
                          title=f'Durchschnittliche Sternebewertung nach Datum ({count_all_feedback} Feedbacks)')

        #############################################################################
        #############################################################################
        #############################################################################

        # Eine horizontale ein Pixel Linie hinzufügen
        draw_line(1)

        # Berechne den die Anzahl der Feedbacks pro Wochentag
        feedbacks['weekday'] = feedbacks['date_converted'].dt.weekday

        grouped_avg_count_over_weekday= feedbacks.groupby('weekday').agg(
            avg_count_of_stars=('count_of_feedback_stars', 'mean')).reset_index()

     
        grouped_avg_count_over_weekday = grouped_avg_count_over_weekday.rename(
            columns={'weekday': 'Weekday',
                     'avg_count_of_stars': 'Avg Count of Stars'})

        # Visualisieren
        create_line_chart(grouped_avg_count_over_weekday,
                          x='Weekday',
                          y='Avg Count of Stars',
                          z=False,
                          title=f'Durchschnittlicher Sternebewertung nach Wochentag ({count_all_feedback} Feedbacks)')


        #############################################################################
        #############################################################################
        #############################################################################
        # Eine horizontale ein Pixel Linie hinzufügen
        draw_line(1)

        # Berechne den Mittelwert für die Anzahl der Sterne pro Stunde
        feedbacks['hour'] = pd.to_datetime(feedbacks['date'].astype(str)+' '+feedbacks['time'].astype(str)).dt.hour
        grouped_avg_count_over_hour = feedbacks.groupby('hour').agg(
            avg_count_of_stars=('count_of_feedback_stars', 'mean')).reset_index()

        grouped_avg_count_over_hour = grouped_avg_count_over_hour.rename(columns={'hour': 'Hour',
                                                                                  'avg_count_of_stars': 'Avg Count of Stars'})

        # Visualisieren
        create_line_chart(grouped_avg_count_over_hour,
                          x='Hour',
                          y='Avg Count of Stars',
                          z=False,
                          title=f'Durchschnittliche Sternebewertung nach Uhrzeit ({count_all_feedback} Feedbacks)' )




        #############################################################################
        #############################################################################
        #############################################################################

        # Eine horizontale ein Pixel Linie hinzufügen
        draw_line(1)

        # Anzahl der Sterne analysieren
        # Scores
        st.markdown(
            f"""
                                         <div style='text-align: center; font-weight: bold; font-size: 1.2vw;'>
                                             Sterne-Analyse
                                         </div>
                                             """,
            unsafe_allow_html=True
        )
        st.write('')
        st.write('')
        st.write('')

        stars_analysis = feedbacks['count_of_feedback_stars'].value_counts().reset_index()

        stars_analysis = stars_analysis.rename(columns={'index': 'Stars',
                                                        'count_of_feedback_stars': 'Count'})

        count_all_stars = stars_analysis['Count'].sum()

        # Data Frame  nach sortieren 'Stars' aufsteigend sortieren
        stars_analysis = stars_analysis.sort_values(by='Stars',
                                                    ascending=True)

        one_star_col, two_star_col, three_star_col, four_star_col, five_star_col = st.columns(5)

        with one_star_col:
            iteration = 1
            for index, row in stars_analysis.loc[:, ['Stars', 'Count']].iterrows():

                stars, count = row['Stars'], row['Count']
                if iteration % 5 == 1:
                    make_stars_metric(stars * "★", count,count_all_feedback)
                iteration += 1

        with two_star_col:
            iteration = 1
            for index, row in stars_analysis.loc[:, ['Stars', 'Count']].iterrows():

                stars, count = row['Stars'], row['Count']
                if iteration % 5 == 2:
                    make_stars_metric(stars * "★", count,count_all_feedback)
                iteration += 1

        with three_star_col:
            iteration = 1
            for index, row in stars_analysis.loc[:, ['Stars', 'Count']].iterrows():

                stars, count = row['Stars'], row['Count']
                if iteration % 5 == 3:
                    make_stars_metric(stars * "★", count,count_all_feedback)
                iteration += 1

        with four_star_col:
            iteration = 1
            for index, row in stars_analysis.loc[:, ['Stars', 'Count']].iterrows():

                stars, count = row['Stars'], row['Count']
                if iteration % 5 == 4:
                    make_stars_metric(stars * "★", count,count_all_feedback)
                iteration += 1

        with five_star_col:
            iteration = 1
            for index, row in stars_analysis.loc[:, ['Stars', 'Count']].iterrows():

                stars, count = row['Stars'], row['Count']
                if iteration % 5 != 1 and iteration % 5 != 2 and iteration % 5 != 3 and iteration % 5 != 4:
                    make_stars_metric(stars * "★", count,count_all_feedback)
                iteration += 1

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
