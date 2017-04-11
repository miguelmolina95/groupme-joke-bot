from app import Joke
from app import db

db.drop_all()
db.create_all()

with open('jokes.txt') as file:
	for line in file:
		entry = line.split('|')
		if len(entry) == 2:
			joke = Joke(entry[0], entry[1])
			db.session.add(joke)
			db.session.commit()

result = Joke.query.all()[0]
print (result.joke)
