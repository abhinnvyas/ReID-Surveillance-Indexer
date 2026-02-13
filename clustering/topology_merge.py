import json
from collections import defaultdict
from topology import CAMERA_GRAPH
from config import METADATA_PATH, IDENTITIES_PATH


MAX_TRANSITION_TIME = 15_000_000  # microseconds


def topology_merge():

    with open(METADATA_PATH) as f:
        metadata = json.load(f)

    with open(IDENTITIES_PATH) as f:
        identities = json.load(f)

    # group by identity
    person_tracks = defaultdict(list)

    for i, meta in enumerate(metadata):
        person_tracks[identities[i]].append(
            (meta["timestamp"], meta["camera_id"], i)
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

    ids = list(person_tracks.keys())

    # compare identities
    for i in range(len(ids)):
        for j in range(i + 1, len(ids)):

            id1 = ids[i]
            id2 = ids[j]

            track1 = sorted(person_tracks[id1])
            track2 = sorted(person_tracks[id2])

            for t1, cam1, _ in track1:
                for t2, cam2, _ in track2:

                    if abs(t2 - t1) > MAX_TRANSITION_TIME:
                        continue

                    if cam2 in CAMERA_GRAPH.get(cam1, []):
                        union(id1, id2)
                        break

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

    print("Topology merge identities:", cid)


if __name__ == "__main__":
    topology_merge()
