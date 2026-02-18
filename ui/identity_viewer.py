import streamlit as st
import json
import cv2
from collections import defaultdict
from merge_identity import merge_identities

# ==============================
# PAGE CONFIG
# ==============================
st.set_page_config(layout="wide")
st.title("⭐ ReID Identity Viewer")

# ==============================
# LOAD DATA
# ==============================
with open("data/metadata.json") as f:
    metadata = json.load(f)

with open("data/identities.json") as f:
    identities = json.load(f)

with open("data/identity_registry.json") as f:
    registry = json.load(f)

# ==============================
# GROUP BY IDENTITY
# ==============================
groups = defaultdict(list)

for meta, pid in zip(metadata, identities):
    groups[pid].append(meta)

# sort by number of detections (largest first)
identity_ids = sorted(
    groups.keys(),
    key=lambda x: len(groups[x]),
    reverse=True
)

# ==============================
# SIDEBAR LIST
# ==============================
st.sidebar.title("Identities")

if "selected_id" not in st.session_state:
    st.session_state.selected_id = identity_ids[0]

for pid in identity_ids:

    info = registry[str(pid)]

    label = (
        f"{pid} | "
        f"{info['confidence'].upper()} | "
        f"{info['num_detections']} | "
        f"{info['consistency']:.2f}"
    )

    # highlight active identity
    if pid == st.session_state.selected_id:
        label = "➡ " + label

    if st.sidebar.button(label):
        st.session_state.selected_id = pid

selected_id = st.session_state.selected_id
info = registry[str(selected_id)]

# ==============================
# HEADER INFO
# ==============================
st.subheader(f"Identity {selected_id}")

st.write(
    f"""
**Confidence:** {info['confidence'].upper()}  
**Detections:** {info['num_detections']}  
**Consistency:** {info['consistency']:.3f}  
**First Seen:** {info['first_seen']}  
**Last Seen:** {info['last_seen']}
"""
)

st.markdown("---")
st.markdown("### 🔧 Merge Identities")

merge_target = st.number_input(
    "Merge current identity INTO:",
    min_value=0,
    step=1
)

if st.button("Merge"):
    merge_identities(selected_id, merge_target)
    st.success(f"Merged {selected_id} → {merge_target}")
    st.experimental_rerun()


# ==============================
# IMAGE GRID
# ==============================
cols_per_row = 6
cols = st.columns(cols_per_row)

for i, item in enumerate(groups[selected_id]):

    img = cv2.imread(item["path"])

    if img is None:
        continue

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    with cols[i % cols_per_row]:
        st.image(
            img,
            caption=f"{item['camera_id']}\n{item['timestamp']}",
            use_container_width=True
        )
