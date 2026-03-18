from flask import Blueprint, request, jsonify
from source.perfumes import get_perfume_by_id

# ===== BLUEPRINTS ===== 

id_bp = Blueprint("id", __name__)

# ===== ROUTES ID ===== 

@id_bp.route("/api/parfurm/<season>/<id>", methods=["GET"])
def get_parfurm(season, id):

    perfume = get_perfume_by_id(season, id)

    if not perfume:
        return jsonify({
            "error": "Perfume not found",
            "season": season,
            "id": id
        }), 404

    return jsonify(perfume), 200

