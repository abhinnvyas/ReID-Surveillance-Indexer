import faiss
import numpy as np
from config import EMBEDDINGS_PATH, FAISS_INDEX_PATH


def build_faiss():

    embeddings = np.load(EMBEDDINGS_PATH)

    faiss.normalize_L2(embeddings)

    dim = embeddings.shape[1]

    # EXACT SEARCH (NOT HNSW)
    index = faiss.IndexFlatIP(dim)

    index.add(embeddings)

    faiss.write_index(index, FAISS_INDEX_PATH)

    print("FAISS index created (Exact Search)")


if __name__ == "__main__":
    build_faiss()
