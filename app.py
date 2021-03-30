from flask import Flask, request
from flask_heroku import Heroku
from flask_sqlalchemy import SQLAlchemy
import endpoints
import sys

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
heroku = Heroku(app)
db = SQLAlchemy(app)


class Dataentry(db.Model):
    __tablename__ = 'test'
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Text())

    def __init__(self, data):
        self.data = data


@app.route('/submit', methods=['POST'])
def post_to_db():
    in_data = Dataentry(request.form['data'])
    data = in_data.__dict__.copy()
    del data['_sa_instance_state']
    try:
        db.session.add(indata)
        db.session.commit()
    except Exception as e:
        print(f'\n FAILED entry: {data}\n')
        print(e)
        sys.stdout.flush()
    return 'Success!'


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
