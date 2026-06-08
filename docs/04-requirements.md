# Requirements

## Requirement-writing conventions
- Each requirement has an ID.
- Each requirement uses "shall".
- Each requirement is testable.
- Provisional thresholds are marked clearly.

## Functional requirements

### FR1: Event ingestion
The system shall ingest a market-data event containing an event ID,
instrument identifier, market timestamp, and price data.

### FR2: Validation
The system shall validate incoming events and reject malformed payloads.

### FR3: Decision processing
The system shall process each valid event using a configurable portfolio-decision
workload.

### FR4: Decision output
The system shall create a portfolio decision for each successfully processed event.

### FR5: Decision storage
The system shall persist the event ID, timestamps, decision, architecture ID,
experiment ID, and status.

### FR6: State handling (maybe)
The system shall retrieve and update simulated portfolio state where required.

### FR7: Replay
The test harness shall replay historical market events at a configurable rate.

### FR8: Duplicate handling
The system shall identify or safely handle duplicated event IDs.

### FR9: Telemetry
The system shall record sufficient telemetry to calculate end-to-end and
stage-specific latency.

### FR10: Experiment identification
Each experimental run shall attach a unique experiment ID to generated events.

## Non-functional requirements

### NFR1: Latency
Define a provisional p95 latency requirement.

### NFR2: Tail latency
Define a provisional p99 latency requirement.

### NFR3: Throughput
Define a target event-processing rate.

### NFR4: Reliability
Define the acceptable completion rate.

### NFR5: Scalability
Describe how the system should behave as load increases.

### NFR6: Recovery
Define an acceptable recovery-time target.

### NFR7: Data correctness
Define the expected handling of duplicates and invalid events.

### NFR8: Cost efficiency
Require cost-per-event reporting.

### NFR9: Observability
Require traceable event processing.

### NFR10: Reproducibility
Require recorded configurations, dataset versions, code versions, and
infrastructure definitions.