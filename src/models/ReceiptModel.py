from . import db
from datetime import datetime
from marshmallow import fields, Schema, INCLUDE

class ReceiptModel(db.Model):
    __tablename__ = 'receipts'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)  # Assuming you have a User model
    imageinbytes = db.Column(db.LargeBinary, nullable=True)
    upload_time = db.Column(db.DateTime, default=datetime.utcnow)
    filename = db.Column(db.String(256), nullable=False)
    result = db.Column(db.String, nullable=True)
    raw_text = db.Column(db.Text, nullable=True)
    parsed_data = db.Column(db.JSON, nullable=True)  # Assuming the parsed data is JSON
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    modified_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, onupdate=datetime.utcnow)

    def __init__(self, data=None):
        if data is not None:
            self.user_id = data.get('user_id')
            self.imageinbytes = data.get('imageinbytes')
            self.upload_time = data.get('upload_time', datetime.utcnow())
            self.filename = data.get('filename')
            self.result = data.get('result')
            self.raw_text = data.get('raw_text')
            self.parsed_data = data.get('parsed_data')
            self.created_at = datetime.utcnow()
            self.modified_at = datetime.utcnow()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        for key, item in data.items():
            setattr(self, key, item)
        self.modified_at = datetime.utcnow()  # Update modified time
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return ReceiptModel.query.order_by(ReceiptModel.upload_time.desc()).all()

    @staticmethod
    def get_one(id):
        return ReceiptModel.query.get(id)

    def __repr__(self):
        return '<Receipt id {}>'.format(self.id)


class ReceiptSchema(Schema):
    class Meta:
        unknown = INCLUDE
    
    id = fields.Int(dump_only=True)
    user_id = fields.Int(dump_only=True)
    upload_time = fields.DateTime()
    filename = fields.Str()
    result = fields.Str()
    raw_text = fields.Str()
    parsed_data = fields.Dict()  # Treat as dictionary
    created_at = fields.DateTime(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)

