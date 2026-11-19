"""Assign complete connected lineage/family groups to fixed partitions."""
import argparse
import csv
from datetime import date
import random


def lineage_components(rows):
    """Return connected components across shared lineage and malware family keys."""
    parent = list(range(len(rows)))
    rank = [0] * len(rows)
    owner = {}

    def find(index):
        while parent[index] != index:
            parent[index] = parent[parent[index]]
            index = parent[index]
        return index

    def union(left, right):
        left, right = find(left), find(right)
        if left == right:
            return
        if rank[left] < rank[right]:
            left, right = right, left
        parent[right] = left
        if rank[left] == rank[right]:
            rank[left] += 1

    for index, row in enumerate(rows):
        keys = [("lineage", row["lineage_id"])]
        if row.get("malware_family"):
            keys.append(("family", row["malware_family"]))
        for key in keys:
            if key in owner:
                union(index, owner[key])
            else:
                owner[key] = index

    components = {}
    for index in range(len(rows)):
        components.setdefault(find(index), []).append(index)
    return sorted(components.values(), key=lambda component: min(
        rows[index].get("sample_id", str(index)) for index in component
    ))


def lineage_component_ids(rows):
    """Return one stable group ID per row for leakage checks and cluster resampling."""
    result = [None] * len(rows)
    for component in lineage_components(rows):
        group_id = min(rows[index].get("sample_id", str(index)) for index in component)
        for index in component:
            result[index] = group_id
    return result


def assign(rows, strategy="group", seed=17, test_source=None, validation_source=None,
           validation_date=None, test_date=None):
    rows = [dict(row) for row in rows]
    hashes = [r["sha256"].lower() for r in rows]
    if len(set(hashes)) != len(hashes):
        raise ValueError("Deduplicate hashes and resolve conflicting labels first")
    groups = [[rows[index] for index in component] for component in lineage_components(rows)]
    random.Random(seed).shuffle(groups)
    for i, members in enumerate(groups):
        if strategy == "group":
            partition = "test" if i < len(groups)*0.2 else "validation" if i < len(groups)*0.4 else "train"
        else:
            choices = set()
            for row in members:
                if strategy == "source":
                    if not test_source or not validation_source or test_source == validation_source:
                        raise ValueError("Provide distinct validation and test sources")
                    choices.add("test" if row["source"] == test_source else "validation" if row["source"] == validation_source else "train")
                else:
                    if not validation_date or not test_date or date.fromisoformat(validation_date) >= date.fromisoformat(test_date):
                        raise ValueError("Provide ordered ISO date boundaries")
                    collected = date.fromisoformat(row["collection_date"])
                    choices.add("test" if collected >= date.fromisoformat(test_date) else "validation" if collected >= date.fromisoformat(validation_date) else "train")
            if len(choices) != 1:
                raise ValueError("Related group spans holdout boundaries; curate or exclude the entire group")
            partition = choices.pop()
        for row in members:
            row["split"] = partition
    for split in ("train", "validation", "test"):
        if {r["ground_truth_label"] for r in rows if r["split"] == split} != {"benign","malicious"}:
            raise ValueError(f"{split} lacks both classes; supply more independent groups")
    return rows


def main():
    p = argparse.ArgumentParser()
    p.add_argument("input")
    p.add_argument("output")
    p.add_argument("--strategy", choices=["group","source","temporal"], default="group")
    p.add_argument("--test-source")
    p.add_argument("--validation-source")
    p.add_argument("--validation-date")
    p.add_argument("--test-date")
    args = p.parse_args()
    with open(args.input, newline="") as f:
        rows = list(csv.DictReader(f))
    result = assign(rows, args.strategy, test_source=args.test_source,
                    validation_source=args.validation_source,
                    validation_date=args.validation_date, test_date=args.test_date)
    with open(args.output, "x", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=result[0])
        writer.writeheader()
        writer.writerows(result)

if __name__ == "__main__":
    main()
