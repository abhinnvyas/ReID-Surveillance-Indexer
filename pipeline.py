from scanner.scan import scan_detections
from embeddings.extractor import extract_embeddings
from clustering.identity_cluster import cluster_identities
from clustering.temporal_merge import temporal_merge
from timeline.builder import build_timeline
from timeline.identity_registry import build_identity_registry
from patterns.daily_pattern_detector import detect_patterns

from pipelinem.pipeline_status import stop_requested


def check_stop(stage):

    if stop_requested():
        print(f"Pipeline stopped before stage: {stage}")
        return True

    return False


def run_pipeline():

    print("Pipeline started")

    if check_stop("scan_detections"):
        return
    scan_detections()

    if check_stop("extract_embeddings"):
        return
    extract_embeddings()

    if check_stop("cluster_identities"):
        return
    cluster_identities()

    if check_stop("temporal_merge"):
        return
    temporal_merge()

    if check_stop("build_timeline"):
        return
    build_timeline()

    if check_stop("build_identity_registry"):
        return
    build_identity_registry()

    if check_stop("detect_patterns"):
        return
    detect_patterns()

    print("Pipeline complete.")