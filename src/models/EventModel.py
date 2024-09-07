# src/models/ActivityModel.py
from . import db
import datetime
from marshmallow import fields, Schema, INCLUDE, ValidationError

        
class EventModel(db.Model):

    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.DateTime)
    source = db.Column(db.String(512), nullable=True)
    eventtype = db.Column(db.String(512), nullable=True)
    info = db.Column(db.String(512), nullable=True)
    details = db.Column(db.String(512), nullable=True)


    def __init__(self, data = None):

        if data is not None:
            self.datetime = data.get('datetime')
            self.source = data.get('source')
            self.eventtype = data.get('eventtype')
            self.info = data.get('info')
            self.details = data.get('details')

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        for key, item in data.items():
            setattr(self, key, item)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
  
    @staticmethod
    def get_all():
        return EventModel.query.order_by(EventModel.datetime.desc()).limit(1000).all()

        # return EventModel.query.all()
    @staticmethod
    def get_all_by_date(start, end):
        return EventModel.query.filter((EventModel.datetime>= start) & (EventModel.datetime <= end)).order_by(EventModel.datetime.desc()).limit(1000).all()


    @staticmethod
    def get_one(id):
        return EventModel.query.get(id)

    def __repr__(self):
        return '<id {}>'.format(self.id)

class EventSchema(Schema):
    class Meta:
        unknown = INCLUDE
    id = fields.Int(dump_only=True)

    
    datetime = fields.DateTime()
    source = fields.Str()
    eventtype = fields.Str()
    info = fields.Str()
    details = fields.Str()

