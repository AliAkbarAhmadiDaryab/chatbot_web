from chat_bot_package import tweet_utils as tu

t_db = tu.DBTweet(file_path=r"C:\Users\closer\PycharmProjects\chatbot_web\2019-05-16.json")
t_db.save_to_db()
