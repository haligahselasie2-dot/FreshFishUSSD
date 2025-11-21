from datetime import datetime
from . import db
import json

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    phone = db.Column(db.String(32), unique=True, nullable=False)

    payment_method = db.Column(db.String(32), default='MoMo')
    primary_location = db.Column(db.String(128), nullable=True)
    registration_step = db.Column(db.Integer, default=0)
    registered = db.Column(db.Boolean, default=False)
    locations = db.Column(db.Text, default='{}')  # JSON string

    completed_orders = db.Column(db.Integer, default=0)
    avg_rating = db.Column(db.Float, default=0.0)
    on_time_rate = db.Column(db.Float, default=1.0)
    credit_score = db.Column(db.Integer, default=50)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def get_locations(self):
        try:
            return json.loads(self.locations or "{}")
        except:
            return {}

    def set_location(self, label, gps):
        locs = self.get_locations()
        locs[label] = gps
        self.locations = json.dumps(locs)
