# src/models/ActivityModel.py
from . import db
import datetime
from marshmallow import fields, Schema, INCLUDE, ValidationError

        
class IncidentModel(db.Model):

    __tablename__ = 'incidents'

    id = db.Column(db.Integer, primary_key=True)

    datetime = db.Column(db.DateTime)
    source = db.Column(db.String(512), nullable=True)
    incidenttype = db.Column(db.String(512), nullable=True)
    info = db.Column(db.String(512), nullable=True)
    positionx = db.Column(db.Float, nullable=True)
    positiony = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    latitude = db.Column(db.Float, nullable=True)
    altitude = db.Column(db.Float, nullable=True)
    distanceinmeter = db.Column(db.Float, nullable=True)
    imageinbytes = db.Column(db.LargeBinary, nullable=True)
    imagepath = db.Column(db.String, nullable=True)
    videopath = db.Column(db.String, nullable=True)
    section = db.Column(db.String, nullable=True)
    aiversion = db.Column(db.String, nullable=True)

    actualincident = db.Column(db.String, nullable=True)
    exportflag = db.Column(db.Boolean, nullable=True)
    actualincidentdetails = db.Column(db.String, nullable=True)

    
    # sequenceno = db.Column(db.Integer, nullable=True)

    # sequenceno = db.Column(db.Integer, nullable=True)
    # positionx = db.Column(db.Float, nullable=True)
    # positiony = db.Column(db.Float, nullable=True)
    # zoom = db.Column(db.Float, nullable=True)
    # focus = db.Column(db.Float, nullable=True)
    # remark = db.Column(db.String(128), nullable=True)

    def __init__(self, data = None):

        if data is not None:
            self.datetime = data.get('datetime')
            self.source = data.get('source')
            self.incidenttype = data.get('incidenttype')
            self.info = data.get('info')
            self.positionx = data.get('positionx')
            self.positiony = data.get('positiony')
            self.longitude = data.get('longitude')
            self.latitude = data.get('latitude')
            self.altitude = data.get('altitude')
            self.distanceinmeter = data.get('distanceinmeter')
            self.imageinbytes = data.get('imageinbytes')
            self.imagepath = data.get('imagepath')
            self.videopath = data.get('videopath')
            self.section = data.get('section')
            self.aiversion = data.get('aiversion')

            self.actualincident = data.get('actualincident')
            self.exportflag = data.get('exportflag')
            self.actualincidentdetails = data.get('actualincidentdetails')
            

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
        return IncidentModel.query.order_by(IncidentModel.datetime.desc()).limit(1000).all()

    # @staticmethod
    # def get_all_by_date(start, end):
    #     return IncidentModel.query.filter((IncidentModel.datetime>= start) & (IncidentModel.datetime <= end)).order_by(IncidentModel.datetime.desc()).limit(1000).all()


    @staticmethod
    def get_all_by_date(start, end):
        return IncidentModel.query.with_entities(
            IncidentModel.id ,
            IncidentModel.datetime ,
            IncidentModel.source ,
            IncidentModel.incidenttype,
            IncidentModel.info ,
            IncidentModel.positionx ,
            IncidentModel.positiony,
            IncidentModel.longitude,
            IncidentModel.latitude,
            IncidentModel.altitude ,
            IncidentModel.distanceinmeter ,
            IncidentModel.imagepath ,
            IncidentModel.videopath,
            IncidentModel.section,
            IncidentModel.aiversion,
            IncidentModel.actualincident,
            IncidentModel.exportflag,
            IncidentModel.actualincidentdetails
            ).filter((IncidentModel.datetime>= start) & (IncidentModel.datetime <= end)).order_by(IncidentModel.datetime.desc()).limit(1000).all()

    @staticmethod
    def get_all_by_latest10():
        return IncidentModel.query.with_entities(
            IncidentModel.id ,
            IncidentModel.datetime ,
            IncidentModel.info ,
            IncidentModel.imagepath ,
            ).order_by(IncidentModel.datetime.desc()).limit(10).all()



    @staticmethod
    def get_one(id):
        return IncidentModel.query.get(id)

    def __repr__(self):
        return '<id {}>'.format(self.id)

class IncidentSchema(Schema):
    class Meta:
        unknown = INCLUDE
    id = fields.Int(dump_only=True)

    
    datetime = fields.DateTime()
    source = fields.Str()
    incidenttype = fields.Str()
    info = fields.Str()
    positionx = fields.Float()
    positiony = fields.Float()
    longitude = fields.Float()
    latitude = fields.Float()
    altitude = fields.Float()
    distanceinmeter = fields.Float()

    imagepath = fields.Str()
    videopath = fields.Str()
    section = fields.Str()
    aiversion= fields.Str()

    actualincident= fields.Str()
    exportflag= fields.Boolean()
    actualincidentdetails= fields.Str()


    # imageinbytes = fields.Str()


    # datetime = db.Column(db.DateTime)
    # source = db.Column(db.String(512), nullable=True)
    # incidenttype = db.Column(db.String(512), nullable=True)
    # info = db.Column(db.String(512), nullable=True)
    # positionx = db.Column(db.Float, nullable=True)
    # positiony = db.Column(db.Float, nullable=True)
    # longitude = db.Column(db.Double, nullable=True)
    # latitude = db.Column(db.Double, nullable=True)
    # altitude = db.Column(db.Double, nullable=True)
    # distanceinmeter = db.Column(db.Float, nullable=True)
    # imageinbytes = db.Column(db.BytesField, nullable=True)

