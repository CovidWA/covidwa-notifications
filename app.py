from flask import Flask
import routes

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def root():  # For testing
    return '<h1>Covidwa Notifications</h1>'


app.route('/text', methods=['GET', 'POST'])(routes.text)

app.route('/voice', methods=['GET', 'POST'])(routes.voice)
app.route('/gather', methods=['GET', 'POST'])(routes.voice_gather)

app.route('/notifier', methods=['POST'])(routes.notifier)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
