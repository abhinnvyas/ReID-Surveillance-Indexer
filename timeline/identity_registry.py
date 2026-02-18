import json
import numpy as np
from collections import defaultdict


def build_identity_registry():

    # -----------------------------
    # LOAD DATA
    # -----------------------------
    with open("data/metadata.json") as f:
        metadata = json.load(f)

    with open("data/identities.json") as f:
        identities = json.load(f)

    embeddings = np.load("data/embeddings.npy")

    # normalize embeddings
    embeddings = embeddings / np.linalg.norm(
        embeddings, axis=1, keepdims=True
    )

    # -----------------------------
    # GROUP BY IDENTITY
    # -----------------------------
    groups = defaultdict(list)

    for idx, pid in enumerate(identities):
        groups[pid].append(idx)

    registry = {}

    # -----------------------------
    # BUILD REGISTRY
    # -----------------------------
    for pid, indices in groups.items():

        times = [metadata[i]["timestamp"] for i in indices]
        cams = [metadata[i]["camera_id"] for i in indices]

        # embeddings for this identity
        embs = embeddings[indices]

        # center embedding
        center = np.mean(embs, axis=0)
        center = center / np.linalg.norm(center)

        # consistency score (cluster tightness)
        sims = embs @ center
        consistency = float(np.mean(sims))

        count = len(indices)

        # confidence rule
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
            "consistency": consistency,
            "first_seen": min(times),
            "last_seen": max(times),
            "center_embedding": center.tolist()
        }

    # -----------------------------
    # SAVE OUTPUT
    # -----------------------------
    with open("data/identity_registry.json", "w") as f:
        json.dump(registry, f, indent=2)

    print("Identity registry built:", len(registry))


if __name__ == "__main__":
    build_identity_registry()
