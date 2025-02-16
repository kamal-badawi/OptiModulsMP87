def run_feedback_analysis_general_information(language_index,feedbacks):

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
        fig.update_xaxes(title_font=dict(color='black'), tickfont=dict(color='black'),dtick=1)
        fig.update_yaxes(title_font=dict(color='black'), tickfont=dict(color='black'))

        # Change the line color
        fig.update_traces(line=dict(color='#009999'))

        # Diagramm in Streamlit anzeigen
        st.plotly_chart(fig, use_container_width=True)


    try:


        # Berechne den die Anzahl der Feedbacks pro Jahr
        feedbacks['date_converted'] = pd.to_datetime(feedbacks['date'])
        feedbacks['year'] = feedbacks['date_converted'].dt.year

        grouped_count_of_feedbacks_over_year = feedbacks.groupby('year').agg(
            count_feedbacks=('feedback_text', 'count')).reset_index()


        grouped_count_of_feedbacks_over_year = grouped_count_of_feedbacks_over_year.rename(columns={'year': 'Year',
                                                                                                    'count_feedbacks': 'Count of Feedbacks'})


        count_all_feedback = grouped_count_of_feedbacks_over_year['Count of Feedbacks'].sum()
        # Visualisieren
        create_line_chart(grouped_count_of_feedbacks_over_year,
                          x='Year',
                          y='Count of Feedbacks',
                          z=False,
                          title=f'Anzahl der Feedbacks pro Jahr ({count_all_feedback} Feedbacks)')


        #############################################################################
        #############################################################################
        #############################################################################
        # Eine horizontale ein Pixel Linie hinzufügen
        draw_line(1)

        # Berechne den die Anzahl der Feedbacks pro Jahr-Monat
        feedbacks['month'] = feedbacks['date_converted'].dt.month
        feedbacks['year-month'] = feedbacks['year'].astype(str) +'_'+feedbacks['month'].astype(str).str.zfill(2)


        grouped_count_of_feedbacks_over_year_month = feedbacks.groupby('year-month').agg(
            count_feedbacks=('feedback_text', 'count')).reset_index()

        grouped_count_of_feedbacks_over_year_month = grouped_count_of_feedbacks_over_year_month.rename(columns={'year-month': 'Year-Month',
                                                                                                    'count_feedbacks': 'Count of Feedbacks'})

        count_all_feedback = grouped_count_of_feedbacks_over_year_month['Count of Feedbacks'].sum()
        # Visualisieren
        create_line_chart(grouped_count_of_feedbacks_over_year_month,
                          x='Year-Month',
                          y='Count of Feedbacks',
                          z=False,
                          title=f'Anzahl der Feedbacks pro Jahr-Monat ({count_all_feedback} Feedbacks)')

        #############################################################################
        #############################################################################
        #############################################################################
        # Eine horizontale ein Pixel Linie hinzufügen
        draw_line(1)

        # Berechne den die Anzahl der Feedbacks pro Quartal
        feedbacks['quarter'] = feedbacks['date_converted'].dt.quarter
        grouped_count_of_feedbacks_over_quarter= feedbacks.groupby('quarter').agg(
            count_feedbacks=('feedback_text', 'count')).reset_index()

        grouped_count_of_feedbacks_over_quarter = grouped_count_of_feedbacks_over_quarter.rename(
            columns={'quarter': 'Quarter',
                     'count_feedbacks': 'Count of Feedbacks'})

        count_all_feedback = grouped_count_of_feedbacks_over_quarter['Count of Feedbacks'].sum()
        # Visualisieren
        create_line_chart(grouped_count_of_feedbacks_over_quarter,
                          x='Quarter',
                          y='Count of Feedbacks',
                          z=False,
                          title=f'Anzahl der Feedbacks pro Quartal ({count_all_feedback} Feedbacks)')

        #############################################################################
        #############################################################################
        #############################################################################
        # Eine horizontale ein Pixel Linie hinzufügen
        draw_line(1)

        # Berechne den die Anzahl der Feedbacks pro Monat
        grouped_count_of_feedbacks_over_month = feedbacks.groupby('month').agg(
            count_feedbacks=('feedback_text', 'count')).reset_index()

        grouped_count_of_feedbacks_over_month = grouped_count_of_feedbacks_over_month.rename(
            columns={'month': 'Month',
                     'count_feedbacks': 'Count of Feedbacks'})

        count_all_feedback = grouped_count_of_feedbacks_over_month['Count of Feedbacks'].sum()
        # Visualisieren
        create_line_chart(grouped_count_of_feedbacks_over_month,
                          x='Month',
                          y='Count of Feedbacks',
                          z=False,
                          title=f'Anzahl der Feedbacks pro Monat ({count_all_feedback} Feedbacks)')

        #############################################################################
        #############################################################################
        #############################################################################
        # Eine horizontale ein Pixel Linie hinzufügen
        draw_line(1)

        # Berechne den die Anzahl der Feedbacks pro Wochentag
        feedbacks['weekday'] = feedbacks['date_converted'].dt.weekday
        grouped_count_of_feedbacks_over_weekday = feedbacks.groupby('weekday').agg(
            count_feedbacks=('feedback_text', 'count')).reset_index()

        grouped_count_of_feedbacks_over_weekday = grouped_count_of_feedbacks_over_weekday.rename(
            columns={'weekday': 'Weekday',
                     'count_feedbacks': 'Count of Feedbacks'})

        count_all_feedback = grouped_count_of_feedbacks_over_weekday['Count of Feedbacks'].sum()
        # Visualisieren
        create_line_chart(grouped_count_of_feedbacks_over_weekday,
                          x='Weekday',
                          y='Count of Feedbacks',
                          z=False,
                          title=f'Anzahl der Feedbacks pro Wochentag ({count_all_feedback} Feedbacks)')

        #############################################################################
        #############################################################################
        #############################################################################
        # Eine horizontale ein Pixel Linie hinzufügen
        draw_line(1)

        # Berechne den die Anzahl der Feedbacks pro Stunde
        feedbacks['hour'] = pd.to_datetime(feedbacks['date'].astype(str)+' '+feedbacks['time'].astype(str)).dt.hour

        grouped_count_of_feedbacks_over_hour = feedbacks.groupby('hour').agg(
            count_feedbacks=('feedback_text', 'count')).reset_index()


        grouped_count_of_feedbacks_over_hour = grouped_count_of_feedbacks_over_hour.rename(
            columns={'hour': 'Hour',
                     'count_feedbacks': 'Count of Feedbacks'})

        count_all_feedback = grouped_count_of_feedbacks_over_hour['Count of Feedbacks'].sum()
        # Visualisieren
        create_line_chart(grouped_count_of_feedbacks_over_hour,
                          x='Hour',
                          y='Count of Feedbacks',
                          z=False,
                          title=f'Anzahl der Feedbacks pro Stunde ({count_all_feedback} Feedbacks)')

    except:
        st.warning('Keine Feedbacks')

    #  Eine horizontale drei Pixel Linie hinzufügen
    draw_line(3)

    # Footer importieren
    import Footer as ft
    ft.run_footer(language_index=language_index)
