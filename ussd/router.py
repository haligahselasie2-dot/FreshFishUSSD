from flask import Blueprint, request, Response
from .registration import handle_registration
from .ordering import handle_ordering
from .locations import handle_locations

ussd_bp = Blueprint('ussd_bp', __name__)

@ussd_bp.route("", methods=["POST"])
def ussd_entry():
    # telco will POST phoneNumber (or msisdn) and text
    phone = request.values.get('phoneNumber') or request.values.get('msisdn') or request.values.get('phone') or 'unknown'
    text = request.values.get('text', '')  # e.g. "1*2*3" or ""
    parts = text.split('*') if text else []

    if not parts:
        return Response("CON Welcome to FreshFish\n1. Register\n2. Order Fish\n3. My Orders\n4. Locations\n5. Help", mimetype='text/plain')

    first = parts[0]
    if first == '1':
        return handle_registration(phone, text)
    if first == '2':
        return handle_ordering(phone, text)
    if first == '4':
        return handle_locations(phone, text)

    return Response("END Option not implemented yet.", mimetype='text/plain')
