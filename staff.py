from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    session,
    flash,
    url_for
)

from models import db
from models.user import User
from models.trek import Trek
from models.booking import Booking

staff_bp = Blueprint(
    "staff",
    __name__
)

@staff_bp.route("/dashboard")
def staff_dashboard():

    if "user_id" not in session:

        flash("Please login first.")

        return redirect("/login")

    if session.get("role") != "STAFF":

        flash("Access denied.")

        return redirect("/login")

    staff_id = session["user_id"]

    assigned_treks = Trek.query.filter_by(
        assigned_staff_id=staff_id
    ).all()

    trek_counts = {}

    for trek in assigned_treks:

        count = Booking.query.filter_by(
            trek_id=trek.id
        ).count()

        trek_counts[trek.id] = count

    return render_template(
        "staff_dashboard.html",
        assigned_treks=assigned_treks,
        trek_counts=trek_counts
    )

@staff_bp.route(
    "/update-trek/<int:trek_id>",
    methods=["GET", "POST"]
)
def update_trek(trek_id):

    if "user_id" not in session:
        flash("Please login first.")

        return redirect("/login")

    if session.get("role") != "STAFF":
        flash("Access denied.")

        return redirect("/login")

    trek = Trek.query.get_or_404(trek_id)

    # Ee trek ee staff ki assign ayyindha ani check chestham
    if trek.assigned_staff_id != session["user_id"]:
        flash("You can only manage your assigned treks.")

        return redirect(
            url_for("staff.staff_dashboard")
        )

    if request.method == "POST":
        trek.available_slots = request.form[
            "available_slots"
        ]
        trek.status = request.form[
            "status"
        ]
        if trek.status == "Completed":
            bookings = Booking.query.filter_by(
                trek_id=trek.id
            ).all()
            for booking in bookings:
                booking.status = "COMPLETED"

        db.session.commit()
        flash("Trek updated successfully.")

        return redirect(
            url_for("staff.staff_dashboard")
        )

    return render_template(
        "update_trek.html",
        trek=trek
    )

@staff_bp.route("/participants/<int:trek_id>")
def view_participants(trek_id):

    if "user_id" not in session:
        flash("Please login first.")

        return redirect("/login")

    if session.get("role") != "STAFF":
        flash("Access denied.")

        return redirect("/login")

    trek = Trek.query.get_or_404(trek_id)

    # Ee trek ee staff ki assign ayyindha check chestham
    if trek.assigned_staff_id != session["user_id"]:
        flash(
            "You can only view participants of your assigned treks."
        )
        return redirect(
            url_for("staff.staff_dashboard")
        )

    participants = Booking.query.filter_by(
        trek_id=trek.id
    ).all()

    return render_template(
        "assigned_trek_users.html",
        trek=trek,
        participants=participants
    )