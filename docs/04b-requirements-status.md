# Requirements Status Table

## Functional Requirements

| ID   | Requirement                                   | Priority | Status          | Validation                      |
| ---- | --------------------------------------------- | -------- | --------------- | ------------------------------- |
| FR1  | Ingest market-data events                     | Must     | Not implemented | Submit a valid event            |
| FR2  | Validate events and reject invalid data       | Must     | Not implemented | Submit malformed events         |
| FR3  | Process events using a configurable workload  | Must     | Not implemented | Run each workload profile       |
| FR4  | Generate a portfolio decision                 | Must     | Not implemented | Check decision output           |
| FR5  | Store decisions and metadata                  | Must     | Not implemented | Inspect stored record           |
| FR6  | Retrieve and update portfolio state           | Must     | Not implemented | Process a sequence of events    |
| FR7  | Replay historical data at a configurable rate | Must     | Not implemented | Replay events at multiple rates |
| FR8  | Handle duplicate events safely                | Must     | Not implemented | Submit the same event twice     |
| FR9  | Record timestamps and telemetry               | Must     | Not implemented | Inspect logs                    |
| FR10 | Attach an experiment ID to each run           | Must     | Not implemented | Compare two experiment outputs  |

## Non-Functional Requirements

| ID    | Requirement                                                        | Priority | Status                    | Validation                             |
| ----- | ------------------------------------------------------------------ | -------- | ------------------------- | -------------------------------------- |
| NFR1  | Meet the p95 latency target                                        | Should   | Target not defined        | Average-load test                      |
| NFR2  | Meet the p99 latency target                                        | Should   | Target not defined        | Tail-latency test                      |
| NFR3  | Process the target event rate without a growing backlog            | Must     | Target not defined        | Stress test                            |
| NFR4  | Meet the successful-completion-rate target                         | Must     | Target not defined        | Compare submitted and completed events |
| NFR5  | Scale as demand increases                                          | Should   | Requires cloud deployment | Scaling test                           |
| NFR6  | Recover from component failures                                    | Should   | Target not defined        | Fault-recovery test                    |
| NFR7  | Handle invalid, duplicate, delayed, and out-of-order events safely | Must     | Partially specified       | Data-correctness tests                 |
| NFR8  | Report cost per event and cost per hour                            | Should   | Requires cloud deployment | Cost analysis                          |
| NFR9  | Trace each event through the workflow                              | Must     | Not implemented           | Reconstruct one event from logs        |
| NFR10 | Reproduce experiments from saved versions and configurations       | Must     | Partially implemented     | Re-run a saved experiment              |

## Status Legend

| Status                    | Meaning                                         |
| ------------------------- | ----------------------------------------------- |
| Not implemented           | Code or process has not been created            |
| Partially specified       | More design decisions are needed                |
| Partially implemented     | Some supporting work exists                     |
| Target not defined        | A measurable threshold must still be chosen     |
| Requires cloud deployment | Cannot be fully tested locally                  |
| Implemented               | Feature exists but has not been formally tested |
| Validated locally         | Passed a local test                             |
| Validated in cloud        | Passed a cloud experiment                       |
