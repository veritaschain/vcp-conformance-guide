"""Smoke checks plus negative controls for the checked-in legacy fixtures."""

import ast
import copy
import hashlib
import json
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from generate_fixtures import generated_files
from legacy_fixtures import canonicalize, event_hash, load_events, validate_fixtures, validate_stream


class FixtureSmokeTests(unittest.TestCase):
    def setUp(self):
        self.events = load_events(ROOT / "examples/sample_sig_ord_exe_xauusd.jsonl")

    def test_all_fixtures(self):
        validate_fixtures()

    def test_reproducible_from_document(self):
        for name, content in generated_files().items():
            self.assertEqual((ROOT / "examples" / name).read_text(encoding="utf-8"), content, name)

    def test_document_links_and_pinned_vector(self):
        for document in list(ROOT.glob("*.md")) + [ROOT / "examples/README.md"]:
            text = document.read_text(encoding="utf-8")
            links = re.findall(r'\]\(([^)]+)\)|href="([^"]+)"', text)
            for markdown, html in links:
                target = markdown or html
                if not target.startswith(("#", "http:", "https:", "mailto:")):
                    self.assertTrue((document.parent / target.split("#")[0]).exists(), target)
        guide = (ROOT / "VCP_CONFORMANCE_TEST_GUIDE_v1_0_EN.md").read_text(encoding="utf-8")
        section = guide.split("#### A.3 Hash Calculation Test Vectors", 1)[1]
        pinned = re.search(r"```text\n([0-9a-f]{64})\n```", section)[1]
        self.assertEqual(self.events[0]["security"]["event_hash"], pinned)

    def test_actual_guide_hch_003(self):
        # Execute the guide's own hash functions, independently of our helper.
        guide = (ROOT / "VCP_CONFORMANCE_TEST_GUIDE_v1_0_EN.md").read_text(encoding="utf-8")
        section = guide.split("#### Test HCH-003: Hash Calculation (CRITICAL)", 1)[1]
        code = re.search(r"```python\n(.*?)\n```", section, re.S)[1]
        tree = ast.parse(code)
        tree.body = [node for node in tree.body if isinstance(node, ast.FunctionDef)
                     and node.name in {"canonicalize_json", "calculate_expected_hash"}]
        self.assertEqual(len(tree.body), 2)
        namespace = {"json": json, "hashlib": hashlib}
        exec(compile(tree, "guide:HCH-003", "exec"), namespace)
        for path in sorted((ROOT / "examples").glob("*.json*")):
            for event in load_events(path):
                expected = namespace["calculate_expected_hash"](
                    event["header"], event["payload"], event["security"]["prev_hash"], "SHA256")
                self.assertEqual(event["security"]["event_hash"], expected, path.name)

    def test_hash_tampering_rejected(self):
        for section, key, value in [
            ("header", "symbol", "TAMPERED"),
            ("payload", "injected", "tampered"),
            ("security", "event_hash", hashlib.sha256(b"").hexdigest()),
        ]:
            with self.subTest(section=section):
                events = copy.deepcopy(self.events)
                events[0][section][key] = value
                with self.assertRaisesRegex(ValueError, "HCH-003"):
                    validate_stream(events)

    def test_broken_genesis_link_removal_and_order_rejected(self):
        variants = []
        for index in (0, 1):
            events = copy.deepcopy(self.events)
            events[index]["security"]["prev_hash"] = "1" * 64
            events[index]["security"]["event_hash"] = event_hash(events[index])
            variants.append(events)
        variants += [self.events[:1] + self.events[2:], list(reversed(self.events)), []]
        for events in variants:
            with self.subTest(events=len(events)), self.assertRaises(ValueError):
                validate_stream(events)

    def test_rehashed_invalid_timestamp_and_numeric_type_rejected(self):
        for kind in ("timestamp", "price"):
            events = copy.deepcopy(self.events)
            if kind == "timestamp":
                events[0]["header"]["timestamp_int"] = "1732536000000000000"
            else:
                events[1]["payload"]["trade_data"]["price"] = 2650
            previous = "0" * 64
            for event in events:
                event["security"]["prev_hash"] = previous
                previous = event_hash(event)
                event["security"]["event_hash"] = previous
            with self.subTest(kind=kind), self.assertRaisesRegex(ValueError, "TST-001|SCH-030/031"):
                validate_stream(events)

    def test_unsupported_canonicalization_rejected(self):
        for value in ({"value": 0.1}, {"value": 2**53}, {"\U0001f600": "value"}):
            with self.subTest(value=value), self.assertRaisesRegex(ValueError, "canonicalization"):
                canonicalize(value)


if __name__ == "__main__":
    unittest.main()
