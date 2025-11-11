import re
import numpy as np
from typing import List, Dict, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import MiniBatchKMeans

def _norm(s: str) -> str:
    s = re.sub(r"\s+", " ", str(s)).strip().lower()
    s = s.replace("×","x").replace("*","x")
    return s

def cluster_item_names(names: List[str], max_clusters: int = 50) -> Tuple[Dict[int, List[str]], Dict[str, int], Dict[int, str]]:
    uniq = list({_norm(x) for x in names if str(x).strip()})
    if len(uniq) <= 50:
        rep_map = {i:[n] for i,n in enumerate(uniq)}
        lab_map = {n:i for i,n in enumerate(uniq)}
        reps = {i:n for i,n in enumerate(uniq)}
        return rep_map, lab_map, reps
    vec = TfidfVectorizer(analyzer="char", ngram_range=(3,5), min_df=1)
    X = vec.fit_transform(uniq)
    k = min(max_clusters, max(2, int(np.sqrt(len(uniq)))))
    km = MiniBatchKMeans(n_clusters=k, random_state=42, n_init=5, batch_size=256, max_iter=100)
    labels = km.fit_predict(X)
    rep_map = {}
    lab_map = {}
    reps = {}
    for idx, lab in enumerate(labels):
        rep_map.setdefault(lab, []).append(uniq[idx])
        lab_map[uniq[idx]] = lab
    for lab, members in rep_map.items():
        reps[lab] = min(members, key=len)
    return rep_map, lab_map, reps
