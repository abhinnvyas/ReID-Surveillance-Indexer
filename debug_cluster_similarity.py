import json
import numpy as np
from collections import defaultdict

embeddings = np.load("data/embeddings.npy")

with open("data/identities.json") as f:
    identities = json.load(f)

# normalize
embeddings = embeddings / np.linalg.norm(
    embeddings, axis=1, keepdims=True
)

groups = defaultdict(list)

for emb, pid in zip(embeddings, identities):
    groups[pid].append(emb)

centers = {}

for pid, embs in groups.items():
    center = np.mean(embs, axis=0)
    center = center / np.linalg.norm(center)
    centers[pid] = center

ids = list(centers.keys())

print("\nTop identity similarities:\n")

for i in range(len(ids)):
    for j in range(i + 1, len(ids)):

        sim = np.dot(centers[ids[i]], centers[ids[j]])

        if sim > 0.60:
            print(f"{ids[i]} <-> {ids[j]} : {sim:.3f}")
