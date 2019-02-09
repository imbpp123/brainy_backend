from flask import request, json
from app import app
from app.models import Measurand
import statistics


@app.route('/station/<string:station>/variable/<string:variable>')
def stations_stats(station: str, variable: str):
    def get_real_measure(value: str):
        result = ['sum', 'mean', 'max', 'min', 'median']
        if value != 'all' and value in result:
            result.clear()
            result.append(value)
        return result

    timestamp_start = request.args.get('timestamp_start')
    timestamp_stop = request.args.get('timestamp_stop')
    measure = get_real_measure(request.args.get('measure', default='all'))

    result = Measurand.query\
        .filter_by(id_entity=station)\
        .filter(Measurand.time_instant > timestamp_start) \
        .filter(Measurand.time_instant < timestamp_stop) \
        .all()

    data = []
    for measurement in result:
        data.append(getattr(measurement, variable))

    maths = {
        'sum': sum(data),
        'mean': statistics.mean(data),
        'max': max(data),
        'min': min(data),
        'median': statistics.median(data)
    }

    result = {}
    for measure_type in measure:
        result[measure_type] = maths[measure_type]

    response = app.response_class(
        response=json.dumps(result),
        status=200,
        mimetype='application/json'
    )
    return response
