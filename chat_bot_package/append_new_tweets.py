from chat_bot_package import db
from chat_bot_package.database_tables import MainTweet, ReplyTweet
import json
import time


def save_to_db(location='2019-05-15.json'):
    with open(location, 'r', encoding='utf-8') as read_file:
        tweet_replies = json.load(read_file)
        for t_id, t_data in tweet_replies.items():
            from chat_bot_package import db
            t_tweet = t_data['tweet']
            if isinstance(t_tweet, list):
                t_tweet = " ".join(t_tweet)
            if len(list(MainTweet.query.filter_by(tweeter_id=t_id))) == 0:
                time.sleep(2)
                t_id_replies = t_data['ids_replied']
                t_replies = t_data['replied_tweets']
                if len(t_id_replies) > 2:
                    m_tweet = MainTweet(tweeter_id=t_id, tweet=t_tweet)
                    db.session.add(m_tweet)
                    db.session.commit()
                    print('Main Tweet: ', t_tweet)
                    for r_id, r_reply in zip(t_id_replies, t_replies):
                        if len(list(ReplyTweet.query.filter_by(tweeter_id=r_id))) == 0:
                            time.sleep(2)
                            r_tweet = ReplyTweet(tweeter_id=r_id, reply_tweet=r_reply[1], tweet_id=t_id)
                            db.session.add(r_tweet)
                            db.session.commit()
                            print('Reply Tweet: ', r_reply[1])


def delete_from_db(location='2019-05-15.json'):
    with open(location, 'r', encoding='utf-8') as read_file:
        tweet_replies = json.load(read_file)
        for t_id, t_data in tweet_replies.items():
            t_id_replies = t_data['ids_replied']
            if len(t_id_replies) < 2:
                if len(list(MainTweet.query.filter_by(tweeter_id=t_id))) == 1:
                    MainTweet.query.filter_by(tweeter_id=t_id).delete()
                    print(t_id)
                    db.session.commit()


if __name__ == '__main__':
    # save_to_db(r"C:\Users\closer\PycharmProjects\chatbot_web\2019-05-15.json")
    delete_from_db(r"C:\Users\closer\PycharmProjects\chatbot_web\2019-05-15.json")
