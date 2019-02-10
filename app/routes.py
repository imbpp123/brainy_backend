from flask import request, json
from sqlalchemy.sql import func
import pandas as pd
from app import app, db, auth
from app.models import Measurand

users = {
    'test': 'password',
    'admin': 'coolpassword'
}


@auth.get_password
def get_pw(username):
    if username in users:
        return users.get(username)
    return None


def get_response(data=None, status=200, body=None):
    if body is not None:
        response = app.response_class(
            response=body,
            status=status,
            mimetype='application/json'
        )
    else:
        response = app.response_class(
            response=json.dumps(data),
            status=status,
            mimetype='application/json'
        )
    return response


@app.route('/variable/<string:variable>/station/<string:station>/timeseries')
@auth.login_required
def variable_timeseries(variable: str, station: str):
    timestamp_start = request.args.get('timestamp_start')
    timestamp_stop = request.args.get('timestamp_stop')
    measure = request.args.get('measure')
    period = request.args.get('period', default=5)

    try:
        period = int(period)
    except ValueError:
        return get_response({'error': 'Field value does not exits'}, 400)

    if measure not in ['sum', 'mean', 'max', 'min']:
        return get_response({'error': 'Field value does not exits'}, 400)

    if timestamp_start is None or timestamp_stop is None:
        return get_response({'error': 'Field does not exits'}, 400)

    if hasattr(Measurand, variable) is not True:
        return get_response({'error': 'Field does not exits'}, 400)
    measurand_attr = getattr(Measurand, variable)

    data = db.session.query(Measurand.time_instant, measurand_attr.label(variable)) \
        .filter_by(id_entity=station) \
        .filter(Measurand.time_instant > timestamp_start) \
        .filter(Measurand.time_instant < timestamp_stop) \
        .all()

    df = pd.DataFrame(data, columns=['time_instant', variable])
    df.index = df['time_instant']
    del df['time_instant']

    df_resample = df.resample("%iT" % period)
    result = getattr(df_resample, measure)()

    return get_response(status=200,body=result.to_json(orient='columns'))


@app.route('/variable/<string:variable>/station/<string:station>/overcome')
@auth.login_required
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

    if timestamp_start is None or timestamp_stop is None:
        return get_response({'error': 'Field does not exits'}, 400)

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

    return get_response(data=result, status=200)


@app.route('/variable/<string:variable>')
@auth.login_required
def stations_stats(variable: str):
    timestamp_start = request.args.get('timestamp_start')
    timestamp_stop = request.args.get('timestamp_stop')
    measure = request.args.get('measure', default='all')

    if timestamp_start is None or timestamp_stop is None:
        return get_response({'error': 'Field does not exits'}, 400)

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

    return get_response(data=data, status=200)
