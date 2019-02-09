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


@app.route('/stations/<string:station>/overcome')
def stations_overcome(station: str):
    pass


@app.route('/station/<string:station>/variable/<string:variable>')
def stations_stats(station: str, variable: str):
    def get_real_measure(value: str):
        result = ['sum', 'mean', 'max', 'min']
        if value != 'all' and value in result:
            result.clear()
            result.append(value)
        return result

    timestamp_start = request.args.get('timestamp_start')
    timestamp_stop = request.args.get('timestamp_stop')
    measure = get_real_measure(request.args.get('measure', default='all'))

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
