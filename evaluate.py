#!/usr/bin/env python3
"""Evaluate classification against labeled safe laboratory data."""

import json
from collections import defaultdict
from pathlib import Path

from decoyai.classifier import classify


def evaluate(dataset: Path) -> dict:
    rows = [json.loads(line) for line in dataset.read_text(encoding="utf-8").splitlines() if line.strip()]
    correct, by_class = 0, defaultdict(lambda: {"correct": 0, "total": 0})
    results = []
    for row in rows:
        predicted = classify(row["payload"]).category
        expected = row["expected_category"]
        is_correct = predicted == expected
        correct += int(is_correct)
        by_class[expected]["total"] += 1
        by_class[expected]["correct"] += int(is_correct)
        results.append({**row, "predicted_category": predicted, "correct": is_correct})
    return {"samples": len(rows), "correct": correct,
            "accuracy": correct / len(rows) if rows else 0,
            "per_class": dict(by_class), "results": results}


def main() -> int:
    result = evaluate(Path("evaluation/lab_dataset.jsonl"))
    output = Path("evaluation/results.json")
    output.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(f"Samples: {result['samples']}")
    print(f"Correct: {result['correct']}")
    print(f"Accuracy: {result['accuracy']:.1%}")
    print(f"Report: {output}")
    return 0 if result["accuracy"] >= 0.80 else 1


if __name__ == "__main__":
    raise SystemExit(main())
