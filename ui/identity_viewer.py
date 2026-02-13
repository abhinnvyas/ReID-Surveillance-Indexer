import streamlit as st
import json
import cv2
from collections import defaultdict

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(layout="wide")
st.title("ReID Identity Viewer")

# -----------------------------
# LOAD DATA
# -----------------------------
with open("data/metadata.json") as f:
    metadata = json.load(f)

with open("data/identities.json") as f:
    identities = json.load(f)

with open("data/identity_registry.json") as f:
    registry = json.load(f)


# -----------------------------
# GROUP DATA BY IDENTITY
# -----------------------------
groups = defaultdict(list)

for meta, pid in zip(metadata, identities):
    groups[pid].append(meta)

# sort identities by size (largest first)
identity_ids = sorted(
    groups.keys(),
    key=lambda x: len(groups[x]),
    reverse=True
)

# -----------------------------
# SIDEBAR - IDENTITY LIST
# -----------------------------
st.sidebar.title(f"Identities ({len(identity_ids)})")

# persistent selection
if "selected_id" not in st.session_state:
    st.session_state.selected_id = identity_ids[0]

# identity buttons
for pid in identity_ids:

    info = registry[str(pid)]
    label = f"{pid} | {info['confidence']} | {info['num_detections']}"

    # highlight selected identity
    if pid == st.session_state.selected_id:
        label = "➡ " + label

    if st.sidebar.button(label):
        st.session_state.selected_id = pid

selected_id = st.session_state.selected_id

# -----------------------------
# MAIN VIEW
# -----------------------------
st.subheader(f"Identity {selected_id}")

st.write(f"Total detections: {len(groups[selected_id])}")

# -----------------------------
# IMAGE GRID DISPLAY
# -----------------------------
cols_per_row = 6
cols = st.columns(cols_per_row)

for i, item in enumerate(groups[selected_id]):

    img = cv2.imread(item["path"])

    if img is None:
        continue

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    col = cols[i % cols_per_row]

    with col:
        st.image(
            img,
            caption=f"{item['camera_id']}\n{item['timestamp']}",
            use_container_width=True
        )
