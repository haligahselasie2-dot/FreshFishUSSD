from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db
from models.customer import Customer
from models.order import Order
from models.driver import Driver   # ✅ IMPORTANT: Import Driver model
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash


admin_bp = Blueprint('admin_bp', __name__, template_folder='templates')

# ==================================================
#   /admin (root) → ALWAYS require login
# ==================================================
@admin_bp.route("/")
def admin_home():
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_bp.login"))

    return redirect(url_for("admin_bp.dashboard"))

# ============================================
#   ADMIN DASHBOARD (Customers + Orders)
# ============================================
@admin_bp.route("/")
def dasboard():
    if not session.get("admin_logged_in"):
     return redirect(url_for("admin_bp.login"))

    customers = Customer.query.order_by(Customer.id.desc()).all()
    orders = Order.query.order_by(Order.created_at.desc()).all()
    drivers = Driver.query.order_by(Driver.id.desc()).all()  # ✅ pass drivers list
    return render_template("admin.html", customers=customers, orders=orders, drivers=drivers)
# ============================================
#    ADMIN CREDENTIALS
# ============================================
ADMIN_USER = {
    "username": "DICKSON",
    "password": generate_password_hash("26012011")  # hashed password
}

#  ============================================
#   ADMIN LOGIN ROUTE
# ============================================
@admin_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
#===========================
# check credentials
#===========================
        if username == ADMIN_USER["username"] and check_password_hash(ADMIN_USER["password"], password):
            session["admin_logged_in"] = True
            return redirect(url_for("admin_bp.index"))
        else:
            flash("Invalid credentials", "danger")
    
    return render_template("login.html")

# ============================================
# admin logout route
# ============================================
@admin_bp.route("/logout")
def logout():
    session.pop("admin_logged_in", None)
    return redirect(url_for("admin_bp.login"))




# ============================================
#   DRIVER LIST PAGE
# ============================================
@admin_bp.route("/drivers")
def drivers():
    if not session.get("admin_logged_in"):
     return redirect(url_for("admin_bp.login"))

    all_drivers = Driver.query.order_by(Driver.id.desc()).all()
    return render_template("drivers.html", drivers=all_drivers)



# ============================================
#   ADD DRIVER
# ============================================
@admin_bp.route("/drivers/add", methods=["POST"])
def add_driver():
    if not session.get("admin_logged_in"):
     return redirect(url_for("admin_bp.login"))

    name = request.form.get("name")
    phone = request.form.get("phone")

    new_driver = Driver(name=name, phone=phone)
    db.session.add(new_driver)
    db.session.commit()

    flash("Driver added successfully!")
    return redirect(url_for("admin_bp.drivers"))   # ✅ FIXED



# ============================================
#   ASSIGN DRIVER TO ORDER
# ============================================
@admin_bp.route("/assign_driver/<int:order_id>", methods=["POST"])
def assign_driver(order_id):
    driver_id = request.form.get("driver_id")

    order = Order.query.get_or_404(order_id)
    driver = Driver.query.get_or_404(driver_id)

    # update order fields
    order.driver = driver.name
    order.status = "Assigned"

    # update driver status
    driver.status = "Busy"

    db.session.commit()

    flash("Driver assigned successfully!")
    return redirect(url_for("admin_bp.index"))   # ✅ FIXED REDIRECT



# ❌ REMOVE THIS OLD ROUTE (NOT NEEDED ANYMORE)
# @admin_bp.route("/assign/<int:order_id>", methods=["POST"])
# def assign(order_id):
#     ...
