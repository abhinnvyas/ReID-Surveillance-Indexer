import json
import numpy as np
import faiss


THRESHOLD = 0.90


def cluster_tracklets():

    emb = np.load("data/tracklet_embeddings.npy").astype("float32")

    faiss.normalize_L2(emb)

    index = faiss.IndexFlatIP(emb.shape[1])
    index.add(emb)

    D, I = index.search(emb, 5)

    parent = list(range(len(emb)))

    def find(x):
        while parent[x] != x:
            x = parent[x]
        return x

    def union(a,b):
        pa,pb = find(a),find(b)
        if pa!=pb:
            parent[pb]=pa

    for i in range(len(emb)):
        for j, s in zip(I[i], D[i]):
            if i == j:
                continue
            if s > THRESHOLD:
                union(i,j)

    # map back to image identities
    with open("data/tracklets.json") as f:
        tracklets = json.load(f)

    root_map = {}
    identities = []
    cid = 0

    img_ids = [None]*sum(len(t) for t in tracklets)

    for t_idx, tr in enumerate(tracklets):

        r = find(t_idx)

        if r not in root_map:
            root_map[r] = cid
            cid += 1

        for img_idx in tr:
            img_ids[img_idx] = root_map[r]

    with open("data/identities.json","w") as f:
        json.dump(img_ids,f)

    print("Final identities:", cid)
