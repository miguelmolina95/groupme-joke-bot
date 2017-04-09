from flask import *
from flask_sqlalchemy import SQLAlchemy
import requests
import re
import json
import random
import os
from preprocess import *
from stemmer import *
app = Flask(__name__, template_folder='templates')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://acumpyderhsdmr:72e27d46c70162bbb212e4f94817786a3b3fd90095f49ebbd664a23da2d8ec41@ec2-54-221-220-82.compute-1.amazonaws.com:5432/d8lf3gpn63kgl8'
db = SQLAlchemy(app)

# basic database model for storing jokes
class Joke(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	joke = db.Column(db.String(300))
	labels = db.Column(db.String(300))

	def __init__(self, joke, labels):
		self.joke = joke
		self.labels = labels.split('|')

	def check_labels_satisfied(sentence):
		A = set(sentence.split())
		B = set(self.labels)

		sim = float(len(A.intersection(B))) / len(A.union(B))

		return sim

headers = {'Content-Type': 'application/json'}
bot_ids = {'29075120': '9a3cc4a1c84fb5fd6e1b499b72', '30076812': 'b7fd76a8184164b143f586e05a'}

GREETING_KEYWORDS = ["hello", "hi", "greetings", "sup", "what's up", "hola", "hey"]

GREETING_RESPONSES = ["sup bro", "hey", "*nods*", "hey you get my snap?", "hola", "greetings human"]

def check_for_greeting(sentence):
	"""If any of the words in the user's input was a greeting, return a greeting response"""
	for key_word in GREETING_KEYWORDS:
		if key_word in sentence:
			return random.choice(GREETING_RESPONSES)
	return False

def send_message(content, bot_id, old_message):
	print 'About send message'
	requests.post('https://api.groupme.com/v3/bots/post', json={'bot_id': bot_id, 'text': content, 'attachments': ["loci": [], "type": "mentions", "user_ids": [old_message['user_id']]]}, headers=headers)

@app.route('/', methods=['GET', 'POST'])
def chat():
	if request.method == 'GET':
		return render_template('home.jinja')

	message = request.get_json(silent=True)
	bot_id = bot_ids[message['group_id']]

	if message['name'].lower() != 'joke bot':
		resp = check_for_greeting(message['text'].lower())

		if resp and 'joke bot' in message['text'].lower():
			# resp = '@' + message['name'] + ' ' + resp
			send_message(resp, bot_id, message)
		elif 'chicken' in message['text'].lower():
			result = Joke.query.all()[0]
			print result.joke
			assert(isinstance(result.joke, str))
			send_message(result.joke, bot_id, message)

	return "ok", 200

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000, debug=True)
