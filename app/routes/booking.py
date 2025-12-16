from flask import Blueprint, jsonify

bp = Blueprint('booking', __name__)

@bp.route("/", methods=["GET"])
def get_bookings():
    return jsonify({"bookings": ["booking1", "booking2"]})
