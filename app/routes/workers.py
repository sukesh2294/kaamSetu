from flask import Blueprint, jsonify

bp = Blueprint('workers', __name__)

@bp.route("/", methods=["GET"])
def get_workers():
    return jsonify({"workers": ["worker1", "worker2"]})
