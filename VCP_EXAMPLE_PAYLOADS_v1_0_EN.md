# VeritasChain Protocol Example Payload Collections v1.0

**Document ID:** VSO-EXAMPLES-001  
**Status:** Release Candidate  
**Version:** 1.0.0  
**Date:** 2025-11-25  
**Maintainer:** VeritasChain Standards Organization (VSO)  
**License:** Apache 2.0

---

## Abstract

This document provides a comprehensive collection of example VCP event payloads for implementers, integrators, and QA engineers. These examples demonstrate correct VCP v1.0 event structure across various trading scenarios, including successful trades, rejections, risk controls, and AI governance events.

All examples are production-ready and can be used directly for testing, demonstration, and development purposes.

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Event Structure Reference](#2-event-structure-reference)
3. [Trade Lifecycle Examples](#3-trade-lifecycle-examples)
   - 3.1 [Scenario A: Complete SIG→ORD→ACK→EXE](#31-scenario-a-complete-sig→ord→ack→exe)
   - 3.2 [Scenario B: Partial Fill (PRT→EXE)](#32-scenario-b-partial-fill-prt→exe)
   - 3.3 [Scenario C: Order Rejection (REJ)](#33-scenario-c-order-rejection-rej)
   - 3.4 [Scenario D: Order Cancellation (CXL)](#34-scenario-d-order-cancellation-cxl)
   - 3.5 [Scenario E: Order Modification (MOD)](#35-scenario-e-order-modification-mod)
4. [Risk Management Examples](#4-risk-management-examples)
   - 4.1 [VCP-RISK: Real-time Risk Snapshot](#41-vcp-risk-real-time-risk-snapshot)
   - 4.2 [VCP-RISK: Risk Control Triggered](#42-vcp-risk-risk-control-triggered)
   - 4.3 [News Embargo Trading Halt](#43-news-embargo-trading-halt)
5. [Algorithm Governance Examples](#5-algorithm-governance-examples)
   - 5.1 [VCP-GOV: Rule-Based Algorithm](#51-vcp-gov-rule-based-algorithm)
   - 5.2 [VCP-GOV: AI/ML Model with SHAP](#52-vcp-gov-aiml-model-with-shap)
   - 5.3 [VCP-GOV: Hybrid Algorithm](#53-vcp-gov-hybrid-algorithm)
   - 5.4 [Algorithm Update Event (ALG)](#54-algorithm-update-event-alg)
6. [System Events Examples](#6-system-events-examples)
   - 6.1 [Heartbeat (HBT)](#61-heartbeat-hbt)
   - 6.2 [Error Event (ERR)](#62-error-event-err)
   - 6.3 [Recovery Event (REC)](#63-recovery-event-rec)
   - 6.4 [Sync Event (SNC)](#64-sync-event-snc)
7. [Multi-Asset Examples](#7-multi-asset-examples)
   - 7.1 [Forex (EURUSD)](#71-forex-eurusd)
   - 7.2 [Precious Metals (XAUUSD)](#72-precious-metals-xauusd)
   - 7.3 [Crypto (BTCUSDT)](#73-crypto-btcusdt)
   - 7.4 [Futures (ES)](#74-futures-es)
8. [JSONL Collections](#8-jsonl-collections)
9. [Validation Utilities](#9-validation-utilities)

---

## 1. Introduction

### 1.1 Purpose

These examples serve multiple purposes:

1. **Implementation Reference**: Developers can copy and adapt these patterns
2. **Testing**: QA teams can use these as test fixtures
3. **Documentation**: Technical writers can reference concrete examples
4. **Sales Demos**: Business teams can show realistic VCP event data

### 1.2 Conventions

All examples follow these conventions:

- **UUIDs**: Use valid UUID v7 format (timestamp-ordered)
- **Timestamps**: Use realistic 2025 timestamps
- **Numeric Values**: All financial values are **strings**
- **Hashes**: Use realistic SHA-256 hex strings (64 characters)
- **Symbols**: Use standard market symbols (XAUUSD, EURUSD, etc.)

### 1.3 How to Use

```bash
# Copy a single example
cat examples/sig_ord_exe_xauusd.json | jq .

# Validate against schema
vcp-test validate-schema examples/sig_ord_exe_xauusd.json

# Submit to sandbox
vcp-test submit examples/sig_ord_exe_xauusd.jsonl --endpoint sandbox
```

---

## 2. Event Structure Reference

### 2.1 Minimal Valid Event

The absolute minimum required fields for a valid VCP event:

```json
{
  "header": {
    "event_id": "01934e3a-6a1b-7c82-9d1b-0987654321dc",
    "trace_id": "01934e3a-6a1a-7000-8000-000000000001",
    "timestamp_int": "1732492800000000000",
    "timestamp_iso": "2025-11-25T00:00:00.000Z",
    "event_type": "HBT",
    "event_type_code": 98,
    "timestamp_precision": "MILLISECOND",
    "clock_sync_status": "BEST_EFFORT",
    "hash_algo": "SHA256",
    "venue_id": "TEST-VENUE",
    "symbol": "TEST",
    "account_id": "acc_test123"
  },
  "payload": {},
  "security": {
    "event_hash": "a1b2c3d4e5f6789012345678901234567890123456789012345678901234abcd",
    "prev_hash": "0000000000000000000000000000000000000000000000000000000000000000"
  }
}
```

### 2.2 Field Types Summary

| Field | Type | Example |
|-------|------|---------|
| `event_id` | UUID v7 string | `"01934e3a-6a1b-7c82-..."` |
| `trace_id` | UUID v7 string | `"01934e3a-6a1a-7000-..."` |
| `timestamp_int` | string (ns) | `"1732492800000000000"` |
| `timestamp_iso` | ISO 8601 string | `"2025-11-25T00:00:00.000Z"` |
| `event_type_code` | integer | `4` |
| `price` | string | `"2650.50"` |
| `quantity` | string | `"1.00"` |
| `event_hash` | hex string (64 chars) | `"a1b2c3d4..."` |

---

## 3. Trade Lifecycle Examples

### 3.1 Scenario A: Complete SIG→ORD→ACK→EXE

A complete successful trade lifecycle for XAUUSD (Gold):

#### Event 1: SIG (Signal Generation)

```json
{
  "header": {
    "event_id": "01934e3a-6a1a-7c82-9d1b-000000000001",
    "trace_id": "01934e3a-6a1a-7000-8000-aaaaaaaaaaaa",
    "timestamp_int": "1732536000000000000",
    "timestamp_iso": "2025-11-25T12:00:00.000Z",
    "event_type": "SIG",
    "event_type_code": 1,
    "timestamp_precision": "MILLISECOND",
    "clock_sync_status": "NTP_SYNCED",
    "hash_algo": "SHA256",
    "venue_id": "MT5-BROKER-ALPHA",
    "symbol": "XAUUSD",
    "account_id": "acc_7f83b162a9c4e521"
  },
  "payload": {
    "vcp_gov": {
      "algo_id": "gold-momentum-v2.3",
      "algo_version": "2.3.1",
      "algo_type": "HYBRID",
      "model_hash": "sha256:9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08",
      "risk_classification": "MEDIUM",
      "last_approval_by": "risk-committee@example.com",
      "approval_timestamp_int": "1732449600000000000",
      "decision_factors": {
        "features": [
          {
            "name": "rsi_14",
            "value": "28.5",
            "weight": "0.35",
            "contribution": "0.12"
          },
          {
            "name": "ma_cross_50_200",
            "value": "1",
            "weight": "0.25",
            "contribution": "0.08"
          },
          {
            "name": "volume_surge",
            "value": "2.3",
            "weight": "0.20",
            "contribution": "0.06"
          },
          {
            "name": "support_proximity",
            "value": "0.002",
            "weight": "0.20",
            "contribution": "0.05"
          }
        ],
        "confidence_score": "0.87",
        "explainability_method": "SHAP"
      }
    }
  },
  "security": {
    "event_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    "prev_hash": "0000000000000000000000000000000000000000000000000000000000000000"
  }
}
```

#### Event 2: ORD (Order Submission)

```json
{
  "header": {
    "event_id": "01934e3a-6a1b-7c82-9d1b-000000000002",
    "trace_id": "01934e3a-6a1a-7000-8000-aaaaaaaaaaaa",
    "timestamp_int": "1732536000050000000",
    "timestamp_iso": "2025-11-25T12:00:00.050Z",
    "event_type": "ORD",
    "event_type_code": 2,
    "timestamp_precision": "MILLISECOND",
    "clock_sync_status": "NTP_SYNCED",
    "hash_algo": "SHA256",
    "venue_id": "MT5-BROKER-ALPHA",
    "symbol": "XAUUSD",
    "account_id": "acc_7f83b162a9c4e521"
  },
  "payload": {
    "trade_data": {
      "order_id": "12345678",
      "side": "BUY",
      "order_type": "MARKET",
      "price": "2650.50",
      "quantity": "1.00",
      "currency": "USD",
      "time_in_force": "IOC"
    }
  },
  "security": {
    "event_hash": "d7a8fbb307d7809469ca9abcb0082e4f8d5651e46d3cdb762d02d0bf37c9e592",
    "prev_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
  }
}
```

#### Event 3: ACK (Order Acknowledgment)

```json
{
  "header": {
    "event_id": "01934e3a-6a1c-7c82-9d1b-000000000003",
    "trace_id": "01934e3a-6a1a-7000-8000-aaaaaaaaaaaa",
    "timestamp_int": "1732536000120000000",
    "timestamp_iso": "2025-11-25T12:00:00.120Z",
    "event_type": "ACK",
    "event_type_code": 3,
    "timestamp_precision": "MILLISECOND",
    "clock_sync_status": "NTP_SYNCED",
    "hash_algo": "SHA256",
    "venue_id": "MT5-BROKER-ALPHA",
    "symbol": "XAUUSD",
    "account_id": "acc_7f83b162a9c4e521"
  },
  "payload": {
    "trade_data": {
      "order_id": "12345678",
      "broker_order_id": "BRK-2025112500001234",
      "side": "BUY",
      "order_type": "MARKET",
      "price": "2650.50",
      "quantity": "1.00"
    }
  },
  "security": {
    "event_hash": "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824",
    "prev_hash": "d7a8fbb307d7809469ca9abcb0082e4f8d5651e46d3cdb762d02d0bf37c9e592"
  }
}
```

#### Event 4: EXE (Full Execution)

```json
{
  "header": {
    "event_id": "01934e3a-6a1d-7c82-9d1b-000000000004",
    "trace_id": "01934e3a-6a1a-7000-8000-aaaaaaaaaaaa",
    "timestamp_int": "1732536000180000000",
    "timestamp_iso": "2025-11-25T12:00:00.180Z",
    "event_type": "EXE",
    "event_type_code": 4,
    "timestamp_precision": "MILLISECOND",
    "clock_sync_status": "NTP_SYNCED",
    "hash_algo": "SHA256",
    "venue_id": "MT5-BROKER-ALPHA",
    "symbol": "XAUUSD",
    "account_id": "acc_7f83b162a9c4e521"
  },
  "payload": {
    "trade_data": {
      "order_id": "12345678",
      "broker_order_id": "BRK-2025112500001234",
      "exchange_order_id": "EX-98765432",
      "side": "BUY",
      "execution_price": "2650.55",
      "executed_qty": "1.00",
      "remaining_qty": "0.00",
      "currency": "USD",
      "commission": "7.50",
      "slippage": "0.05"
    }
  },
  "security": {
    "event_hash": "ef2d127de37b942baad06145e54b0c619a1f22327b2ebbcfbec78f5564afe39d",
    "prev_hash": "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"
  }
}
```

### 3.2 Scenario B: Partial Fill (PRT→EXE)

Large order filled in two parts:

#### Event 1: ORD (Large Order)

```json
{
  "header": {
    "event_id": "01934e3b-0001-7c82-9d1b-bbbbbbbbbb01",
    "trace_id": "01934e3b-0000-7000-8000-bbbbbbbbbbbb",
    "timestamp_int": "1732536060000000000",
    "timestamp_iso": "2025-11-25T12:01:00.000Z",
    "event_type": "ORD",
    "event_type_code": 2,
    "timestamp_precision": "MILLISECOND",
    "clock_sync_status": "NTP_SYNCED",
    "hash_algo": "SHA256",
    "venue_id": "MT5-BROKER-ALPHA",
    "symbol": "EURUSD",
    "account_id": "acc_7f83b162a9c4e521"
  },
  "payload": {
    "trade_data": {
      "order_id": "22334455",
      "side": "SELL",
      "order_type": "LIMIT",
      "price": "1.08500",
      "quantity": "100.00",
      "currency": "USD",
      "time_in_force": "GTC"
    }
  },
  "security": {
    "event_hash": "9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08",
    "prev_hash": "0000000000000000000000000000000000000000000000000000000000000000"
  }
}
```

#### Event 2: PRT (Partial Fill - 60 lots)

```json
{
  "header": {
    "event_id": "01934e3b-0002-7c82-9d1b-bbbbbbbbbb02",
    "trace_id": "01934e3b-0000-7000-8000-bbbbbbbbbbbb",
    "timestamp_int": "1732536120000000000",
    "timestamp_iso": "2025-11-25T12:02:00.000Z",
    "event_type": "PRT",
    "event_type_code": 5,
    "timestamp_precision": "MILLISECOND",
    "clock_sync_status": "NTP_SYNCED",
    "hash_algo": "SHA256",
    "venue_id": "MT5-BROKER-ALPHA",
    "symbol": "EURUSD",
    "account_id": "acc_7f83b162a9c4e521"
  },
  "payload": {
    "trade_data": {
      "order_id": "22334455",
      "broker_order_id": "BRK-2025112500002234",
      "side": "SELL",
      "execution_price": "1.08502",
      "executed_qty": "60.00",
      "remaining_qty": "40.00",
      "commission": "4.50"
    }
  },
  "security": {
    "event_hash": "a9993e364706816aba3e25717850c26c9cd0d89d5a6d31e5b0b5f8c8c8c8c8c8",
    "prev_hash": "9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08"
  }
}
```

#### Event 3: EXE (Final Fill - 40 lots)

```json
{
  "header": {
    "event_id": "01934e3b-0003-7c82-9d1b-bbbbbbbbbb03",
    "trace_id": "01934e3b-0000-7000-8000-bbbbbbbbbbbb",
    "timestamp_int": "1732536180000000000",
    "timestamp_iso": "2025-11-25T12:03:00.000Z",
    "event_type": "EXE",
    "event_type_code": 4,
    "timestamp_precision": "MILLISECOND",
    "clock_sync_status": "NTP_SYNCED",
    "hash_algo": "SHA256",
    "venue_id": "MT5-BROKER-ALPHA",
    "symbol": "EURUSD",
    "account_id": "acc_7f83b162a9c4e521"
  },
  "payload": {
    "trade_data": {
      "order_id": "22334455",
      "broker_order_id": "BRK-2025112500002234",
      "side": "SELL",
      "execution_price": "1.08498",
      "executed_qty": "40.00",
      "remaining_qty": "0.00",
      "commission": "3.00"
    }
  },
  "security": {
    "event_hash": "b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0",
    "prev_hash": "a9993e364706816aba3e25717850c26c9cd0d89d5a6d31e5b0b5f8c8c8c8c8c8"
  }
}
```

### 3.3 Scenario C: Order Rejection (REJ)

Order rejected due to insufficient margin:

#### Event 1: ORD (Order Attempt)

```json
{
  "header": {
    "event_id": "01934e3c-0001-7c82-9d1b-cccccccccc01",
    "trace_id": "01934e3c-0000-7000-8000-cccccccccccc",
    "timestamp_int": "1732536240000000000",
    "timestamp_iso": "2025-11-25T12:04:00.000Z",
    "event_type": "ORD",
    "event_type_code": 2,
    "timestamp_precision": "MILLISECOND",
    "clock_sync_status": "NTP_SYNCED",
    "hash_algo": "SHA256",
    "venue_id": "MT5-BROKER-ALPHA",
    "symbol": "XAUUSD",
    "account_id": "acc_7f83b162a9c4e521"
  },
  "payload": {
    "trade_data": {
      "order_id": "33445566",
      "side": "BUY",
      "order_type": "MARKET",
      "price": "2651.00",
      "quantity": "50.00"
    }
  },
  "security": {
    "event_hash": "c1c1c1c1c1c1c1c1c1c1c1c1c1c1c1c1c1c1c1c1c1c1c1c1c1c1c1c1c1c1c1c1",
    "prev_hash": "0000000000000000000000000000000000000000000000000000000000000000"
  }
}
```

#### Event 2: REJ (Rejection)

```json
{
  "header": {
    "event_id": "01934e3c-0002-7c82-9d1b-cccccccccc02",
    "trace_id": "01934e3c-0000-7000-8000-cccccccccccc",
    "timestamp_int": "1732536240100000000",
    "timestamp_iso": "2025-11-25T12:04:00.100Z",
    "event_type": "REJ",
    "event_type_code": 6,
    "timestamp_precision": "MILLISECOND",
    "clock_sync_status": "NTP_SYNCED",
    "hash_algo": "SHA256",
    "venue_id": "MT5-BROKER-ALPHA",
    "symbol": "XAUUSD",
    "account_id": "acc_7f83b162a9c4e521"
  },
  "payload": {
    "trade_data": {
      "order_id": "33445566",
      "side": "BUY",
      "reject_reason": "INSUFFICIENT_MARGIN",
      "price": "2651.00",
      "quantity": "50.00"
    }
  },
  "security": {
    "event_hash": "d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2",
    "prev_hash": "c1c1c1c1c1c1c1c1c1c1c1c1c1c1c1c1c1c1c1c1c1c1c1c1c1c1c1c1c1c1c1c1"
  }
}
```

### 3.4 Scenario D: Order Cancellation (CXL)

User cancels a pending limit order:

#### Event 1: ORD (Limit Order)

```json
{
  "header": {
    "event_id": "01934e3d-0001-7c82-9d1b-dddddddddd01",
    "trace_id": "01934e3d-0000-7000-8000-dddddddddddd",
    "timestamp_int": "1732536300000000000",
    "timestamp_iso": "2025-11-25T12:05:00.000Z",
    "event_type": "ORD",
    "event_type_code": 2,
    "timestamp_precision": "MILLISECOND",
    "clock_sync_status": "NTP_SYNCED",
    "hash_algo": "SHA256",
    "venue_id": "MT5-BROKER-ALPHA",
    "symbol": "GBPUSD",
    "account_id": "acc_7f83b162a9c4e521"
  },
  "payload": {
    "trade_data": {
      "order_id": "44556677",
      "side": "BUY",
      "order_type": "LIMIT",
      "price": "1.26000",
      "quantity": "5.00",
      "time_in_force": "GTC"
    }
  },
  "security": {
    "event_hash": "e3e3e3e3e3e3e3e3e3e3e3e3e3e3e3e3e3e3e3e3e3e3e3e3e3e3e3e3e3e3e3e3",
    "prev_hash": "0000000000000000000000000000000000000000000000000000000000000000"
  }
}
```

#### Event 2: ACK (Order Acknowledged)

```json
{
  "header": {
    "event_id": "01934e3d-0002-7c82-9d1b-dddddddddd02",
    "trace_id": "01934e3d-0000-7000-8000-dddddddddddd",
    "timestamp_int": "1732536300100000000",
    "timestamp_iso": "2025-11-25T12:05:00.100Z",
    "event_type": "ACK",
    "event_type_code": 3,
    "timestamp_precision": "MILLISECOND",
    "clock_sync_status": "NTP_SYNCED",
    "hash_algo": "SHA256",
    "venue_id": "MT5-BROKER-ALPHA",
    "symbol": "GBPUSD",
    "account_id": "acc_7f83b162a9c4e521"
  },
  "payload": {
    "trade_data": {
      "order_id": "44556677",
      "broker_order_id": "BRK-2025112500004456"
    }
  },
  "security": {
    "event_hash": "f4f4f4f4f4f4f4f4f4f4f4f4f4f4f4f4f4f4f4f4f4f4f4f4f4f4f4f4f4f4f4f4",
    "prev_hash": "e3e3e3e3e3e3e3e3e3e3e3e3e3e3e3e3e3e3e3e3e3e3e3e3e3e3e3e3e3e3e3e3"
  }
}
```

#### Event 3: CXL (Cancellation)

```json
{
  "header": {
    "event_id": "01934e3d-0003-7c82-9d1b-dddddddddd03",
    "trace_id": "01934e3d-0000-7000-8000-dddddddddddd",
    "timestamp_int": "1732536600000000000",
    "timestamp_iso": "2025-11-25T12:10:00.000Z",
    "event_type": "CXL",
    "event_type_code": 7,
    "timestamp_precision": "MILLISECOND",
    "clock_sync_status": "NTP_SYNCED",
    "hash_algo": "SHA256",
    "venue_id": "MT5-BROKER-ALPHA",
    "symbol": "GBPUSD",
    "account_id": "acc_7f83b162a9c4e521"
  },
  "payload": {
    "trade_data": {
      "order_id": "44556677",
      "broker_order_id": "BRK-2025112500004456",
      "remaining_qty": "5.00"
    }
  },
  "security": {
    "event_hash": "a5a5a5a5a5a5a5a5a5a5a5a5a5a5a5a5a5a5a5a5a5a5a5a5a5a5a5a5a5a5a5a5",
    "prev_hash": "f4f4f4f4f4f4f4f4f4f4f4f4f4f4f4f4f4f4f4f4f4f4f4f4f4f4f4f4f4f4f4f4"
  }
}
```

### 3.5 Scenario E: Order Modification (MOD)

Modifying a limit order's price:

```json
{
  "header": {
    "event_id": "01934e3e-0001-7c82-9d1b-eeeeeeeeee01",
    "trace_id": "01934e3e-0000-7000-8000-eeeeeeeeeeee",
    "timestamp_int": "1732536660000000000",
    "timestamp_iso": "2025-11-25T12:11:00.000Z",
    "event_type": "MOD",
    "event_type_code": 8,
    "timestamp_precision": "MILLISECOND",
    "clock_sync_status": "NTP_SYNCED",
    "hash_algo": "SHA256",
    "venue_id": "MT5-BROKER-ALPHA",
    "symbol": "USDJPY",
    "account_id": "acc_7f83b162a9c4e521"
  },
  "payload": {
    "trade_data": {
      "order_id": "55667788",
      "broker_order_id": "BRK-2025112500005566",
      "side": "SELL",
      "order_type": "LIMIT",
      "price": "150.500",
      "quantity": "10.00"
    }
  },
  "security": {
    "event_hash": "b6b6b6b6b6b6b6b6b6b6b6b6b6b6b6b6b6b6b6b6b6b6b6b6b6b6b6b6b6b6b6b6",
    "prev_hash": "0000000000000000000000000000000000000000000000000000000000000000"
  }
}
```

---

## 4. Risk Management Examples

### 4.1 VCP-RISK: Real-time Risk Snapshot

Periodic risk snapshot during trading:

```json
{
  "header": {
    "event_id": "01934e40-0001-7c82-9d1b-111111111101",
    "trace_id": "01934e40-0000-7000-8000-111111111111",
    "timestamp_int": "1732536720000000000",
    "timestamp_iso": "2025-11-25T12:12:00.000Z",
    "event_type": "RSK",
    "event_type_code": 21,
    "timestamp_precision": "MILLISECOND",
    "clock_sync_status": "NTP_SYNCED",
    "hash_algo": "SHA256",
    "venue_id": "MT5-BROKER-ALPHA",
    "symbol": "PORTFOLIO",
    "account_id": "acc_7f83b162a9c4e521"
  },
  "payload": {
    "vcp_risk": {
      "snapshot": {
        "total_equity": "125000.00",
        "margin_used": "45000.00",
        "margin_available": "80000.00",
        "margin_level_pct": "277.78",
        "open_positions": "5",
        "unrealized_pnl": "2350.00",
        "realized_pnl_today": "1500.00",
        "max_drawdown_pct": "8.5",
        "var_1d_95": "3200.00",
        "var_5d_95": "7150.00",
        "sharpe_ratio_30d": "1.85",
        "exposure_xauusd": "3.00",
        "exposure_eurusd": "10.00",
        "exposure_gbpusd": "5.00"
      }
    }
  },
  "security": {
    "event_hash": "c7c7c7c7c7c7c7c7c7c7c7c7c7c7c7c7c7c7c7c7c7c7c7c7c7c7c7c7c7c7c7c7",
    "prev_hash": "0000000000000000000000000000000000000000000000000000000000000000"
  }
}
```

### 4.2 VCP-RISK: Risk Control Triggered

Risk limit breach causing automatic position reduction:

```json
{
  "header": {
    "event_id": "01934e41-0001-7c82-9d1b-222222222201",
    "trace_id": "01934e41-0000-7000-8000-222222222222",
    "timestamp_int": "1732536780000000000",
    "timestamp_iso": "2025-11-25T12:13:00.000Z",
    "event_type": "RSK",
    "event_type_code": 21,
    "timestamp_precision": "MILLISECOND",
    "clock_sync_status": "NTP_SYNCED",
    "hash_algo": "SHA256",
    "venue_id": "MT5-BROKER-ALPHA",
    "symbol": "XAUUSD",
    "account_id": "acc_7f83b162a9c4e521"
  },
  "payload": {
    "vcp_risk": {
      "snapshot": {
        "total_equity": "118000.00",
        "margin_level_pct": "115.00",
        "unrealized_pnl": "-7000.00",
        "max_drawdown_pct": "12.8"
      },
      "triggered_controls": [
        {
          "control_name": "MAX_DRAWDOWN_LIMIT",
          "trigger_value": "12.8",
          "action": "REDUCE",
          "timestamp_int": "1732536780000000000"
        },
        {
          "control_name": "MARGIN_CALL_WARNING",
          "trigger_value": "115.00",
          "action": "ALERT",
          "timestamp_int": "1732536780000000000"
        }
      ]
    }
  },
  "security": {
    "event_hash": "d8d8d8d8d8d8d8d8d8d8d8d8d8d8d8d8d8d8d8d8d8d8d8d8d8d8d8d8d8d8d8d8",
    "prev_hash": "0000000000000000000000000000000000000000000000000000000000000000"
  }
}
```

### 4.3 News Embargo Trading Halt

Algorithm halts trading before major news event:

```json
{
  "header": {
    "event_id": "01934e42-0001-7c82-9d1b-333333333301",
    "trace_id": "01934e42-0000-7000-8000-333333333333",
    "timestamp_int": "1732545600000000000",
    "timestamp_iso": "2025-11-25T14:40:00.000Z",
    "event_type": "RSK",
    "event_type_code": 21,
    "timestamp_precision": "MILLISECOND",
    "clock_sync_status": "NTP_SYNCED",
    "hash_algo": "SHA256",
    "venue_id": "MT5-BROKER-ALPHA",
    "symbol": "EURUSD",
    "account_id": "acc_7f83b162a9c4e521"
  },
  "payload": {
    "vcp_risk": {
      "snapshot": {
        "trading_enabled": "false",
        "halt_reason": "NEWS_EMBARGO",
        "next_allowed_trading": "1732548600000000000"
      },
      "triggered_controls": [
        {
          "control_name": "NEWS_EMBARGO_15MIN",
          "trigger_value": "ECB_RATE_DECISION",
          "action": "HALT",
          "timestamp_int": "1732545600000000000"
        }
      ]
    },
    "vcp_gov": {
      "algo_id": "fx-momentum-v3",
      "decision_factors": {
        "features": [
          {
            "name": "news_calendar_event",
            "value": "ECB_RATE_DECISION",
            "contribution": "-1.00"
          },
          {
            "name": "embargo_window_minutes",
            "value": "15",
            "contribution": "0.00"
          }
        ],
        "confidence_score": "0.00",
        "explainability_method": "RULE_TRACE"
      }
    }
  },
  "security": {
    "event_hash": "e9e9e9e9e9e9e9e9e9e9e9e9e9e9e9e9e9e9e9e9e9e9e9e9e9e9e9e9e9e9e9e9",
    "prev_hash": "0000000000000000000000000000000000000000000000000000000000000000"
  }
}
```

---

## 5. Algorithm Governance Examples

### 5.1 VCP-GOV: Rule-Based Algorithm

Simple moving average crossover strategy:

```json
{
  "header": {
    "event_id": "01934e50-0001-7c82-9d1b-444444444401",
    "trace_id": "01934e50-0000-7000-8000-444444444444",
    "timestamp_int": "1732536840000000000",
    "timestamp_iso": "2025-11-25T12:14:00.000Z",
    "event_type": "SIG",
    "event_type_code": 1,
    "timestamp_precision": "MILLISECOND",
    "clock_sync_status": "NTP_SYNCED",
    "hash_algo": "SHA256",
    "venue_id": "MT5-BROKER-ALPHA",
    "symbol": "EURUSD",
    "account_id": "acc_7f83b162a9c4e521"
  },
  "payload": {
    "vcp_gov": {
      "algo_id": "ma-crossover-v1",
      "algo_version": "1.0.0",
      "algo_type": "RULE_BASED",
      "risk_classification": "LOW",
      "last_approval_by": "trading-desk@example.com",
      "approval_timestamp_int": "1732363200000000000",
      "testing_record_link": "https://internal.example.com/testing/ma-crossover-v1",
      "decision_factors": {
        "features": [
          {
            "name": "ma_fast_20",
            "value": "1.08520"
          },
          {
            "name": "ma_slow_50",
            "value": "1.08480"
          },
          {
            "name": "crossover_direction",
            "value": "BULLISH"
          },
          {
            "name": "signal_strength",
            "value": "0.0040"
          }
        ],
        "confidence_score": "1.00",
        "explainability_method": "RULE_TRACE"
      }
    }
  },
  "security": {
    "event_hash": "f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0",
    "prev_hash": "0000000000000000000000000000000000000000000000000000000000000000"
  }
}
```

### 5.2 VCP-GOV: AI/ML Model with SHAP

Neural network with SHAP explainability (EU AI Act compliant):

```json
{
  "header": {
    "event_id": "01934e51-0001-7c82-9d1b-555555555501",
    "trace_id": "01934e51-0000-7000-8000-555555555555",
    "timestamp_int": "1732536900000000000",
    "timestamp_iso": "2025-11-25T12:15:00.000Z",
    "event_type": "SIG",
    "event_type_code": 1,
    "timestamp_precision": "MILLISECOND",
    "clock_sync_status": "NTP_SYNCED",
    "hash_algo": "SHA256",
    "venue_id": "MT5-BROKER-ALPHA",
    "symbol": "XAUUSD",
    "account_id": "acc_7f83b162a9c4e521"
  },
  "payload": {
    "vcp_gov": {
      "algo_id": "neural-gold-predictor-v3",
      "algo_version": "3.2.1",
      "algo_type": "AI_MODEL",
      "model_hash": "sha256:7d865e959b2466918c9863afca942d0fb89d7c9ac0c99bafc3749504ded97730",
      "risk_classification": "HIGH",
      "last_approval_by": "ai-governance-committee@example.com",
      "approval_timestamp_int": "1732276800000000000",
      "testing_record_link": "https://mlops.example.com/models/neural-gold-predictor-v3/validation",
      "decision_factors": {
        "features": [
          {
            "name": "price_momentum_5m",
            "value": "0.0023",
            "weight": "0.18",
            "contribution": "0.15"
          },
          {
            "name": "rsi_14",
            "value": "32.5",
            "weight": "0.15",
            "contribution": "0.12"
          },
          {
            "name": "volume_ratio",
            "value": "1.85",
            "weight": "0.12",
            "contribution": "0.10"
          },
          {
            "name": "usd_index_correlation",
            "value": "-0.82",
            "weight": "0.14",
            "contribution": "0.11"
          },
          {
            "name": "vix_level",
            "value": "18.5",
            "weight": "0.10",
            "contribution": "0.08"
          },
          {
            "name": "bond_yield_10y",
            "value": "4.25",
            "weight": "0.08",
            "contribution": "0.06"
          },
          {
            "name": "gold_etf_flows",
            "value": "125.5",
            "weight": "0.08",
            "contribution": "0.07"
          },
          {
            "name": "central_bank_sentiment",
            "value": "0.65",
            "weight": "0.07",
            "contribution": "0.05"
          },
          {
            "name": "technical_support_distance",
            "value": "0.003",
            "weight": "0.08",
            "contribution": "0.06"
          }
        ],
        "confidence_score": "0.89",
        "explainability_method": "SHAP"
      }
    }
  },
  "security": {
    "event_hash": "a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1",
    "prev_hash": "0000000000000000000000000000000000000000000000000000000000000000"
  }
}
```

### 5.3 VCP-GOV: Hybrid Algorithm

Combination of rule-based filters and ML prediction:

```json
{
  "header": {
    "event_id": "01934e52-0001-7c82-9d1b-666666666601",
    "trace_id": "01934e52-0000-7000-8000-666666666666",
    "timestamp_int": "1732536960000000000",
    "timestamp_iso": "2025-11-25T12:16:00.000Z",
    "event_type": "SIG",
    "event_type_code": 1,
    "timestamp_precision": "MILLISECOND",
    "clock_sync_status": "NTP_SYNCED",
    "hash_algo": "SHA256",
    "venue_id": "MT5-BROKER-ALPHA",
    "symbol": "BTCUSDT",
    "account_id": "acc_7f83b162a9c4e521"
  },
  "payload": {
    "vcp_gov": {
      "algo_id": "crypto-hybrid-v2",
      "algo_version": "2.1.0",
      "algo_type": "HYBRID",
      "model_hash": "sha256:2c26b46b68ffc68ff99b453c1d30413413422d706483bfa0f98a5e886266e7ae",
      "risk_classification": "HIGH",
      "decision_factors": {
        "features": [
          {
            "name": "rule:trend_filter",
            "value": "PASS",
            "contribution": "0.00"
          },
          {
            "name": "rule:volatility_filter",
            "value": "PASS",
            "contribution": "0.00"
          },
          {
            "name": "rule:liquidity_check",
            "value": "PASS",
            "contribution": "0.00"
          },
          {
            "name": "ml:direction_probability",
            "value": "0.72",
            "weight": "0.60",
            "contribution": "0.43"
          },
          {
            "name": "ml:volatility_forecast",
            "value": "0.015",
            "weight": "0.20",
            "contribution": "0.12"
          },
          {
            "name": "ml:optimal_entry",
            "value": "97850.00",
            "weight": "0.20",
            "contribution": "0.10"
          }
        ],
        "confidence_score": "0.72",
        "explainability_method": "SHAP"
      }
    }
  },
  "security": {
    "event_hash": "b2b2b2b2b2b2b2b2b2b2b2b2b2b2b2b2b2b2b2b2b2b2b2b2b2b2b2b2b2b2b2b2",
    "prev_hash": "0000000000000000000000000000000000000000000000000000000000000000"
  }
}
```

### 5.4 Algorithm Update Event (ALG)

Recording algorithm version update:

```json
{
  "header": {
    "event_id": "01934e53-0001-7c82-9d1b-777777777701",
    "trace_id": "01934e53-0000-7000-8000-777777777777",
    "timestamp_int": "1732537020000000000",
    "timestamp_iso": "2025-11-25T12:17:00.000Z",
    "event_type": "ALG",
    "event_type_code": 20,
    "timestamp_precision": "MILLISECOND",
    "clock_sync_status": "NTP_SYNCED",
    "hash_algo": "SHA256",
    "venue_id": "MT5-BROKER-ALPHA",
    "symbol": "SYSTEM",
    "account_id": "acc_7f83b162a9c4e521"
  },
  "payload": {
    "vcp_gov": {
      "algo_id": "gold-momentum-v2.3",
      "algo_version": "2.3.2",
      "algo_type": "HYBRID",
      "model_hash": "sha256:fcde2b2edba56bf408601fb721fe9b5c338d10ee429ea04fae5511b68fbf8fb9",
      "risk_classification": "MEDIUM",
      "last_approval_by": "risk-committee@example.com",
      "approval_timestamp_int": "1732536900000000000",
      "testing_record_link": "https://internal.example.com/testing/gold-momentum-v2.3.2"
    }
  },
  "security": {
    "event_hash": "c3c3c3c3c3c3c3c3c3c3c3c3c3c3c3c3c3c3c3c3c3c3c3c3c3c3c3c3c3c3c3c3",
    "prev_hash": "0000000000000000000000000000000000000000000000000000000000000000"
  }
}
```

---

## 6. System Events Examples

### 6.1 Heartbeat (HBT)

Regular system health check:

```json
{
  "header": {
    "event_id": "01934e60-0001-7c82-9d1b-888888888801",
    "trace_id": "01934e60-0000-7000-8000-888888888888",
    "timestamp_int": "1732537080000000000",
    "timestamp_iso": "2025-11-25T12:18:00.000Z",
    "event_type": "HBT",
    "event_type_code": 98,
    "timestamp_precision": "MILLISECOND",
    "clock_sync_status": "NTP_SYNCED",
    "hash_algo": "SHA256",
    "venue_id": "MT5-BROKER-ALPHA",
    "symbol": "HEARTBEAT",
    "account_id": "acc_7f83b162a9c4e521"
  },
  "payload": {},
  "security": {
    "event_hash": "d4d4d4d4d4d4d4d4d4d4d4d4d4d4d4d4d4d4d4d4d4d4d4d4d4d4d4d4d4d4d4d4",
    "prev_hash": "0000000000000000000000000000000000000000000000000000000000000000"
  }
}
```

### 6.2 Error Event (ERR)

Recording an error condition:

```json
{
  "header": {
    "event_id": "01934e61-0001-7c82-9d1b-999999999901",
    "trace_id": "01934e61-0000-7000-8000-999999999999",
    "timestamp_int": "1732537140000000000",
    "timestamp_iso": "2025-11-25T12:19:00.000Z",
    "event_type": "ERR",
    "event_type_code": 99,
    "timestamp_precision": "MILLISECOND",
    "clock_sync_status": "NTP_SYNCED",
    "hash_algo": "SHA256",
    "venue_id": "MT5-BROKER-ALPHA",
    "symbol": "XAUUSD",
    "account_id": "acc_7f83b162a9c4e521"
  },
  "payload": {
    "trade_data": {
      "order_id": "99887766"
    },
    "vcp_recovery": {
      "error_code": "BROKER_TIMEOUT",
      "error_message": "Order submission timeout after 5000ms",
      "recoverable": true,
      "retry_count": 2
    }
  },
  "security": {
    "event_hash": "e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5",
    "prev_hash": "0000000000000000000000000000000000000000000000000000000000000000"
  }
}
```

### 6.3 Recovery Event (REC)

Connection restored after disconnection:

```json
{
  "header": {
    "event_id": "01934e62-0001-7c82-9d1b-aaaaaaaaaa01",
    "trace_id": "01934e62-0000-7000-8000-aaaaaaaaaaaa",
    "timestamp_int": "1732537200000000000",
    "timestamp_iso": "2025-11-25T12:20:00.000Z",
    "event_type": "REC",
    "event_type_code": 100,
    "timestamp_precision": "MILLISECOND",
    "clock_sync_status": "NTP_SYNCED",
    "hash_algo": "SHA256",
    "venue_id": "MT5-BROKER-ALPHA",
    "symbol": "SYSTEM",
    "account_id": "acc_7f83b162a9c4e521"
  },
  "payload": {
    "vcp_recovery": {
      "reason": "CONNECTION_RESTORED",
      "cached_event_count": 15,
      "cache_start_timestamp": "1732536900000000000",
      "cache_end_timestamp": "1732537180000000000",
      "gap_detection": {
        "expected_count": 15,
        "actual_count": 15,
        "missing_event_ids": []
      }
    }
  },
  "security": {
    "event_hash": "f6f6f6f6f6f6f6f6f6f6f6f6f6f6f6f6f6f6f6f6f6f6f6f6f6f6f6f6f6f6f6f6",
    "prev_hash": "0000000000000000000000000000000000000000000000000000000000000000"
  }
}
```

### 6.4 Sync Event (SNC)

Manual synchronization after system restart:

```json
{
  "header": {
    "event_id": "01934e63-0001-7c82-9d1b-bbbbbbbbbb01",
    "trace_id": "01934e63-0000-7000-8000-bbbbbbbbbbbb",
    "timestamp_int": "1732537260000000000",
    "timestamp_iso": "2025-11-25T12:21:00.000Z",
    "event_type": "SNC",
    "event_type_code": 101,
    "timestamp_precision": "MILLISECOND",
    "clock_sync_status": "NTP_SYNCED",
    "hash_algo": "SHA256",
    "venue_id": "MT5-BROKER-ALPHA",
    "symbol": "SYSTEM",
    "account_id": "acc_7f83b162a9c4e521"
  },
  "payload": {
    "vcp_recovery": {
      "reason": "SYSTEM_RESTART",
      "last_known_event_id": "01934e60-0001-7c82-9d1b-888888888801",
      "sync_status": "COMPLETE"
    }
  },
  "security": {
    "event_hash": "a7a7a7a7a7a7a7a7a7a7a7a7a7a7a7a7a7a7a7a7a7a7a7a7a7a7a7a7a7a7a7a7",
    "prev_hash": "0000000000000000000000000000000000000000000000000000000000000000"
  }
}
```

---

## 7. Multi-Asset Examples

### 7.1 Forex (EURUSD)

Standard forex trade with pip-based pricing:

```json
{
  "header": {
    "event_id": "01934e70-0001-7c82-9d1b-cccccccccc01",
    "trace_id": "01934e70-0000-7000-8000-cccccccccccc",
    "timestamp_int": "1732537320000000000",
    "timestamp_iso": "2025-11-25T12:22:00.000Z",
    "event_type": "EXE",
    "event_type_code": 4,
    "timestamp_precision": "MILLISECOND",
    "clock_sync_status": "NTP_SYNCED",
    "hash_algo": "SHA256",
    "venue_id": "MT5-BROKER-ALPHA",
    "symbol": "EURUSD",
    "account_id": "acc_7f83b162a9c4e521"
  },
  "payload": {
    "trade_data": {
      "order_id": "FX001",
      "broker_order_id": "BRK-FX-001",
      "side": "BUY",
      "order_type": "MARKET",
      "execution_price": "1.08523",
      "executed_qty": "100000.00",
      "currency": "EUR",
      "commission": "7.00",
      "slippage": "0.00003"
    }
  },
  "security": {
    "event_hash": "b8b8b8b8b8b8b8b8b8b8b8b8b8b8b8b8b8b8b8b8b8b8b8b8b8b8b8b8b8b8b8b8",
    "prev_hash": "0000000000000000000000000000000000000000000000000000000000000000"
  }
}
```

### 7.2 Precious Metals (XAUUSD)

Gold trade with larger tick size:

```json
{
  "header": {
    "event_id": "01934e71-0001-7c82-9d1b-dddddddddd01",
    "trace_id": "01934e71-0000-7000-8000-dddddddddddd",
    "timestamp_int": "1732537380000000000",
    "timestamp_iso": "2025-11-25T12:23:00.000Z",
    "event_type": "EXE",
    "event_type_code": 4,
    "timestamp_precision": "MILLISECOND",
    "clock_sync_status": "NTP_SYNCED",
    "hash_algo": "SHA256",
    "venue_id": "MT5-BROKER-ALPHA",
    "symbol": "XAUUSD",
    "account_id": "acc_7f83b162a9c4e521"
  },
  "payload": {
    "trade_data": {
      "order_id": "GOLD001",
      "broker_order_id": "BRK-GOLD-001",
      "side": "SELL",
      "order_type": "LIMIT",
      "execution_price": "2652.35",
      "executed_qty": "5.00",
      "currency": "USD",
      "commission": "37.50",
      "slippage": "-0.15"
    }
  },
  "security": {
    "event_hash": "c9c9c9c9c9c9c9c9c9c9c9c9c9c9c9c9c9c9c9c9c9c9c9c9c9c9c9c9c9c9c9c9",
    "prev_hash": "0000000000000000000000000000000000000000000000000000000000000000"
  }
}
```

### 7.3 Crypto (BTCUSDT)

Cryptocurrency trade:

```json
{
  "header": {
    "event_id": "01934e72-0001-7c82-9d1b-eeeeeeeeee01",
    "trace_id": "01934e72-0000-7000-8000-eeeeeeeeeeee",
    "timestamp_int": "1732537440000000000",
    "timestamp_iso": "2025-11-25T12:24:00.000Z",
    "event_type": "EXE",
    "event_type_code": 4,
    "timestamp_precision": "MILLISECOND",
    "clock_sync_status": "NTP_SYNCED",
    "hash_algo": "SHA256",
    "venue_id": "BINANCE-SPOT",
    "symbol": "BTCUSDT",
    "account_id": "acc_7f83b162a9c4e521"
  },
  "payload": {
    "trade_data": {
      "order_id": "BTC001",
      "exchange_order_id": "BN-1234567890",
      "side": "BUY",
      "order_type": "LIMIT",
      "execution_price": "97852.50",
      "executed_qty": "0.25000000",
      "currency": "USDT",
      "commission": "24.46"
    }
  },
  "security": {
    "event_hash": "d0d0d0d0d0d0d0d0d0d0d0d0d0d0d0d0d0d0d0d0d0d0d0d0d0d0d0d0d0d0d0d0",
    "prev_hash": "0000000000000000000000000000000000000000000000000000000000000000"
  }
}
```

### 7.4 Futures (ES)

E-mini S&P 500 futures trade:

```json
{
  "header": {
    "event_id": "01934e73-0001-7c82-9d1b-ffffffffffff01",
    "trace_id": "01934e73-0000-7000-8000-ffffffffffff",
    "timestamp_int": "1732537500000000000",
    "timestamp_iso": "2025-11-25T12:25:00.000Z",
    "event_type": "EXE",
    "event_type_code": 4,
    "timestamp_precision": "MICROSECOND",
    "clock_sync_status": "NTP_SYNCED",
    "hash_algo": "SHA256",
    "venue_id": "CME-GLOBEX",
    "symbol": "ESZ25",
    "account_id": "acc_7f83b162a9c4e521"
  },
  "payload": {
    "trade_data": {
      "order_id": "ES001",
      "exchange_order_id": "CME-9876543210",
      "side": "BUY",
      "order_type": "LIMIT",
      "execution_price": "6025.25",
      "executed_qty": "2",
      "currency": "USD",
      "commission": "4.20"
    }
  },
  "security": {
    "event_hash": "e1e1e1e1e1e1e1e1e1e1e1e1e1e1e1e1e1e1e1e1e1e1e1e1e1e1e1e1e1e1e1e1",
    "prev_hash": "0000000000000000000000000000000000000000000000000000000000000000"
  }
}
```

---

## 8. JSONL Collections

### 8.1 Complete Trade Lifecycle (sig_ord_ack_exe_xauusd.jsonl)

```jsonl
{"header":{"event_id":"01934e3a-6a1a-7c82-9d1b-000000000001","trace_id":"01934e3a-6a1a-7000-8000-aaaaaaaaaaaa","timestamp_int":"1732536000000000000","timestamp_iso":"2025-11-25T12:00:00.000Z","event_type":"SIG","event_type_code":1,"timestamp_precision":"MILLISECOND","clock_sync_status":"NTP_SYNCED","hash_algo":"SHA256","venue_id":"MT5-BROKER-ALPHA","symbol":"XAUUSD","account_id":"acc_7f83b162a9c4e521"},"payload":{"vcp_gov":{"algo_id":"gold-momentum-v2.3","algo_version":"2.3.1","algo_type":"HYBRID","decision_factors":{"confidence_score":"0.87","explainability_method":"SHAP"}}},"security":{"event_hash":"e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855","prev_hash":"0000000000000000000000000000000000000000000000000000000000000000"}}
{"header":{"event_id":"01934e3a-6a1b-7c82-9d1b-000000000002","trace_id":"01934e3a-6a1a-7000-8000-aaaaaaaaaaaa","timestamp_int":"1732536000050000000","timestamp_iso":"2025-11-25T12:00:00.050Z","event_type":"ORD","event_type_code":2,"timestamp_precision":"MILLISECOND","clock_sync_status":"NTP_SYNCED","hash_algo":"SHA256","venue_id":"MT5-BROKER-ALPHA","symbol":"XAUUSD","account_id":"acc_7f83b162a9c4e521"},"payload":{"trade_data":{"order_id":"12345678","side":"BUY","order_type":"MARKET","price":"2650.50","quantity":"1.00"}},"security":{"event_hash":"d7a8fbb307d7809469ca9abcb0082e4f8d5651e46d3cdb762d02d0bf37c9e592","prev_hash":"e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"}}
{"header":{"event_id":"01934e3a-6a1c-7c82-9d1b-000000000003","trace_id":"01934e3a-6a1a-7000-8000-aaaaaaaaaaaa","timestamp_int":"1732536000120000000","timestamp_iso":"2025-11-25T12:00:00.120Z","event_type":"ACK","event_type_code":3,"timestamp_precision":"MILLISECOND","clock_sync_status":"NTP_SYNCED","hash_algo":"SHA256","venue_id":"MT5-BROKER-ALPHA","symbol":"XAUUSD","account_id":"acc_7f83b162a9c4e521"},"payload":{"trade_data":{"order_id":"12345678","broker_order_id":"BRK-2025112500001234"}},"security":{"event_hash":"2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824","prev_hash":"d7a8fbb307d7809469ca9abcb0082e4f8d5651e46d3cdb762d02d0bf37c9e592"}}
{"header":{"event_id":"01934e3a-6a1d-7c82-9d1b-000000000004","trace_id":"01934e3a-6a1a-7000-8000-aaaaaaaaaaaa","timestamp_int":"1732536000180000000","timestamp_iso":"2025-11-25T12:00:00.180Z","event_type":"EXE","event_type_code":4,"timestamp_precision":"MILLISECOND","clock_sync_status":"NTP_SYNCED","hash_algo":"SHA256","venue_id":"MT5-BROKER-ALPHA","symbol":"XAUUSD","account_id":"acc_7f83b162a9c4e521"},"payload":{"trade_data":{"order_id":"12345678","broker_order_id":"BRK-2025112500001234","execution_price":"2650.55","executed_qty":"1.00","commission":"7.50","slippage":"0.05"}},"security":{"event_hash":"ef2d127de37b942baad06145e54b0c619a1f22327b2ebbcfbec78f5564afe39d","prev_hash":"2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"}}
```

### 8.2 Rejection Scenario (ord_rej.jsonl)

```jsonl
{"header":{"event_id":"01934e3c-0001-7c82-9d1b-cccccccccc01","trace_id":"01934e3c-0000-7000-8000-cccccccccccc","timestamp_int":"1732536240000000000","timestamp_iso":"2025-11-25T12:04:00.000Z","event_type":"ORD","event_type_code":2,"timestamp_precision":"MILLISECOND","clock_sync_status":"NTP_SYNCED","hash_algo":"SHA256","venue_id":"MT5-BROKER-ALPHA","symbol":"XAUUSD","account_id":"acc_7f83b162a9c4e521"},"payload":{"trade_data":{"order_id":"33445566","side":"BUY","order_type":"MARKET","price":"2651.00","quantity":"50.00"}},"security":{"event_hash":"c1c1c1c1c1c1c1c1c1c1c1c1c1c1c1c1c1c1c1c1c1c1c1c1c1c1c1c1c1c1c1c1","prev_hash":"0000000000000000000000000000000000000000000000000000000000000000"}}
{"header":{"event_id":"01934e3c-0002-7c82-9d1b-cccccccccc02","trace_id":"01934e3c-0000-7000-8000-cccccccccccc","timestamp_int":"1732536240100000000","timestamp_iso":"2025-11-25T12:04:00.100Z","event_type":"REJ","event_type_code":6,"timestamp_precision":"MILLISECOND","clock_sync_status":"NTP_SYNCED","hash_algo":"SHA256","venue_id":"MT5-BROKER-ALPHA","symbol":"XAUUSD","account_id":"acc_7f83b162a9c4e521"},"payload":{"trade_data":{"order_id":"33445566","reject_reason":"INSUFFICIENT_MARGIN"}},"security":{"event_hash":"d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2","prev_hash":"c1c1c1c1c1c1c1c1c1c1c1c1c1c1c1c1c1c1c1c1c1c1c1c1c1c1c1c1c1c1c1c1"}}
```

### 8.3 Risk Control Triggered (risk_triggered.jsonl)

```jsonl
{"header":{"event_id":"01934e41-0001-7c82-9d1b-222222222201","trace_id":"01934e41-0000-7000-8000-222222222222","timestamp_int":"1732536780000000000","timestamp_iso":"2025-11-25T12:13:00.000Z","event_type":"RSK","event_type_code":21,"timestamp_precision":"MILLISECOND","clock_sync_status":"NTP_SYNCED","hash_algo":"SHA256","venue_id":"MT5-BROKER-ALPHA","symbol":"XAUUSD","account_id":"acc_7f83b162a9c4e521"},"payload":{"vcp_risk":{"snapshot":{"total_equity":"118000.00","margin_level_pct":"115.00","unrealized_pnl":"-7000.00","max_drawdown_pct":"12.8"},"triggered_controls":[{"control_name":"MAX_DRAWDOWN_LIMIT","trigger_value":"12.8","action":"REDUCE","timestamp_int":"1732536780000000000"},{"control_name":"MARGIN_CALL_WARNING","trigger_value":"115.00","action":"ALERT","timestamp_int":"1732536780000000000"}]}},"security":{"event_hash":"d8d8d8d8d8d8d8d8d8d8d8d8d8d8d8d8d8d8d8d8d8d8d8d8d8d8d8d8d8d8d8d8","prev_hash":"0000000000000000000000000000000000000000000000000000000000000000"}}
```

---

## 9. Validation Utilities

### 9.1 Quick Validation Script (Python)

```python
#!/usr/bin/env python3
"""
VCP Event Validator
Usage: python validate_event.py event.json
"""

import json
import re
import sys
from typing import Dict, List, Tuple

UUID_V7_PATTERN = re.compile(
    r'^[0-9a-f]{8}-[0-9a-f]{4}-7[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$',
    re.IGNORECASE
)

VALID_EVENT_TYPES = {
    'SIG': 1, 'ORD': 2, 'ACK': 3, 'EXE': 4, 'PRT': 5,
    'REJ': 6, 'CXL': 7, 'MOD': 8, 'CLS': 9,
    'ALG': 20, 'RSK': 21, 'AUD': 22,
    'HBT': 98, 'ERR': 99, 'REC': 100, 'SNC': 101
}

FINANCIAL_FIELDS = [
    'price', 'quantity', 'executed_qty', 'remaining_qty',
    'execution_price', 'commission', 'slippage'
]

def validate_event(event: Dict) -> List[Tuple[str, str]]:
    """Validate a VCP event and return list of (severity, message) tuples."""
    errors = []
    warnings = []
    
    # Check structure
    for section in ['header', 'payload', 'security']:
        if section not in event:
            errors.append(('ERROR', f'Missing required section: {section}'))
    
    if errors:
        return errors
    
    header = event['header']
    security = event['security']
    
    # Validate event_id (UUID v7)
    event_id = header.get('event_id', '')
    if not UUID_V7_PATTERN.match(event_id):
        errors.append(('ERROR', f'Invalid UUID v7 format for event_id: {event_id}'))
    
    # Validate trace_id (UUID v7)
    trace_id = header.get('trace_id', '')
    if not UUID_V7_PATTERN.match(trace_id):
        errors.append(('ERROR', f'Invalid UUID v7 format for trace_id: {trace_id}'))
    
    # Validate timestamp_int is string
    ts_int = header.get('timestamp_int')
    if not isinstance(ts_int, str):
        errors.append(('ERROR', f'timestamp_int must be string, got {type(ts_int).__name__}'))
    
    # Validate event_type and event_type_code match
    event_type = header.get('event_type')
    event_type_code = header.get('event_type_code')
    if event_type in VALID_EVENT_TYPES:
        if event_type_code != VALID_EVENT_TYPES[event_type]:
            errors.append(('ERROR', 
                f'event_type_code mismatch: {event_type} should be {VALID_EVENT_TYPES[event_type]}, got {event_type_code}'))
    else:
        errors.append(('ERROR', f'Unknown event_type: {event_type}'))
    
    # Validate financial fields are strings
    trade_data = event.get('payload', {}).get('trade_data', {})
    for field in FINANCIAL_FIELDS:
        if field in trade_data and not isinstance(trade_data[field], str):
            errors.append(('ERROR', 
                f'Financial field {field} must be string, got {type(trade_data[field]).__name__}'))
    
    # Validate hashes
    event_hash = security.get('event_hash', '')
    prev_hash = security.get('prev_hash', '')
    
    if len(event_hash) != 64:
        errors.append(('ERROR', f'event_hash must be 64 chars, got {len(event_hash)}'))
    if len(prev_hash) != 64:
        errors.append(('ERROR', f'prev_hash must be 64 chars, got {len(prev_hash)}'))
    
    # Warnings
    if event_type == 'SIG' and 'vcp_gov' not in event.get('payload', {}):
        warnings.append(('WARN', 'SIG event should include vcp_gov payload'))
    
    return errors + warnings

def main():
    if len(sys.argv) < 2:
        print('Usage: python validate_event.py event.json')
        sys.exit(1)
    
    with open(sys.argv[1], 'r') as f:
        event = json.load(f)
    
    results = validate_event(event)
    
    if not results:
        print('✓ Event is valid')
        sys.exit(0)
    
    has_errors = False
    for severity, message in results:
        if severity == 'ERROR':
            print(f'✗ {message}')
            has_errors = True
        else:
            print(f'⚠ {message}')
    
    sys.exit(1 if has_errors else 0)

if __name__ == '__main__':
    main()
```

### 9.2 Batch Validation Script

```bash
#!/bin/bash
# validate_all.sh - Validate all JSONL files in a directory

for file in examples/*.jsonl; do
    echo "Validating $file..."
    while IFS= read -r line; do
        echo "$line" | python validate_event.py /dev/stdin
    done < "$file"
done
```

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2025-11-25 | VSO | Initial release |

---

*Copyright © 2025 VeritasChain Standards Organization. Licensed under Apache 2.0.*
