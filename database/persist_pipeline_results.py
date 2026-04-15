import json

from torch import amp
from database.mongo_client import (
    observations_col,
    identities_col
)
from datetime import datetime

now = datetime.utcnow()





def persist_observations():

    with open("data/metadata.json") as f:
        metadata = json.load(f)

    with open("data/identities.json") as f:
        identities = json.load(f)

    docs = []

    for meta, pid in zip(metadata, identities):

        timestamp = datetime.fromtimestamp(meta["timestamp"] / 1_000_000)

        docs.append({
        "identityId": str(pid),
        "cameraId": meta["camera_id"],
        "timestamp": timestamp,
        "imagePath": meta["path"],
        "createdAt": now,
        "updatedAt": now
    })

    observations_col.delete_many({})
    observations_col.insert_many(docs)

    print("Observations inserted:", len(docs))


def persist_identities():

    with open("data/identity_registry.json") as f:
        registry = json.load(f)

    docs = []

    for pid, data in registry.items():
        

        docs.append({
        "identityId": pid,
        "confidence": data["confidence"],
        "consistency": data["consistency"],
        "detectionCount": data["num_detections"],
        "firstSeen": datetime.fromtimestamp(data["first_seen"] / 1_000_000),
        "lastSeen": datetime.fromtimestamp(data["last_seen"] / 1_000_000),
        "createdAt": now,
        "updatedAt": now
    })

    identities_col.delete_many({})
    identities_col.insert_many(docs)

    print("Identities inserted:", len(docs))