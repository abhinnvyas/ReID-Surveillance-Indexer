import os
import cv2
from tqdm import tqdm
from config import DETECTIONS_PATH


def convert_detections():

    converted = 0

    for root, _, files in os.walk(DETECTIONS_PATH):

        for file in files:

            if not file.endswith(".ppm"):
                continue

            ppm_path = os.path.join(root, file)

            jpg_file = file.replace(".ppm", ".jpg")
            jpg_path = os.path.join(root, jpg_file)

            # skip if already converted
            if os.path.exists(jpg_path):
                continue

            img = cv2.imread(ppm_path)

            if img is None:
                continue

            cv2.imwrite(
                jpg_path,
                img,
                [cv2.IMWRITE_JPEG_QUALITY, 85],
            )

            converted += 1

    print(f"Converted {converted} detection images to JPG")