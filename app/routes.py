from flask import Blueprint, render_template
from .service import get_port_mappings

bp = Blueprint("main", __name__)

@bp.route("/")
def home():
    rows = get_port_mappings()
    return render_template("index.html", rows=rows)
