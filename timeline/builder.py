import json
from collections import defaultdict
from config import METADATA_PATH, IDENTITIES_PATH


def build_timeline():

    with open(METADATA_PATH) as f:
        metadata = json.load(f)

    with open(IDENTITIES_PATH) as f:
        identities = json.load(f)

    timeline = defaultdict(list)

    for meta, pid in zip(metadata, identities):
        timeline[str(pid)].append({
            "camera": meta["camera_id"],
            "timestamp": meta["timestamp"]
        })

    for k in timeline:
        timeline[k].sort(key=lambda x: x["timestamp"])

    with open("data/timeline.json", "w") as f:
        json.dump(timeline, f)

    print("Timeline built")


if __name__ == "__main__":
    build_timeline()
