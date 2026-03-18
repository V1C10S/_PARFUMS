from flask import Blueprint, jsonify
import json
from pathlib import Path

# ===== BLUEPRINTS ===== 

summer_bp = Blueprint("summer", __name__)

# ===== ROUTES ===== 

BASE_DIR = Path(__file__).resolve().parent.parent
SUMMER_FILE = BASE_DIR / "source" / "summer.json"

def load_summer_data():
    with open(SUMMER_FILE, "r", encoding="utf-8") as file:
        return json.load(file)

# ===== GET & POST SUMMER =====

@summer_bp.route("/parfurm/seasons/summer", methods=["GET"])
def get_summer_perfumes():
    data = load_summer_data()
    return jsonify(data)

# ===== GET & POST ID =====

@summer_bp.route("/parfurm/seasons/summer/<perfume_id>", methods=["GET"])
def get_summer_perfume(perfume_id):
    perfume = get_summer_perfume_by_id(perfume_id)

    if perfume:
        return jsonify(perfume)
    else:
        return jsonify({"error": "Perfume não encontrado"}), 404
    
# ===== FUNCTIONS ===== 

def get_summer_perfume_by_id(perfume_id):
    data = load_summer_data()

    for perfume in data:
        if perfume.get("id") == perfume_id:
            return perfume

    return None