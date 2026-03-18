import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FILE = os.path.join(BASE_DIR, "featured.json")

SEASON_FILES = [
    "winter.json",
    "spring.json",
    "summer.json",
    "fall.json",
]


def get_featured_perfumes():
    featured_perfumes = []

    for filename in SEASON_FILES:
        file_path = os.path.join(BASE_DIR, filename)

        if not os.path.exists(file_path):
            print(f"Arquivo não encontrado: {filename}")
            continue

        with open(file_path, "r", encoding="utf-8") as file:
            try:
                perfumes = json.load(file)
            except json.JSONDecodeError:
                print(f"Erro ao ler {filename}")
                continue

            if not isinstance(perfumes, list):
                print(f"{filename} não contém uma lista.")
                continue

            for perfume in perfumes:
                if isinstance(perfume, dict) and perfume.get("featured") is True:
                    featured_perfumes.append(perfume)

    return featured_perfumes


def save_featured_perfumes(featured_perfumes):
    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(featured_perfumes, file, indent=2, ensure_ascii=False)


def main():
    featured_perfumes = get_featured_perfumes()
    save_featured_perfumes(featured_perfumes)
    print(f"featured.json criado com {len(featured_perfumes)} perfume(s).")


if __name__ == "__main__":
    main()