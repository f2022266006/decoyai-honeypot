import tempfile
import unittest
from pathlib import Path

from decoyai.classifier import classify, risk_level
from decoyai.dashboard import create_dashboard
from decoyai.service import ThreadedDecoyServer
from decoyai.storage import EventStore
from evaluate import evaluate


class DecoyAITests(unittest.TestCase):
    def test_classifier_categories(self):
        cases = {"hello": "unknown_probe", "root login": "credential_probe",
                 "nmap scan": "scanner_probe", "curl example.invalid": "command_probe",
                 "' OR 1=1": "injection_probe", "": "empty_probe"}
        for payload, expected in cases.items():
            with self.subTest(payload=payload):
                self.assertEqual(classify(payload).category, expected)

    def test_risk_levels(self):
        self.assertEqual(risk_level(10), "low")
        self.assertEqual(risk_level(45), "medium")
        self.assertEqual(risk_level(80), "high")

    def test_storage_statistics(self):
        with tempfile.TemporaryDirectory() as directory:
            store = EventStore(Path(directory) / "test.db")
            store.record("127.0.0.1", 50000, "fake-ssh", "curl example.invalid", classify("curl example.invalid"))
            stats = store.statistics()
            self.assertEqual(stats["total_interactions"], 1)
            self.assertEqual(stats["high_risk_interactions"], 1)

    def test_non_loopback_decoy_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            store = EventStore(Path(directory) / "test.db")
            with self.assertRaises(ValueError):
                ThreadedDecoyServer(("0.0.0.0", 0), store)

    def test_non_loopback_dashboard_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            store = EventStore(Path(directory) / "test.db")
            with self.assertRaises(ValueError):
                create_dashboard(("0.0.0.0", 0), store)

    def test_evaluation_dataset(self):
        result = evaluate(Path("evaluation/lab_dataset.jsonl"))
        self.assertGreaterEqual(result["accuracy"], 0.80)


if __name__ == "__main__":
    unittest.main()
