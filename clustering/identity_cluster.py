import json
import faiss
import numpy as np

from config import (
    EMBEDDINGS_PATH,
    FAISS_INDEX_PATH,
    IDENTITIES_PATH,
    TOP_K,
    SIMILARITY_THRESHOLD
)


def cluster_identities():

    embeddings = np.load(EMBEDDINGS_PATH)
    faiss.normalize_L2(embeddings)

    index = faiss.read_index(FAISS_INDEX_PATH)

    D, I = index.search(embeddings, TOP_K)

    parent = list(range(len(embeddings)))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        pa, pb = find(a), find(b)
        if pa != pb:
            parent[pb] = pa

    # SIMPLE GRAPH MERGE
    for i in range(len(embeddings)):
        for j, score in zip(I[i], D[i]):

            if i == j:
                continue

            if score >= SIMILARITY_THRESHOLD:
                union(i, j)

    # assign IDs
    root_map = {}
    identities = []
    cid = 0

    for i in range(len(embeddings)):
        r = find(i)

        if r not in root_map:
            root_map[r] = cid
            cid += 1

        identities.append(root_map[r])

    with open(IDENTITIES_PATH, "w") as f:
        json.dump(identities, f)

    print("Total identities:", cid)


if __name__ == "__main__":
    cluster_identities()
