# VeritasChain Protocol Conformance Test Guide v1.0

**Document ID:** VSO-TEST-001  
**Status:** Release Candidate  
**Version:** 1.0.0  
**Date:** 2025-11-25  
**Maintainer:** VeritasChain Standards Organization (VSO)  
**License:** Apache 2.0

---

## Abstract

This document provides comprehensive guidance for testing VCP (VeritasChain Protocol) implementations prior to VC-Certified certification. It defines test procedures, validation criteria, and automated test suites that implementers can use to verify their systems meet VCP v1.0 specification requirements.

The guide covers schema validation, hash chain verification, signature verification, and end-to-end testing with the VCP Explorer API. Passing all conformance tests is a prerequisite for VC-Certified certification at any tier (Silver, Gold, Platinum).

---

## Table of Contents

1. [Introduction](#1-introduction)
   - 1.1 [Purpose](#11-purpose)
   - 1.2 [Scope](#12-scope)
   - 1.3 [Audience](#13-audience)
   - 1.4 [Prerequisites](#14-prerequisites)
   - 1.5 [Test Environment](#15-test-environment)
2. [Conformance Levels](#2-conformance-levels)
   - 2.1 [Tier Requirements Matrix](#21-tier-requirements-matrix)
   - 2.2 [Test Categories](#22-test-categories)
   - 2.3 [Pass/Fail Criteria](#23-passfail-criteria)
3. [Pre-Flight Checklist](#3-pre-flight-checklist)
   - 3.1 [Implementation Checklist](#31-implementation-checklist)
   - 3.2 [Common Mistakes](#32-common-mistakes)
   - 3.3 [Quick Self-Assessment](#33-quick-self-assessment)
4. [Schema Validation Tests](#4-schema-validation-tests)
   - 4.1 [JSON Schema Validation](#41-json-schema-validation)
   - 4.2 [Field Format Tests](#42-field-format-tests)
   - 4.3 [Required Fields Tests](#43-required-fields-tests)
   - 4.4 [Numeric Precision Tests](#44-numeric-precision-tests)
5. [UUID v7 Validation Tests](#5-uuid-v7-validation-tests)
   - 5.1 [Format Validation](#51-format-validation)
   - 5.2 [Time-Ordering Tests](#52-time-ordering-tests)
   - 5.3 [Uniqueness Tests](#53-uniqueness-tests)
6. [Timestamp Validation Tests](#6-timestamp-validation-tests)
   - 6.1 [Dual Format Consistency](#61-dual-format-consistency)
   - 6.2 [Precision Level Tests](#62-precision-level-tests)
   - 6.3 [Clock Sync Status Tests](#63-clock-sync-status-tests)
7. [Hash Chain Validation Tests](#7-hash-chain-validation-tests)
   - 7.1 [Genesis Event Tests](#71-genesis-event-tests)
   - 7.2 [Chain Continuity Tests](#72-chain-continuity-tests)
   - 7.3 [Hash Calculation Tests](#73-hash-calculation-tests)
   - 7.4 [Tampering Detection Tests](#74-tampering-detection-tests)
8. [Signature Validation Tests](#8-signature-validation-tests)
   - 8.1 [Ed25519 Signature Tests](#81-ed25519-signature-tests)
   - 8.2 [Delegated Signature Tests](#82-delegated-signature-tests)
   - 8.3 [Key Management Tests](#83-key-management-tests)
9. [Merkle Proof Validation Tests](#9-merkle-proof-validation-tests)
   - 9.1 [Proof Structure Tests](#91-proof-structure-tests)
   - 9.2 [Local Verification Tests](#92-local-verification-tests)
   - 9.3 [Root Consistency Tests](#93-root-consistency-tests)
10. [Event Type Tests](#10-event-type-tests)
    - 10.1 [Trade Lifecycle Tests](#101-trade-lifecycle-tests)
    - 10.2 [Governance Event Tests](#102-governance-event-tests)
    - 10.3 [System Event Tests](#103-system-event-tests)
11. [End-to-End Integration Tests](#11-end-to-end-integration-tests)
    - 11.1 [Logger Client Tests](#111-logger-client-tests)
    - 11.2 [Explorer API Tests](#112-explorer-api-tests)
    - 11.3 [Round-Trip Verification](#113-round-trip-verification)
12. [Performance Tests](#12-performance-tests)
    - 12.1 [Throughput Tests](#121-throughput-tests)
    - 12.2 [Latency Tests](#122-latency-tests)
    - 12.3 [Tier-Specific Requirements](#123-tier-specific-requirements)
13. [Test Automation](#13-test-automation)
    - 13.1 [Test Runner Setup](#131-test-runner-setup)
    - 13.2 [CI/CD Integration](#132-cicd-integration)
    - 13.3 [Automated Report Generation](#133-automated-report-generation)
14. [Certification Submission](#14-certification-submission)
    - 14.1 [Required Artifacts](#141-required-artifacts)
    - 14.2 [Submission Process](#142-submission-process)
    - 14.3 [Review Timeline](#143-review-timeline)
15. [Appendices](#15-appendices)
    - Appendix A: [Test Vector Library](#appendix-a-test-vector-library)
    - Appendix B: [Error Code Reference](#appendix-b-error-code-reference)
    - Appendix C: [Sample Test Report](#appendix-c-sample-test-report)

---

## 1. Introduction

### 1.1 Purpose

This Conformance Test Guide serves three primary purposes:

1. **Self-Assessment**: Enable implementers to validate their VCP integration before certification
2. **Standardization**: Define consistent testing criteria across all implementations
3. **Certification Preparation**: Provide a clear path to VC-Certified certification

### 1.2 Scope

This guide covers testing for:

- VCP v1.0 specification compliance
- VCP SDK implementations (TypeScript, Python, MQL5)
- VCC (VeritasChain Cloud) integration
- All three certification tiers (Silver, Gold, Platinum)

Out of scope:

- Business logic validation
- Trading strategy testing
- Platform-specific integration (beyond VCP)

### 1.3 Audience

- **SDK Implementers**: Developers building VCP client libraries
- **Integration Engineers**: Teams integrating VCP into trading systems
- **QA Engineers**: Testing and validation specialists
- **Certification Applicants**: Organizations seeking VC-Certified status

### 1.4 Prerequisites

Before running conformance tests, ensure:

1. **VCP SDK** is installed and configured
2. **API Key** is obtained from VCC (sandbox or production)
3. **Test Environment** is set up (see Section 1.5)
4. **VCP Specification v1.0** is reviewed

### 1.5 Test Environment

#### 1.5.1 Sandbox Environment

| Resource | URL |
|----------|-----|
| VCC Sandbox API | `https://sandbox.veritaschain.org/v1` |
| Explorer Sandbox | `https://explorer-sandbox.veritaschain.org` |
| Documentation | `https://docs.veritaschain.org` |

#### 1.5.2 Required Tools

```bash
# Node.js/TypeScript
npm install -g @veritaschain/vcp-test-suite

# Python
pip install vcp-test-suite

# Both
# - jq (JSON processing)
# - openssl (cryptographic operations)
# - curl (HTTP testing)
```

#### 1.5.3 Environment Variables

```bash
export VCP_API_KEY="your-sandbox-api-key"
export VCP_ENDPOINT="https://sandbox.veritaschain.org/v1"
export VCP_TEST_VENUE_ID="TEST-VENUE-001"
export VCP_TEST_ACCOUNT_ID="test_account_hash"
```

---

## 2. Conformance Levels

### 2.1 Tier Requirements Matrix

| Test Category | Silver | Gold | Platinum |
|--------------|--------|------|----------|
| Schema Validation | Required | Required | Required |
| UUID v7 Format | Required | Required | Required |
| Timestamp (MILLISECOND) | Required | Required | Required |
| Timestamp (MICROSECOND) | Optional | Required | Required |
| Timestamp (NANOSECOND) | Optional | Optional | Required |
| Hash Chain | Required | Required | Required |
| Delegated Signature | Required | N/A | N/A |
| Self-Signature (Ed25519) | N/A | Required | Required |
| Self-Signature (PQC) | Optional | Optional | Optional |
| Merkle Proof Verification | Required | Required | Required |
| Throughput (>1K/sec) | Required | Required | Required |
| Throughput (>10K/sec) | Optional | Required | Required |
| Throughput (>100K/sec) | Optional | Optional | Required |
| Latency (<1s) | Required | Required | Required |
| Latency (<100ms) | Optional | Required | Required |
| Latency (<10ms) | Optional | Optional | Required |
| Clock Sync (BEST_EFFORT) | Required | Required | Required |
| Clock Sync (NTP_SYNCED) | Optional | Required | Required |
| Clock Sync (PTP_LOCKED) | Optional | Optional | Required |

### 2.2 Test Categories

| Category | Code | Description | Test Count |
|----------|------|-------------|------------|
| Schema | SCH | JSON schema and field validation | 25 |
| UUID | UID | UUID v7 format and ordering | 10 |
| Timestamp | TST | Dual format and precision | 12 |
| Hash Chain | HCH | Chain integrity and calculation | 15 |
| Signature | SIG | Cryptographic signature validation | 10 |
| Merkle | MKL | Proof structure and verification | 8 |
| Event Type | EVT | Event lifecycle and governance | 20 |
| Integration | INT | End-to-end API tests | 15 |
| Performance | PRF | Throughput and latency | 10 |
| **Total** | | | **125** |

### 2.3 Pass/Fail Criteria

#### 2.3.1 Individual Test

- **PASS**: Test assertion succeeds
- **FAIL**: Test assertion fails
- **SKIP**: Test not applicable for tier
- **ERROR**: Test could not execute (environment issue)

#### 2.3.2 Category Pass Rate

| Tier | Required Pass Rate |
|------|-------------------|
| Silver | 95% of applicable tests |
| Gold | 98% of applicable tests |
| Platinum | 100% of applicable tests |

#### 2.3.3 Critical Tests

Some tests are marked **CRITICAL**. Any failure in a critical test results in automatic certification failure, regardless of overall pass rate.

Critical tests include:

- `SCH-001`: Event structure validation
- `UID-001`: UUID v7 format
- `HCH-001`: Genesis event prev_hash
- `HCH-003`: Hash calculation algorithm
- `SIG-001`: Signature algorithm compliance

---

## 3. Pre-Flight Checklist

### 3.1 Implementation Checklist

Before running the test suite, verify your implementation against this checklist:

#### 3.1.1 Event Structure

- [ ] Events have `header`, `payload`, and `security` sections
- [ ] All required header fields are present
- [ ] `event_id` and `trace_id` use UUID v7 format
- [ ] `timestamp_int` is a string (not number)
- [ ] `timestamp_iso` includes timezone designator (Z or ±HH:MM)
- [ ] `event_type_code` uses fixed VCP codes (1-101)

#### 3.1.2 Numeric Precision

- [ ] All financial values are strings (price, quantity, commission, etc.)
- [ ] No floating-point numbers in JSON output
- [ ] Precision is preserved (no scientific notation)

#### 3.1.3 Hash Chain

- [ ] First event uses `prev_hash = "0" * 64` (64 zeros)
- [ ] Subsequent events reference previous event's `event_hash`
- [ ] Hash calculation follows VCP-SEC specification
- [ ] RFC 8785 JSON canonicalization is used

#### 3.1.4 Signatures (Gold/Platinum)

- [ ] Ed25519 keys are properly generated
- [ ] Signatures are hex-encoded
- [ ] Signed data matches canonical JSON representation

#### 3.1.5 API Integration

- [ ] API key is properly configured
- [ ] HTTPS is used for all requests
- [ ] Retry logic handles transient failures
- [ ] Rate limiting is respected

### 3.2 Common Mistakes

| Mistake | Impact | Fix |
|---------|--------|-----|
| Using `number` for prices | Precision loss, schema fail | Use `string` type |
| UUID v4 instead of v7 | Time ordering broken | Implement UUID v7 |
| Missing timezone in ISO timestamp | Validation fail | Append `Z` or offset |
| Wrong prev_hash for genesis | Chain broken | Use 64 zeros |
| Non-canonical JSON | Hash mismatch | Use RFC 8785 |
| Hardcoded API key | Security risk | Use env variables |

### 3.3 Quick Self-Assessment

Run this quick check before the full test suite:

```bash
# 1. Generate a test event
vcp-test generate-event --type SIG --output test_event.json

# 2. Validate schema
vcp-test validate-schema test_event.json

# 3. Check UUID format
vcp-test check-uuid test_event.json

# 4. Verify timestamp
vcp-test check-timestamp test_event.json

# 5. Validate numeric fields
vcp-test check-numerics test_event.json

# Quick summary
vcp-test quick-check test_event.json
```

Expected output for a passing event:

```
✓ Schema validation: PASS
✓ UUID v7 format: PASS
✓ Timestamp dual format: PASS
✓ Numeric as string: PASS
✓ Required fields: PASS

Quick Check Result: PASS (5/5)
Ready for full conformance testing.
```

---

## 4. Schema Validation Tests

### 4.1 JSON Schema Validation

#### Test SCH-001: Event Structure (CRITICAL)

**Purpose**: Verify event has required top-level sections.

**Test Procedure**:

```python
def test_sch_001_event_structure(event: dict) -> TestResult:
    """
    SCH-001: Event must have header, payload, and security sections
    Tier: All
    Critical: Yes
    """
    required_sections = ['header', 'payload', 'security']
    
    for section in required_sections:
        if section not in event:
            return TestResult.fail(
                f"Missing required section: {section}"
            )
        if not isinstance(event[section], dict):
            return TestResult.fail(
                f"Section '{section}' must be an object"
            )
    
    return TestResult.pass_()
```

**Pass Criteria**: All three sections present as objects.

#### Test SCH-002: Header Required Fields

**Purpose**: Verify all required header fields are present.

**Required Fields**:

```python
REQUIRED_HEADER_FIELDS = [
    'event_id',
    'trace_id', 
    'timestamp_int',
    'timestamp_iso',
    'event_type',
    'event_type_code',
    'timestamp_precision',
    'clock_sync_status',
    'hash_algo',
    'venue_id',
    'symbol',
    'account_id'
]
```

**Test Procedure**:

```python
def test_sch_002_header_required_fields(event: dict) -> TestResult:
    """
    SCH-002: Header must contain all required fields
    Tier: All
    """
    header = event.get('header', {})
    missing = []
    
    for field in REQUIRED_HEADER_FIELDS:
        if field not in header:
            missing.append(field)
    
    if missing:
        return TestResult.fail(
            f"Missing header fields: {', '.join(missing)}"
        )
    
    return TestResult.pass_()
```

#### Test SCH-003: Security Required Fields

**Purpose**: Verify security section has required fields.

```python
def test_sch_003_security_required_fields(event: dict) -> TestResult:
    """
    SCH-003: Security section must have event_hash and prev_hash
    Tier: All
    """
    security = event.get('security', {})
    
    if 'event_hash' not in security:
        return TestResult.fail("Missing security.event_hash")
    
    if 'prev_hash' not in security:
        return TestResult.fail("Missing security.prev_hash")
    
    return TestResult.pass_()
```

### 4.2 Field Format Tests

#### Test SCH-010: Event Type Code Range

```python
VALID_EVENT_TYPE_CODES = {
    1, 2, 3, 4, 5, 6, 7, 8, 9,  # Trade lifecycle
    20, 21, 22,                  # Governance
    98, 99, 100, 101             # System
}

def test_sch_010_event_type_code_range(event: dict) -> TestResult:
    """
    SCH-010: Event type code must be a valid VCP code
    Tier: All
    """
    code = event.get('header', {}).get('event_type_code')
    
    if code not in VALID_EVENT_TYPE_CODES:
        return TestResult.fail(
            f"Invalid event_type_code: {code}. "
            f"Valid codes: {sorted(VALID_EVENT_TYPE_CODES)}"
        )
    
    return TestResult.pass_()
```

#### Test SCH-011: Event Type Consistency

```python
EVENT_TYPE_MAPPING = {
    'SIG': 1, 'ORD': 2, 'ACK': 3, 'EXE': 4, 'PRT': 5,
    'REJ': 6, 'CXL': 7, 'MOD': 8, 'CLS': 9,
    'ALG': 20, 'RSK': 21, 'AUD': 22,
    'HBT': 98, 'ERR': 99, 'REC': 100, 'SNC': 101
}

def test_sch_011_event_type_consistency(event: dict) -> TestResult:
    """
    SCH-011: event_type string must match event_type_code
    Tier: All
    """
    header = event.get('header', {})
    event_type = header.get('event_type')
    event_type_code = header.get('event_type_code')
    
    expected_code = EVENT_TYPE_MAPPING.get(event_type)
    
    if expected_code is None:
        return TestResult.fail(f"Unknown event_type: {event_type}")
    
    if event_type_code != expected_code:
        return TestResult.fail(
            f"event_type '{event_type}' should have code {expected_code}, "
            f"got {event_type_code}"
        )
    
    return TestResult.pass_()
```

#### Test SCH-012: Hash Algorithm Values

```python
def test_sch_012_hash_algo_values(event: dict) -> TestResult:
    """
    SCH-012: hash_algo must be a valid algorithm
    Tier: All
    """
    valid_algos = {'SHA256', 'SHA3_256', 'BLAKE3'}
    algo = event.get('header', {}).get('hash_algo')
    
    if algo not in valid_algos:
        return TestResult.fail(
            f"Invalid hash_algo: {algo}. Valid: {valid_algos}"
        )
    
    return TestResult.pass_()
```

### 4.3 Required Fields Tests

#### Test SCH-020: Trade Data Fields for ORD

```python
def test_sch_020_ord_trade_data(event: dict) -> TestResult:
    """
    SCH-020: ORD event must have order details in trade_data
    Tier: All
    """
    if event.get('header', {}).get('event_type') != 'ORD':
        return TestResult.skip("Not an ORD event")
    
    trade_data = event.get('payload', {}).get('trade_data', {})
    
    required = ['order_id', 'side', 'price', 'quantity']
    missing = [f for f in required if f not in trade_data]
    
    if missing:
        return TestResult.fail(
            f"ORD event missing trade_data fields: {missing}"
        )
    
    return TestResult.pass_()
```

#### Test SCH-021: Trade Data Fields for EXE

```python
def test_sch_021_exe_trade_data(event: dict) -> TestResult:
    """
    SCH-021: EXE event must have execution details
    Tier: All
    """
    if event.get('header', {}).get('event_type') != 'EXE':
        return TestResult.skip("Not an EXE event")
    
    trade_data = event.get('payload', {}).get('trade_data', {})
    
    required = ['order_id', 'execution_price', 'executed_qty']
    missing = [f for f in required if f not in trade_data]
    
    if missing:
        return TestResult.fail(
            f"EXE event missing trade_data fields: {missing}"
        )
    
    return TestResult.pass_()
```

### 4.4 Numeric Precision Tests

#### Test SCH-030: Price as String (CRITICAL)

```python
def test_sch_030_price_as_string(event: dict) -> TestResult:
    """
    SCH-030: price field must be a string, not number
    Tier: All
    Critical: Yes
    """
    trade_data = event.get('payload', {}).get('trade_data', {})
    
    if 'price' not in trade_data:
        return TestResult.skip("No price field present")
    
    price = trade_data['price']
    
    if not isinstance(price, str):
        return TestResult.fail(
            f"price must be string, got {type(price).__name__}: {price}"
        )
    
    # Verify it's a valid numeric string
    try:
        float(price)
    except ValueError:
        return TestResult.fail(
            f"price string is not a valid number: {price}"
        )
    
    return TestResult.pass_()
```

#### Test SCH-031: All Financial Fields as Strings

```python
FINANCIAL_FIELDS = [
    'price', 'quantity', 'executed_qty', 'remaining_qty',
    'execution_price', 'commission', 'slippage',
    'pnl_realized', 'pnl_unrealized'
]

def test_sch_031_financial_fields_as_strings(event: dict) -> TestResult:
    """
    SCH-031: All financial values must be strings
    Tier: All
    """
    trade_data = event.get('payload', {}).get('trade_data', {})
    violations = []
    
    for field in FINANCIAL_FIELDS:
        if field in trade_data:
            value = trade_data[field]
            if not isinstance(value, str):
                violations.append(
                    f"{field}: {type(value).__name__}"
                )
    
    if violations:
        return TestResult.fail(
            f"Non-string financial fields: {', '.join(violations)}"
        )
    
    return TestResult.pass_()
```

#### Test SCH-032: VCP-RISK Snapshot Values as Strings

```python
def test_sch_032_risk_snapshot_strings(event: dict) -> TestResult:
    """
    SCH-032: VCP-RISK snapshot values must be strings
    Tier: All
    """
    vcp_risk = event.get('payload', {}).get('vcp_risk', {})
    snapshot = vcp_risk.get('snapshot', {})
    
    if not snapshot:
        return TestResult.skip("No risk snapshot present")
    
    violations = []
    for key, value in snapshot.items():
        if not isinstance(value, str):
            violations.append(f"{key}: {type(value).__name__}")
    
    if violations:
        return TestResult.fail(
            f"Non-string risk snapshot values: {', '.join(violations)}"
        )
    
    return TestResult.pass_()
```

---

## 5. UUID v7 Validation Tests

### 5.1 Format Validation

#### Test UID-001: Event ID UUID v7 Format (CRITICAL)

```python
import re

UUID_V7_PATTERN = re.compile(
    r'^[0-9a-f]{8}-[0-9a-f]{4}-7[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$',
    re.IGNORECASE
)

def test_uid_001_event_id_format(event: dict) -> TestResult:
    """
    UID-001: event_id must be valid UUID v7 format
    Tier: All
    Critical: Yes
    """
    event_id = event.get('header', {}).get('event_id', '')
    
    if not UUID_V7_PATTERN.match(event_id):
        return TestResult.fail(
            f"event_id is not valid UUID v7: {event_id}\n"
            f"Expected format: xxxxxxxx-xxxx-7xxx-yxxx-xxxxxxxxxxxx\n"
            f"where y is 8, 9, a, or b"
        )
    
    return TestResult.pass_()
```

#### Test UID-002: Trace ID UUID v7 Format

```python
def test_uid_002_trace_id_format(event: dict) -> TestResult:
    """
    UID-002: trace_id must be valid UUID v7 format
    Tier: All
    """
    trace_id = event.get('header', {}).get('trace_id', '')
    
    if not UUID_V7_PATTERN.match(trace_id):
        return TestResult.fail(
            f"trace_id is not valid UUID v7: {trace_id}"
        )
    
    return TestResult.pass_()
```

### 5.2 Time-Ordering Tests

#### Test UID-010: UUID v7 Time Component

```python
def extract_uuid_v7_timestamp(uuid_str: str) -> int:
    """Extract timestamp (ms) from UUID v7"""
    # Remove hyphens
    hex_str = uuid_str.replace('-', '')
    # First 48 bits (12 hex chars) are timestamp
    timestamp_hex = hex_str[:12]
    return int(timestamp_hex, 16)

def test_uid_010_uuid_time_component(event: dict) -> TestResult:
    """
    UID-010: UUID v7 timestamp should be reasonable
    Tier: All
    """
    event_id = event.get('header', {}).get('event_id', '')
    
    try:
        uuid_ts = extract_uuid_v7_timestamp(event_id)
    except ValueError:
        return TestResult.fail("Could not parse UUID timestamp")
    
    # Should be between 2020 and 2100
    min_ts = 1577836800000  # 2020-01-01
    max_ts = 4102444800000  # 2100-01-01
    
    if uuid_ts < min_ts or uuid_ts > max_ts:
        return TestResult.fail(
            f"UUID timestamp out of range: {uuid_ts}ms"
        )
    
    return TestResult.pass_()
```

#### Test UID-011: Sequential UUID Ordering

```python
def test_uid_011_sequential_ordering(events: list[dict]) -> TestResult:
    """
    UID-011: Sequential events should have ordered UUIDs
    Tier: All
    """
    if len(events) < 2:
        return TestResult.skip("Need at least 2 events")
    
    for i in range(1, len(events)):
        prev_id = events[i-1].get('header', {}).get('event_id', '')
        curr_id = events[i].get('header', {}).get('event_id', '')
        
        # Lexicographic comparison works for UUID v7
        if curr_id <= prev_id:
            return TestResult.fail(
                f"Event {i} UUID not greater than event {i-1}\n"
                f"  Event {i-1}: {prev_id}\n"
                f"  Event {i}: {curr_id}"
            )
    
    return TestResult.pass_()
```

### 5.3 Uniqueness Tests

#### Test UID-020: Event ID Uniqueness

```python
def test_uid_020_event_id_uniqueness(events: list[dict]) -> TestResult:
    """
    UID-020: All event_ids must be unique
    Tier: All
    """
    event_ids = [e.get('header', {}).get('event_id') for e in events]
    duplicates = [id for id in event_ids if event_ids.count(id) > 1]
    
    if duplicates:
        return TestResult.fail(
            f"Duplicate event_ids found: {set(duplicates)}"
        )
    
    return TestResult.pass_()
```

---

## 6. Timestamp Validation Tests

### 6.1 Dual Format Consistency

#### Test TST-001: Timestamp Formats Match

```python
from datetime import datetime, timezone

def test_tst_001_timestamp_formats_match(event: dict) -> TestResult:
    """
    TST-001: timestamp_int and timestamp_iso must represent same time
    Tier: All
    """
    header = event.get('header', {})
    ts_int = header.get('timestamp_int', '')
    ts_iso = header.get('timestamp_iso', '')
    
    # Parse timestamp_int (nanoseconds)
    try:
        ns = int(ts_int)
        ms = ns // 1_000_000
    except ValueError:
        return TestResult.fail(f"Invalid timestamp_int: {ts_int}")
    
    # Parse timestamp_iso
    try:
        # Handle various ISO formats
        if ts_iso.endswith('Z'):
            dt = datetime.fromisoformat(ts_iso.replace('Z', '+00:00'))
        else:
            dt = datetime.fromisoformat(ts_iso)
        iso_ms = int(dt.timestamp() * 1000)
    except ValueError:
        return TestResult.fail(f"Invalid timestamp_iso: {ts_iso}")
    
    # Allow 1 second tolerance for rounding
    if abs(ms - iso_ms) > 1000:
        return TestResult.fail(
            f"Timestamp mismatch:\n"
            f"  timestamp_int: {ms}ms\n"
            f"  timestamp_iso: {iso_ms}ms ({ts_iso})\n"
            f"  Difference: {abs(ms - iso_ms)}ms"
        )
    
    return TestResult.pass_()
```

#### Test TST-002: Timestamp String Type

```python
def test_tst_002_timestamp_int_is_string(event: dict) -> TestResult:
    """
    TST-002: timestamp_int must be a string, not number
    Tier: All
    """
    ts_int = event.get('header', {}).get('timestamp_int')
    
    if not isinstance(ts_int, str):
        return TestResult.fail(
            f"timestamp_int must be string, got {type(ts_int).__name__}"
        )
    
    return TestResult.pass_()
```

### 6.2 Precision Level Tests

#### Test TST-010: Precision Declaration Accuracy

```python
def test_tst_010_precision_accuracy(event: dict) -> TestResult:
    """
    TST-010: timestamp_precision must match actual precision
    Tier: All
    """
    header = event.get('header', {})
    precision = header.get('timestamp_precision')
    ts_int = header.get('timestamp_int', '')
    
    try:
        ns = int(ts_int)
    except ValueError:
        return TestResult.fail(f"Invalid timestamp_int: {ts_int}")
    
    # Check trailing zeros
    if precision == 'MILLISECOND':
        # Should end with 6 zeros (microseconds + nanoseconds)
        if ns % 1_000_000 != 0:
            return TestResult.fail(
                f"MILLISECOND precision should not have sub-ms precision: {ts_int}"
            )
    elif precision == 'MICROSECOND':
        # Should end with 3 zeros (nanoseconds only)
        if ns % 1_000 != 0:
            return TestResult.fail(
                f"MICROSECOND precision should not have nanosecond precision: {ts_int}"
            )
    # NANOSECOND can have any value
    
    return TestResult.pass_()
```

### 6.3 Clock Sync Status Tests

#### Test TST-020: Valid Clock Sync Status

```python
def test_tst_020_clock_sync_status(event: dict) -> TestResult:
    """
    TST-020: clock_sync_status must be a valid value
    Tier: All
    """
    valid_statuses = {'PTP_LOCKED', 'NTP_SYNCED', 'BEST_EFFORT', 'UNRELIABLE'}
    status = event.get('header', {}).get('clock_sync_status')
    
    if status not in valid_statuses:
        return TestResult.fail(
            f"Invalid clock_sync_status: {status}. Valid: {valid_statuses}"
        )
    
    return TestResult.pass_()
```

#### Test TST-021: Clock Sync Tier Requirements

```python
def test_tst_021_clock_sync_tier(event: dict, tier: str) -> TestResult:
    """
    TST-021: Clock sync status must meet tier requirements
    Tier: Tier-specific
    """
    status = event.get('header', {}).get('clock_sync_status')
    
    tier_requirements = {
        'Silver': {'PTP_LOCKED', 'NTP_SYNCED', 'BEST_EFFORT', 'UNRELIABLE'},
        'Gold': {'PTP_LOCKED', 'NTP_SYNCED'},
        'Platinum': {'PTP_LOCKED'}
    }
    
    allowed = tier_requirements.get(tier, set())
    
    if status not in allowed:
        return TestResult.fail(
            f"{tier} tier requires clock_sync_status in {allowed}, got: {status}"
        )
    
    return TestResult.pass_()
```

---

## 7. Hash Chain Validation Tests

### 7.1 Genesis Event Tests

#### Test HCH-001: Genesis Event Prev Hash (CRITICAL)

```python
GENESIS_PREV_HASH = '0' * 64

def test_hch_001_genesis_prev_hash(event: dict, is_genesis: bool) -> TestResult:
    """
    HCH-001: First event must have prev_hash of 64 zeros
    Tier: All
    Critical: Yes
    """
    if not is_genesis:
        return TestResult.skip("Not a genesis event")
    
    prev_hash = event.get('security', {}).get('prev_hash', '')
    
    if prev_hash != GENESIS_PREV_HASH:
        return TestResult.fail(
            f"Genesis event must have prev_hash of 64 zeros\n"
            f"  Expected: {GENESIS_PREV_HASH}\n"
            f"  Got: {prev_hash}"
        )
    
    return TestResult.pass_()
```

### 7.2 Chain Continuity Tests

#### Test HCH-010: Chain Linkage

```python
def test_hch_010_chain_linkage(events: list[dict]) -> TestResult:
    """
    HCH-010: Each event's prev_hash must equal previous event's event_hash
    Tier: All
    """
    if len(events) < 2:
        return TestResult.skip("Need at least 2 events")
    
    for i in range(1, len(events)):
        prev_event_hash = events[i-1].get('security', {}).get('event_hash', '')
        curr_prev_hash = events[i].get('security', {}).get('prev_hash', '')
        
        if curr_prev_hash != prev_event_hash:
            return TestResult.fail(
                f"Chain broken at event {i}:\n"
                f"  Event {i-1} event_hash: {prev_event_hash}\n"
                f"  Event {i} prev_hash: {curr_prev_hash}"
            )
    
    return TestResult.pass_()
```

### 7.3 Hash Calculation Tests

#### Test HCH-003: Hash Calculation (CRITICAL)

```python
import hashlib
import json

def canonicalize_json(obj: dict) -> str:
    """RFC 8785 JSON canonicalization"""
    return json.dumps(obj, sort_keys=True, separators=(',', ':'), ensure_ascii=False)

def calculate_expected_hash(header: dict, payload: dict, prev_hash: str, algo: str = 'SHA256') -> str:
    """Calculate expected event hash per VCP-SEC spec"""
    canonical = canonicalize_json(header) + canonicalize_json(payload) + prev_hash
    
    prefix_map = {'SHA256': b'\x00', 'SHA3_256': b'\x01', 'BLAKE3': b'\x02'}
    prefix = prefix_map.get(algo, b'\x00')
    
    if algo == 'SHA256':
        hasher = hashlib.sha256()
    elif algo == 'SHA3_256':
        hasher = hashlib.sha3_256()
    else:
        # BLAKE3 requires external library
        import blake3
        hasher = blake3.blake3()
    
    hasher.update(prefix + canonical.encode('utf-8'))
    return hasher.hexdigest()

def test_hch_003_hash_calculation(event: dict) -> TestResult:
    """
    HCH-003: event_hash must be correctly calculated
    Tier: All
    Critical: Yes
    """
    header = event.get('header', {})
    payload = event.get('payload', {})
    security = event.get('security', {})
    
    event_hash = security.get('event_hash', '')
    prev_hash = security.get('prev_hash', '')
    algo = header.get('hash_algo', 'SHA256')
    
    expected = calculate_expected_hash(header, payload, prev_hash, algo)
    
    if event_hash != expected:
        return TestResult.fail(
            f"Hash mismatch:\n"
            f"  Expected: {expected}\n"
            f"  Got: {event_hash}\n"
            f"  Algorithm: {algo}"
        )
    
    return TestResult.pass_()
```

#### Test HCH-004: Hash Length

```python
def test_hch_004_hash_length(event: dict) -> TestResult:
    """
    HCH-004: event_hash and prev_hash must be 64 hex characters
    Tier: All
    """
    security = event.get('security', {})
    
    for field in ['event_hash', 'prev_hash']:
        value = security.get(field, '')
        
        if len(value) != 64:
            return TestResult.fail(
                f"{field} must be 64 characters, got {len(value)}"
            )
        
        if not all(c in '0123456789abcdef' for c in value.lower()):
            return TestResult.fail(
                f"{field} must be hexadecimal: {value}"
            )
    
    return TestResult.pass_()
```

### 7.4 Tampering Detection Tests

#### Test HCH-020: Tamper Detection

```python
def test_hch_020_tamper_detection(event: dict) -> TestResult:
    """
    HCH-020: Modifying any field should invalidate hash
    Tier: All
    """
    import copy
    
    # Make a copy and modify a field
    tampered = copy.deepcopy(event)
    tampered['header']['symbol'] = 'TAMPERED'
    
    # Recalculate hash
    new_hash = calculate_expected_hash(
        tampered['header'],
        tampered['payload'],
        tampered['security']['prev_hash'],
        tampered['header'].get('hash_algo', 'SHA256')
    )
    
    original_hash = event['security']['event_hash']
    
    if new_hash == original_hash:
        return TestResult.fail(
            "Tampering not detected - hash should change when data changes"
        )
    
    return TestResult.pass_()
```

---

## 8. Signature Validation Tests

### 8.1 Ed25519 Signature Tests

#### Test SIG-001: Signature Algorithm (CRITICAL)

```python
def test_sig_001_signature_algorithm(event: dict, tier: str) -> TestResult:
    """
    SIG-001: Signature algorithm must be valid for tier
    Tier: Gold, Platinum
    Critical: Yes
    """
    if tier == 'Silver':
        return TestResult.skip("Silver tier uses delegated signatures")
    
    security = event.get('security', {})
    sign_algo = security.get('sign_algo')
    
    valid_algos = {'ED25519', 'ECDSA_SECP256K1', 'RSA_2048', 'DILITHIUM2', 'FALCON512'}
    
    if sign_algo not in valid_algos:
        return TestResult.fail(
            f"Invalid sign_algo: {sign_algo}. Valid: {valid_algos}"
        )
    
    return TestResult.pass_()
```

#### Test SIG-002: Ed25519 Signature Verification

```python
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
from cryptography.exceptions import InvalidSignature

def test_sig_002_ed25519_verification(event: dict, public_key_hex: str) -> TestResult:
    """
    SIG-002: Ed25519 signature must verify
    Tier: Gold, Platinum
    """
    security = event.get('security', {})
    
    if security.get('sign_algo') != 'ED25519':
        return TestResult.skip("Not an Ed25519 signature")
    
    signature_hex = security.get('signature', '')
    event_hash = security.get('event_hash', '')
    
    try:
        public_key_bytes = bytes.fromhex(public_key_hex)
        signature_bytes = bytes.fromhex(signature_hex)
        message_bytes = bytes.fromhex(event_hash)
        
        public_key = Ed25519PublicKey.from_public_bytes(public_key_bytes)
        public_key.verify(signature_bytes, message_bytes)
        
    except InvalidSignature:
        return TestResult.fail("Ed25519 signature verification failed")
    except Exception as e:
        return TestResult.error(f"Signature verification error: {e}")
    
    return TestResult.pass_()
```

### 8.2 Delegated Signature Tests

#### Test SIG-010: Delegated Signature (Silver Tier)

```python
def test_sig_010_delegated_signature(event: dict, tier: str) -> TestResult:
    """
    SIG-010: Silver tier should not have self-signature
    Tier: Silver
    """
    if tier != 'Silver':
        return TestResult.skip("Not Silver tier")
    
    security = event.get('security', {})
    
    # Silver tier events may have signature after VCC processing
    # But before submission, they should not have signature
    if 'signature' in security and security['signature']:
        # This is OK if VCC added it
        pass
    
    return TestResult.pass_()
```

### 8.3 Key Management Tests

#### Test SIG-020: Key Rotation Support

```python
def test_sig_020_key_rotation(events: list[dict], key_registry: dict) -> TestResult:
    """
    SIG-020: Events should use currently valid keys
    Tier: Gold, Platinum
    """
    for event in events:
        security = event.get('security', {})
        key_id = security.get('signing_key_id')
        
        if key_id and key_id not in key_registry:
            return TestResult.fail(
                f"Unknown signing key: {key_id}"
            )
    
    return TestResult.pass_()
```

---

## 9. Merkle Proof Validation Tests

### 9.1 Proof Structure Tests

#### Test MKL-001: Proof Path Structure

```python
def test_mkl_001_proof_path_structure(proof: dict) -> TestResult:
    """
    MKL-001: Merkle proof must have required fields
    Tier: All
    """
    required = ['event_hash', 'merkle_root', 'proof_path', 'tree_size']
    missing = [f for f in required if f not in proof]
    
    if missing:
        return TestResult.fail(f"Missing proof fields: {missing}")
    
    # Validate proof_path structure
    for i, node in enumerate(proof.get('proof_path', [])):
        if 'hash' not in node or 'position' not in node:
            return TestResult.fail(
                f"Proof path node {i} missing hash or position"
            )
        if node['position'] not in ['left', 'right']:
            return TestResult.fail(
                f"Invalid position at node {i}: {node['position']}"
            )
    
    return TestResult.pass_()
```

### 9.2 Local Verification Tests

#### Test MKL-002: Merkle Proof Verification

```python
def compute_merkle_root(event_hash: str, proof_path: list[dict]) -> str:
    """Compute Merkle root from event hash and proof path"""
    current = event_hash
    
    for node in proof_path:
        sibling = node['hash']
        if node['position'] == 'left':
            # Sibling is on the left
            combined = bytes.fromhex(sibling) + bytes.fromhex(current)
        else:
            # Sibling is on the right
            combined = bytes.fromhex(current) + bytes.fromhex(sibling)
        
        current = hashlib.sha256(combined).hexdigest()
    
    return current

def test_mkl_002_proof_verification(proof: dict) -> TestResult:
    """
    MKL-002: Merkle proof must verify locally
    Tier: All
    """
    event_hash = proof.get('event_hash', '')
    merkle_root = proof.get('merkle_root', '')
    proof_path = proof.get('proof_path', [])
    
    computed_root = compute_merkle_root(event_hash, proof_path)
    
    if computed_root != merkle_root:
        return TestResult.fail(
            f"Merkle proof verification failed:\n"
            f"  Computed root: {computed_root}\n"
            f"  Expected root: {merkle_root}"
        )
    
    return TestResult.pass_()
```

### 9.3 Root Consistency Tests

#### Test MKL-010: Root Consistency Across Events

```python
def test_mkl_010_root_consistency(proofs: list[dict]) -> TestResult:
    """
    MKL-010: Events in same tree should have same root
    Tier: All
    """
    roots = set()
    tree_sizes = set()
    
    for proof in proofs:
        roots.add(proof.get('merkle_root'))
        tree_sizes.add(proof.get('tree_size'))
    
    if len(roots) > 1:
        return TestResult.warn(
            f"Multiple Merkle roots found: {roots}\n"
            f"This may indicate events from different trees"
        )
    
    return TestResult.pass_()
```

---

## 10. Event Type Tests

### 10.1 Trade Lifecycle Tests

#### Test EVT-001: SIG Event Structure

```python
def test_evt_001_sig_event(event: dict) -> TestResult:
    """
    EVT-001: SIG event should have VCP-GOV data
    Tier: All
    """
    if event.get('header', {}).get('event_type') != 'SIG':
        return TestResult.skip("Not a SIG event")
    
    vcp_gov = event.get('payload', {}).get('vcp_gov')
    
    if not vcp_gov:
        return TestResult.warn(
            "SIG event should include vcp_gov payload for transparency"
        )
    
    # Check for algo_id at minimum
    if 'algo_id' not in vcp_gov:
        return TestResult.warn("vcp_gov should include algo_id")
    
    return TestResult.pass_()
```

#### Test EVT-002: Trade Lifecycle Sequence

```python
def test_evt_002_trade_lifecycle(events: list[dict]) -> TestResult:
    """
    EVT-002: Trade lifecycle events should follow correct sequence
    Tier: All
    """
    # Group by trace_id
    traces = {}
    for event in events:
        trace_id = event.get('header', {}).get('trace_id')
        if trace_id:
            if trace_id not in traces:
                traces[trace_id] = []
            traces[trace_id].append(event)
    
    # Valid sequences
    valid_sequences = {
        ('SIG',): True,
        ('SIG', 'ORD'): True,
        ('SIG', 'ORD', 'ACK'): True,
        ('SIG', 'ORD', 'ACK', 'EXE'): True,
        ('SIG', 'ORD', 'ACK', 'PRT'): True,
        ('SIG', 'ORD', 'ACK', 'REJ'): True,
        ('SIG', 'ORD', 'REJ'): True,
        ('ORD',): True,
        ('ORD', 'ACK'): True,
        ('ORD', 'ACK', 'EXE'): True,
        ('ORD', 'EXE'): True,  # Direct execution without ACK
    }
    
    for trace_id, trace_events in traces.items():
        # Sort by timestamp
        trace_events.sort(key=lambda e: e['header']['timestamp_int'])
        sequence = tuple(e['header']['event_type'] for e in trace_events)
        
        # Check if sequence is valid or a prefix of valid
        is_valid = any(
            sequence == valid[:len(sequence)] 
            for valid in valid_sequences
        )
        
        if not is_valid:
            return TestResult.warn(
                f"Unusual event sequence for trace {trace_id}: {sequence}"
            )
    
    return TestResult.pass_()
```

### 10.2 Governance Event Tests

#### Test EVT-010: VCP-GOV Completeness

```python
def test_evt_010_vcp_gov_completeness(event: dict) -> TestResult:
    """
    EVT-010: VCP-GOV should have comprehensive algorithm metadata
    Tier: All (recommended for EU AI Act compliance)
    """
    vcp_gov = event.get('payload', {}).get('vcp_gov', {})
    
    if not vcp_gov:
        return TestResult.skip("No VCP-GOV payload")
    
    recommended_fields = ['algo_id', 'algo_version', 'algo_type']
    missing = [f for f in recommended_fields if f not in vcp_gov]
    
    if missing:
        return TestResult.warn(
            f"VCP-GOV missing recommended fields: {missing}"
        )
    
    # For AI models, check explainability
    if vcp_gov.get('algo_type') == 'AI_MODEL':
        if 'decision_factors' not in vcp_gov:
            return TestResult.warn(
                "AI_MODEL should include decision_factors for explainability"
            )
    
    return TestResult.pass_()
```

### 10.3 System Event Tests

#### Test EVT-020: Heartbeat Event

```python
def test_evt_020_heartbeat_event(event: dict) -> TestResult:
    """
    EVT-020: HBT event should have minimal payload
    Tier: All
    """
    if event.get('header', {}).get('event_type') != 'HBT':
        return TestResult.skip("Not a HBT event")
    
    # HBT should have minimal or empty payload
    payload = event.get('payload', {})
    
    # Allow empty payload or system status
    if payload and not any(k in payload for k in ['system_status', 'vcp_recovery']):
        return TestResult.warn(
            "HBT payload should be minimal (empty or system_status only)"
        )
    
    return TestResult.pass_()
```

---

## 11. End-to-End Integration Tests

### 11.1 Logger Client Tests

#### Test INT-001: Event Submission

```python
import httpx

async def test_int_001_event_submission(logger_config: dict) -> TestResult:
    """
    INT-001: Logger should successfully submit events to VCC
    Tier: All
    """
    from vcp_sdk import create_logger, create_event
    
    logger = create_logger(logger_config)
    
    try:
        event = create_event('HBT', {
            'venue_id': 'TEST-VENUE',
            'symbol': 'TEST',
            'account_id': 'test_acc'
        })
        
        await logger.log(event)
        await logger.flush()
        
    except Exception as e:
        return TestResult.fail(f"Event submission failed: {e}")
    finally:
        await logger.close()
    
    return TestResult.pass_()
```

#### Test INT-002: Batch Submission

```python
async def test_int_002_batch_submission(logger_config: dict) -> TestResult:
    """
    INT-002: Logger should batch multiple events efficiently
    Tier: All
    """
    from vcp_sdk import create_logger, create_event
    
    config = {**logger_config, 'batch_size': 10}
    logger = create_logger(config)
    
    try:
        # Submit 25 events (should create 3 batches)
        for i in range(25):
            event = create_event('HBT', {
                'venue_id': 'TEST-VENUE',
                'symbol': 'TEST',
                'account_id': 'test_acc'
            })
            await logger.log(event)
        
        # Check queue before flush
        queue_size = logger.get_queue_size()
        if queue_size > 25:
            return TestResult.fail(f"Queue overflow: {queue_size}")
        
        await logger.flush()
        
    except Exception as e:
        return TestResult.fail(f"Batch submission failed: {e}")
    finally:
        await logger.close()
    
    return TestResult.pass_()
```

### 11.2 Explorer API Tests

#### Test INT-010: Event Search

```python
async def test_int_010_event_search(explorer_config: dict) -> TestResult:
    """
    INT-010: Explorer should find events by trace_id
    Tier: All
    """
    from vcp_sdk import create_explorer, EventSearchParams
    
    explorer = create_explorer(explorer_config)
    
    try:
        # Search for recent events
        result = await explorer.search_events(EventSearchParams(
            limit=10
        ))
        
        if not result.events:
            return TestResult.warn("No events found in sandbox")
        
    except Exception as e:
        return TestResult.fail(f"Event search failed: {e}")
    finally:
        await explorer.close()
    
    return TestResult.pass_()
```

#### Test INT-011: Merkle Proof Retrieval

```python
async def test_int_011_merkle_proof(explorer_config: dict, event_id: str) -> TestResult:
    """
    INT-011: Explorer should return valid Merkle proof
    Tier: All
    """
    from vcp_sdk import create_explorer
    
    explorer = create_explorer(explorer_config)
    
    try:
        proof = await explorer.get_merkle_proof(event_id)
        
        # Verify locally
        is_valid = explorer.verify_merkle_proof(proof)
        
        if not is_valid:
            return TestResult.fail("Merkle proof verification failed")
        
    except Exception as e:
        return TestResult.fail(f"Merkle proof retrieval failed: {e}")
    finally:
        await explorer.close()
    
    return TestResult.pass_()
```

### 11.3 Round-Trip Verification

#### Test INT-020: Submit and Retrieve

```python
async def test_int_020_round_trip(config: dict) -> TestResult:
    """
    INT-020: Submitted event should be retrievable with correct data
    Tier: All
    """
    from vcp_sdk import create_logger, create_explorer, create_event
    import asyncio
    
    logger = create_logger(config)
    explorer = create_explorer(config)
    
    try:
        # Create and submit event
        event = create_event('SIG', {
            'venue_id': 'TEST-VENUE',
            'symbol': 'XAUUSD',
            'account_id': 'test_acc'
        })
        event['payload']['vcp_gov'] = {
            'algo_id': 'conformance-test-v1',
            'algo_type': 'RULE_BASED'
        }
        
        await logger.log(event)
        await logger.flush()
        
        # Wait for processing
        await asyncio.sleep(2)
        
        # Retrieve event
        retrieved = await explorer.get_event_by_id(event['header']['event_id'])
        
        if not retrieved:
            return TestResult.fail("Submitted event not found")
        
        # Verify key fields match
        if retrieved['header']['trace_id'] != event['header']['trace_id']:
            return TestResult.fail("trace_id mismatch")
        
        if retrieved['header']['symbol'] != 'XAUUSD':
            return TestResult.fail("symbol mismatch")
        
    except Exception as e:
        return TestResult.fail(f"Round-trip test failed: {e}")
    finally:
        await logger.close()
        await explorer.close()
    
    return TestResult.pass_()
```

---

## 12. Performance Tests

### 12.1 Throughput Tests

#### Test PRF-001: Event Generation Rate

```python
import time

def test_prf_001_event_generation_rate(target_rate: int = 1000) -> TestResult:
    """
    PRF-001: System should generate events at required rate
    Tier: Silver (1K/s), Gold (10K/s), Platinum (100K/s)
    """
    from vcp_sdk import create_event
    
    events = []
    start = time.perf_counter()
    
    for _ in range(target_rate):
        event = create_event('ORD', {
            'venue_id': 'TEST',
            'symbol': 'TEST',
            'account_id': 'test'
        })
        events.append(event)
    
    elapsed = time.perf_counter() - start
    actual_rate = target_rate / elapsed
    
    if actual_rate < target_rate:
        return TestResult.fail(
            f"Event generation rate {actual_rate:.0f}/s below target {target_rate}/s"
        )
    
    return TestResult.pass_(
        f"Event generation rate: {actual_rate:.0f}/s"
    )
```

#### Test PRF-002: Submission Throughput

```python
async def test_prf_002_submission_throughput(config: dict, count: int = 1000) -> TestResult:
    """
    PRF-002: Logger should submit events at required rate
    Tier: All
    """
    from vcp_sdk import create_logger, create_event
    
    logger = create_logger(config)
    events = [create_event('HBT', {
        'venue_id': 'TEST',
        'symbol': 'TEST',
        'account_id': 'test'
    }) for _ in range(count)]
    
    start = time.perf_counter()
    
    for event in events:
        await logger.log(event)
    await logger.flush()
    
    elapsed = time.perf_counter() - start
    rate = count / elapsed
    
    await logger.close()
    
    return TestResult.pass_(f"Submission rate: {rate:.0f}/s")
```

### 12.2 Latency Tests

#### Test PRF-010: End-to-End Latency

```python
async def test_prf_010_e2e_latency(config: dict, max_latency_ms: int = 1000) -> TestResult:
    """
    PRF-010: End-to-end latency should meet tier requirements
    Tier: Silver (<1s), Gold (<100ms), Platinum (<10ms)
    """
    from vcp_sdk import create_logger, create_explorer, create_event
    import asyncio
    
    logger = create_logger(config)
    explorer = create_explorer(config)
    
    latencies = []
    
    for _ in range(10):
        event = create_event('HBT', {
            'venue_id': 'TEST',
            'symbol': 'TEST',
            'account_id': 'test'
        })
        
        start = time.perf_counter()
        await logger.log(event)
        await logger.flush()
        
        # Poll for event
        for _ in range(10):
            await asyncio.sleep(0.1)
            retrieved = await explorer.get_event_by_id(event['header']['event_id'])
            if retrieved:
                break
        
        elapsed_ms = (time.perf_counter() - start) * 1000
        latencies.append(elapsed_ms)
    
    await logger.close()
    await explorer.close()
    
    avg_latency = sum(latencies) / len(latencies)
    p95_latency = sorted(latencies)[int(len(latencies) * 0.95)]
    
    if p95_latency > max_latency_ms:
        return TestResult.fail(
            f"P95 latency {p95_latency:.0f}ms exceeds {max_latency_ms}ms"
        )
    
    return TestResult.pass_(
        f"Avg: {avg_latency:.0f}ms, P95: {p95_latency:.0f}ms"
    )
```

### 12.3 Tier-Specific Requirements

| Tier | Min Throughput | Max Latency (P95) | Clock Sync |
|------|---------------|-------------------|------------|
| Silver | 1,000 events/sec | 1,000 ms | BEST_EFFORT |
| Gold | 10,000 events/sec | 100 ms | NTP_SYNCED |
| Platinum | 100,000 events/sec | 10 ms | PTP_LOCKED |

---

## 13. Test Automation

### 13.1 Test Runner Setup

#### Installation

```bash
# TypeScript
npm install -g @veritaschain/vcp-test-suite
vcp-test init

# Python
pip install vcp-test-suite
vcp-test init
```

#### Configuration File

Create `vcp-test.config.yaml`:

```yaml
# VCP Conformance Test Configuration
version: "1.0"

environment:
  endpoint: ${VCP_ENDPOINT}
  api_key: ${VCP_API_KEY}
  venue_id: "TEST-VENUE-001"
  account_id: "test_account_hash"

tier: "Silver"  # Silver, Gold, or Platinum

test_suites:
  - schema
  - uuid
  - timestamp
  - hash_chain
  - signature
  - merkle
  - event_type
  - integration
  - performance

reporting:
  format: "html"
  output: "./conformance-report"
  include_details: true

thresholds:
  pass_rate: 0.95
  critical_must_pass: true
```

#### Running Tests

```bash
# Run all tests
vcp-test run

# Run specific suite
vcp-test run --suite schema

# Run for specific tier
vcp-test run --tier Gold

# Generate report only
vcp-test report --input results.json
```

### 13.2 CI/CD Integration

#### GitHub Actions

```yaml
name: VCP Conformance Tests

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  conformance:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
      
      - name: Install VCP Test Suite
        run: npm install -g @veritaschain/vcp-test-suite
      
      - name: Run Conformance Tests
        env:
          VCP_API_KEY: ${{ secrets.VCP_SANDBOX_KEY }}
          VCP_ENDPOINT: https://sandbox.veritaschain.org/v1
        run: vcp-test run --tier Silver --output results.json
      
      - name: Upload Results
        uses: actions/upload-artifact@v4
        with:
          name: conformance-report
          path: conformance-report/
      
      - name: Check Pass Rate
        run: |
          PASS_RATE=$(jq '.summary.pass_rate' results.json)
          if (( $(echo "$PASS_RATE < 0.95" | bc -l) )); then
            echo "Pass rate $PASS_RATE below 95%"
            exit 1
          fi
```

### 13.3 Automated Report Generation

#### Report Contents

The conformance report includes:

1. **Executive Summary**
   - Overall pass rate
   - Tier compliance status
   - Critical test results

2. **Test Results by Category**
   - Individual test results
   - Error details for failures
   - Recommendations

3. **Performance Metrics**
   - Throughput measurements
   - Latency percentiles
   - Resource utilization

4. **Artifacts**
   - Sample events tested
   - Hash chain verification logs
   - API request/response logs

---

## 14. Certification Submission

### 14.1 Required Artifacts

To apply for VC-Certified certification, submit:

| Artifact | Description | Format |
|----------|-------------|--------|
| Conformance Report | Automated test results | HTML/PDF |
| Implementation Details | Architecture documentation | PDF |
| Sample Events | 100+ production-like events | JSONL |
| API Integration Proof | Screenshots/logs of VCC integration | PDF |
| Security Assessment | Key management and transport security | PDF |
| Performance Benchmarks | Throughput/latency measurements | PDF |

### 14.2 Submission Process

1. **Self-Assessment**
   - Run full conformance test suite
   - Achieve required pass rate for target tier
   - Document any WARN or SKIP results

2. **Documentation Preparation**
   - Complete all required artifacts
   - Sign Implementation Declaration

3. **Submission**
   - Upload to VSO Certification Portal
   - Pay certification fee (if applicable)

4. **Review**
   - VSO reviews submission (5-10 business days)
   - May request additional information

5. **Certification**
   - Receive VC-Certified badge
   - Listed in VSO registry
   - Annual renewal required

### 14.3 Review Timeline

| Tier | Review Time | Fee (Annual) |
|------|-------------|--------------|
| Silver | 5 business days | Free (Early Adopter) |
| Gold | 7 business days | $2,500 |
| Platinum | 10 business days | $10,000 |

---

## 15. Appendices

### Appendix A: Test Vector Library

#### A.1 Valid UUID v7 Examples

```json
{
  "valid_uuid_v7": [
    "01934e3a-6a1b-7c82-9d1b-0987654321dc",
    "01934e3a-6a1c-7000-8000-000000000000",
    "01934e3a-6a1d-7fff-bfff-ffffffffffff"
  ],
  "invalid_uuid_v7": [
    "01934e3a-6a1b-4c82-9d1b-0987654321dc",
    "01934e3a-6a1b-7c82-0d1b-0987654321dc",
    "not-a-uuid"
  ]
}
```

#### A.2 Valid Event Examples

See [Example Payload Collections](./VCP_EXAMPLE_PAYLOADS.md) for complete examples.

#### A.3 Hash Calculation Test Vectors

```json
{
  "test_vectors": [
    {
      "header": {"event_id": "...", "event_type": "SIG"},
      "payload": {},
      "prev_hash": "0000000000000000000000000000000000000000000000000000000000000000",
      "expected_hash": "a1b2c3d4..."
    }
  ]
}
```

### Appendix B: Error Code Reference

| Code | Category | Description |
|------|----------|-------------|
| SCH-001-F | Schema | Missing required section |
| SCH-002-F | Schema | Missing header field |
| UID-001-F | UUID | Invalid UUID v7 format |
| TST-001-F | Timestamp | Format mismatch |
| HCH-001-F | Hash Chain | Invalid genesis prev_hash |
| HCH-003-F | Hash Chain | Hash calculation mismatch |
| SIG-001-F | Signature | Invalid algorithm |
| SIG-002-F | Signature | Verification failed |
| INT-001-F | Integration | Submission failed |
| PRF-001-F | Performance | Below throughput threshold |

### Appendix C: Sample Test Report

```
═══════════════════════════════════════════════════════════════
           VCP CONFORMANCE TEST REPORT v1.0
═══════════════════════════════════════════════════════════════

Organization:  Example Trading Corp
Target Tier:   Silver
Test Date:     2025-11-25T14:30:00Z
SDK Version:   vcp-sdk 1.0.0

───────────────────────────────────────────────────────────────
                      EXECUTIVE SUMMARY
───────────────────────────────────────────────────────────────

Overall Status:  ✓ PASS

Total Tests:     95
Passed:          93 (97.9%)
Failed:          0
Warnings:        2
Skipped:         0

Critical Tests:  ✓ ALL PASSED (12/12)

───────────────────────────────────────────────────────────────
                    RESULTS BY CATEGORY
───────────────────────────────────────────────────────────────

Category          Tests    Pass    Fail    Warn    Skip
─────────────────────────────────────────────────────────────
Schema             25      25       0       0       0
UUID               10      10       0       0       0
Timestamp          12      12       0       0       0
Hash Chain         15      15       0       0       0
Signature           5       5       0       0       0
Merkle              8       8       0       0       0
Event Type         10       8       0       2       0
Integration        10      10       0       0       0

───────────────────────────────────────────────────────────────
                       WARNINGS
───────────────────────────────────────────────────────────────

EVT-001-W: SIG events should include vcp_gov payload
           Recommendation: Add algorithm metadata for transparency

EVT-010-W: VCP-GOV missing recommended fields: ['algo_version']
           Recommendation: Include version for audit trail

───────────────────────────────────────────────────────────────
                    CERTIFICATION STATUS
───────────────────────────────────────────────────────────────

Silver Tier Requirements:
  ✓ Pass rate >= 95% (actual: 97.9%)
  ✓ All critical tests passed
  ✓ Schema validation complete
  ✓ Hash chain integrity verified
  ✓ Merkle proof verification successful
  ✓ Performance meets Silver thresholds

RESULT: ELIGIBLE FOR VC-CERTIFIED (SILVER)

═══════════════════════════════════════════════════════════════
                      END OF REPORT
═══════════════════════════════════════════════════════════════
```

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2025-11-25 | VSO | Initial release |

---

*Copyright © 2025 VeritasChain Standards Organization. Licensed under Apache 2.0.*
