import json
import numpy as np
from collections import defaultdict


def build_identity_registry():

    with open("data/metadata.json") as f:
        metadata = json.load(f)

    with open("data/identities.json") as f:
        identities = json.load(f)

    embeddings = np.load("data/embeddings.npy")

    # normalize embeddings
    embeddings = embeddings / np.linalg.norm(
        embeddings, axis=1, keepdims=True
    )

    groups = defaultdict(list)

    for idx, pid in enumerate(identities):
        groups[pid].append(idx)

    registry = {}

    for pid, indices in groups.items():

        times = [metadata[i]["timestamp"] for i in indices]
        cams = [metadata[i]["camera_id"] for i in indices]

        center = np.mean(embeddings[indices], axis=0)
        center = center / np.linalg.norm(center)

        count = len(indices)

        # confidence rule (simple but powerful)
        if count >= 5:
            confidence = "high"
        elif count >= 3:
            confidence = "medium"
        else:
            confidence = "low"

        registry[str(pid)] = {
            "camera_id": cams[0],
            "num_detections": count,
            "confidence": confidence,
            "first_seen": min(times),
            "last_seen": max(times),
            "center_embedding": center.tolist()
        }

    with open("data/identity_registry.json", "w") as f:
        json.dump(registry, f)

    print("Identity registry built:", len(registry))
