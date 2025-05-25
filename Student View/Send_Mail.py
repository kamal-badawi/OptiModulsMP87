
def send_email_run(to_email, attachment, created_datetime_send_mail, created_datetime_download ):
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.base import MIMEBase
    from email import encoders
    from email.utils import formataddr
    from dotenv import load_dotenv
    import os
    from pathlib import Path


    env_path = Path(__file__).resolve().parent.parent / '.env'
    load_dotenv(dotenv_path=env_path)
    from_email = os.getenv("FROM_EMAIL")
    smtp_password = os.getenv("FROM_EMAIL_PASSWORD")
    smtp_server = "smtp.gmail.com"
    smtp_port = 587


    body = f'''
       Liebe Studentin, lieber Student,<br><br><br>
       anbei übersenden wir Ihnen die Zusammenfassung des Tests als PDF-Datei.<br><br>
       Mit freundlichen Grüßen<br><br><br>
       
       Ihr OptiModuls-Team<br><br><br>
       
       Erstellt am {created_datetime_send_mail}
       '''

    msg = MIMEMultipart()
    msg['From'] = formataddr(("OptiModuls-Team", from_email))
    msg['To'] = to_email
    msg['Subject'] = f'OptiModuls Ergebnis vom {created_datetime_send_mail}'

    msg.attach(MIMEText(body, 'html'))

    # Sicherstellen, dass der Buffer an der richtigen Stelle ist
    attachment.seek(0)

    part = MIMEBase('application', 'pdf')
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header(
        'Content-Disposition',
        f'attachment; filename="OptiModuls-Ergebnis-{created_datetime_download}.pdf"'
    )
    msg.attach(part)

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(from_email, smtp_password)
        server.sendmail(from_email, to_email, msg.as_string())


