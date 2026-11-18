"""Paired cluster bootstrap conditional on a fixed held-out set."""
import numpy as np
from sklearn.metrics import average_precision_score, roc_auc_score


def intervals(labels, scores, groups, repetitions=1000, seed=17):
    labels = np.asarray(labels)
    groups = np.asarray(groups)
    units = np.unique(groups)
    if len(units) < 10:
        return {"status": "insufficient independent groups", "groups": len(units)}
    rng = np.random.default_rng(seed)
    draws = {name: {"roc_auc": [], "average_precision": []} for name in scores}
    deltas = []
    for _ in range(repetitions):
        sampled = rng.choice(units, len(units), replace=True)
        indices = np.concatenate([np.flatnonzero(groups == unit) for unit in sampled])
        if len(np.unique(labels[indices])) < 2:
            continue
        for name, score in scores.items():
            draws[name]["roc_auc"].append(roc_auc_score(labels[indices], np.asarray(score)[indices]))
            draws[name]["average_precision"].append(average_precision_score(labels[indices], np.asarray(score)[indices]))
        deltas.append(draws["combined"]["average_precision"][-1] - draws["static"]["average_precision"][-1])
    if len(deltas) < repetitions * 0.9:
        return {"status": "too many single-class resamples"}
    return {"status": "conditional cluster bootstrap", "seed": seed,
            "valid_resamples": len(deltas), "confidence": 0.95,
            "intervals": {name: {metric: np.quantile(values, [0.025,0.975]).tolist()
                                for metric, values in metrics.items()} for name, metrics in draws.items()},
            "combined_minus_static_average_precision": np.quantile(deltas,[0.025,0.975]).tolist()}
