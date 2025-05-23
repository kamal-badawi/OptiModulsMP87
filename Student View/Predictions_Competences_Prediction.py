#WICHTIG: Die Methoden parse_text_to_lines und create_pdf wurden mit ChatGPT erzeugt
def run_predictions_competences_prediction(language_index):
    import streamlit as st
    import google.generativeai as genai
    import re
    import os
    from datetime import datetime
    import Send_Mail
    import Process_Button_Styling as pbs
    import Background_Style
    pbs.run_process_button_style()
    Background_Style.run_background_styl()

    # Erstelle eine dicke Linie Funktion
    def draw_line(groesse):
        st.markdown(f"<hr style='border: {groesse}px solid black;'>", unsafe_allow_html=True)


    def down_load_pdf(pdf_buffer,  created_datetime_download):
        # Get user's home directory
        home_dir = os.path.expanduser('~')

        # Define path to Downloads folder (common names for Windows/Mac/Linux)
        downloads_folder = os.path.join(home_dir, 'Downloads')

        # Create full path for the PDF file
        file_path = os.path.join(downloads_folder, f'OptiModuls-Ergebnis-{created_datetime_download}.pdf')

        # Save PDF buffer to Downloads folder
        with open(file_path, 'wb') as f:
            f.write(pdf_buffer.read())

    def parse_text_to_lines(text, c, max_width, font_name="Helvetica"):
        """
        Gibt eine Liste von (text, bold) Paaren pro Zeile zurück,
        wobei langer Text umgebrochen wird und **fett** erkannt wird.
        """
        lines = []
        current_line = []
        current_width = 0



        for paragraph in text.split('\n'):
            if paragraph.strip() == "--------":
                lines.extend([[], [], [], []])  # 4 Leerzeilen
                continue


            if paragraph.strip() == "----":
                lines.extend([[], []])  # 2 Leerzeile
                continue

            if paragraph.strip() == "--":
                lines.extend([[]])  # 1 Leerzeile
                continue




            tokens = re.split(r'(\*\*.*?\*\*|\s+)', paragraph)
            line = []
            line_width = 0

            for token in tokens:
                if not token:
                    continue

                is_bold = token.startswith("**") and token.endswith("**")

                display_text = token[2:-2]  if is_bold  else token

                font = "Helvetica-Bold" if is_bold else font_name
                text_width = c.stringWidth(display_text, font, 14 if is_bold else 12)

                if line_width + text_width > max_width:
                    lines.append(line)
                    line = []
                    line_width = 0

                line.append((display_text, is_bold))
                line_width += text_width

            if line:
                lines.append(line)

        return lines

    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import mm
    from reportlab.pdfgen import canvas
    from reportlab.lib.utils import ImageReader
    from io import BytesIO

    def create_pdf(text):
        logo_image_path = '../Images/OptiModuls Logo with BG.png'  # Lokaler Pfad zum Bild
        logo_image = ImageReader(logo_image_path)

        signature_image_path = '../Images/OptiModuls Signature.png'  # Lokaler Pfad zum Bild
        signature_image = ImageReader(signature_image_path)

        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4

        margin = 20 * mm
        max_width = width - 2 * margin
        x = margin
        y = height - margin
        line_height = 14

        # Bild mit fester Größe 200x100 px zeichnen (oben links)
        c.drawImage(logo_image, (max_width/2)-100+x, y - 100, width=200, height=100)
        y -= (150 + 10)  # Platz unter dem Bild

        # Jetzt den Header-Text einfügen, immer Platz vorher prüfen
        header_lines = [
            'Liebe Studentin, lieber Student,',
            ' ',
            'anbei übersenden wir Ihnen die Zusammenfassung des Tests.',
            ' ',
            ' ',
        ]

        for header_text in header_lines:
            if y - line_height < margin:
                c.showPage()
                y = height - margin
                c.setFont('Helvetica', 12)

            y -= line_height
            c.drawString(x, y, header_text)

        # --- Trennlinie---
        def create_sep_line(y):
            if y -  line_height < margin:
                c.showPage()
                y = height - margin
                c.setFont('Helvetica', 12)


            y -= line_height
            c.setDash(3, 2)  # gestrichelte Linie: 3 Punkte Linie, 2 Punkte Lücke
            c.line(x, y, width - margin, y)
            c.setDash()  # zurücksetzen auf durchgezogene Linie
            y -= line_height
            return y

        y = create_sep_line(y)-line_height



        # Text vorbereiten (parse_text_to_lines musst du selbst definiert haben)
        lines = parse_text_to_lines(text, c, max_width)
        c.setFont('Helvetica', 12)

        for line in lines:
            # Platz für eine Zeile prüfen
            if y - line_height < margin:
                c.showPage()
                y = height - margin
                c.setFont('Helvetica', 12)

            if not line:
                y -= line_height
                continue

            current_x = x
            for word, is_bold in line:
                font = "Helvetica-Bold" if is_bold else "Helvetica"
                c.setFont(font, 12)
                c.drawString(current_x, y, word)
                current_x += c.stringWidth(word, font, 12)
            y -= line_height

        y = create_sep_line(y)

        now = datetime.now()
        created_datetime = now.strftime("%d. %m. %Y um %H:%M:%S")
        created_datetime_download = now.strftime("%d-%m-%Y-%H-%M-%S")
        created_datetime_send_mail = created_datetime

        # Jetzt den Schluss-Text einfügen, immer Platz vorher prüfen
        footer_lines = [
            'Vielen Dank für die Nutzung von OptiModuls.',
            ' ',
            'Mit freundlichen Grüßen,',
            ' ',
            ' ',
            'Ihr OptiModuls-Team'
        ]

        for footer_text in footer_lines:
            if y - line_height < margin:
                c.showPage()
                y = height - margin
                c.setFont('Helvetica', 12)

            y -= line_height
            c.drawString(x, y, footer_text)

        # Abschließend Bild unten einfügen (eventuell neue Seite)
        if y - 60 < margin:
            c.showPage()
            y = height - margin

        y -= 60
        c.drawImage(signature_image, x+40, y, width=100, height=50)

        if y - (line_height) < margin:
            c.showPage()
            y = height - margin
            c.setFont('Helvetica', 12)

        y -= (line_height)
        c.drawString(x, y, f'Erstellt am {created_datetime}')

        c.save()
        buffer.seek(0)
        return buffer, buffer, created_datetime_download, created_datetime_send_mail

    # Fragen erstellen, um die Kompetenzen festzustellen.
    @st.cache_resource
    def create_competences_questions():
        # Lese den Key aus der Lokalen-Datei
        with open(r'../Google Gemini Key/API_KEY.txt', mode='r', encoding='utf-8') as file:
            API_KEY = file.read()

        genai.configure(api_key=API_KEY)

        prompt = f"""
        Du bist ein sehr erfahrener Prof. Dr. an der Technischen Hochschule Mittelhessen 
        und betreuen den Bachelor-Studiengang Wirtschaftsinformatik.

        Ich möchte die Kompetenzen eines Studierenden anhand von 10 gezielten Fragen evaluieren.

        Die zu bewertenden Kompetenzbereiche sind:

        1) Technologische Kompetenz 
           (z. B. Programmierung, Datenbanken, IT-Systeme)

        2) Betriebswirtschaftliches Verständnis 
           (z. B. BWL-Grundlagen, Geschäftsprozesse, Controlling)

        3) Analytisch-konzeptionelle Fähigkeiten 
           (z. B. Modellierung, Problemlösung, Systemdenken)

        4) Kommunikations- und Schnittstellenkompetenz 
           (z. B. Vermittlung zwischen IT und Fachabteilungen, Anforderungsanalyse, Präsentationstechniken)
        
        
        Erstelle mir **10 gezielten Fragen**, die helfen, diese Kompetenzen möglichst gut zu erfassen.
        Die Fragen sind durch <<<>>> getrennt
        
        bitte immer neue kreative Fragen stellen
        
        Der Nutzer kann darauf nur mit einem Text (minimal 100 Zeichen) Antworten, also kein Audio, Zeichnung oder Ähnliches
        
        Die Fragen sollen möglichst praxisnah, verständlich und differenzierend formuliert sein
        
        bitte nur die Fragen zurückgeben und nicht mehr, z.B. Frage 1 <<<>>> Frage 2 <<<>>> Frage ... <<<>>> Frage 10
        """

        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)

        return response.text

    # Fragen erstellen, um die Kompetenzen festzustellen.
    @st.cache_resource
    def create_dummy_answers(questions_list, level):
        # Lese den Key aus der Lokalen-Datei
        with open(r'../Google Gemini Key/API_KEY.txt', mode='r', encoding='utf-8') as file:
            API_KEY = file.read()

        genai.configure(api_key=API_KEY)

        prompt = f"""
        Du bist ein:e {level}e:r Student:in im Bachelorstudiengang Wirtschaftsinformatik an der Technischen Hochschule Mittelhessen.

        Bitte beantworte die folgenden 10 Fragen, die in der Liste {questions_list} enthalten sind.

        - Gib **genau 10 Antworten** in Textform.
        - Jede Antwort soll **mindestens 100 Zeichen lang** sein.
        - Die Qualität und Tiefe der Antworten soll dem Niveau eines {level}en Studierenden entsprechen.
        - {level} entspricht die genauigkeit der Antwort, z. B. Top-Level bedeutet, dass der Student 100% kompetenz auf die Frage geantwortet hat. 
        - Trenne die Antworten jeweils mit <<<>>>.
        - Gib **nur die Antworten** zurück – keine Nummerierungen, Einleitungen oder sonstige Texte.

        Beginne jetzt.
        """

        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)

        return response.text

    # Die Kompetenzen in % zwischen 0 und 100% feststellen.
    @st.cache_resource
    def figure_out_me_competences(questions_and_answers):
        # Lese den Key aus der Lokalen-Datei
        with open(r'../Google Gemini Key/API_KEY.txt', mode='r', encoding='utf-8') as file:
            API_KEY = file.read()

        genai.configure(api_key=API_KEY)

        prompt = f"""
        Du bist ein erfahrener Professor (Prof. Dr.) an der Technischen Hochschule Mittelhessen und betreust den Bachelor-Studiengang Wirtschaftsinformatik.

        Deine Aufgabe ist es, die fachlichen und methodischen Kompetenzen eines Studierenden anhand seiner Antworten auf gezielte Fachfragen zu bewerten. Die Fragen und Antworten befinden sich im folgenden Python-Dictionary:  
        `{questions_and_answers}`

        Dabei entspricht jeder Key einer Frage und jeder Value der Antwort des Studierenden.

        Bewerte die folgenden **vier Kompetenzbereiche**:

        1. **Technologische Kompetenz**  
           (z. B. Programmierung, Datenbanken, IT-Systeme)

        2. **Betriebswirtschaftliches Verständnis**  
           (z. B. BWL-Grundlagen, Geschäftsprozesse, Controlling)

        3. **Analytisch-konzeptionelle Fähigkeiten**  
           (z. 
        4. **Kommunikations- und Schnittstellenkompetenz**  
           (z. B. Vermittlung zwischen IT und Fachbereichen, Anforderungsanalyse, Präsentationsfähigkeiten)

        --------

        **Deine Aufgabe im Detail:**

        1. Analysiere den **inhaltlichen Zusammenhang** zwischen jeder Frage und der dazugehörigen Antwort.
        2. Berechne einen **Prozentwert (0–100 %)** für **jeden der vier Kompetenzbereiche**, basierend auf der gesamten Antwortleistung des Studierenden.
        3. Gib eine **präzise Begründung** für jede Kompetenzbewertung (mindestens 10 Sätze).
        5. Kurze, nichtssagende oder irrelevante Antworten wirken sich negativ auf die Bewertung aus.

        --------

        **Antwortformat (bitte exakt so strukturieren, keine zusätzlichen Informationen oder Kommentare):**

        **Ihre Fragen und Antworten:**\n 
        ○ Frage 1: [Fragetext]\n
        ○ Antwort 1: [Antworttext]\n
        ----
        ...  
        ○ Frage 10: [Fragetext]\n
        ○ Antwort 10: [Antworttext]\n
        ----

        --------

        **Ihre Kompetenzen:**\n
        ○ Technologische Kompetenz: XX %\n
        --
        ○ Betriebswirtschaftliches Verständnis: XX %\n
        --
        ○ Analytisch-konzeptionelle Fähigkeiten: XX %\n
        --
        ○ Kommunikations- und Schnittstellenkompetenz: XX %\n
        --

        --------

        **Begründung:**\n
        ○ Technologische Kompetenz: [mindestens 10 Begründung]\n
        ----
        ○ Betriebswirtschaftliches Verständnis: [mindestens 10 Sätze Begründung]\n
        ----
        ○ Analytisch-konzeptionelle Fähigkeiten: [mindestens 10 Sätze Begründung]\n
        ----
        ○ Kommunikations- und Schnittstellenkompetenz: [mindestens 10 Sätze Begründung]\n
        ----

        --------
        **Hinweis:**  
        - Achte auf Klarheit, Differenzierung, Objektivität und akademisches Niveau bei Beurteilung und Begründung.
        - Bei der Begründung sprechen Sie den Studenten direkt mit Sie an, z. B. Sie haben ...
        
        """

        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)

        return response.text


    try:
        level = st.selectbox(label='Wählen Sie den Studenten Level aus (Dummy)',
                             options= ['Sehr schlecht', 'Mittelmäßig', 'Ausgezeichnet'],
                             key='student_level')

        # Eine horizontale ein Pixel Linie hinzufügen
        draw_line(1)

        questions_and_answers = {}
        answers_list = []
        questions_list = []
        questions = create_competences_questions()

        for question in questions.split('<<<>>>'):
            # Lösche den Zeilenumbruch, wenn es existiert
            if question.startswith('\n'):
                question = question[1:]

            questions_list.append(question)

        dummy_answers = create_dummy_answers(questions_list, str(level).lower())
        dummy_answers_list = []

        for dummy_answer in dummy_answers.split('<<<>>>'):
            # Lösche den Zeilenumbruch, wenn es existiert
            if dummy_answer.startswith('\n'):
                dummy_answer = dummy_answer[1:]

            dummy_answers_list.append(dummy_answer)


        question_number = 1
        for question in questions_list:
            answer = st.text_area(label= f'{question_number}). {question}',
                                  height =3,
                                  placeholder='Schreiben Sie etwas... (mind. 100 Zeichen)',
                                  value=dummy_answers_list[question_number-1][1:] if dummy_answers_list[question_number-1].startswith('\n') else dummy_answers_list[question_number-1],
                                  key= f'{question_number})_competence_question')
            if len(answer) > 100:
                questions_and_answers[question[1:] if question.startswith('\n') else question] = answer
                answers_list.append(answer)
            question_number +=1

        # Eine horizontale ein Pixel Linie hinzufügen
        draw_line(1)

        send_mail_cb = st.checkbox('Wollen Sie das Ergebnis per Mail erhalten?',
                                   key='send_mail_cb')

        valid_email = True
        if send_mail_cb:
            email_address = st.text_input("Geben Sie Ihre E-Mail-Adresse ein")
            if email_address:
                if re.match(r"[^@]+@[^@]+\.[^@]+", email_address):
                    valid_email= True
                    st.success("Gültige E-Mail-Adresse")
                else:
                    valid_email = False
                    st.error("Ungültige E-Mail-Adresse")
            else:
                valid_email = False
                st.error("Keine E-Mail-Adresse wurde eingegeben")


        # Eine horizontale drei Pixel Linie hinzufügen
        draw_line(3)





        if st.button('Kompetenzen bestimmen') and valid_email:
            if len(answers_list) == len(questions_list):




                text_from_google_gemini = figure_out_me_competences(questions_and_answers)

                pdf_buffer_download,pdf_buffer_send_mail, created_datetime_download, created_datetime_send_mail = create_pdf(text_from_google_gemini)
                down_load_pdf(pdf_buffer_download, created_datetime_download)


                if send_mail_cb:
                    Send_Mail.send_email_run(email_address,pdf_buffer_send_mail,created_datetime_send_mail,created_datetime_download)
                    st.success('Das Ergebnis wurde erfolgreich per Mail versendet und lokal gespeichert')

                else:
                    st.success('Das Ergebnis wurde erfolgreich lokal gespeichert')



            else:
                # Eine horizontale ein Pixel Linie hinzufügen
                draw_line(1)
                st.warning(
                    # "Please complete your details and check them for accuracy"
                    f'Bitte vervollständigen')




    except Exception as e:
        # Eine horizontale ein Pixel Linie hinzufügen
        draw_line(1)
        st.warning(f'Fehler {e}')







    # Footer importieren
    import Footer as ft
    ft.run_footer(language_index=language_index)






