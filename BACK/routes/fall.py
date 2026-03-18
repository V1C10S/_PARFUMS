from flask import Blueprint, jsonify
import json
from pathlib import Path

# ===== BLUEPRINTS ===== 

fall_bp = Blueprint("fall", __name__)

# ===== ROUTES ===== 

BASE_DIR = Path(__file__).resolve().parent.parent
FALL_FILE = BASE_DIR / "source" / "fall.json"

def load_fall_data():
    with open(FALL_FILE, "r", encoding="utf-8") as file:
        return json.load(file)

# ===== GET & POST ===== 

@fall_bp.route("/parfurm/seasons/fall", methods=["GET"])
def get_fall_perfumes():
    data = load_fall_data()
    return jsonify(data)

# ===== FUNCTIONS ===== 

def get_fall_perfume_by_id(perfume_id):
    data = load_fall_data()

    for perfume in data:
        if perfume.get("id") == perfume_id:
            return perfume

    return None