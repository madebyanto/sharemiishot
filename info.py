import json
import os

# percorso relativo al file JSON
json_path = os.path.join(os.path.dirname(__file__), "docs", ".info.json")

try:
    with open(json_path, "r", encoding="utf-8") as f:
        info = json.load(f)

    print(f"{info['name']} v{info['version']}")
    print(f"Developer: {info['developer']}")
    print(f"Release date: {info['release_date']}")
    print(f"Description: {info['description']}")
    print(f"Support: {info['support']}")
except Exception as e:
    print("Error! ;-(", e)
