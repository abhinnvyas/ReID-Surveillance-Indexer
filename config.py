import os

# ROOT DETECTIONS FOLDER
DETECTIONS_PATH = "detections"

# OUTPUT FILES
METADATA_PATH = "data/metadata.json"
EMBEDDINGS_PATH = "data/embeddings.npy"
FAISS_INDEX_PATH = "data/faiss.index"
IDENTITIES_PATH = "data/identities.json"

# REID SETTINGS
EMBEDDING_DIM = 1280
SIMILARITY_THRESHOLD = 0.65
TOP_K = 10