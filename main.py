from scanner.scan import scan_detections
from embeddings.extractor import extract_embeddings
from indexing.faiss_manager import build_faiss
from clustering.identity_cluster import cluster_identities
from clustering.temporal_merge import temporal_merge
from timeline.builder import build_timeline
from timeline.identity_registry import build_identity_registry

if __name__ == "__main__":

    scan_detections()
    extract_embeddings()
    build_faiss()
    cluster_identities()
    temporal_merge()
    build_timeline()
    build_identity_registry()

    print("Pipeline complete.")
