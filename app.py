from dotenv import load_dotenv
from flask import Flask
import endpoints

app = Flask(__name__)
load_dotenv()

# For testing
app.route('/', methods=['GET', 'POST'])(lambda: '<h1>Covidwa Notifications</h1>')

# SMS endpoint
app.route('/text', methods=['GET', 'POST'])(endpoints.text)

# Voice endpoints
app.route('/voice', methods=['GET', 'POST'])(endpoints.voice)
app.route('/gather', methods=['GET', 'POST'])(endpoints.voice_gather)

# API endpoint
app.route('/notifier', methods=['POST'])(endpoints.notifier)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
