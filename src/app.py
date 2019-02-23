import json
from db import db, Eatery
from flask import Flask, request

db_filename = "eateries.db"
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///%s' % db_filename
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

db.init_app(app)
with app.app_context():
  db.create_all()

@app.route('/eateries/', methods=['POST'])
def create_eatery():
  print(request.data)
  content = json.loads(request.data)

  existing_eatery = Eatery.query.filter_by(
      name=content.get('name', ''),
      in_session=content.get('in_session'),
      weekday=content.get('weekday'),
      start_time=content.get('start_time'),
      end_time=content.get('end_time')
  ).first()

  if existing_eatery is not None:
    print('existing eatery found')
    existing_eatery.swipes += content.get('swipes', 0)
    existing_eatery.counter += content.get('counter', 0)
    db.session.commit()
    return json.dumps({'success': True, 'data': existing_eatery.serialize()})

  new_eatery = Eatery(
    name=content.get('name', ''),
    in_session=content.get('in_session', True),
    weekday=content.get('weekday', ''),
    start_time=content.get('start_time', ''),
    end_time=content.get('end_time', ''),
    swipes=content.get('swipes', 0),
    counter=content.get('counter', 0)
  )

  db.session.add(new_eatery)
  db.session.commit()

  return json.dumps({'success': True, 'data': new_eatery.serialize()})


@app.route('/eateries/<int:eatery_id>/', methods=['POST'])
def update_eatery(eatery_id):
  eatery = Eatery.query.filter_by(id=eatery_id).first()
  content = json.loads(request.data)

  eatery.swipes += content.get('swipes', 0)
  eatery.counter += content.get('counter', 0)

  db.session.commit()

  return json.dumps({'success': True, 'data': eatery.serialize()})


@app.route('/eateries/')
def get_eateries():
  eateries = Eatery.query.all()
  return json.dumps({'success': True, 'data': [eatery.serialize() for eatery in eateries]})


@app.route('/eateries/<int:in_session>/<string:weekday>/')
def get_filtered_eateries(in_session, weekday):
  eateries = Eatery.query.filter_by(in_session=in_session, weekday=weekday)
  return json.dumps({'success': True, 'data': [eatery.serialize() for eatery in eateries]})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    print('running on port 5000, use route /eateries/')
