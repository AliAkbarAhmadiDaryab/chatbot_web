from chat_bot_package import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.BigInteger, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    replies = db.relationship('ReplyTweetTagger', backref='reply_tagger', lazy=True)
    tweets = db.relationship('MainTweetTagger', backref='tweet_tagger', lazy=True)

    def __repr__(self):
        return f"User details: User ID: {self.id},  Username: {self.username},  Email: {self.email}"


class MainTweet(db.Model):
    __table_args__ = {'extend_existing': True}
    tweeter_id = db.Column(db.BigInteger, primary_key=True)
    tweet = db.Column(db.String(400), nullable=False)
    replies = db.relationship('ReplyTweet', backref='reply', lazy=True)
    tagger_user = db.relationship('MainTweetTagger', backref='tagger_user', lazy=True)

    def __repr__(self):
        return f"Main Tweet: ID: {self.tweeter_id},  Tweet: {self.tweet}"


class ReplyTweet(db.Model):
    __table_args__ = {'extend_existing': True}
    tweeter_id = db.Column(db.BigInteger, primary_key=True)
    reply_tweet = db.Column(db.String(400), nullable=False)
    tagger_user = db.relationship('ReplyTweetTagger', backref='tagger_user', lazy=True)
    tweet_id = db.Column(db.BigInteger, db.ForeignKey('main_tweet.tweeter_id'), nullable=False)

    def __repr__(self):
        return f"Reply ID: {self.tweeter_id}  Main Tweet ID: {self.tweet_id}, " \
               f"reply: {self.reply_tweet}"


class MainTweetTagger(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.BigInteger, primary_key=True)
    sentiment = db.Column(db.String(50), nullable=True)
    topic = db.Column(db.String(50), nullable=True)
    style = db.Column(db.String(50), nullable=True)
    user_id = db.Column(db.BigInteger, db.ForeignKey('user.id'), nullable=False)
    id_main = db.Column(db.BigInteger, db.ForeignKey('main_tweet.tweeter_id'), nullable=False)

    def __repr__(self):
        return f"Reply Tweet: Id: {self.id},  Main Tweet ID: {self.id_main}, user: {self.user_id}, " \
               f"sentiment: {self.sentiment}, topic: {self.topic}"


class ReplyTweetTagger(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.BigInteger, primary_key=True)
    sentiment = db.Column(db.String(50), nullable=True)
    topic = db.Column(db.String(50), nullable=True)
    style = db.Column(db.String(50), nullable=True)
    user_id = db.Column(db.BigInteger, db.ForeignKey('user.id'), nullable=False)
    id_reply = db.Column(db.BigInteger, db.ForeignKey('reply_tweet.tweeter_id'), nullable=False)

    def __repr__(self):
        return f"Reply Tweet: Id: {self.id},  Main Tweet ID: {self.id_reply}, user: {self.user_id}, " \
               f"sentiment: {self.sentiment}, topic: {self.topic}"


class TestDialogueResponse(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    dialogue = db.Column(db.String(400), nullable=False)
    response = db.Column(db.String(400), nullable=False)

    def __repr__(self):
        return f"Id: {self.id}, Dialogue : {self.dialogue}, Response: {self.response}"


class TestModelPrediction(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    id_d_r = db.Column(db.Integer,  db.ForeignKey('test_dialogue_response.id'), nullable=False)
    model_name = db.Column(db.String(100), nullable=False)
    prediction = db.Column(db.String(400), nullable=False)

    def __repr__(self):
        return f"Id: {self.id}, Dialogue : {self.dialogue}, Response: {self.response}"
