import json
from collections import defaultdict
import numpy as np


TIMELINE_PATH = "data/timeline.json"
PATTERN_PATH = "data/patterns.json"


def detect_patterns():

    with open(TIMELINE_PATH) as f:
        timeline = json.load(f)

    patterns = []

    for identity, observations in timeline.items():

        camera_groups = defaultdict(list)

        for obs in observations:
            camera_groups[obs["camera"]].append(obs["timestamp"])

        for camera, timestamps in camera_groups.items():

            if len(timestamps) < 5:
                continue

            # convert to hours of day
            hours = [
                (ts / 1e6) % 86400 / 3600
                for ts in timestamps
            ]

            mean_hour = np.mean(hours)
            std_hour = np.std(hours)

            if std_hour < 0.5:   # appears around same time

                patterns.append({
                    "identity": identity,
                    "camera": camera,
                    "pattern_type": "DAILY_VISIT",
                    "time_mean_hour": float(mean_hour),
                    "time_std_hour": float(std_hour),
                    "occurrences": len(timestamps)
                })

    with open(PATTERN_PATH, "w") as f:
        json.dump(patterns, f, indent=2)

    print("Patterns detected:", len(patterns))