import json
from datetime import datetime
import os

def save_response(result: str, folder="data"):
    if not os.path.exists(folder):
        os.makedirs(folder)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{folder}/suggestion_{timestamp}.json"
    with open(filename, "w") as f:
        json.dump({"timestamp": timestamp, "result": result}, f, indent=2)

    return filename

# this would return a list of all saved responses history

def list_saved_suggestions(folder="data"):
    if not os.path.exists(folder):
        return []

    files = sorted(os.listdir(folder))
    results = []

    for f in files:
        if f.endswith(".json"):
            path = os.path.join(folder, f)
            with open(path, "r") as file:
                try:
                    data = json.load(file)
                    results.append(data)
                except Exception as e:
                    results.append({"error": str(e), "file": f})

    return results

