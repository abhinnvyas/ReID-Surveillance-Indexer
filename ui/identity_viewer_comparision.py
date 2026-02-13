import streamlit as st
import json
import cv2
import numpy as np
from collections import defaultdict

# ==============================
# PAGE CONFIG
# ==============================
st.set_page_config(layout="wide")
st.title("⭐ ReID Pro Debug Mode")

# ==============================
# LOAD DATA
# ==============================
with open("data/metadata.json") as f:
    metadata = json.load(f)

with open("data/identities.json") as f:
    identities = json.load(f)

embeddings = np.load("data/embeddings.npy")

# normalize embeddings
embeddings = embeddings / np.linalg.norm(
    embeddings, axis=1, keepdims=True
)

# ==============================
# GROUP BY IDENTITY
# ==============================
groups = defaultdict(list)

for idx, (meta, pid) in enumerate(zip(metadata, identities)):
    groups[pid].append((idx, meta))

identity_ids = sorted(
    groups.keys(),
    key=lambda x: len(groups[x]),
    reverse=True
)

# ==============================
# SIDEBAR LIST
# ==============================
st.sidebar.title("Identities")

if "left_id" not in st.session_state:
    st.session_state.left_id = identity_ids[0]

if "right_id" not in st.session_state:
    st.session_state.right_id = identity_ids[1]

st.sidebar.subheader("LEFT Identity")

for pid in identity_ids:

    label = f"{pid} ({len(groups[pid])})"

    if pid == st.session_state.left_id:
        label = "➡ " + label

    if st.sidebar.button(label, key=f"L{pid}"):
        st.session_state.left_id = pid

st.sidebar.markdown("---")

st.sidebar.subheader("RIGHT Identity")

for pid in identity_ids:

    label = f"{pid} ({len(groups[pid])})"

    if pid == st.session_state.right_id:
        label = "➡ " + label

    if st.sidebar.button(label, key=f"R{pid}"):
        st.session_state.right_id = pid

left_id = st.session_state.left_id
right_id = st.session_state.right_id

# ==============================
# SIMILARITY CALCULATION
# ==============================
def identity_similarity(id1, id2):

    emb1 = np.array([embeddings[i] for i, _ in groups[id1]])
    emb2 = np.array([embeddings[i] for i, _ in groups[id2]])

    sim = emb1 @ emb2.T
    return np.mean(sim)

sim_score = identity_similarity(left_id, right_id)

# ==============================
# MAIN HEADER
# ==============================
st.subheader(
    f"Identity {left_id}  ↔  Identity {right_id}"
)

st.write(f"Average similarity: **{sim_score:.3f}**")

# ==============================
# DISPLAY SIDE BY SIDE
# ==============================
left_col, right_col = st.columns(2)

# -------- LEFT --------
with left_col:

    st.markdown(f"### LEFT ({len(groups[left_id])})")

    cols = st.columns(4)

    for i, (_, item) in enumerate(groups[left_id]):

        img = cv2.imread(item["path"])

        if img is None:
            continue

        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        with cols[i % 4]:
            st.image(
                img,
                caption=f"{item['camera_id']}\n{item['timestamp']}",
                use_container_width=True
            )

# -------- RIGHT --------
with right_col:

    st.markdown(f"### RIGHT ({len(groups[right_id])})")

    cols = st.columns(4)

    for i, (_, item) in enumerate(groups[right_id]):

        img = cv2.imread(item["path"])

        if img is None:
            continue

        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        with cols[i % 4]:
            st.image(
                img,
                caption=f"{item['camera_id']}\n{item['timestamp']}",
                use_container_width=True
            )
