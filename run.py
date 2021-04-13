from chat_bot_package import app
import os


if __name__ == '__main__':
    print(os.path.dirname(__file__))
    app.run(debug=True)
