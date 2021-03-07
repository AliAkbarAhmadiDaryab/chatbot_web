from flask import render_template, url_for, flash, redirect, request
import json

from chat_bot_package import app, db, pass_crypt
from chat_bot_package.all_froms import RegistrationForm, LoginForm, TweetForm, ReplyForm
from chat_bot_package.database_tables import User, MainTweet, ReplyTweet, MainTweetTagger, ReplyTweetTagger
from flask_login import login_user, current_user, logout_user, login_required

# max_id_main_tweet = db.session.query(db.func.max(MainTweet.id).label('Max ID')).first()[0]
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
    flag_last_tweet = False
    form = TweetForm()
    if form.validate_on_submit():
        print('Hello world 1')
        flash(f' توییت با شناسه {form.id.data} ذخیره شد ', 'success')
        return redirect(url_for('home'))
    else:

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
