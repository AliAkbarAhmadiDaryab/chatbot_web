from chat_bot_package import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f"User details: Username: {self.username},  Email: {self.email}"


class MainTweet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tweet = db.Column(db.String(300), nullable=False)
    sentiment = db.Column(db.String(50), nullable=False)
    topic = db.Column(db.String(50), nullable=False)
    reply = db.relationship('ReplyTweet', backref='Main Tweet', lazy=True)

    def __repr__(self):
        return f"Main Tweet: Id: {self.id},  tweet: {self.tweet}, sentiment: {self.sentiment}, topic: {self.topic}"


class ReplyTweet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reply_tweet = db.Column(db.String(300), nullable=False)
    sentiment = db.Column(db.String(50), nullable=False)
    topic = db.Column(db.String(50), nullable=False)
    id_main = db.Column(db.Integer, db.ForeignKey('main_tweet.id'), nullable=False)

    def __repr__(self):
        return f"Reply Tweet: Id: {self.id},  Main Tweet ID: {self.id_main}, reply: {self.reply_tweet}, " \
               f"sentiment: {self.sentiment}, topic: {self.topic}"
