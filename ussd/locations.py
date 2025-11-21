from .helpers import make_con, make_end
from models.customer import Customer
from models import db

def handle_locations(phone, text):
    parts = text.split('*') if text else []
    # entry: '4'
    if len(parts) == 1:
        return make_con('1. View Saved Locations\\n2. Add Location\\n3. Set Default\\n4. Delete Location')

    action = parts[1] if len(parts) > 1 else ''
    if action == '1':
        cust = Customer.query.filter_by(phone=phone).first()
        if not cust: return make_end('No customer found.')
        locs = cust.get_locations()
        if not locs: return make_end('No saved locations.')
        resp = ''
        for k,v in locs.items():
            resp += f"{k} - {v}\\n"
        return make_end(resp)

    if action == '2':
        # adding: '4*2' => ask GPS; '4*2*GPS*Label' => add
        if len(parts) == 2:
            return make_con('Enter GPS code for new location:')
        gps = parts[2]
        label = parts[3] if len(parts) > 3 else 'Other'
        cust = Customer.query.filter_by(phone=phone).first()
        if not cust: return make_end('No customer found.')
        cust.set_location(label, gps)
        db.session.commit()
        return make_end('Location added.')

    return make_end('Feature not complete yet.')
