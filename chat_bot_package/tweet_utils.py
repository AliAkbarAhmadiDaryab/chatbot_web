from glob import glob
from datetime import datetime, timedelta
import json
import codecs
import tweepy
import os
import time
import re
import pickle as pkl

config_path = os.path.dirname(__file__)
tweeter_keys = json.load(open(os.path.join(config_path, 'config/keys.json'), 'rb'))

auth = tweepy.OAuthHandler(tweeter_keys['API key'], tweeter_keys['API secret key'])
auth.set_access_token(tweeter_keys['Access token'], tweeter_keys['Access token secret'])
api = tweepy.API(auth)


class RawTweet:
    def __init__(self, file_pattern=r"E:\98-1\twitter\twitter_data\*reply*",
                 dir_location=r"E:\98-1\twitter\twitter_data"):
        self.dir_location = dir_location
        self.file_pattern = file_pattern
        self.file_names = []

    def get_file_names(self):
        file_names = glob(self.file_pattern)
        file_names = [os.path.basename(x) for x in file_names]
        self.file_names = file_names

    def export_tweet_json(self):
        for file_name in self.file_names:
            tweets = self.read_tweet(file_name)
            tweets_replied = self.read_ids(file_name, tweets)
            with codecs.open(file_name[:10] + ".json", 'w', encoding='utf-8') as tweets_to_save:
                json.dump(tweets_replied, tweets_to_save, ensure_ascii=False)
                tweets_to_save.close()

    @staticmethod
    def read_ids(file_name, tweets_dict):
        with open(os.path.join(RawTweet.dir_location, '{}').format(file_name), 'r', encoding='Latin-1') as read_file:
            all_ids = read_file.readlines()
            main_tweet_dict = dict()
            for ids in all_ids:
                if len(ids) > 20:
                    try:
                        main_tweet = ids.split('\t')[1].strip().split()[-1]
                        replied_tweet = ids.split('\t')[0].strip().split()[-1]
                        if main_tweet not in main_tweet_dict.keys():
                            main_tweet_dict[main_tweet] = {}
                            if main_tweet in tweets_dict.keys():
                                main_tweet_dict[main_tweet]['tweet'] = tweets_dict[main_tweet]
                            else:
                                main_tweet_dict[main_tweet]['tweet'] = \
                                    f"https://twitter.com/ali_heidari99/status/{main_tweet}"
                            main_tweet_dict[main_tweet]['ids_replied'] = []
                            main_tweet_dict[main_tweet]['replied_tweets'] = []
                        main_tweet_dict[main_tweet]['ids_replied'].append(replied_tweet)
                        if replied_tweet in tweets_dict.keys():
                            main_tweet_dict[main_tweet]['replied_tweets'].append(tweets_dict[replied_tweet])
                        else:
                            main_tweet_dict[main_tweet]['replied_tweet'].append(
                                f"https://twitter.com/ali_heidari99/status/{replied_tweet}")
                    except:
                        continue
            return main_tweet_dict

    @staticmethod
    def read_tweet(filename_reply):
        file_name_list = [filename_reply[:10]]
        file_name_date_one = datetime.strptime(file_name_list[0], '%Y-%m-%d') - timedelta(days=1)
        file_name_date_two = datetime.strptime(file_name_list[0], '%Y-%m-%d') - timedelta(days=2)
        file_name_date_one_neg = datetime.strptime(file_name_list[0], '%Y-%m-%d') - timedelta(days=-1)
        file_name_date_two_neg = datetime.strptime(file_name_list[0], '%Y-%m-%d') - timedelta(days=-2)
        file_name_list.append(file_name_date_one.strftime('%Y-%m-%d'))
        file_name_list.append(file_name_date_two.strftime('%Y-%m-%d'))
        file_name_list.append(file_name_date_one_neg.strftime('%Y-%m-%d'))
        file_name_list.append(file_name_date_two_neg.strftime('%Y-%m-%d'))
        ids_tweets_dict = dict()
        for file_name in file_name_list:
            with open(os.path.join(RawTweet.dir_location, '{}.txt').format(file_name[:10]), 'r',
                      encoding='utf-8') as read_file:
                ids_tweets = read_file.readlines()
                for id_tweet in ids_tweets:
                    if len(id_tweet) > 18:
                        try:
                            id_of_tweet = id_tweet.split('\t')[0].strip()
                            if len(id_tweet.split('\t')) > 3:
                                tweet_owner = id_tweet.split('\t')[1].strip() + ": " + id_tweet.split('\t')[2].strip()
                            else:
                                tweet_owner = id_tweet.split('\t')[1].strip()
                            tweet = id_tweet.split('\t')[-1].strip()
                            ids_tweets_dict[id_of_tweet] = []
                            ids_tweets_dict[id_of_tweet].append(tweet_owner)
                            ids_tweets_dict[id_of_tweet].append(tweet)
                        except:
                            continue
        return ids_tweets_dict

    @staticmethod
    def get_tweet(tweet_id):
        tweets = api.statuses_lookup([tweet_id])
        if not tweets == []:
            tweets = json.dumps(tweets[0]._json)
            tweets = json.loads(tweets)
            text = tweets['text']
            return text
        return None


