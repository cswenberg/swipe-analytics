import json
import requests
from datetime import datetime, timedelta

file_path = '../data.log'
endpoint = 'http://localhost:5000/eateries/'
weekdays = {
  0: 'monday',
  1: 'tuesday',
  2: 'wednesday',
  3: 'thursday',
  4: 'friday',
  5: 'saturday',
  6: 'sunday'
}


def read():
  with open(file_path, 'r') as f:
    i = 0
    test_string = ""
    for line in f:
      try:
        if i % 2 == 1:
          i += 1
          continue
        obj = json.loads(line)
        if obj['TIMESTAMP'] == 'Invalid date':
          raise Exception
        date = datetime.strptime(obj['TIMESTAMP'], '%Y-%m-%d %I:%M:00 %p')
        in_session = True
        weekday = weekdays[date.weekday()]
        if date.minute > 30:
          delta = timedelta(minutes=30)
          start_time = date.strftime('%I:30 %p')
          end_time = (date+delta).strftime('%I:00 %p')
        elif date.minute == 0:
          delta = timedelta(minutes=1)
          start_time = (date-delta).strftime('%I:30 %p')
          end_time = date.strftime('%I:00 %p')
        elif date.minute <= 30:
          start_time = date.strftime('%I:00 %p')
          end_time = date.strftime('%I:30 %p')
        if ('{} {} - {}'.format(weekday, start_time, end_time)) != test_string:
          count = 1
          test_string = '{} {} - {}'.format(weekday, start_time, end_time)
          print(test_string)
        else:
          count = 0
        for place in obj['UNITS']:
          print('Place: %s, Start_time: %s, End_time: %s, Counter: %d', place['UNIT_NAME'], start_time, end_time, count)
          requests.post(endpoint, data=json.dumps({
              "name": place['UNIT_NAME'],
              "in_session": in_session,
              "weekday": weekday,
              "start_time": start_time,
              "end_time": end_time,
              "swipes": place['CROWD_COUNT'],
              "counter": count
          }))
      except Exception as e:
        print(e)
      i += 1


read()
