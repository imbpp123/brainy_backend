import click
import csv
from app import app, db
from app.models import Measurand


def saveToDb(row):
    try:
        object = Measurand(
            id=row[0],
            id_entity=row[8],
            so2=row[2],
            no2=row[3],
            o3=row[7],
            co=row[6],
            pm10=row[4],
            pm2_5=row[5],
            time_instant=row[1],
            created_at=row[9],
            updated_at=row[10]
        )
        db.session.add(object)
    except ValueError:
        pass


@click.command()
@click.argument('filename')
def upload(filename):
    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quoting=0)
        for row in reader:
            saveToDb(row)
    db.session.commit()


if __name__ == '__main__':
    upload()
