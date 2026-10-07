"""Local checks for this repository's legacy v1.0 fixtures, not a VCP certifier."""

import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path
from uuid import UUID

ROOT = Path(__file__).resolve().parents[1]
FILES = {
    "sample_sig_ord_exe_xauusd.jsonl": ("SIG", "ORD", "ACK", "EXE"),
    "sample_rej_cxl_case.jsonl": ("ORD", "REJ", "ORD", "ACK", "CXL"),
    "sample_risk_snapshot_news_block.json": ("RSK",),
    "sample_gov_ai_decision.json": ("SIG",),
}
ZERO = "0" * 64
HEADER_FIELDS = set("event_id trace_id timestamp_int timestamp_iso event_type "
                    "event_type_code timestamp_precision clock_sync_status hash_algo "
                    "venue_id symbol account_id".split())
CODES = {"SIG": 1, "ORD": 2, "ACK": 3, "EXE": 4, "REJ": 6, "CXL": 7, "RSK": 21}
FINANCIAL = set("price quantity executed_qty remaining_qty execution_price commission "
                "slippage pnl_realized pnl_unrealized".split())


def require(condition, message):
    if not condition:
        raise ValueError(message)


def canonicalize(value):
    """HCH-003 serialization, restricted to ASCII keys and safe integer numbers.

    This is NOT a general RFC 8785 implementation. These fixtures use strings
    for decimal values; floats and non-ASCII keys are deliberately rejected.
    """
    if isinstance(value, dict):
        require(all(isinstance(k, str) and k.isascii() for k in value),
                "Unsupported canonicalization: non-ASCII key")
        for item in value.values():
            canonicalize(item)
    elif isinstance(value, list):
        for item in value:
            canonicalize(item)
    elif type(value) is int:
        require(abs(value) <= 2**53 - 1, "Unsupported canonicalization: unsafe integer")
    elif not (value is None or isinstance(value, (str, bool))):
        raise ValueError("Unsupported canonicalization: use strings for decimal values")
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False, allow_nan=False)


def event_hash(event):
    require(event["header"]["hash_algo"] == "SHA256", "Only SHA256 fixtures are supported")
    data = canonicalize(event["header"]) + canonicalize(event["payload"]) + event["security"]["prev_hash"]
    return hashlib.sha256(b"\x00" + data.encode("utf-8")).hexdigest()


def iso_ns(value):
    dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    require(dt.tzinfo is not None, "TST-001: timezone required")
    delta = dt - datetime(1970, 1, 1, tzinfo=timezone.utc)
    return (delta.days * 86400 + delta.seconds) * 1_000_000_000 + delta.microseconds * 1000


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, f"Duplicate JSON key: {key}")
        result[key] = value
    return result


def load_events(path):
    text = path.read_text(encoding="utf-8")
    if path.suffix == ".jsonl":
        require(bool(text.strip()), f"Empty fixture: {path.name}")
        return [json.loads(line, object_pairs_hook=unique_object) for line in text.splitlines()]
    return [json.loads(text, object_pairs_hook=unique_object)]


def validate_stream(events):
    require(bool(events), "Empty event stream")
    previous_hash, previous_id = ZERO, ""
    seen = set()
    for event in events:
        require(isinstance(event, dict), "SCH-001: event must be an object")
        for section in ("header", "payload", "security"):
            require(isinstance(event.get(section), dict), f"SCH-001: missing object {section}")
        h, p, s = event["header"], event["payload"], event["security"]
        require(HEADER_FIELDS <= h.keys(), "SCH-002: missing header fields")
        for field in ("event_hash", "prev_hash"):
            require(isinstance(s.get(field), str) and re.fullmatch(r"[0-9a-f]{64}", s[field]),
                    f"HCH-004: invalid {field}")
        require(s["prev_hash"] == previous_hash,
                "HCH-001/HCH-010: genesis or chain linkage mismatch")
        require(s["event_hash"] == event_hash(event), "HCH-003: event hash mismatch")
        for field in ("event_id", "trace_id"):
            uid = UUID(h[field])
            require(uid.version == 7 and str(uid) == h[field], f"UID-001/002: invalid {field}")
        require(h["event_id"] not in seen, "UID-020: duplicate event_id")
        require(h["event_id"] > previous_id, "UID-011: event IDs out of order")
        seen.add(h["event_id"])
        require(type(h["event_type_code"]) is int and
                h["event_type"] in CODES and CODES[h["event_type"]] == h["event_type_code"],
                "SCH-010/011: event type/code mismatch")
        require(isinstance(h["timestamp_int"], str) and h["timestamp_int"].isdigit(),
                "TST-002: timestamp_int must be a decimal string")
        ns = int(h["timestamp_int"])
        require(ns == iso_ns(h["timestamp_iso"]), "TST-001: timestamp mismatch")
        require(h["timestamp_precision"] == "MILLISECOND" and ns % 1_000_000 == 0,
                "TST-010: expected millisecond precision")
        uuid_ms = UUID(h["event_id"]).int >> 80
        require(1577836800000 <= uuid_ms <= 4102444800000 and uuid_ms == ns // 1_000_000,
                "UID-010: UUID timestamp mismatch")
        require(h["clock_sync_status"] == "NTP_SYNCED", "TST-020: fixture expects NTP_SYNCED")
        trade = p.get("trade_data", {})
        required = {"ORD": {"order_id", "side", "price", "quantity"},
                    "EXE": {"order_id", "execution_price", "executed_qty"}}.get(h["event_type"], set())
        require(required <= trade.keys(), "SCH-020/021: missing trade fields")
        for field in FINANCIAL & trade.keys():
            value = trade[field]
            require(isinstance(value, str), f"SCH-030/031: {field} must be a string")
            try:
                require(Decimal(value).is_finite(), f"SCH-030/031: invalid {field}")
            except InvalidOperation as exc:
                raise ValueError(f"SCH-030/031: invalid {field}") from exc
        snapshot = p.get("vcp_risk", {}).get("snapshot", {})
        require(all(isinstance(v, str) for v in snapshot.values()), "SCH-032: snapshot values must be strings")
        if h["event_type"] == "SIG":
            require(bool(p.get("vcp_gov", {}).get("algo_id")), "EVT-001: missing algo_id")
        previous_hash, previous_id = s["event_hash"], h["event_id"]


def validate_fixtures():
    directory = ROOT / "examples"
    actual = {p.name for p in directory.iterdir() if p.suffix in (".json", ".jsonl")}
    require(actual == set(FILES), "Fixture inventory differs from the four expected files")
    all_ids = set()
    for name, types in FILES.items():
        events = load_events(directory / name)
        validate_stream(events)
        require(tuple(e["header"]["event_type"] for e in events) == types,
                f"Unexpected event sequence: {name}")
        ids = {e["header"]["event_id"] for e in events}
        require(not all_ids & ids, "UID-020: event ID reused across fixtures")
        all_ids.update(ids)
        print(f"PASS {name}: {len(events)} events")


if __name__ == "__main__":
    try:
        if len(sys.argv) > 1:
            for filename in sys.argv[1:]:
                validate_stream(load_events(Path(filename)))
                print(f"PASS {filename} (legacy local checks only)")
        else:
            validate_fixtures()
    except (ValueError, KeyError, TypeError, AttributeError, OSError) as exc:
        sys.exit(f"FAIL: {exc}")
