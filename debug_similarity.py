import numpy as np
import faiss

from config import EMBEDDINGS_PATH

embeddings = np.load(EMBEDDINGS_PATH).astype("float32")

faiss.normalize_L2(embeddings)

index = faiss.IndexFlatIP(embeddings.shape[1])
index.add(embeddings)

D, I = index.search(embeddings, 5)

print("Top similarities:")

for i in range(10):
    print(D[i])
