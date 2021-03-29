from flask import render_template, url_for, flash, redirect, request
import json

from chat_bot_package import app, db, pass_crypt
from chat_bot_package.all_froms import RegistrationForm, LoginForm, TweetForm, ReplyForm
from chat_bot_package.database_tables import User, MainTweet, ReplyTweet, MainTweetTagger, ReplyTweetTagger
from flask_login import login_user, current_user, logout_user, login_required
from chat_bot_package.read_tweet_by_id import get_tweet
from collections import namedtuple

CONFIG = json.load(open('config/chatbot_config.json', 'rb'))
tweets = [
    {
        "text": "اولین توییت ما",
        "replies": ["از دیدن شما خوشحالم", "از دیدن شما خیلی خوشحالم", "خیلی خوب هستی"]
    },
    {
        "text": "دومین توییت ما",
        "replies": ["از دیدن شما خوشحالم", "از دیدن شما خیلی خوشحالم", "خیلی خوب هستی"]
    }
]

default_tweets = [{
    "text": "اولین توییت ما",
    "replies": ["از دیدن شما خوشحالم", "از دیدن شما خیلی خوشحالم", "خیلی خوب هستی"]
}]

tweet_titles = ['سیاسی', 'اجتماعی', 'طنز', 'ورزشی']
sentiments = ['احساس خنثی', 'احساس مثبت', 'احساس منفی']
saved_button = '   ذخیره   '


@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
@login_required
def home():
    form = TweetForm()
    if form.validate_on_submit():
        main_tweet_tagger = MainTweetTagger(sentiment=form.tweet_sentiment.data, topic=form.tweet_topic.data,
                                            user_id=current_user.id, id_main=form.id.data)
        db.session.add(main_tweet_tagger)
        db.session.commit()
        for fr in form.replies:
            reply_tweet_tagger = ReplyTweetTagger(sentiment=fr.reply_sentiment.data, topic=fr.reply_topic.data,
                                                  user_id=current_user.id, id_reply=fr.tweeter_id.data)
            db.session.add(reply_tweet_tagger)
            db.session.commit()
        flash(f' توییت با شناسه {form.id.data} ذخیره شد ', 'success')
        return redirect(url_for('home'))
    else:
        tweets_all = db.session.query(MainTweet, MainTweetTagger).outerjoin(MainTweetTagger,
                                      (MainTweet.tweeter_id == MainTweetTagger.id_main) &
                                      (MainTweetTagger.user_id == current_user.id)).all()
        user_tweeter_id = None
        user_tweet_text = None
        for tweet in tweets_all:
            if tweet[1] is None:
                user_tweeter_id = tweet[0].tweeter_id
                user_tweet_text = tweet[0].tweet
                if str(user_tweeter_id) in user_tweet_text:
                    read_tweet = get_tweet(user_tweeter_id)
                    if read_tweet is not None:
                        db.session.query(MainTweet).filter(MainTweet.tweeter_id == user_tweeter_id).update(
                            {MainTweet.tweet: read_tweet}, synchronize_session=False)
                        db.session.commit()
                        user_tweet_text = read_tweet
                        break

        form.id.data = user_tweeter_id
        form.tweet_content.data = user_tweet_text
        reply_tweets = ReplyTweet.query.filter_by(tweet_id=user_tweeter_id).all()
        for reply_tweet in reply_tweets:
            reply = ReplyForm()
            reply.tweeter_id = str(reply_tweet.tweeter_id)
            reply.reply_content.data = reply_tweet.reply_tweet
            reply.reply_sentiment.data = sentiments
            reply.reply_topic.data = tweet_titles
            reply.id_backup.data = str(reply_tweet.tweeter_id)
            form.replies.append_entry(reply)

        return render_template("home.html", tweets=tweets, title=CONFIG['general_info']['title'],
                               nav_bar=CONFIG['nav_bar'],
                               side_bar=CONFIG['sidebar'], tweet_titles=tweet_titles, sentiments=sentiments,
                               app_buttons=CONFIG['buttons'], form=form)


@app.route("/next")
@login_required
def next_tweet():
    main_tweet = ReplyTweet(id=4, tweeter_id=2347,
                            reply_tweet='توییت شماره دوم', id_main=2)
    db.session.execute('pragma foreign_keys=on')
    db.session.add(main_tweet)
    db.session.commit()
    return render_template('Hello world')


@app.route("/about")
def about():
    return render_template("about.html", tweets=tweets, title=CONFIG['general_info']['about'],
                           nav_bar=CONFIG['nav_bar'],
                           side_bar=CONFIG['sidebar'])


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hash_password = pass_crypt.generate_password_hash(form.password.data).decode('utf-8')
        new_user = User(username=form.username.data, email=form.email.data, password=hash_password)
        db.session.add(new_user)
        db.session.commit()
        flash(f'کاربر جدید درست شد {form.username.data} ', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', title=CONFIG['general_info']['register'], form=form,
                           nav_bar=CONFIG['nav_bar'],
                           side_bar=CONFIG['sidebar'],
                           tweets=default_tweets)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        logged_user = User.query.filter_by(email=form.email.data).first()
        if logged_user and pass_crypt.check_password_hash(logged_user.password, form.password.data):
            login_user(logged_user, remember=form.remember_me.data)
            request_page = request.args.get('next')
            if request_page:
                return redirect(request_page)
            return redirect(url_for('home'))
            flash('شما موفقانه وارد سیستم شدید', 'success')
        else:
            flash('اطلاعات وارد شده درست نیست', 'danger')
    return render_template('login.html', title=CONFIG['general_info']['login'], form=form,
                           nav_bar=CONFIG['nav_bar'],
                           side_bar=CONFIG['sidebar'],
                           tweets=default_tweets
                           )


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))