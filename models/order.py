from datetime import datetime
from . import db

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    fish_type = db.Column(db.String(64))
    quantity = db.Column(db.Float)
    price = db.Column(db.Float)
    location_label = db.Column(db.String(64))
    location_gps = db.Column(db.String(128))
    status = db.Column(db.String(32), default='Pending')  # Pending, PickedUp, Delivered, Cancelled
    qr_path = db.Column(db.String(256), nullable=True)
    driver = db.Column(db.String(64), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    picked_at = db.Column(db.DateTime, nullable=True)
    delivered_at = db.Column(db.DateTime, nullable=True)
