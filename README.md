<!DOCTYPE html>
<html lang='en'>
<head>
  <meta charset='utf-8'>
  <title>VeritasChain Protocol Conformance Guide</title>
</head>
<body>
  <h1>VeritasChain Protocol Conformance Guide v1.0</h1>

  <p>
    This repository provides the conformance testing guide and reference
    example payloads for implementations of the VeritasChain Protocol VCP.
    It is intended to be used as a self check step before requesting
    formal VC Certified compliance auditing.
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
      <code>CONFORMANCE_TEST_GUIDE_v1_0_EN.md</code>
    </li>
  </ul>

  <h2>Example payload collections</h2>
  <p>
    The <code>examples/</code> directory contains ready to use payloads that represent
    valid VCP event streams. These files can be used for local testing, SDK
    development, or as input for automated conformance suites.
  </p>
  <ul>
    <li><code>examples/sample_sig_ord_exe_xauusd.jsonl</code>  full SIG → ORD → EXE lifecycle</li>
    <li><code>examples/sample_rej_cxl_case.jsonl</code>  risk rejection and cancel scenarios</li>
    <li><code>examples/sample_risk_snapshot_news_block.json</code>  VCP RISK snapshot with news trading block</li>
    <li><code>examples/sample_gov_ai_decision.json</code>  VCP GOV payload for AI driven decisions</li>
  </ul>

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
</body>
</html>
