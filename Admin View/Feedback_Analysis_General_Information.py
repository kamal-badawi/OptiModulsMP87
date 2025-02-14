def run_feedback_analysis_general_information(language_index,feedbacks):

    import streamlit as st
    import pandas as pd
    import sqlite3
    import Process_Button_Styling
    import Background_Style
    Process_Button_Styling.run_process_button_style()
    Background_Style.run_background_styl()


    def insert_dummy_feedbacks():
        import sqlite3
        import random
        from datetime import datetime, timedelta

        # Verbindung zur SQLite-Datenbank
        connection = sqlite3.connect(r'Databases\Students Feedbacks Database.db')
        cursor = connection.cursor()

        # Listen mit Feedback-Texten
        # Listen mit Feedback-Texten auf Deutsch
        positive_feedbacks = [
            "Diese App ist großartig!", "Einfach fantastisch!", "Sehr empfehlenswert!",
            "Hervorragende Benutzererfahrung.",
            "Sehr intuitives Design!", "Erstklassige Leistung.", "Ich liebe diese App!",
            "Beste App, die ich je ausprobiert habe!",
            "Tolle Funktionen und Bedienung.", "Wirklich hilfreich und benutzerfreundlich.", "Ausgezeichneter Support!",
            "Beeindruckend und zuverlässig.", "Unverzichtbar für meinen Alltag.", "Super schnell und flüssig.",
            "Fünf Sterne sind verdient.", "Perfekt für meine Bedürfnisse!", "Absolut lohnenswert.",
            "Diese App ist ein Lebensretter.",
            "Gut durchdacht und effizient.", "Großartige Arbeit der Entwickler!",
            "Benutzerfreundlich und leistungsstark.",
            "Die beste App auf dem Markt.", "Hat meine Erwartungen weit übertroffen.",
            "Erstaunliche Updates und Features.",
            "Macht das Leben so viel einfacher.", "Brillantes Konzept und Umsetzung.",
            "Sehr gut gemacht und professionell.",
            "Unglaublich nützliche App mit tollem Design.", "Nahtlos und angenehm zu bedienen.",
            "Sehr reaktionsschnell und schnell.",
            "Das ultimative App-Erlebnis.", "Sehr effektiv und einfach zu nutzen.", "Wirklich außergewöhnlich.",
            "Jeden Cent wert!", "Besser geht es nicht.", "Ich bin von der Funktionalität beeindruckt.",
            "Perfekte Balance der Funktionen.", "Sehr verlässlich und konsistent.", "Atemberaubend gut.",
            "Makellos und zuverlässig."
        ]

        neutral_feedbacks = [
            "Es ist okay, nichts Besonderes.", "Durchschnittliche App, erfüllt ihren Zweck.",
            "Ganz in Ordnung, könnte aber besser sein.",
            "Nicht schlecht, aber es fehlen einige Funktionen.", "Naja, es funktioniert.", "Manchmal nützlich.",
            "Habe neutrale Gefühle dazu.", "Gut für einfache Zwecke.", "Nicht viel zu sagen, es ist in Ordnung.",
            "Tut, was es soll, aber nichts Extra.", "Okay, aber es gibt bessere Apps.",
            "Könnte besser sein, aber nicht das Schlechteste.",
            "Erfüllt den Zweck einigermaßen.", "Nutzbar, aber Updates wären hilfreich.",
            "Die Grundfunktionen sind in Ordnung.",
            "Neutrale Erfahrung insgesamt.", "Akzeptabel, aber Verbesserungsmöglichkeiten vorhanden.",
            "In Ordnung für gelegentliche Nutzung.",
            "Nicht bemerkenswert, aber okay.", "Mittelmäßig, aber zufriedenstellend.",
            "Ausreichend für einfache Aufgaben.",
            "Ziemlich durchschnittlich.", "Nichts Beeindruckendes, aber okay.",
            "In Ordnung, aber nichts Herausragendes.",
            "Gut für das, was es ist.", "Erfüllt die Grundanforderungen.", "Weder gut noch schlecht.",
            "Funktional, aber uninspiriert.", "Genug für kleine Aufgaben.", "Durchschnittlich bestenfalls.",
            "Es ist nutzbar, aber nicht aufregend.", "Neutrale Leistung bisher.", "Für mich okay.",
            "Gut, aber könnte besser sein.", "Zufriedenstellend für einfache Anforderungen.",
            "Schlicht und unauffällig.",
            "Funktioniert, aber nichts Besonderes.", "Ausreichend für den Moment.",
            "Erfüllt seinen Zweck, aber kaum mehr.",
            "Mittelmäßig, aber es funktioniert."
        ]

        negative_feedbacks = [
            "Schreckliche Erfahrung.", "Furchtbare App, meiden Sie sie!", "Sehr enttäuschend.",
            "Diese App ist eine Zeitverschwendung.",
            "Fehlerhaft und unzuverlässig.", "Funktioniert nicht wie beworben.",
            "Schrecklich, braucht große Überarbeitungen.",
            "Frustrierend und schlecht gestaltet.", "Kann diese App überhaupt nicht empfehlen.",
            "Schlechteste App, die ich je benutzt habe.",
            "Völlig unbrauchbar.", "Stürzt ständig ab.", "Voller Fehler und Probleme.", "Extrem frustrierend.",
            "Absolut schlechter Support.", "Erfüllt die Erwartungen nicht.", "Ein komplettes Desaster.",
            "Sehr schlechte Leistung.", "Nicht wert, heruntergeladen zu werden.", "Bereue die Installation dieser App.",
            "Schlechtes Design und Ausführung.", "Null Sterne, wenn ich könnte.", "So enttäuschend.",
            "Kann nicht liefern, was versprochen wurde.", "Schreckliche Erfahrung insgesamt.",
            "Finger weg von dieser App.",
            "Nicht das Geld wert.", "Extrem fehlerhaft und langsam.", "Schreckliche Benutzeroberfläche.",
            "Funktioniert überhaupt nicht.", "Verschwendung von Ressourcen.", "So viele Probleme mit dieser App.",
            "Grauenhafte Benutzererfahrung.", "Enttäuschend und unzuverlässig.", "Schlechteste App in ihrer Kategorie.",
            "Unbrauchbar und frustrierend.", "Funktioniert ständig nicht.", "Lädt nicht einmal richtig.",
            "Völlig nutzlos.", "So eine Enttäuschung."
        ]

        # Start- und Enddatum für zufällige Daten
        start_date = datetime.strptime("2022-01-01", "%Y-%m-%d")
        end_date = datetime.strptime("2025-03-30", "%Y-%m-%d")
        date_range = (end_date - start_date).days

        for _ in range(400):
            # Zufälliges Datum generieren
            random_date = start_date + timedelta(days=random.randint(0, date_range))
            date_str = random_date.strftime("%Y-%m-%d")

            # Zufällige Zeit zwischen 10:00 und 15:00 Uhr (Mitternacht selten)
            if random.random() < 0.95:
                random_time = f"{random.randint(12, 13)}:{random.randint(0, 59):02d}:{random.randint(0, 59):02d}"
            else:
                random_time = f"00:{random.randint(0, 59):02d}:{random.randint(0, 59):02d}"

            # Zufällige Sternebewertung und dazugehöriges Feedback
            stars = random.randint(1, 5)
            if stars in [4, 5]:
                feedback_text = random.choice(positive_feedbacks)
                sentiment_text = "Positive"
                sentiment_value = 1
                sentiment_probability = round(random.uniform(0.85, 1.0), 2)
            elif stars in [2, 3]:
                feedback_text = random.choice(neutral_feedbacks)
                sentiment_text = "Neutral"
                sentiment_value = 0
                sentiment_probability = round(random.uniform(0.5, 0.8), 2)
            else:
                feedback_text = random.choice(negative_feedbacks)
                sentiment_text = "Negative"
                sentiment_value = -1
                sentiment_probability = round(random.uniform(0.3, 0.6), 2)

            # Net Promoter Score abhängig vom Sentiment
            if sentiment_value == 1:
                nps_score = random.randint(8, 10)
            elif sentiment_value == 0:
                nps_score = random.randint(5, 7)
            else:
                nps_score = random.randint(0, 4)

            # Kreative Verteilung von Antworten (-1 oder 1)
            if sentiment_value == 1:
                answers = [random.choice([1, 1, -1]) for _ in range(15)]  # Überwiegend positiv, aber vereinzelt negativ
            elif sentiment_value == -1:
                answers = [random.choice([-1, -1, 1]) for _ in
                           range(15)]  # Überwiegend negativ, aber vereinzelt positiv
            else:
                answers = [random.choice([-1, 1]) for _ in range(15)]  # Zufällige Mischung bei neutralem Feedback

            # Daten einfügen
            cursor.execute('''
                        INSERT INTO students_feedback_data (
                            date, time, count_of_feedback_stars, feedback_text, sentiment_text, sentiment_probability,
                            nps_score, app_support_subjects, forecast_accuracy, strengths_awareness, strength_tips_effectiveness,
                            subject_selection_ease, subject_relevance, career_match_helpfulness, ui_evaluation, navigation_ease,
                            feature_gap, decision_influence, subject_career_link, recommendation_likelihood, forecast_reliability,
                            tips_personalization_importance
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                date_str, random_time, stars, feedback_text, sentiment_text, sentiment_probability,
                nps_score, *answers
            ))

        # Änderungen speichern und Verbindung schließen
        connection.commit()
        connection.close()

    #insert_dummy_feedbacks()

    # Erstelle eine dicke Linie Funktion
    def draw_line(groesse):
        st.markdown(f"<hr style='border: {groesse}px solid black;'>", unsafe_allow_html=True)







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
