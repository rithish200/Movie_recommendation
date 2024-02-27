from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import random
from mail import send

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
movie_list = []
acclaimed_list = []
genre_list = ["action", "animation", "classics", "comedy", "documentary", "drama", "kids", "fiction", "horror", "international", "musical", "mystery", "romance", "special", "sports", "television", "western"]

for r in res:
    movie_list.append(r[1])

for r in res:
    if r[2] == 100:
        acclaimed_list.append(r[1])


class Data(db.Model):
    __tablename__ = "data"
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(120))
    genre = db.Column(db.String)

    def __init__(self, email, genre):
        self.email = email
        self.genre = genre


@app.route("/")
def index():
    return render_template("homepage.html")

@app.route("/submit_success", methods = ["POST"])
def success():
    if request.method == "POST":
        email = request.form["nemail"].lower().strip()
        genre = request.form["ngenre"].lower().strip()
        if genre in genre_list:
            send(email, genre)
            data = Data(email, genre)
            db.session.add(data)
            db.session.commit()
            return render_template("success.html")
    return render_template("homepage.html", text = "The genre you've entered is unavailable! Try Again.")

@app.route("/random", methods = ["POST"])
def random_m():
    random_movie = acclaimed_list[random.randint(0, len(acclaimed_list)-1)]
    return render_template("random_movie.html", random_movie = random_movie)

@app.route("/info", methods = ["POST"])
def info():
    return render_template("info.html")

if __name__ == "__main__":
    app.run()