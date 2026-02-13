import json
import numpy as np
from collections import defaultdict

from config import IDENTITIES_PATH


CLUSTER_SIM_THRESHOLD = 0.78  # safe starting value


def cluster_merge():

    with open("data/metadata.json") as f:
        metadata = json.load(f)

    with open(IDENTITIES_PATH) as f:
        identities = json.load(f)

    embeddings = np.load("data/embeddings.npy")

    # normalize
    embeddings = embeddings / np.linalg.norm(
        embeddings, axis=1, keepdims=True
    )

    # group embeddings by identity
    groups = defaultdict(list)

    for emb, pid in zip(embeddings, identities):
        groups[pid].append(emb)

    # compute identity centers
    centers = {}

    for pid, embs in groups.items():
        center = np.mean(embs, axis=0)
        center = center / np.linalg.norm(center)
        centers[pid] = center

    ids = list(centers.keys())

    parent = {i: i for i in ids}

    def find(x):
        while parent[x] != x:
            x = parent[x]
        return x

    def union(a, b):
        pa, pb = find(a), find(b)
        if pa != pb:
            parent[pb] = pa

    # compare identity centers
    for i in range(len(ids)):
        for j in range(i + 1, len(ids)):

            id1 = ids[i]
            id2 = ids[j]

            sim = np.dot(centers[id1], centers[id2])

            if sim > CLUSTER_SIM_THRESHOLD:
                union(id1, id2)

    # remap IDs
    new_map = {}
    new_ids = []
    cid = 0

    for old in identities:
        root = find(old)

        if root not in new_map:
            new_map[root] = cid
            cid += 1

        new_ids.append(new_map[root])

    with open(IDENTITIES_PATH, "w") as f:
        json.dump(new_ids, f)

    print("Cluster merge identities:", cid)


if __name__ == "__main__":
    cluster_merge()
