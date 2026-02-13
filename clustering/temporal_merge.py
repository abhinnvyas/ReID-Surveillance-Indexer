import json
import numpy as np
from collections import defaultdict

from config import METADATA_PATH, IDENTITIES_PATH


TEMPORAL_WINDOW = 5_000_000
TEMPORAL_SIM_THRESHOLD = 0.70


def temporal_merge():

    with open(METADATA_PATH) as f:
        metadata = json.load(f)

    with open(IDENTITIES_PATH) as f:
        identities = json.load(f)

    embeddings = np.load("data/embeddings.npy")

    # normalize embeddings
    embeddings = embeddings / np.linalg.norm(
        embeddings, axis=1, keepdims=True
    )

    cam_groups = defaultdict(list)

    for idx, meta in enumerate(metadata):
        cam_groups[meta["camera_id"]].append(
            (meta["timestamp"], idx)
        )

    parent = list(range(len(set(identities))))

    def find(x):
        while parent[x] != x:
            x = parent[x]
        return x

    def union(a, b):
        pa, pb = find(a), find(b)
        if pa != pb:
            parent[pb] = pa

    # SAFE TEMPORAL MERGE
    for cam, entries in cam_groups.items():

        entries.sort()

        for i in range(len(entries) - 1):

            t1, idx1 = entries[i]
            t2, idx2 = entries[i + 1]

            if (t2 - t1) > TEMPORAL_WINDOW:
                continue

            id1 = identities[idx1]
            id2 = identities[idx2]

            if id1 == id2:
                continue

            # appearance check
            sim = np.dot(
                embeddings[idx1],
                embeddings[idx2]
            )

            if sim > TEMPORAL_SIM_THRESHOLD:
                union(id1, id2)

    # remap IDs
    new_map = {}
    new_ids = []
    cid = 0

    for id_ in identities:
        root = find(id_)

        if root not in new_map:
            new_map[root] = cid
            cid += 1

        new_ids.append(new_map[root])

    with open(IDENTITIES_PATH, "w") as f:
        json.dump(new_ids, f)

    print("Temporal merge identities:", cid)


if __name__ == "__main__":
    temporal_merge()
