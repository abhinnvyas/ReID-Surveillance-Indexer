import os
import json
from tqdm import tqdm
from config import DETECTIONS_PATH, METADATA_PATH


def scan_detections():

    results = []

    for cam_folder in tqdm(os.listdir(DETECTIONS_PATH)):
        cam_path = os.path.join(DETECTIONS_PATH, cam_folder)

        if not os.path.isdir(cam_path):
            continue

        camera_id = cam_folder.replace("camera_", "").replace("{", "").replace("}", "")

        for file in os.listdir(cam_path):

            parts = file.split("_")

            if len(parts) < 5:
                continue

            class_name = parts[2]

            if class_name != "person":
                continue

            try:
                timestamp = int(parts[3])
            except:
                continue

            jpg_file = file.replace(".ppm", ".jpg")

            results.append({
                "camera_id": camera_id,
                "timestamp": timestamp,
                "path": os.path.join(cam_path, jpg_file)
            })

    results.sort(key=lambda x: x["timestamp"])

    os.makedirs("data", exist_ok=True)

    with open(METADATA_PATH, "w") as f:
        json.dump(results, f)

    print(f"Total person detections: {len(results)}")


if __name__ == "__main__":
    scan_detections()
