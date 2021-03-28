from flask import Flask
import text
import voice
import notifier_api

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def root():  # For testing
    return '<h1>Covidwa Notifications</h1>'


app.route('/text', methods=['GET', 'POST'])(text.respond)

app.route('/voice', methods=['GET', 'POST'])(voice.answer)
app.route('/gather', methods=['GET', 'POST'])(voice.gather)

app.route('/notifier', methods=['POST'])(notifier_api.notify)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
