from flask import Flask, render_template, url_for
import json

app = Flask(__name__)

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
    return render_template("about.html", tweets=tweets, title=CONFIG['general_info']['about'], nav_bar=CONFIG['nav_bar'],
                           side_bar=CONFIG['sidebar'])


if __name__ == '__main__':
    app.run(debug=True)
