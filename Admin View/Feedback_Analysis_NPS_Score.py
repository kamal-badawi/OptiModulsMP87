def run_feedback_nps_score(language_index,feedbacks):
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


    # Anazhl der jeweiligen NPS mit % visualsiieren
    def make_nps_groups_metric(nps_value, count_of_nps_values, count_of_all_nps_values):
        import streamlit as st

        percent_of_nps= (count_of_nps_values / count_of_all_nps_values) * 100
        st.markdown(
            f"""
                        <div style='border: 1px solid black; box-shadow: 0px 0px 25px 3px black; padding: 10px; background-color: #f8f8f8; display: flex; flex-direction: column; justify-content: center;'>
                            <h1 style='text-align: center; background-color:#d5d5d5; margin: 0; padding: 5px; flex: 1;'>
                                {count_of_nps_values}  
                            </h1>
                            <h1 style='text-align: center; background-color:#eeeeee; margin: 0; padding: 5px; flex: 1;'>
                                <span style='color:#FFD700;'>
                                <span style='color:#FFD700; '>‎ 
                                </span>
                                {nps_value}
                                </span>
                            </h1>
                            <h1 style='text-align: center; background-color:#d5d5d5; color:#009999; margin: 0; padding: 5px; flex: 1;'>{percent_of_nps:.1f} %</h1>
                        </div>
                        """, unsafe_allow_html=True)

        st.write('')
        st.write('')
        st.write('')
        st.write('')


    # Anazhl der jeweiligen NPS mit % visualsiieren
    def make_nps_scores_metric(nps_value):
        import streamlit as st

        nps_value = nps_value * 100
        st.markdown(
            f"""
                               <div style='border: 1px solid black; box-shadow: 0px 0px 25px 3px black; padding: 10px; background-color: #f8f8f8; display: flex; flex-direction: column; justify-content: center;'>
                                   <h1 style='text-align: center; background-color:#eeeeee; margin: 0; padding: 5px; flex: 1;'>
                                       <span style='color:black; min-height:200px'>‎ 
                                       {'NPS-Score'}
                                       </span>
                                   </h1>
                                   <h1 style='text-align: center; background-color:#d5d5d5; color:#009999; margin: 0; padding: 5px; flex: 1;'>{nps_value:.1f} %</h1>
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

        # Berechne den Mittelwert für die Anzahl der NPS pro Tag
        grouped_avg_count_of_nps_over_date = feedbacks.groupby('date').agg(
            avg_count_of_nps=('nps_score', 'mean')).reset_index()

        grouped_avg_count_of_nps_over_date = grouped_avg_count_of_nps_over_date.rename(columns={'date': 'Date',
                                                                                  'avg_count_of_nps': 'Avg Count of NPS'})

        # Visualisieren
        create_line_chart(grouped_avg_count_of_nps_over_date,
                          x='Date',
                          y='Avg Count of NPS',
                          z=False,
                          title=f'Durchschnittlicher NPS nach Datum ({count_all_feedback} Feedbacks)')

        #############################################################################
        #############################################################################
        #############################################################################

        # Eine horizontale ein Pixel Linie hinzufügen
        draw_line(1)

        # Berechne den durschnitlichen NPS pro Wochentag
        feedbacks['weekday'] = feedbacks['date_converted'].dt.weekday

        grouped_avg_count_of_nps_over_weekday = feedbacks.groupby('weekday').agg(
            avg_count_of_nps=('nps_score', 'mean')).reset_index()

        grouped_avg_count_of_nps_over_weekday = grouped_avg_count_of_nps_over_weekday.rename(columns={'weekday': 'Weekday',
                                                                                                'avg_count_of_nps': 'Avg Count of NPS'})

        # Visualisieren
        create_line_chart(grouped_avg_count_of_nps_over_weekday,
                          x='Weekday',
                          y='Avg Count of NPS',
                          z=False,
                          title=f'Durchschnittlicher NPS nach Wochentag ({count_all_feedback} Feedbacks)')

        #############################################################################
        #############################################################################
        #############################################################################
        # Eine horizontale ein Pixel Linie hinzufügen
        draw_line(1)

        # Berechne den durschnitlichen NPS pro pro Stunde
        feedbacks['hour'] = pd.to_datetime(feedbacks['date'].astype(str)+' '+feedbacks['time'].astype(str)).dt.hour

        grouped_avg_count_of_nps_over_hour = feedbacks.groupby('hour').agg(
            avg_count_of_nps=('nps_score', 'mean')).reset_index()

        grouped_avg_count_of_nps_over_hour = grouped_avg_count_of_nps_over_hour.rename(
            columns={'hour': 'Hour',
                     'avg_count_of_nps': 'Avg Count of NPS'})

        # Visualisieren
        create_line_chart(grouped_avg_count_of_nps_over_hour,
                          x='Hour',
                          y='Avg Count of NPS',
                          z=False,
                          title=f'Durchschnittlicher NPS nach Uhrzeit ({count_all_feedback} Feedbacks)')

        #############################################################################
        #############################################################################
        #############################################################################

        # Eine horizontale ein Pixel Linie hinzufügen
        draw_line(1)

        # Anzahl der NPS analysieren
        # Scores
        st.markdown(
            f"""
                 <div style='text-align: center; font-weight: bold; font-size: 1.2vw;'>
                     NPS-Analyse
                 </div>
                     """,
            unsafe_allow_html=True
        )
        st.write('')
        st.write('')
        st.write('')



        nps_analysis = feedbacks['nps_score'].value_counts().reset_index()

        nps_analysis = nps_analysis.rename(columns={'index': 'NPS',
                                                        'nps_score': 'Count'})

        nps_bins = [1, 6,  8,  11]
        nps_labels = ['Detraktoren', 'Passive', 'Promotoren']


        nps_analysis['NPS_Groups'] = pd.cut(nps_analysis['NPS'],
                                                      bins=nps_bins,
                                                      labels=nps_labels,
                                                      right=False)


        nps_analysis = nps_analysis.groupby('NPS_Groups')['Count'].sum()
        nps_analysis = nps_analysis.reset_index()

        # Detraktoren
        nps_category_detraktoren = 'detraktoren ' + ' ☹️'
        count_detraktoren = nps_analysis.loc[nps_analysis['NPS_Groups'] == 'Detraktoren', 'Count'].values[0]

        # Passive
        nps_category_passive = 'Passive ' + ' 😐'
        count_passive = nps_analysis.loc[nps_analysis['NPS_Groups'] == 'Passive', 'Count'].values[0]

        # Promotoren
        nps_category_promotoren = 'Promotoren ' + ' 😊'
        count_promotoren = nps_analysis.loc[nps_analysis['NPS_Groups'] == 'Promotoren', 'Count'].values[0]


        nps_value =  (count_promotoren / count_all_feedback) -  (count_detraktoren / count_all_feedback)

        nps_col_one, nps_col_two, nps_col_three = st.columns(3)

        with nps_col_one:
            pass

        with nps_col_two:
            make_nps_scores_metric(nps_value)

        with nps_col_three:
            pass



        nps_col_one, nps_col_two, nps_col_three = st.columns(3)

        with nps_col_one:
            make_nps_groups_metric(nps_category_detraktoren, count_detraktoren, count_all_feedback)


        with nps_col_two:
            make_nps_groups_metric(nps_category_passive, count_passive, count_all_feedback)


        with nps_col_three:
            make_nps_groups_metric(nps_category_promotoren, count_promotoren, count_all_feedback)

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
