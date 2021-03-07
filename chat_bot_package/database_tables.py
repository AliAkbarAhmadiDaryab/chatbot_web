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
    replies = db.relationship('ReplyTweetTagger', backref='reply_tagger', lazy=True)
    tweets = db.relationship('MainTweetTagger', backref='tweet_tagger', lazy=True)

    def __repr__(self):
        return f"User details: User ID: {self.id},  Username: {self.username},  Email: {self.email}"


class MainTweet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tweeter_id = db.Column(db.Integer, nullable=False, unique=True)
    tweet = db.Column(db.String(300), nullable=False)
    replies = db.relationship('ReplyTweet', backref='reply', lazy=True)
    tagger_user = db.relationship('MainTweetTagger', backref='tagger_user', lazy=True)

    def __repr__(self):
        return f"Main Tweet: ID: {self.id},  Tweeter ID: {self.tweeter_id}  Tweet: {self.tweet}"


class ReplyTweet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tweeter_id = db.Column(db.Integer, nullable=False, unique=True)
    reply_tweet = db.Column(db.String(300), nullable=False)
    tagger_user = db.relationship('ReplyTweetTagger', backref='tagger_user', lazy=True)
    tweet_id = db.Column(db.Integer, db.ForeignKey('main_tweet.id'), nullable=False)

    def __repr__(self):
        return f"Reply Tweet: Id: {self.id},  Tweeter ID: {self.tweeter_id}  Main Tweet ID: {self.tweet_id}, " \
               f"reply: {self.reply_tweet}"


class MainTweetTagger(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sentiment = db.Column(db.String(50), nullable=True)
    topic = db.Column(db.String(50), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    id_main = db.Column(db.Integer, db.ForeignKey('main_tweet.id'), nullable=False)

    def __repr__(self):
        return f"Reply Tweet: Id: {self.id},  Main Tweet ID: {self.id_main}, user: {self.user_id}, " \
               f"sentiment: {self.sentiment}, topic: {self.topic}"


class ReplyTweetTagger(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sentiment = db.Column(db.String(50), nullable=True)
    topic = db.Column(db.String(50), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    id_reply = db.Column(db.Integer, db.ForeignKey('reply_tweet.id'), nullable=False)

    def __repr__(self):
        return f"Reply Tweet: Id: {self.id},  Main Tweet ID: {self.id_reply}, user: {self.user_id}, " \
               f"sentiment: {self.sentiment}, topic: {self.topic}"
