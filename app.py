import os
import smtplib
from flask import Flask, render_template, request
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

# Load environment variables
MAIL_ADDRESS = os.getenv("EMAIL_KEY")
MAIL_APP_PW = os.getenv("PASSWORD_KEY")
print(MAIL_ADDRESS,MAIL_APP_PW)
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/resume")
def resume():
    return render_template("resume.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        data = request.form
        send_email(data["name"], data["email"], data["phone"], data["message"])
        return render_template("contact.html", msg_sent=True)
    return render_template("contact.html", msg_sent=False)

def send_email(name, email, phone, message):
    email_message = f"""Subject: New Message from Portfolio\n\n
    Name: {name}
    Email: {email}
    Phone: {phone}
    Message: {message}
    """
    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        print(MAIL_ADDRESS,MAIL_APP_PW)
        connection.login(MAIL_ADDRESS, MAIL_APP_PW)
        connection.sendmail(from_addr=email, to_addrs=MAIL_ADDRESS, msg=email_message)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
