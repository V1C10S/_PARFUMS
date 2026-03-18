import json
import os


# ===== BASE PATH =====

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# ===== FILES =====

SEASON_FILES = {
    "spring": "spring.json",
    "summer": "summer.json",
    "fall": "fall.json",
    "winter": "winter.json",
}


# ===== DEFAULT DATA =====

def default_perfume(card_id: str, season: str) -> dict:
    return {

  "id": "",
  "slug": "",
  "name": "",
  "brand": "",
  "season": "",

  "price": 0,
  "currency": "BRL",

  "main_image": "",
  "images": [],

  "volume": "",
  "family": "",

  "rating": 0,

  "performance": {
    "projection": 0,
    "longevity": 0,
    "day_use": 0,
    "night_use": 0
  },

  "description": "",

    "accords": [],

  "notes": {
    "top": [],
    "middle": [],
    "base": []
  },

  "in_stock": False,
  "featured": False
}


def default_season_data(season: str) -> list:
    return [default_perfume(f"card{i}", season) for i in range(1, 13)]


# ===== CREATE FILES =====

def ensure_json_files():
    for season, filename in SEASON_FILES.items():
        file_path = os.path.join(BASE_DIR, filename)

        if not os.path.exists(file_path):
            with open(file_path, "w", encoding="utf-8") as file:
                json.dump(default_season_data(season), file, indent=2, ensure_ascii=False)

            print(f"[CREATED] {filename}")
        else:
            print(f"[OK] {filename} already exists")


# ===== LOAD FILE =====

def load_season_perfumes(season: str):
    filename = SEASON_FILES.get(season.lower())

    if not filename:
        return None

    file_path = os.path.join(BASE_DIR, filename)

    if not os.path.exists(file_path):
        return None

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


# ===== GET PERFUME BY ID =====

def get_perfume_by_id(season: str, perfume_id: str):
    perfumes = load_season_perfumes(season)

    if not perfumes:
        return None

    for perfume in perfumes:
        if perfume.get("id") == perfume_id:
            return perfume

    return None


# ===== START =====

if __name__ == "__main__":
    ensure_json_files()