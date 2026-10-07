# Legacy v1.0 test data

These four fixtures are synthetic, unsigned local test data for the **legacy
v1.0 guide in this repository**. They are not production evidence, certification,
or a statement of VCP v1.2 conformance. No v1.2 conformance has been verified.

| File | Source in the [example document](../VCP_EXAMPLE_PAYLOADS_v1_0_EN.md) | Contents |
| --- | --- | --- |
| `sample_sig_ord_exe_xauusd.jsonl` | §3.1 | SIG → ORD → ACK → EXE, four events |
| `sample_rej_cxl_case.jsonl` | §3.3 and §3.4 | ORD → REJ, then ORD → ACK → CXL, five events |
| `sample_risk_snapshot_news_block.json` | §4.3 | One RSK event with news embargo snapshot |
| `sample_gov_ai_decision.json` | §5.2 | One SIG event with AI governance data |

Every file is a separate hash chain beginning with 64 zero characters. The
rejection/cancellation file has two trace IDs but **one continuous hash chain**:
the second ORD links to the preceding REJ, without resetting to genesis.

## Run locally

From the repository root, with Python 3.10+ and no third-party dependencies:

```bash
python3 tools/legacy_fixtures.py
python3 -m unittest discover -s tests -v
python3 tools/generate_fixtures.py --check
```

The validator is read-only, returns nonzero on failure, and accepts specific
JSON/JSONL paths as optional arguments. Each supplied file must be a complete
independent chain. The unit tests include deliberate tampering, link corruption,
event removal/reordering, timestamp mismatch and numeric-type violations.

## Hash calculation and regeneration

Run `python3 tools/generate_fixtures.py` to regenerate all four files. The generator
extracts the full JSON examples from the sections above, not the shortened §8
illustrations. It uses each header's ISO timestamp as the source of truth,
recalculates its nanosecond string, updates UUID v7 timestamp bits (preserving
version/variant/random bits), and shifts related payload timestamps by the same
delta to preserve the illustrated time offsets. Trace IDs remain shared within
each scenario. All values remain synthetic.

The generator discards the embedded security objects, initializes genesis,
and calculates each hash and the next link using this guide's HCH-003:

```text
SHA256(0x00 || UTF8(compact_sorted_json(header)
                 + compact_sorted_json(payload) + prev_hash_hex_text))
```

`0x00` is one binary prefix byte; `prev_hash` is 64 lowercase hexadecimal text
characters, not decoded bytes. Security fields are excluded from the preimage.
The test also runs the actual HCH-003 functions extracted from the guide against
every stored event. It does not regenerate fixtures before validating them.

The serialization helper is deliberately limited to ASCII object keys, strings,
booleans, null, arrays, and safe integers. These fixtures contain no floating-point
numbers. Python `json.dumps(sort_keys=True, ...)` is **not a general RFC 8785
implementation**; arbitrary Unicode keys and floating-point input are outside
this test profile and rejected. This legacy equation is not a claim about v1.2.

## Validation scope

The smoke test covers local structure and required fields (SCH-001/002/003), the
fixture event codes and SHA256 selection (SCH-010/011/012), ORD/EXE fields
(SCH-020/021), financial strings and risk snapshot strings (SCH-030/031/032),
UUID v7 format/order/uniqueness (UID-001/002/010/011/020), timestamp consistency
and declarations (TST-001/002/010/020), SIG algorithm ID (EVT-001), and genesis,
hash length/calculation, linkage and tampering (HCH-001/003/004/010/020).
Timestamp equality is exact and event UUID timestamps also match header times,
which is stricter than the guide's tolerance/range checks.

This is a fixture-specific subset, not the complete conformance suite. It does
not test signatures or delegated signing, Merkle proofs, external anchors,
live clock accuracy, API submission, performance, tier certification or legal
compliance. Model hashes, approvals and explanation fields are illustrative;
no model files, approval evidence or external services are supplied. In
particular, the risk example's partial governance metadata and the guide's
limited lifecycle warning rules are not asserted to pass EVT-010 or EVT-002.
