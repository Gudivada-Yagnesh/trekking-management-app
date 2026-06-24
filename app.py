from flask import (
    Flask,              # Flask application create cheyyadaniki
    render_template,    # HTML templates render cheyyadaniki
    request,            # Form data access cheyyadaniki
    redirect,           # Vere route ki pampadaniki
    session,            # User login state maintain cheyyadaniki
    flash               # Temporary messages display cheyyadaniki
)
from config import Config
from models import db
from models.user import User
from models.staff_profile import StaffProfile
from models.trek import Trek
from models.booking import Booking
from werkzeug.security import generate_password_hash
from datetime import datetime
from admin import admin_bp
from staff import staff_bp
from trekker import trekker_bp

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app) #sqlalchemy

app.register_blueprint(
    admin_bp,
    url_prefix="/admin"
)

app.register_blueprint(
    staff_bp,
    url_prefix="/staff"
)

app.register_blueprint(
    trekker_bp,
    url_prefix="/trekker"
)

# Application context create chesthunam
with app.app_context():

    # Models prakaram SQLite tables create chesthundhi
    db.create_all()

    # Admin user already undho ledho check chesthunam
    admin = User.query.filter_by(
        email="admin@gmail.com"
    ).first()

    # Admin lekapothe create chestham
    if admin is None:

        # Admin object create chesthunam
        admin = User(
            name="Admin",
            email="admin@gmail.com",
            password=generate_password_hash("admin123"),
            role="ADMIN",
            status="ACTIVE"
        )

        db.session.add(admin)
        db.session.commit()

        print("Admin user created successfully.")

    else:

        print("Admin user already exists.")


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        role = request.form["role"]

        existing_user = User.query.filter_by(
            email=email
        ).first()

        if existing_user:

            flash("Email already registered.")
            return redirect("/register")

        if role == "STAFF":
            status = "PENDING_APPROVAL"
        else:
            status = "ACTIVE"

        user = User(
            name=name,
            email=email,
            role=role,
            status=status
        )

        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        flash("Registration successful. Please login.")
        return redirect("/login")

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]
        user = User.query.filter_by(
            email=email
        ).first()

        if user is None:

            flash("No account found with this email.")
            return redirect("/login")

        if not user.check_password(password):

            flash("Invalid email or password.")
            return redirect("/login")

        if user.role == "STAFF" and user.status == "PENDING_APPROVAL":
            flash("Your account is waiting for admin approval.")
            return redirect("/login")
        
        if user.status == "BLACKLISTED":
            flash("Your account has been blacklisted.")
            return redirect("/login")

        session["user_id"] = user.id
        session["name"] = user.name
        session["role"] = user.role

        if user.role == "ADMIN":
            return redirect("/admin/dashboard")
        
        if user.role == "STAFF":       
            return redirect("/staff/dashboard")

        if user.role == "TREKKER":
            return redirect("/trekker/dashboard")

    return render_template("login.html")

@app.route("/logout")
def logout():

    session.clear()
    flash("You have been logged out successfully.")
    return redirect("/login")

@app.route("/staff/dashboard")
def staff_dashboard():

    if "user_id" not in session:
        flash("Please login first.")

        return redirect("/login")

    if session.get("role") != "STAFF":
        flash("Access denied.")

        return redirect("/login")

    return render_template("staff_dashboard.html")

@app.route("/trekker/dashboard")
def trekker_dashboard():

    if "user_id" not in session:
        flash("Please login first.")

        return redirect("/login")

    if session.get("role") != "TREKKER":
        flash("Access denied.")

        return redirect("/login")

    return render_template("trekker_dashboard.html")


if __name__ == "__main__":
    app.run(debug=True)
