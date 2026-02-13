import json

with open("data/metadata.json") as f:
    data = json.load(f)

cams = set(d["camera_id"] for d in data)
print(cams)
