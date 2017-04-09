from flask import *
import requests
import re
import json
import random
app = Flask(__name__, template_folder='templates')

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)

headers = {'Content-Type': 'application/json'}
bot_ids = {'29075120': '9a3cc4a1c84fb5fd6e1b499b72', '30076812': 'b7fd76a8184164b143f586e05a'}

GREETING_KEYWORDS = ["hello", "hi", "greetings", "sup", "what's up", "hola"]

GREETING_RESPONSES = ["sup bro", "hey", "*nods*", "hey you get my snap?", "hola", "greetings human"]

def check_for_greeting(sentence):
	"""If any of the words in the user's input was a greeting, return a greeting response"""
	for word in sentence:
		if word.lower() in GREETING_KEYWORDS:
			return random.choice(GREETING_RESPONSES)
	return False

def send_message(content, bot_id):
	print 'About send message'
	requests.post('https://api.groupme.com/v3/bots/post', json={'bot_id': bot_id, 'text': content}, headers=headers)

@app.route('/', methods=['GET', 'POST'])
def chat():
	if request.method == 'GET':
		return render_template('home.jinja')

	message = request.get_json(silent=True)
	bot_id = bot_ids[message['group_id']]

	if message['name'].lower() != 'joke bot':
		resp = check_for_greeting(message['text'].split())
		if resp and 'joke bot' in message['text'].lower():
			send_message(resp, bot_id)

	return "ok", 200

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000, debug=True)
