# Use Cases

## UC1: Process a normal market event

### Primary actor
Market-data replay application

### Preconditions
- The system is deployed.
- The portfolio state is available.
- The event payload is valid.

### Trigger
A market-data event is emitted.

### Main flow
1. The system receives the event.
2. The system validates the payload.
3. The decision workload processes the event.
4. The portfolio state is retrieved and updated if required.
5. The system stores the resulting decision.
6. The system records telemetry.

### Postconditions
- A decision record exists.
- Latency can be calculated.
- The event can be traced using its event ID.

### Related requirements
FR1, FR2, FR3, FR4, FR5, FR9

### Related tests
Smoke test, baseline test

---

## UC2: Replay a Fixed Dataset

### Primary actor

Market-data replay application

### Preconditions

* A processed dataset exists.
* The replay configuration is valid.
* The system is running.

### Trigger

A replay experiment is started.

### Main flow

1. The replay application loads the dataset.
2. Events are emitted in the configured order.
3. Events are sent at the configured rate.
4. The system processes each event.
5. Results are stored with the experiment ID.

### Postconditions

* The dataset has been replayed.
* Submitted and completed event counts can be compared.
* Results can be reproduced later.

### Related requirements

FR7, FR10, NFR10

### Related tests

Replay-rate test, reproducibility test

---

## UC3: Handle a Burst of Events

### Primary actor

Load generator

### Preconditions

* The system is deployed.
* Monitoring is enabled.
* A burst workload is configured.

### Trigger

The load generator suddenly increases the event rate.

### Main flow

1. The load generator submits a burst of events.
2. The system accepts or queues the events.
3. Additional capacity is created where supported.
4. Events are processed.
5. Latency, throughput, and backlog are recorded.

### Postconditions

* The system returns to normal operation.
* Burst-handling performance is measured.

### Related requirements

NFR3, NFR5

### Related tests

Spike test, scaling test

---

## UC4: Handle Sustained Load

### Primary actor

Load generator

### Preconditions

* The system is deployed.
* A steady workload is configured.
* Monitoring is enabled.

### Trigger

The load generator submits events continuously.

### Main flow

1. Events are submitted at a fixed rate.
2. The system processes events over a defined period.
3. Resource usage is monitored.
4. Throughput and latency are recorded.
5. Backlog growth is checked.

### Postconditions

* The sustainable event rate is measured.
* Performance degradation can be identified.

### Related requirements

NFR1, NFR2, NFR3, NFR5

### Related tests

Average-load test, stress test, soak test

---

## UC5: Handle a Duplicate Event

### Primary actor

Load generator

### Preconditions

* A valid event has already been processed.
* Duplicate handling is enabled.

### Trigger

The same event ID is submitted again.

### Main flow

1. The system receives the duplicate event.
2. The event ID is checked.
3. The duplicate is ignored or safely recorded.
4. Portfolio state is not updated twice.
5. The duplicate outcome is logged.

### Postconditions

* No unintended repeated decision is applied.
* Duplicate handling is auditable.

### Related requirements

FR8, NFR7

### Related tests

Duplicate-event test

---

## UC6: Reject a Malformed Event

### Primary actor

Load generator

### Preconditions

* The system is running.
* Validation rules are defined.

### Trigger

An invalid event is submitted.

### Main flow

1. The system receives the event.
2. Validation detects missing or invalid fields.
3. The event is rejected.
4. The rejection reason is logged.
5. No decision is created.

### Postconditions

* Invalid data does not affect portfolio state.
* The error can be inspected later.

### Related requirements

FR2, NFR7

### Related tests

Malformed-event test

---

## UC7: Recover After a Component Failure

### Primary actor

Fault-injection script

### Preconditions

* The system is deployed.
* Monitoring is enabled.
* A recoverable failure scenario is defined.

### Trigger

A processing component is stopped or forced to fail.

### Main flow

1. The failure is introduced.
2. The system records errors or retries.
3. Events are queued, retried, or rejected safely.
4. The component becomes available again.
5. Normal processing resumes.
6. Recovery time and event loss are measured.

### Postconditions

* Recovery behavior is recorded.
* Any lost or duplicated events are identified.

### Related requirements

NFR4, NFR6, NFR7

### Related tests

Fault-recovery test

---

## UC8: Drain a Queue Backlog

### Primary actor

Load generator

### Preconditions

* The event-driven architecture is deployed.
* A queue is available.
* Monitoring is enabled.

### Trigger

The incoming event rate temporarily exceeds processing capacity.

### Main flow

1. Events accumulate in the queue.
2. Queue depth and oldest-message age increase.
3. The incoming rate is reduced.
4. The system continues processing queued events.
5. The queue returns to an acceptable level.
6. Drainage time is measured.

### Postconditions

* Backlog-drain performance is recorded.
* No silent event loss occurs.

### Related requirements

NFR3, NFR5, NFR6

### Related tests

Backlog-drain test, spike test

---

## UC9: Process an Event After an Idle Period

### Primary actor

Load generator

### Preconditions

* The serverless architecture is deployed.
* The system has been idle for a defined period.
* Monitoring is enabled.

### Trigger

A new event is submitted after inactivity.

### Main flow

1. The event is submitted.
2. The function environment is initialized if required.
3. The event is processed.
4. The decision is stored.
5. Startup and total latency are recorded.

### Postconditions

* Cold-start behavior is measured.
* Warm and cold execution can be compared.

### Related requirements

NFR1, NFR2

### Related tests

Cold-start test

---

## UC10: Trace an Event Through the Workflow

### Primary actor

Researcher

### Preconditions

* Telemetry is enabled.
* At least one event has been processed.

### Trigger

The researcher selects an event ID.

### Main flow

1. The event ID is searched in the logs.
2. The ingestion timestamp is identified.
3. Processing stages are inspected.
4. The decision record is located.
5. End-to-end and stage-specific latency are calculated.

### Postconditions

* The complete event journey can be reconstructed.
* Missing telemetry can be identified.

### Related requirements

FR9, FR10, NFR9

### Related tests

Observability test
