import json


def merge_identities(source_id, target_id):

    with open("data/identities.json") as f:
        ids = json.load(f)

    # replace source with target
    ids = [
        target_id if i == source_id else i
        for i in ids
    ]

    with open("data/identities.json", "w") as f:
        json.dump(ids, f)

    print(f"Merged {source_id} → {target_id}")
