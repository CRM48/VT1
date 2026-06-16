# System Under Test Definition

## SUT summary
The SUT is the deployed cloud workflow responsible for receiving a simulated
market-data event, applying a portfolio-decision workload, retrieving or
updating portfolio state, storing the resulting decision, and recording
operational telemetry.

## SUT boundary

### Inside the SUT
- Ingestion endpoint, queue, or event bus
- Compute service
- Communication between deployed services
- Portfolio-state interactions
- Decision-record persistence
- Retry and failure-handling behavior
- Cloud scaling behavior
- Relevant observability components

### Outside the SUT
- Historical-data download process
- Load-generator resource consumption
- Live market-data provider
- Real brokerage integration
- User interface
- Investment profitability
- Full agentic AI reasoning quality

## Workload

## Architecture variants

### A0: Local baseline

### A1: Always-on containerized monolith

### A2: Serverless monolithic function

### A3: Event-driven workflow

### A4: Decomposed event-driven services

## Independent variables
- Architecture
- Input rate
- Load pattern
- Workload profile
- CPU or memory allocation
- Warm or cold state
- Queue batch size
- Failure condition

## Dependent variables
- Latency
- Throughput
- Success rate
- Queue depth
- Recovery time
- Cost

## Controlled variables
- Dataset
- Event schema
- Decision logic
- Region
- Experiment duration
- Measurement method