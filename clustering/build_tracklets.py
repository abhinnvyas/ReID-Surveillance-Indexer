import json
import numpy as np
from collections import defaultdict

TRACKLET_WINDOW = 5_000_000  # microseconds


def build_tracklets():

    with open("data/metadata.json") as f:
        metadata = json.load(f)

    embeddings = np.load("data/embeddings.npy")

    # normalize
    embeddings = embeddings / np.linalg.norm(
        embeddings, axis=1, keepdims=True
    )

    cam_groups = defaultdict(list)

    for idx, meta in enumerate(metadata):
        cam_groups[meta["camera_id"]].append(
            (meta["timestamp"], idx)
        )

    tracklets = []

    for cam, entries in cam_groups.items():

        entries.sort()

        current = [entries[0][1]]

        for i in range(1, len(entries)):

            t_prev, idx_prev = entries[i-1]
            t_cur, idx_cur = entries[i]

            if t_cur - t_prev < TRACKLET_WINDOW:
                current.append(idx_cur)
            else:
                tracklets.append(current)
                current = [idx_cur]

        tracklets.append(current)

    # average embedding per tracklet
    tracklet_embeddings = []

    for tr in tracklets:
        emb = np.mean(embeddings[tr], axis=0)
        emb = emb / np.linalg.norm(emb)
        tracklet_embeddings.append(emb)

    tracklet_embeddings = np.array(tracklet_embeddings)

    np.save("data/tracklet_embeddings.npy", tracklet_embeddings)

    with open("data/tracklets.json", "w") as f:
        json.dump(tracklets, f)

    print("Total tracklets:", len(tracklets))
