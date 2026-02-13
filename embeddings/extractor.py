import json
import cv2
import numpy as np
from tqdm import tqdm

import torch
import torchvision.models as models
import torchvision.transforms as T

from config import METADATA_PATH, EMBEDDINGS_PATH


device = "cpu"

model = models.efficientnet_b0(weights="DEFAULT")
model.classifier = torch.nn.Identity()

model.eval()
model.to(device)

transform = T.Compose([
    T.ToPILImage(),
    T.Resize((256, 128)),
    T.ToTensor()
])


def extract_feature(img):

    tensor = transform(img).unsqueeze(0).to(device)

    with torch.no_grad():
        feat = model(tensor)

    return feat.squeeze().cpu().numpy()


def extract_embeddings():

    with open(METADATA_PATH, "r") as f:
        metadata = json.load(f)

    embeddings = []

    for item in tqdm(metadata):

        img = cv2.imread(item["path"])

        if img is None:
            continue

        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        emb = extract_feature(img)
        embeddings.append(emb)

    embeddings = np.array(embeddings).astype("float32")

    np.save(EMBEDDINGS_PATH, embeddings)

    print("Embeddings saved:", embeddings.shape)


if __name__ == "__main__":
    extract_embeddings()
