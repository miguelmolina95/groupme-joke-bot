from flask import *
import requests
import re
import json
app = Flask(__name__, template_folder='templates')

headers = {'Content-Type': 'application/json'}
bot_id = '43809307b901e29b876e7ad711'

def send_message(content):
	request.post('https://api.groupme.com/v3/bots/post', data=json.dumps({'bot_id': bot_id, 'text': content}), headers=headers)

@app.route('/', methods=['GET', 'POST'])
def chat():
	if request.method == 'GET':
		return render_template('home.jinja')

	send_message('BS')

	message = request.get_json(silent=True)

	if message['name'].lower() != 'joke bot':
		if 'hello joke bot' in message['text'].lower():
			send_message('Greetings human if you would like to find out more about me visit at my home page:  https://joke-bot-486.herokuapp.com/')

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000, debug=True)
