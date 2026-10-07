"""Deterministically derive legacy v1.0 fixtures from the embedded illustrations."""

import argparse
import json
import re
from uuid import UUID

from legacy_fixtures import FILES, ROOT, ZERO, event_hash, iso_ns, require, validate_stream


def section_events(text, section):
    match = re.search(r"^### " + re.escape(section) + r" .*?(?=^### |^## |\Z)", text, re.M | re.S)
    require(match is not None, f"Missing source section {section}")
    return [json.loads(block) for block in re.findall(r"```json\n(.*?)\n```", match[0], re.S)]


def move_payload_times(value, delta):
    # Preserve the illustrated offsets of approvals, controls and embargo end.
    if isinstance(value, dict):
        for key, item in value.items():
            if key.endswith("timestamp_int") or key == "next_allowed_trading":
                value[key] = str(int(item) + delta)
            else:
                move_payload_times(item, delta)
    elif isinstance(value, list):
        for item in value:
            move_payload_times(item, delta)


def normalize(events):
    previous, traces = ZERO, {}
    for event in events:
        h = event["header"]
        ns = iso_ns(h["timestamp_iso"])
        move_payload_times(event["payload"], ns - int(h["timestamp_int"]))
        h["timestamp_int"] = str(ns)
        ms = ns // 1_000_000
        # Keep the version/variant/random bits; replace only the timestamp bits.
        h["event_id"] = str(UUID(int=(ms << 80) | (UUID(h["event_id"]).int & (2**80 - 1))))
        old_trace = h["trace_id"]
        traces.setdefault(old_trace, str(UUID(int=(ms << 80) | (UUID(old_trace).int & (2**80 - 1)))))
        h["trace_id"] = traces[old_trace]
        # Never copy placeholder hashes, signatures or other security claims.
        event["security"] = {"prev_hash": previous}
        previous = event_hash(event)
        event["security"]["event_hash"] = previous
    validate_stream(events)
    return events


def generated_files():
    text = (ROOT / "VCP_EXAMPLE_PAYLOADS_v1_0_EN.md").read_text(encoding="utf-8")
    collections = [section_events(text, "3.1"),
                   section_events(text, "3.3") + section_events(text, "3.4"),
                   section_events(text, "4.3"), section_events(text, "5.2")]
    output = {}
    for (name, types), events in zip(FILES.items(), collections):
        require(tuple(e["header"]["event_type"] for e in events) == types,
                f"Source events changed: {name}")
        normalize(events)
        if name.endswith(".jsonl"):
            output[name] = "".join(json.dumps(e, ensure_ascii=False, separators=(",", ":")) + "\n" for e in events)
        else:
            output[name] = json.dumps(events[0], ensure_ascii=False, indent=2) + "\n"
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="check byte-for-byte reproducibility without writing")
    args = parser.parse_args()
    for name, content in generated_files().items():
        path = ROOT / "examples" / name
        if args.check:
            require(path.is_file() and path.read_text(encoding="utf-8") == content,
                    f"Fixture needs regeneration: {name}")
        else:
            path.write_text(content, encoding="utf-8")
        print(f"{'CHECK' if args.check else 'WRITE'} {name}")


if __name__ == "__main__":
    main()
