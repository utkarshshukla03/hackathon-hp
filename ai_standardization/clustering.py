import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.metrics.pairwise import cosine_similarity

def cluster_items_with_diagnostics(embeddings):
    clustering = DBSCAN(eps=0.15, min_samples=1, metric="cosine")
    labels = clustering.fit_predict(embeddings)

    diagnostics = {}

    for label in set(labels):
        idxs = [i for i, l in enumerate(labels) if l == label]
        cluster_vectors = embeddings[idxs]
        centroid = cluster_vectors.mean(axis=0)

        sims = cosine_similarity(cluster_vectors, centroid.reshape(1, -1))
        avg_similarity = float(sims.mean())

        diagnostics[label] = {
            "cluster_size": len(idxs),
            "avg_similarity": round(avg_similarity, 3)
        }

    return labels, diagnostics
