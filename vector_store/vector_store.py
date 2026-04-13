from pymongo import MongoClient
import numpy as np
from datetime import datetime

MONGO_URL = "mongodb://localhost:27017"

client = MongoClient(MONGO_URL)

db = client["reid_engine_db"]

vectors_col = db["identity_vectors"]


def get_all_vectors():

    docs = list(vectors_col.find({}))

    if len(docs) == 0:
        return None, None

    ids = []
    vectors = []

    for d in docs:
        ids.append(d["identityId"])
        vectors.append(d["vector"])

    return ids, np.array(vectors).astype("float32")


def insert_new_identity(identity_id, vector):

    vectors_col.insert_one({
        "identityId": identity_id,
        "vector": vector.tolist(),
        "createdAt": datetime.utcnow(),
        "updatedAt": datetime.utcnow()
    })


def update_identity_vector(identity_id, new_vector):

    doc = vectors_col.find_one({"identityId": identity_id})

    if doc is None:
        insert_new_identity(identity_id, new_vector)
        return

    old_vector = np.array(doc["vector"])

    updated = (old_vector + new_vector) / 2
    updated = updated / np.linalg.norm(updated)

    vectors_col.update_one(
        {"identityId": identity_id},
        {
            "$set": {
                "vector": updated.tolist(),
                "updatedAt": datetime.utcnow()
            }
        }
    )