from pprint import pprint

from flask import request, json
import statistics

from sqlalchemy.sql import func

from app import app, db
from app.models import Measurand


def get_response(data, status):
    response = app.response_class(
        response=json.dumps(data),
        status=status,
        mimetype='application/json'
    )
    return response


@app.route('/variable/<string:variable>/station/<string:station>/overcome')
def stations_overcome(variable: str, station: str):
    overcome = {
        'so2': 180,
        'no2': 200,
        'co': 200,
        'o3': 200,
        'pm10': 50,
        'pm2_5': 40
    }
    timestamp_start = request.args.get('timestamp_start')
    timestamp_stop = request.args.get('timestamp_stop')

    if hasattr(Measurand, variable) is not True:
        return get_response({'error': 'Field does not exits'}, 400)
    measurand_attr = getattr(Measurand, variable)

    result = db.session.query(func.date(getattr(Measurand, 'time_instant')).label('date_instant')) \
        .group_by('date_instant') \
        .filter_by(id_entity=station) \
        .filter(Measurand.time_instant > timestamp_start) \
        .filter(Measurand.time_instant < timestamp_stop) \
        .filter(measurand_attr >= overcome[variable]) \
        .count()

    return get_response(result, 200)


@app.route('/variable/<string:variable>')
def stations_stats(variable: str):
    timestamp_start = request.args.get('timestamp_start')
    timestamp_stop = request.args.get('timestamp_stop')
    measure = request.args.get('measure', default='all')

    if measure not in ['sum', 'mean', 'max', 'min']:
        measure = ['sum', 'mean', 'max', 'min']
    else:
        measure = [measure]

    if hasattr(Measurand, variable) is not True:
        return get_response({'error': 'Field does not exits'}, 400)

    measurand_attr = getattr(Measurand, variable)

    result = db.session.query(
            Measurand.id_entity,
            func.avg(measurand_attr).label('mean'),
            func.min(measurand_attr).label('min'),
            func.max(measurand_attr).label('max'),
            func.sum(measurand_attr).label('sum'),
        )\
        .group_by(Measurand.id_entity) \
        .filter(Measurand.time_instant > timestamp_start) \
        .filter(Measurand.time_instant < timestamp_stop) \
        .all()

    data = []
    for item in result:
        new_station_data = {
            'station': item.id_entity
        }
        for val in measure:
            new_station_data[val] = getattr(item, val)
        data.append(new_station_data)

    return get_response(data, 200)
