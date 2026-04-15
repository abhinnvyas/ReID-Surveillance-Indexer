from scanner.scan import scan_detections
from embeddings.extractor import extract_embeddings
from clustering.identity_cluster import cluster_identities
from clustering.temporal_merge import temporal_merge
from timeline.builder import build_timeline
from timeline.identity_registry import build_identity_registry
from patterns.daily_pattern_detector import detect_patterns

from pipelinem.pipeline_status import update_pipeline

from convertdetections.convert_detections import convert_detections
from database.persist_pipeline_results import (
    persist_observations,
    persist_identities
)

TOTAL_STEPS = 8


def run_pipeline():

    step = 1

    update_pipeline(status="RUNNING", progress=0)

    update_pipeline(stage="Converting Detection Images",progress=(step / TOTAL_STEPS) * 100, eta=23)
    convert_detections()
    step += 1

    update_pipeline(stage="Scanning Detections", progress=(step / TOTAL_STEPS) * 100, eta=25)
    scan_detections()
    step += 1

    update_pipeline(stage="Extracting Embeddings", progress=(step / TOTAL_STEPS) * 100, eta=22)
    extract_embeddings()
    step += 1

    update_pipeline(stage="Clustering Identities", progress=(step / TOTAL_STEPS) * 100, eta=18)
    cluster_identities()
    step += 1

    update_pipeline(stage="Temporal Merge", progress=(step / TOTAL_STEPS) * 100, eta=15)
    temporal_merge()
    step += 1

    update_pipeline(stage="Building Timeline", progress=(step / TOTAL_STEPS) * 100, eta=10)
    build_timeline()

    update_pipeline(stage="Persisting Observations", progress=75, eta=5)
    persist_observations()

    step += 1

    update_pipeline(stage="Building Identity Registry", progress=(step / TOTAL_STEPS) * 100, eta=6)
    build_identity_registry()

    update_pipeline(stage="Persisting Identities", progress=90, eta=2)
    persist_identities()

    step += 1

    update_pipeline(stage="Detecting Patterns", progress=(step / TOTAL_STEPS) * 100, eta=2)
    detect_patterns()

    update_pipeline(
        status="COMPLETED",
        progress=100,
        stage="Completed",
        eta=0,
    )

    print("Pipeline complete.")