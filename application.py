# !/usr/bin/env python

from flask import (Flask, render_template, request, redirect,
                   url_for, jsonify, session as login_session,
                   flash)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from database_setup import Base, Genre, Movie, User
from flask_oauth import OAuth
from urllib2 import Request, urlopen, URLError

app = Flask(__name__)

engine = create_engine("sqlite:///catalog.db")
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# scope errors will occur if this is not done
session = scoped_session(DBSession)

# Google login API
CLIENT_ID_PART1 = "523516847358-ft84mnh4dml3dkkaocsbtsk5483r1db9"
CLIENT_ID_PART2 = ".apps.googleusercontent.com"
GOOGLE_CLIENT_ID = CLIENT_ID_PART1 + CLIENT_ID_PART2
GOOGLE_CLIENT_SECRET = "HZ0XO8-YbpvmYP08FjvzkkZ7"
REDIRECT_URL = "/google-oauth-callback"
SECRET_KEY = "dfasfjr341r89ewpfi"
DEBUG = True

app.debug = DEBUG
app.secret_key = SECRET_KEY
oauth = OAuth()
google = oauth.remote_app(
    "google",
    base_url="https://www.google.com/accounts/",
    authorize_url="https://accounts.google.com/o/oauth2/auth",
    request_token_url=None,
    request_token_params={"scope":
                          "https://www.googleapis.com/auth/userinfo.email",
                          "response_type": "code"},
    access_token_url="https://accounts.google.com/o/oauth2/token",
    access_token_method="POST",
    access_token_params={"grant_type": "authorization_code"},
    consumer_key=GOOGLE_CLIENT_ID,
    consumer_secret=GOOGLE_CLIENT_SECRET)


# Load main home page
# valid URL for accessing home page
@app.route("/")
def loadIndex():
    myName = "NoFace@gmail.com"
    genres = session.query(Genre).all()
    if ("email" in login_session):
        myName = login_session["email"]
    return render_template("index.html", genres=genres, myName=myName)


# View items in selected genre
# localhost:5000/genre/1
@app.route("/genre/<int:genre_id>")
def viewMovies(genre_id):
    # get all with matching genre_id
    movies = session.query(Movie).filter_by(genre_id=genre_id).all()
    return render_template("allMovies.html", movies=movies)


# valid URL for accessing add movie page
# localhost:5000/add
@app.route("/add", methods=["GET", "POST"])
def add():
    if (request.method == "POST"):
        if ("email" not in login_session):
            return render_template("error.html")
        new_movie = request.form["Title"]    # get new movie name from form
        genre = select = request.form.get("GenreList")
        m = Movie(name=new_movie, genre_id=genre,
                  user_id=login_session["user_id"])
        session.add(m)
        session.commit()
        return redirect(url_for("loadIndex"))
    else:
        if ("email" in login_session):
            return render_template("movieAdd.html")
        else:
            return render_template("error.html")


# valid URL for viewing movies to delete
# localhost:5000/delete
@app.route("/delete")
def delete():
    if ("email" in login_session):
        the_id = login_session["user_id"]
        movies = session.query(Movie).filter_by(user_id=the_id).all()
        return render_template("movieDelete.html", movies=movies)
    else:
        return render_template("error.html")


# list movies to edit
@app.route("/edit")
def edit():
    if ("email" in login_session):
        the_id = login_session["user_id"]
        movies = session.query(Movie).filter_by(user_id=the_id).all()
        return render_template("movieEdit.html", movies=movies)
    else:
        return render_template("error.html")


# edit movie form
@app.route("/edit/<movie_id>", methods=["GET", "POST"])
def edit_movie(movie_id):
    m = session.query(Movie).filter_by(id=movie_id).first()
    movie_name = m.name
    if (request.method == "POST"):
        if ("email" not in login_session):
            return render_template("error.html")
        if (m.user_id != login_session["user_id"]):
            return render_template("error2.html")
        new_movie = request.form["Title"]    # get new movie name from form
        m.name = new_movie
        session.add(m)
        session.commit()
        return redirect(url_for("loadIndex"))
    else:
        if ("email" in login_session):
            if (m.user_id != login_session["user_id"]):
                return render_template("error2.html")
            return render_template("editForm.html", movie_name=movie_name)
        else:
            return render_template("error.html")


# valid URL to actually delete movie from database
# localhost:5000/delete/2
@app.route("/delete/<movie_id>")
def delete_movie(movie_id):
    m = session.query(Movie).filter_by(id=movie_id).first()
    if ("email" in login_session):
        if (m.user_id != login_session["user_id"]):
            return render_template("error2.html")
        m = session.query(Movie).filter_by(id=movie_id).first()
        session.delete(m)
        session.commit()
        return redirect(url_for("loadIndex"))

    else:
        return render_template("error.html")


# Login Page
@app.route("/login")
def login():
    callback = url_for("authorized", _external=True)
    return google.authorize(callback=callback)


# Logout
@app.route("/logout")
def logout():
    # release session variables
    login_session.pop("id", None)
    login_session.pop("email", None)
    return redirect(url_for("loadIndex"))


# Google authorization handler - required
@app.route(REDIRECT_URL)
@google.authorized_handler
def authorized(resp):
    access_token = resp["access_token"]
    login_session["access_token"] = access_token, ""
    access_token = login_session.get("access_token")

    access_token = access_token[0]

    headers = {"Authorization": "OAuth "+access_token}
    req = Request("https://www.googleapis.com/oauth2/v1/userinfo",
                  None, headers)
    res = urlopen(req)
    # parse response object to get name and email ONLY
    arr = res.read().split(",")
    email_1 = arr[1].split(":")
    name_1 = arr[3].split(":")
    email = email_1[1].replace("\"", "")
    name = name_1[1].replace("\"", "")
    # if user exists
    user = session.query(User).filter_by(email=email).first()
    if (user is None):
        u = User(email=email)
        session.add(u)
        session.commit()
        user = session.query(User).filter_by(email=email).first()
    # set session variables then go to main page
    login_session["email"] = user.email
    login_session["user_id"] = user.id
    return redirect(url_for("loadIndex"))


# required for Google OAuth API
@google.tokengetter
def get_access_token():
    return login_session.get("access_token")


# create json for genre
@app.route("/json/genre")
def genreJson():
    genres = session.query(Genre).all()
    return jsonify(genres=[g.serialize for g in genres])


# create json for movie
@app.route("/json/movie")
def movieJson():
    movies = session.query(Movie).all()
    return jsonify(movies=[m.serialize for m in movies])


# create json for arbitrary genre
@app.route("/json/genre/<int:genre_id>")
def randomGenreJson(genre_id):
    movies = session.query(Movie).filter_by(genre_id=genre_id).all()
    return jsonify(movies=[m.serialize for m in movies])


# create json for arbitrary genre and movieEdit
@app.route("/json/genre/<int:genre_id>/movie/<int:movie_id>")
def randomMovieJson(genre_id, movie_id):
    movie = session.query(Movie).filter_by(genre_id=genre_id,
                                           id=movie_id).first()
    return jsonify(movie=[movie.serialize])


# Main function
if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", port=5000)
