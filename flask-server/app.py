#@author Ozgur Tarim

from asyncio import events
from datetime import datetime
from email.policy import default
from urllib import request
from flask import Flask, request
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)

#had to use mozilla firefox because of CORS , did not work any other browser


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#my local database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:ozgur4520@localhost:5433/social-app'
db = SQLAlchemy(app)
app.config['CORS_HEADERS'] = 'Content-Type'


#creating database model it will be stored in PostgreSQL 14 Tables event
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)

    def __repr__(self):
        return f"Event: {self.description}"

    def __init__(self, description):
        self.description = description

#information about event stored in db
def format_event(event):
    return{
        "description": event.description,
        "id" : event.id,
        "created_at": event.created_at
    }

#post event -Creates a new resource
@app.route('/events', methods = ['POST'])
@cross_origin()
def tweet():
    description = request.json['description']
    event = Event(description)
    db.session.add(event)
    db.session.commit()
    return format_event(event)


#get all events -Retrieves a resource
@app.route('/events', methods = ['GET'])
@cross_origin()
def get_events():
    #using orderby
    events =Event.query.order_by(Event.created_at.asc()).all()
    event_list = []
    for event in events:
        event_list.append(format_event(event))
    return{'events': event_list }

#get single event - Retrieves a resource
@app.route('/events/<id>', methods = ['GET'])
@cross_origin()
def get_event(id):
    event = Event.query.filter_by(id=id).one()
    formatted_event= format_event(event)
    return{'event': formatted_event}


#update an event-	Updates an existing resource
#trying to add comment for each tweet
@app.route('/events/<id>', methods = ['PUT'])
@cross_origin()
def update_event(id):
    event = Event.query.filter_by(id=id)
    description = request.json['description']
    event.update(dict(description= description, created_at = datetime.utcnow()))
    db.session.commit()
    return {'event': format_event(event.one())}


if __name__ == '__main__':
    app.run()

