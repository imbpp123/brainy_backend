import datetime
from sqlalchemy.orm import validates
from app import db


def validate_float(key, value):
    try:
        value = float(value)
    except ValueError:
        raise ValueError("Field %s has wrong value: %s" % (key, value))
    return value


def validate_datetime(key, value):
    def try_to_convert(date_str: str, date_format: str):
        try:
            date_result = datetime.datetime.strptime(date_str, date_format)
        except ValueError:
            date_result = False
        return date_result

    result = try_to_convert(value, '%Y-%m-%d %H:%M:%S.%f')
    if result is False:
        result = try_to_convert(value, '%Y-%m-%d %H:%M:%S')
    if result is False:
        raise ValueError("Field %s has wrong value: %s" % (key, value))
    return result


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
    updated_at = db.Column(db.DateTime)

    @validates('id')
    def validate_id(self, key, value):
        try:
            value = int(value)
        except ValueError:
            raise ValueError("Field %s has wrong value: %s" % (key, value))
        return value

    @validates('so2')
    def validate_so2(self, key, value):
        return validate_float(key, value)

    @validates('no2')
    def validate_no2(self, key, value):
        return validate_float(key, value)

    @validates('o3')
    def validate_o3(self, key, value):
        return validate_float(key, value)

    @validates('pm10')
    def validate_pm10(self, key, value):
        return validate_float(key, value)

    @validates('pm2_5')
    def validate_pm2_5(self, key, value):
        return validate_float(key, value)

    @validates('time_instant')
    def validate_time_instant(self, key, value):
        return validate_datetime(key, value)

    @validates('updated_at')
    def validate_updated_at(self, key, value):
        return validate_datetime(key, value)

    @validates('created_at')
    def validate_created_at(self, key, value):
        return validate_datetime(key, value)

    def __repr__(self):
        return '<Measurand {}>'.format(self.id, self.created_at, self.updated_at, self.time_instant)
