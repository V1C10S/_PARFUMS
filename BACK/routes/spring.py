from flask import Blueprint, jsonify
import json
from pathlib import Path

# ===== BLUEPRINTS ===== 

spring_bp = Blueprint("spring", __name__)

# ===== ROUTES ===== 

BASE_DIR = Path(__file__).resolve().parent.parent
SPRING_FILE = BASE_DIR / "source" / "spring.json"

def load_spring_data():
    with open(SPRING_FILE, "r", encoding="utf-8") as file:
        return json.load(file)

# ===== GET & POST SPRING =====

@spring_bp.route("/parfurm/seasons/spring", methods=["GET"])
def get_spring_perfumes():
    data = load_spring_data()
    return jsonify(data)

# ===== GET & POST ID =====

@spring_bp.route("/parfurm/seasons/spring/<perfume_id>", methods=["GET"])
def get_spring_perfume(perfume_id):
    perfume = get_spring_perfume_by_id(perfume_id)

    if perfume:
        return jsonify(perfume)
    else:
        return jsonify({"error": "Perfume não encontrado"}), 404

# ===== FUNCTIONS ===== 

def get_spring_perfume_by_id(perfume_id):
    data = load_spring_data()

    for perfume in data:
        if perfume.get("id") == perfume_id:
            return perfume

    return None