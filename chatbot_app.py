from flask import Flask, render_template, url_for
import json

from all_froms import RegistrationForm, LoginForm

app = Flask(__name__)

app.config['SECRET_KEY'] = '0650c9411b66221d947b0ea065d18008'

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
print(CONFIG)


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", tweets=tweets, title=CONFIG['general_info']['title'], nav_bar=CONFIG['nav_bar'],
                           side_bar=CONFIG['sidebar'], tweet_titles=tweet_titles, sentiments=sentiments,
                           saved_button=saved_button)


@app.route("/about")
def about():
    return render_template("about.html", tweets=tweets, title=CONFIG['general_info']['about'],
                           nav_bar=CONFIG['nav_bar'],
                           side_bar=CONFIG['sidebar'])


@app.route("/register")
def register():
    form = RegistrationForm()
    return render_template('register.html', title=CONFIG['general_info']['register'], form=form,
                           nav_bar=CONFIG['nav_bar'],
                           side_bar=CONFIG['sidebar'],
                           tweets=default_tweets)


@app.route("/login")
def login():
    form = LoginForm()
    return render_template('login.html', title=CONFIG['general_info']['login'], form=form,
                           nav_bar=CONFIG['nav_bar'],
                           side_bar=CONFIG['sidebar'],
                           tweets=default_tweets
                           )


if __name__ == '__main__':
    app.run(debug=True)
