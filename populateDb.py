from app import Joke
from app import db

db.drop_all()
db.create_all()

joke = Joke("Why did the chicken cross the road? To get to the other side.", "chicken|road")
db.session.add(joke)
db.session.commit()

result = Joke.query.all()[0]
print (result.joke)
