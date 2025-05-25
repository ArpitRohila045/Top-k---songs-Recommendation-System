from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from annoy.model_query import QueryModel
from annoy.pipline import pipline
import numpy as np
from typing import List

app = Flask(__name__)
app.secret_key = "UserAppSecretKey"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
qModel : QueryModel

# Association Table
user_song_association_table = db.Table(
    "user_song_association",
    db.Column("user_id", db.Integer, db.ForeignKey("users.id")),
    db.Column("song_id", db.Integer, db.ForeignKey("songs.id")),
)

# User model
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(25), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    songs = db.relationship("Song", secondary=user_song_association_table, backref="users")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    

# Song model
class Song(db.Model):
    __tablename__ = "songs"
    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(100), nullable=False, unique=True)
    artist = db.Column(db.String(100), nullable=False)
    top_genre = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    bpm = db.Column(db.Integer, nullable=False)
    energy = db.Column(db.Float, nullable=False)
    danceability = db.Column(db.Float, nullable=False)
    dB = db.Column(db.Float, nullable=False)
    liveness = db.Column(db.Float, nullable=False)
    valence = db.Column(db.Float, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    acousticness = db.Column(db.Float, nullable=False)
    speechiness = db.Column(db.Float, nullable=False)
    popularity = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Song {self.title} by {self.artist} ({self.year})>"

# Routes
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    user = User.query.filter_by(username=username).first()

    if user and user.check_password(password):
        session["user_id"] = user.id
        return redirect(url_for("dashboard"))
    else:
        return render_template("index.html", error="Invalid username or password.")


@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("home"))
    user = User.query.get(session["user_id"])
    listnedSongs = user.songs
    return render_template("dashboard.html", username=user.username, songs=listnedSongs)


@app.route("/register", methods=["POST"])
def register():
    username = request.form["username"]
    password = request.form["password"]
    existing_user = User.query.filter_by(username=username).first()

    if existing_user:
        return render_template("index.html", error="Username already exists.")
    
    new_user = User(username=username)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()
    session["user_id"] = new_user.id
    return redirect(url_for("dashboard"))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))


@app.route("/play/<int:song_id>" , methods=["POST"])
def play_song(song_id):
    song = Song.query.get(song_id)
    if not song:
        return "Song not found", 404

    qVector = np.array([
        song.year, song.bpm, song.energy, song.danceability, song.dB, song.liveness,
        song.valence, song.duration, song.acousticness, song.speechiness, song.popularity
    ])

    recommendedSongs = recommendatation(qVector=qVector)

    recommendedSongsObj = []

    for rec in recommendedSongs:
        # rec[0] is [title, artist, top_genre]
        title, artist, top_genre = rec[0]
        song_obj = Song.query.filter_by(title=title, artist=artist, top_genre=top_genre).first()
        if song_obj:
            recommendedSongsObj.append(song_obj)
    
    return render_template("play.html", playingSong=song, recommendedSongs=recommendedSongsObj)


def recommendatation(qVector : np.ndarray) -> List[tuple]:
    return qModel.query.query_tree(q_vec=qVector, k=10)

# Init DB & Test Data

if __name__ == "__main__":
    with app.app_context():

        # list = []
        # file_path = "C:\\Users\\hp\\Downloads\\archive (1)\\song_data.csv.csv"
        # sep = ";"
        # data = ZipDataIngestor()
        # df = data.ingest(file_path, sep)

        # for index, row in df.iterrows():
        #     song = Song(
        #         title=row["title"],
        #         artist=row["artist"],
        #         top_genre=row["top genre"],
        #         year=row["year"],
        #         bpm=row["bpm"],
        #         energy=row["energy"],
        #         danceability=row["danceability "],
        #         dB=row["dB"],
        #         liveness=row["liveness"],
        #         valence=row["valence"],
        #         duration=row["duration"],
        #         acousticness=row["acousticness"],
        #         speechiness=row["speechiness "],
        #         popularity=row["popularity"]
        #     )
        #     list.append(song)

        # db.session.add_all(list)
        # db.session.commit()

        qModel = pipline()
        app.run(debug=True)



