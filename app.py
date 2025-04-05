import os
import smtplib
from flask import Flask, render_template, request
from dotenv import load_dotenv
from email.mime.text import MIMEText
from datetime import datetime


load_dotenv()

app = Flask(__name__)

MAIL_ADDRESS = os.getenv("EMAIL_KEY")
MAIL_APP_PW = os.getenv("PASSWORD_KEY")

@app.route("/")
def splash():
    return render_template("splash.html")

@app.route("/index")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/resume")
def resume():
    return render_template("resume.html")

@app.context_processor
def inject_current_year():
    return {'current_year': datetime.now().year}


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        data = request.form
        send_email(data["name"], data["email"], data["phone"], data["message"])
        return render_template("contact.html", msg_sent=True)
    return render_template("contact.html", msg_sent=False)

def send_email(name, sender_email, phone, message):
    # Email to yourself
    # Email to yourself
    email_message = f"""New Message from Portfolio

    Name: {name}
    Email: {sender_email}
    Phone: {phone}
    Message: {message}
    """
    msg_to_self = MIMEText(email_message, _charset="utf-8")
    msg_to_self['Subject'] = "New Message from Portfolio"
    msg_to_self['From'] = sender_email
    msg_to_self['To'] = MAIL_ADDRESS

    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(MAIL_ADDRESS, MAIL_APP_PW)
        connection.sendmail(sender_email, MAIL_ADDRESS, msg_to_self.as_string())

    # Auto-reply to sender
    auto_reply = f"""Dear {name},

    Thank you for reaching out. I’ve received your message and will get back to you shortly.

    Best regards,
    Shariq Masood
    """
    msg_to_user = MIMEText(auto_reply, _charset="utf-8")
    msg_to_user['Subject'] = "Thanks for contacting me!"
    msg_to_user['From'] = MAIL_ADDRESS
    msg_to_user['To'] = sender_email

    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(MAIL_ADDRESS, MAIL_APP_PW)
        connection.sendmail(MAIL_ADDRESS, sender_email, msg_to_user.as_string())

    # Log submission
    with open("contact_logs.txt", "a") as log:
        log.write(f"\n-----\nName: {name}\nEmail: {sender_email}\nPhone: {phone}\nMessage: {message}\n")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
