from .helpers import make_con, make_end
from models import db
from models.customer import Customer

def handle_registration(phone, text):
    parts = text.split('*') if text else []
    step = len(parts)

    # Step 1: ask name (user typed '1' as first)
    if step == 1:
        return make_con("Enter your FULL NAME:")

    # Step 2: payment method selection
    if step == 2:
        return make_con("Select Payment Method:\\n1. Mobile Money\\n2. Cash\\n3. Card")

    # Step 3: GPS address
    if step == 3:
        return make_con("Enter your GPS Address (GhanaPost):")

    # Step 4: confirm
    if step == 4:
        name = parts[1]
        pay_map = {'1':'MoMo','2':'Cash','3':'Card'}
        payment = pay_map.get(parts[2], 'MoMo')
        gps = parts[3]
        return make_con(f"Confirm Registration:\\nName: {name}\\nPayment: {payment}\\nGPS: {gps}\\n\\n1. Confirm\\n2. Cancel")

    # Step 5: save on confirm
    if step >= 5:
        if parts[4] != '1':
            return make_end('Registration cancelled.')
        name = parts[1]
        pay_map = {'1':'MoMo','2':'Cash','3':'Card'}
        payment = pay_map.get(parts[2], 'MoMo')
        gps = parts[3]

        cust = Customer.query.filter_by(phone=phone).first()
        if not cust:
            cust = Customer(name=name, phone=phone, payment_method=payment, primary_location=gps, registered=True)
            cust.set_location('Home', gps)
            db.session.add(cust)
        else:
            cust.name = name
            cust.payment_method = payment
            cust.primary_location = gps
            cust.registered = True
            cust.set_location('Home', gps)
        db.session.commit()
        return make_end(f"Registration successful. Welcome {name}!")

    return make_end('Invalid registration step.')
