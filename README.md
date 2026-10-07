<h1>VeritasChain Protocol Conformance Guide v1.0</h1>

<p>
  This repository provides the conformance testing guide and reference example payloads
  for the legacy VeritasChain Protocol VCP v1.0 format. The bundled smoke test
  checks a documented local subset only; it is not certification or production evidence.
  <strong>VCP v1.2 conformance has not been verified and is not claimed.</strong>
</p>

<h2>Scope</h2>
<ul>
  <li>How to validate VCP events locally before sending them to VCC</li>
  <li>Checklist for UUID v7, event types, timestamps, and numeric as string rules</li>
  <li>Procedures for verifying hash chains, digital signatures, and Merkle proofs</li>
  <li>End to end tests using the VCP Explorer API search, proof, and certificate endpoints</li>
  <li>Sample payload collections covering common trading and risk scenarios</li>
</ul>

<h2>Main documents</h2>
<ul>
  <li>
    <strong>Conformance Test Guide v1.0 English</strong><br>
    <a href="VCP_CONFORMANCE_TEST_GUIDE_v1_0_EN.md">VCP_CONFORMANCE_TEST_GUIDE_v1_0_EN.md</a>
  </li>
  <li><a href="VCP_EXAMPLE_PAYLOADS_v1_0_EN.md">Example Payload Collections v1.0 English</a></li>
</ul>

<h2>Example payload collections</h2>
<p>
  The <a href="examples/README.md">examples/ directory</a> contains four executable
  legacy v1.0 fixtures derived from the embedded illustrations, with regenerated
  HCH-003 hashes, continuous chain links and consistent timestamps. They are
  unsigned synthetic test data for the documented smoke-test subset, not fully
  certified VCP event streams. The embedded document examples remain illustrative.
</p>
<ul>
  <li><a href="examples/sample_sig_ord_exe_xauusd.jsonl"><code>examples/sample_sig_ord_exe_xauusd.jsonl</code></a>  SIG → ORD → ACK → EXE lifecycle (4 events)</li>
  <li><a href="examples/sample_rej_cxl_case.jsonl"><code>examples/sample_rej_cxl_case.jsonl</code></a>  order rejection and cancellation in one chain (5 events)</li>
  <li><a href="examples/sample_risk_snapshot_news_block.json"><code>examples/sample_risk_snapshot_news_block.json</code></a>  VCP RISK snapshot with news trading block</li>
  <li><a href="examples/sample_gov_ai_decision.json"><code>examples/sample_gov_ai_decision.json</code></a>  VCP GOV payload for AI driven decisions</li>
</ul>

<h2>Run the local smoke test</h2>
<p>From the repository root, using Python 3.10+; no packages, credentials or network access required:</p>

```bash
python3 tools/legacy_fixtures.py
python3 -m unittest discover -s tests -v
python3 tools/generate_fixtures.py --check
```

<p>
  To regenerate the fixtures, run <code>python3 tools/generate_fixtures.py</code>.
  The test validates the stored files without rewriting them, checks them against
  the guide's actual HCH-003 functions, and includes negative tampering cases.
  GitHub Actions runs the same checks on pushes and pull requests.
  See <a href="examples/README.md">fixture provenance, hash formula and validation limits</a>.
  Signatures, Merkle proofs, external anchors, APIs and complete tier conformance
  are outside this smoke test. The broader guide's external SDK/CLI/API examples
  are not bundled or verified by these commands.
</p>

<h2>Position in the VCP ecosystem</h2>
<p>
  This repository works together with the other VeritasChain Protocol artifacts:
</p>
<ul>
  <li><strong>vcp spec</strong>  core VeritasChain Protocol specification</li>
  <li><strong>vcp sdk spec</strong>  language level SDK contracts for TypeScript, Python, and MQL5</li>
  <li><strong>vcp sidecar guide</strong>  Silver tier sidecar integration for MT4 MT5 and white label platforms</li>
  <li><strong>vcp explorer api</strong>  Explorer service and verification API</li>
  <li><strong>vcp market intelligence</strong>  industry and regulatory research supporting VCP adoption</li>
</ul>

<h2>Intended audience</h2>
<ul>
  <li>Engineering teams preparing to integrate VCP in production systems</li>
  <li>SDK maintainers who need a reference for expected behaviour</li>
  <li>Compliance and QA engineers building automated conformance suites</li>
  <li>Organizations planning to apply for VC Certified compliance certification</li>
</ul>

<p>
  Implementers are encouraged to run all checks in this guide and to validate
  their payloads against the example collections before submitting systems for
  formal VC Certified auditing.
</p>
