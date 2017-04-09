from app import Joke

joke = Joke("Why did the chicken cross the road? To get to the other side.", "chicken|road")
db.session.add(joke)
db.session.commit()