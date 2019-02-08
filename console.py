import click
import csv
from app import app

@click.command()
@click.argument('filename')
def upload(filename):
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in reader:
            click.echo(', '.join(row))


if __name__ == '__main__':
    upload()
