from flask import *
import requests
import re
import json
app = Flask(__name__, template_folder='templates')

headers = {'Content-Type': 'application/json'}
bot_id = '192f91528191d46b1eddc30802'

def send_message(content):
	print 'About send message'
	requests.post('https://api.groupme.com/v3/bots/post', json={'bot_id': bot_id, 'text': content}, headers=headers)

@app.route('/', methods=['GET', 'POST'])
def chat():
	if request.method == 'GET':
		return render_template('home.jinja')

	message = request.get_json(silent=True)

	if message['name'].lower() != 'joke bot':
		if 'hello joke bot' in message['text'].lower():
			send_message('Greetings human if you would like to find out more about me visit at my home page:  https://joke-bot-486.herokuapp.com/')

	return "ok", 200

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000, debug=True)
