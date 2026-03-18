from flask import Blueprint, jsonify
import json
from pathlib import Path

# ===== BLUEPRINTS =====

home_bp = Blueprint("home", __name__)

# ===== ROUTES =====

BASE_DIR = Path(__file__).resolve().parent.parent
FEATURED_FILE = BASE_DIR / "source" / "featured.json"

def load_featured_data():
    with open(FEATURED_FILE, "r", encoding="utf-8") as file:
        return json.load(file)

# ===== GET & POST FEATURED =====

@home_bp.route("/parfurm/featured", methods=["GET"])
def get_featured_perfumes():
    data = load_featured_data()
    return jsonify(data)

# ===== GET FEATURED ID =====

@home_bp.route("/parfurm/featured/<perfume_id>", methods=["GET"])
def get_featured_perfume(perfume_id):
    perfume = get_featured_perfume_by_id(perfume_id)

    if perfume:
        return jsonify(perfume)
    else:
        return jsonify({"error": "Perfume não encontrado"}), 404
    
# ===== FUNCTIONS =====

def get_featured_perfume_by_id(perfume_id):
    data = load_featured_data()

    for perfume in data:
        if perfume.get("id") == perfume_id:
            return perfume

    return None