from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Eatery(db.Model):
  __tablename__ = 'eateries'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String, nullable=False)
  in_session = db.Column(db.Boolean, nullable=False)
  weekday = db.Column(db.String, nullable=False)
  start_time = db.Column(db.String, nullable=False)
  end_time = db.Column(db.String, nullable=False)
  swipes = db.Column(db.Integer, nullable=False)
  counter = db.Column(db.Integer, nullable=False)

  def __init__(self, **kwargs):
    self.name = kwargs.get('name', '')
    self.in_session = kwargs.get('in_session', True)
    self.weekday = kwargs.get('weekday', '')
    self.start_time = kwargs.get('start_time', '')
    self.end_time = kwargs.get('end_time', '')
    self.swipes = kwargs.get('swipes', 0)
    self.counter = kwargs.get('counter', 0)

  def serialize(self):
    return {
      'id': self.id,
      'name': self.name,
      'in_session': self.in_session,
      'weekday': self.weekday,
      'start_time': self.start_time,
      'end_time': self.end_time,
      'swipes': self.swipes,
      'counter': self.counter
    }
