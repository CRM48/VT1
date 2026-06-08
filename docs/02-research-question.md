# Research Questions

## Primary research question
How do cloud-native architectural patterns and selected infrastructure
configurations affect the operational performance of a simplified
portfolio-decision workflow?

## Potential sub-questions

### RQ1: Latency
How does the deployment model affect end-to-end and tail latency?

### RQ2: Scalability
How does each architecture respond as the incoming event rate increases?

### RQ3: Reliability and resilience
How does each architecture behave during overload, retries, duplicate events,
and recoverable component failures?

### RQ4: Serverless behavior
How significant are cold starts, concurrency behavior, and provisioned-capacity
trade-offs for the workload?

### RQ5: Event-driven design
Does an asynchronous queue improve resilience and scalability enough to justify
its added complexity and queueing delay?

### RQ6: Cost
How does the operational cost vary between architecture types and load levels?

### RQ7: Thesis recommendation
Which architecture should form the basis of the future agentic AI thesis system?

## Mapping table
| Research Question | Metrics | Relevant Experiments |
| ----------------- | ------- | -------------------- |
| RQ1 | p50, p95, p99 latency | Baseline, average load, cold start |
| RQ2 | Throughput, backlog, scale-out delay| Stress, breakpoint, spike |
| RQ3 | Success rate, retries, recovery time | Fault injection, duplicate tests |
| RQ4 | Cold-start frequency and delay | Idle-state invocation tests |
| RQ5 | Queue-wait time and backlog drainage | Event-driven experiments |
| RQ6 | Cost per n events and hourly cost | All measure cloud runs |
| RQ7 | Everything combine | Final comparison |