class DBTweet:
    def __init__(self, file_path):
        self.location = file_path

    def save_to_db(self):
        from chat_bot_package import db
        from chat_bot_package.database_tables import MainTweet, ReplyTweet
        with open(self.location, 'r', encoding='utf-8') as read_file:
            tweet_replies = json.load(read_file)
            for t_id, t_data in tweet_replies.items():
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

    def delete_from_db(self):
        from chat_bot_package import db
        from chat_bot_package.database_tables import MainTweet, ReplyTweet
        with open(self.location, 'r', encoding='utf-8') as read_file:
            tweet_replies = json.load(read_file)
            for t_id, t_data in tweet_replies.items():
                t_id_replies = t_data['ids_replied']
                if len(t_id_replies) < 2:
                    if len(list(MainTweet.query.filter_by(tweeter_id=t_id))) == 1:
                        MainTweet.query.filter_by(tweeter_id=t_id).delete()
                        print(t_id)
                        db.session.commit()


def fix_JSON(jsonStr):
    # First remove the " from where it is supposed to be.
    jsonStr = re.sub(r'\\', '', jsonStr)
    jsonStr = re.sub(r'{"', '{`', jsonStr)
    jsonStr = re.sub(r'"}', '`}', jsonStr)
    jsonStr = re.sub(r'":"', '`:`', jsonStr)
    jsonStr = re.sub(r'":', '`:', jsonStr)
    jsonStr = re.sub(r'","', '`,`', jsonStr)
    jsonStr = re.sub(r'",', '`,', jsonStr)
    jsonStr = re.sub(r',"', ',`', jsonStr)
    jsonStr = re.sub(r'\["', '\[`', jsonStr)
    jsonStr = re.sub(r'"\]', '`\]', jsonStr)

    # Remove all the unwanted " and replace with ' '
    jsonStr = re.sub(r'"', ' ', jsonStr)

    # Put back all the " where it supposed to be.
    jsonStr = re.sub(r'\`', '\"', jsonStr)

    return jsonStr


def get_models(model_name):
    print(model_name)
    predictions = pkl.load(open(f'chat_bot_package/model_outputs/{model_name}/predictions.pkl', 'rb'))
    responses = pkl.load(open(f'chat_bot_package/model_outputs/{model_name}/responses.pkl', 'rb'))
    dialogues = pkl.load(open(f'chat_bot_package/model_outputs/{model_name}/dialogues.pkl', 'rb'))
    predictions = [fix_JSON(r) for r in predictions]
    responses = [fix_JSON(r) for r in responses]
    dialogues = [fix_JSON(r) for r in dialogues]
    return predictions, responses, dialogues