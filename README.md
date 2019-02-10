# Brainy Project Task

This project uses SQLite as database. It can be easily configured for MySQL, PostgreSQL or anything else b\c it uses
ORM SQLAlchemy

Project uses Basic authorization, but it has very week encryption. It can be easily switched to Digest. I prefer OAuth.

## What can be improved

There is no test coverage here. It is just test project, so, i didnt implement it.
Some parts of code looks like student work. I am not so experienced in Python. I can spend another 1-2 days and makes it looks much better

## Requirements

1. Python version > 3.5

## Installation

1. Clone project to you computer
2. Run ```$ pip3 install -r requirements.txt``` to install all requirements for the project.
3. Run ```$ flask db upgrade``` in project root folder. Database with tables will be created.
4. Run ```$ python3 console.py file_with_data.csv``` in root folder. Data from CSV file will be uploaded to database in some seconds(minutes).
5. Run ```$ flask run``` to run project on your local machine.

You are ready to work with project.

## How To Run Exercises

### Exercise 1

URI parameters:
* variable - Variable to work over (so2, no2, co, ...).

Parameters:
* timestamp_start - Timestamp start;
* timestamp_stop - Timestamp end;
* measure - Statistical measure to return (sum, mean, max, min, ..., all).

Example:

```
curl -X GET \
  'http://127.0.0.1:5000/variable/no2?timestamp_start=2016-10-01%2000:00:00&timestamp_stop=2016-10-11%2020:00:00&measure=all' \
  -H 'Accept: application/json' \
  -H 'Authorization: Basic dGVzdDpwYXNzd29yZA==' \
  -H 'Content-Type: application/json'
```
  
### Exercise 2

URI parameters:
* variable - Variable to work over (so2, no2, co, ...);
* station - Air quality station name.

Parameters:
* timestamp_start - Timestamp start;
* timestamp_stop - Timestamp end.

Example:

```
curl -X GET \
  'http://127.0.0.1:5000/variable/no2/station/aq_alcala_zamora/overcome?timestamp_start=2016-10-01%2000:00:00&timestamp_stop=2016-10-11%2020:00:00' \
  -H 'Accept: application/json' \
  -H 'Authorization: Basic dGVzdDpwYXNzd29yZA==' \
  -H 'Content-Type: application/json' 
```  

### Exercise 3

URI parameters:
* variable - Variable to work over (so2, no2, co, ...);
* station - Air quality station name.

Parameters:
* timestamp_start - Timestamp start;
* timestamp_stop - Timestamp end;
* measure - Statistical measure to return (sum, mean, max, min, ..., all);
* period - Minutes for the step aggregation.

Example:

```
curl -X GET \
  'http://127.0.0.1:5000/variable/no2/station/aq_alcala_zamora/timeseries?timestamp_start=2016-10-01%2000:00:00&timestamp_stop=2016-10-11%2020:00:00&measure=mean&period=55' \
  -H 'Accept: application/json' \
  -H 'Authorization: Basic dGVzdDpwYXNzd29yZA==' \
  -H 'Content-Type: application/json'
```  

