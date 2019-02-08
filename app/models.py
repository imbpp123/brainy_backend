from app import db


class Measurand(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_entity = db.Column(db.String)
    so2 = db.Column(db.Float)
    no2 = db.Column(db.Float)
    o3 = db.Column(db.Float)
    pm10 = db.Column(db.Float)
    pm2_5 = db.Column(db.Float)
    time_instant = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime)

    def __repr__(self):
        return '<Measurand {}>'.format(self.id)
