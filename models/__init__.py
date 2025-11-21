from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

# import models so they register with SQLAlchemy
from .customer import Customer
from .order import Order
from .rating import Rating
from .driver import Driver
