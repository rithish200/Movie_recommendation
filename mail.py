import smtplib, random
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from email.mime.text import MIMEText


app = Flask(__name__)

ENV = 'prod'
if ENV == 'dev':
    app.debug = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "###"
else:
    app.debug = False
    app.config["SQLALCHEMY_DATABASE_URI"] = "###"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

movie = db.Table("movie", db.metadata, autoload = True, autoload_with = db.engine)
res = db.session.query(movie).all()

def send(email, genre):
    recom = []
    from_email = "recaflick.bot@gmail.com"
    from_password = "recaflick"
    to_email = email

    subject = "Our 20 Movie Recommendations based on your favourite Genre!"
    
    for i in res:
        if genre.lower().strip() == i[4]:
            recom.append(i[1])

    recom = random.sample(recom, 20)
    genre = genre.capitalize()
    message =f"<h2>Hey there!<br>The following are our recommendations for your choice of movie genre which is, {genre}.<br>Hope you had a fun time using the Rec-A-Flick!</h2><br>" + '<hr>'.join(recom)

    msg = MIMEText(message, "html")
    msg["Subject"] = subject
    msg["To"] = to_email
    msg["From"] = from_email

    gmail = smtplib.SMTP("smtp.gmail.com", 587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(from_email, from_password)
    gmail.send_message(msg)
