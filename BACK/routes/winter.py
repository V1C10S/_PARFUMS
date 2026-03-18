from flask import Blueprint, jsonify
import json
from pathlib import Path

# ===== BLUEPRINTS =====

winter_bp = Blueprint("winter", __name__)

# ===== ROUTES =====

BASE_DIR = Path(__file__).resolve().parent.parent
WINTER_FILE = BASE_DIR / "source" / "winter.json"

def load_winter_data():
    with open(WINTER_FILE, "r", encoding="utf-8") as file:
        return json.load(file)

# ===== GET & POST WINTER =====

@winter_bp.route("/parfurm/seasons/winter", methods=["GET"])
def get_winter_perfumes():
    data = load_winter_data()
    return jsonify(data)

# ===== GET & POST ID =====

@winter_bp.route("/parfurm/seasons/winter/<perfume_id>", methods=["GET"])
def get_winter_perfume(perfume_id):
    perfume = get_winter_perfume_by_id(perfume_id)

    if perfume:
        return jsonify(perfume)
    else:
        return jsonify({"error": "Perfume não encontrado"}), 404

# ===== FUNCTIONS =====

def get_winter_perfume_by_id(perfume_id):
    data = load_winter_data()

    for perfume in data:
        if perfume.get("id") == perfume_id:
            return perfume

    return None