from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    session,
    flash,
    url_for
)

from datetime import datetime

from models import db
from models.user import User
from models.trek import Trek
from models.booking import Booking

admin_bp = Blueprint(
    "admin",
    __name__
)


@admin_bp.route("/dashboard")
def admin_dashboard():

    if "user_id" not in session:
        flash("Please login first.")

        return redirect("/login")

    if session.get("role") != "ADMIN":
        flash("Access denied.")

        return redirect("/login")

    total_treks = Trek.query.count()
    total_users = User.query.filter_by(role="TREKKER").count()
    total_staff = User.query.filter_by(role="STAFF").count()
    total_bookings = Booking.query.count()

    return render_template(
        "admin_dashboard.html",
        total_treks=total_treks,
        total_users=total_users,
        total_staff=total_staff,
        total_bookings=total_bookings
    )


@admin_bp.route("/pending-staff")
def pending_staff():

    if "user_id" not in session:
        flash("Please login first.")

        return redirect("/login")

    if session.get("role") != "ADMIN":
        flash("Access denied.")

        return redirect("/login")

    pending_staff_list = User.query.filter_by(role="STAFF",status="PENDING_APPROVAL").all()

    return render_template(
        "pending_staff.html",
        pending_staff_list=pending_staff_list
    )


@admin_bp.route("/approve-staff/<int:staff_id>")
def approve_staff(staff_id):

    if "user_id" not in session:
        flash("Please login first.")

        return redirect("/login")

    if session.get("role") != "ADMIN":
        flash("Access denied.")

        return redirect("/login")

    staff = User.query.get_or_404(staff_id)
    if staff.status == "PENDING_APPROVAL":
        staff.status = "ACTIVE"
        db.session.commit()

        flash("Staff approved successfully.")
    else:
        flash("Invalid request.")

    return redirect(
        url_for("admin.pending_staff")
    )


@admin_bp.route("/create-trek", methods=["GET", "POST"])
def create_trek():

    if "user_id" not in session:
        flash("Please login first.")

        return redirect("/login")

    if session.get("role") != "ADMIN":
        flash("Access denied.")

        return redirect("/login")

    if request.method == "POST":

        trek_name = request.form["trek_name"]
        location = request.form["location"]
        difficulty = request.form["difficulty"]
        duration_days = request.form["duration_days"]
        available_slots = request.form["available_slots"]
        start_date = datetime.strptime(request.form["start_date"],"%Y-%m-%d").date()
        end_date = datetime.strptime(request.form["end_date"],"%Y-%m-%d").date()
        status = request.form["status"]

        trek = Trek(
            trek_name=trek_name,
            location=location,
            difficulty=difficulty,
            duration_days=duration_days,
            available_slots=available_slots,
            start_date=start_date,
            end_date=end_date,
            status=status
        )

        db.session.add(trek)
        db.session.commit()

        flash("Trek created successfully.")

        return redirect(
            url_for("admin.manage_treks")
        )

    return render_template(
        "create_trek.html"
    )


@admin_bp.route("/treks")
def manage_treks():

    if "user_id" not in session:
        flash("Please login first.")

        return redirect("/login")

    if session.get("role") != "ADMIN":
        flash("Access denied.")

        return redirect("/login")

    treks = Trek.query.all()

    return render_template(
        "manage_treks.html",
        treks=treks
    )


@admin_bp.route("/delete-trek/<int:trek_id>")
def delete_trek(trek_id):

    if "user_id" not in session:
        flash("Please login first.")

        return redirect("/login")

    if session.get("role") != "ADMIN":
        flash("Access denied.")

        return redirect("/login")

    trek = Trek.query.get_or_404(trek_id)

    db.session.delete(trek)
    db.session.commit()

    flash("Trek deleted successfully.")

    return redirect(
        url_for("admin.manage_treks")
    )


