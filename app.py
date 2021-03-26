from flask import Flask
import text
import voice

if __name__ == '__main__':
    app = Flask(__name__)

    @app.route('/', methods=['GET', 'POST'])
    def root():
        return 'Covidwa Notifications'

    app.route('/text', methods=['GET', 'POST'])(text.respond)

    app.route('/voice', methods=['GET', 'POST'])(voice.answer)
    app.route('/gather', methods=['GET', 'POST'])(voice.gather)

    app.run(debug=True, host='0.0.0.0')
