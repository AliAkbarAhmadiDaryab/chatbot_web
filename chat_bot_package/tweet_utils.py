from glob import glob
import os
from datetime import datetime, timedelta
import json
import codecs


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
            with open(os.path.join(RawTweet.dir_location, '{}.txt').format(file_name[:10]), 'r', encoding='utf-8') as read_file:
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