@admin_bp.route(
    "/edit-trek/<int:trek_id>",
    methods=["GET", "POST"]
)
def edit_trek(trek_id):

    if "user_id" not in session:
        flash("Please login first.")

        return redirect("/login")

    if session.get("role") != "ADMIN":
        flash("Access denied.")

        return redirect("/login")

    trek = Trek.query.get_or_404(trek_id)

    if request.method == "POST":

        trek.trek_name = request.form["trek_name"]
        trek.location = request.form["location"]
        trek.difficulty = request.form["difficulty"]
        trek.duration_days = request.form["duration_days"]
        trek.available_slots = request.form["available_slots"]
        trek.start_date = datetime.strptime(request.form["start_date"],"%Y-%m-%d").date()
        trek.end_date = datetime.strptime(request.form["end_date"],"%Y-%m-%d").date()
        trek.status = request.form["status"]

        db.session.commit()

        flash("Trek updated successfully.")

        return redirect(
            url_for("admin.manage_treks")
        )

    return render_template(
        "edit_trek.html",
        trek=trek
    )

@admin_bp.route(
    "/assign-staff/<int:trek_id>",
    methods=["GET", "POST"]
)
def assign_staff(trek_id):

    if "user_id" not in session:
        flash("Please login first.")

        return redirect("/login")

    if session.get("role") != "ADMIN":
        flash("Access denied.")

        return redirect("/login")

    trek = Trek.query.get_or_404(trek_id)

    active_staff = User.query.filter_by(
        role="STAFF",
        status="ACTIVE"
    ).all()

    if request.method == "POST":

        staff_id = request.form["staff_id"]
        trek.assigned_staff_id = staff_id
        db.session.commit()

        flash("Staff assigned successfully.")

        return redirect(
            url_for("admin.manage_treks")
        )

    return render_template(
        "assign_staff.html",
        trek=trek,
        active_staff=active_staff
    )

@admin_bp.route("/users")
def view_users():

    if "user_id" not in session:
        flash("Please login first.")
        return redirect("/login")

    if session.get("role") != "ADMIN":
        flash("Access denied.")
        return redirect("/login")

    users = User.query.filter_by(
        role="TREKKER"
    ).all()

    return render_template(
        "view_users.html",
        users=users
    )

@admin_bp.route("/staff")
def view_staff():

    if "user_id" not in session:
        flash("Please login first.")
        return redirect("/login")

    if session.get("role") != "ADMIN":
        flash("Access denied.")
        return redirect("/login")

    staff_members = User.query.filter_by(
        role="STAFF"
    ).all()

    return render_template(
        "view_staff.html",
        staff_members=staff_members
    )

@admin_bp.route("/bookings")
def view_bookings():

    if "user_id" not in session:
        flash("Please login first.")
        return redirect("/login")

    if session.get("role") != "ADMIN":
        flash("Access denied.")
        return redirect("/login")

    bookings = Booking.query.all()

    return render_template(
        "view_bookings.html",
        bookings=bookings
    )

@admin_bp.route("/search")
def search():

    if "user_id" not in session:
        flash("Please login first.")
        return redirect("/login")

    if session.get("role") != "ADMIN":
        flash("Access denied.")
        return redirect("/login")

    keyword = request.args.get("keyword", "")

    users = User.query.filter(
        User.name.contains(keyword)
    ).all()

    treks = Trek.query.filter(
        Trek.trek_name.contains(keyword)
    ).all()

    return render_template(
        "search_results.html",
        users=users,
        treks=treks,
        keyword=keyword
    )

@admin_bp.route("/toggle-user-status/<int:user_id>")
def toggle_user_status(user_id):

    if "user_id" not in session:
        flash("Please login first.")
        return redirect("/login")

    if session.get("role") != "ADMIN":
        flash("Access denied.")
        return redirect("/login")

    user = User.query.get_or_404(user_id)

    if user.status == "BLACKLISTED":
        user.status = "ACTIVE"
        flash("User activated successfully.")
    else:
        user.status = "BLACKLISTED"
        flash("User blacklisted successfully.")

    db.session.commit()

    return redirect(request.referrer)