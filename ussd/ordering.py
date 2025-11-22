from .helpers import make_con, make_end
from models.customer import Customer
from models.order import Order
from models import db
import os, json  # qrcode removed
from config import Config

PRICE_PER_KG = 40.0

def handle_ordering(phone, text):
    parts = text.split('*') if text else []

    # entry '2'
    if len(parts) == 1:
        return make_con('Select Fish:\n1. Tilapia\n2. Catfish\n3. Other')

    if len(parts) == 2:
        return make_con('Enter quantity in kg (number only):')

    if len(parts) == 3:
        cust = Customer.query.filter_by(phone=phone).first()
        if not cust:
            return make_end('You must register first.')

        locs = cust.get_locations()
        menu = ''
        i = 1
        for label, gps in locs.items():
            menu += f"{i}. {label} - {gps}\n"
            i += 1

        menu += f"{i}. Add New Location\n{i+1}. Call for Assistance"
        return make_con(menu)

    if len(parts) >= 4:
        fish_map = {'1': 'Tilapia', '2': 'Catfish', '3': 'Other'}
        fish = fish_map.get(parts[1], 'Other')

        try:
            qty = float(parts[2])
        except:
            return make_end('Invalid quantity.')

        loc_choice = parts[3]
        cust = Customer.query.filter_by(phone=phone).first()
        locs = cust.get_locations()

        try:
            lc = int(loc_choice)
            if 1 <= lc <= len(locs):
                label = list(locs.keys())[lc - 1]
                gps = list(locs.values())[lc - 1]
            elif lc == len(locs) + 1:
                return make_con('Enter GPS code for new location:')
            else:
                return make_end('Please call support for assistance.')
        except ValueError:
            # user typed a GPS code directly
            gps = loc_choice
            label = 'Other'
            locs[label] = gps
            cust.locations = json.dumps(locs)
            db.session.commit()

        # create and save order WITHOUT QR
        total = qty * PRICE_PER_KG
        order = Order(
            customer_id=cust.id,
            fish_type=fish,
            quantity=qty,
            price=total,
            location_label=label,
            location_gps=gps
        )

        db.session.add(order)
        db.session.commit()

        # QR REMOVED – nothing else to save

        return make_end(f"Order placed! ID:{order.id} Total: GH₵{total}")

    return make_end('Invalid ordering step.')
