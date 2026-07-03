import json
from pathlib import Path

# Go to project root then API-KEYS folder
API_FILE = Path(__file__).resolve().parents[2] / "API-KEYS" / "api_key.json"


def get_api(key_name):
    try:
        with open(API_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        if key_name not in data:
            raise KeyError(f"'{key_name}' not found in api_key.json")

        return data[key_name]

    except FileNotFoundError:
        raise FileNotFoundError("api_key.json was not found.")

    except json.JSONDecodeError:
        raise ValueError("api_key.json is not a valid JSON file.")