from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    session,
    flash,
    url_for
)

from datetime import date

from models import db
from models.user import User
from models.trek import Trek
from models.booking import Booking

trekker_bp = Blueprint(
    "trekker",
    __name__
)
@trekker_bp.route("/dashboard")
def trekker_dashboard():

    if "user_id" not in session:
        flash("Please login first.")

        return redirect("/login")

    if session.get("role") != "TREKKER":
        flash("Access denied.")

        return redirect("/login")

    available_treks = Trek.query.filter_by(
        status="Open"
    ).all()

    my_bookings = Booking.query.filter_by(
        user_id=session["user_id"]
    ).all()

    booked_trek_ids = []
    for booking in my_bookings:
        booked_trek_ids.append(
            booking.trek_id
        )

    return render_template(
        "trekker_dashboard.html",
        available_treks=available_treks,
        my_bookings=my_bookings,
        booked_trek_ids=booked_trek_ids
    )

@trekker_bp.route("/search")
def search_treks():

    if "user_id" not in session:
        flash("Please login first.")
        return redirect("/login")

    difficulty = request.args.get("difficulty")
    location = request.args.get("location")

    query = Trek.query.filter_by(
        status="Open"
    )

    if difficulty:
        query = query.filter_by(
            difficulty=difficulty
        )

    if location:
        query = query.filter(
            Trek.location.contains(location)
        )

    treks = query.all()

    return render_template(
        "search_treks.html",
        treks=treks
    )

@trekker_bp.route("/book-trek/<int:trek_id>")
def book_trek(trek_id):

    if "user_id" not in session:
        flash("Please login first.")

        return redirect("/login")

    if session.get("role") != "TREKKER":
        flash("Access denied.")

        return redirect("/login")

    trek = Trek.query.get_or_404(trek_id)

    existing_booking = Booking.query.filter_by(
        user_id=session["user_id"],
        trek_id=trek.id
    ).first()

    if existing_booking:
        flash("You have already booked this trek.")

        return redirect(
            url_for("trekker.trekker_dashboard")
        )

    if trek.status != "Open":
        flash("Bookings are closed for this trek.")

        return redirect(
            url_for("trekker.trekker_dashboard")
        )

    if trek.available_slots <= 0:
        flash("No slots available.")

        return redirect(
            url_for("trekker.trekker_dashboard")
        )

    booking = Booking(
        user_id=session["user_id"],
        trek_id=trek.id,
        booking_date=date.today(),
        status="BOOKED",
        payment_status="PENDING"
    )

    trek.available_slots -= 1
    db.session.add(booking)
    db.session.commit()

    flash("Trek booked successfully.")

    return redirect(
        url_for("trekker.trekker_dashboard")
    )

@trekker_bp.route("/history")
def trekking_history():

    if "user_id" not in session:
        flash("Please login first.")

        return redirect("/login")

    if session.get("role") != "TREKKER":
        flash("Access denied.")

        return redirect("/login")

    bookings = Booking.query.filter_by(
        user_id=session["user_id"]
    ).all()
    return render_template(
        "trek_history.html",
        bookings=bookings
    )

@trekker_bp.route(
    "/profile",
    methods=["GET", "POST"]
)
def profile():

    if "user_id" not in session:
        flash("Please login first.")

        return redirect("/login")

    user = User.query.get_or_404(
        session["user_id"]
    )

    if request.method == "POST":

        user.name = request.form["name"]
        user.email = request.form["email"]
        db.session.commit()

        flash("Profile updated successfully.")

        return redirect(
            url_for("trekker.profile")
        )

    return render_template(
        "profile.html",
        user=user
    )

@trekker_bp.route("/cancel-booking/<int:booking_id>")
def cancel_booking(booking_id):

    if "user_id" not in session:
        flash("Please login first.")

        return redirect("/login")

    booking = Booking.query.get_or_404(
        booking_id
    )

    if booking.user_id != session["user_id"]:
        flash("Access denied.")

        return redirect(
            url_for("trekker.trekker_dashboard")
        )

    if booking.status == "BOOKED":
        booking.status = "CANCELLED"
        booking.trek.available_slots += 1
        db.session.commit()

        flash("Booking cancelled.")

    return redirect(
        url_for("trekker.trekker_dashboard")
    )