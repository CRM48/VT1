# Evaluation Plan

## Objectives
Explain which research questions the evaluation will address.

## Test environment
- Cloud provider
- Region
- Runtime
- Resource types
- Data snapshot
- Instrumentation
- Deployment method

## Workload profiles

### Light
Describe the simplest workload.

### Medium
Describe the realistic surrogate workload.

### Heavy
Describe the artificial or computationally heavier workload.

## Load patterns

### Smoke
Minimal requests to verify deployment.

### Baseline
Low stable rate.

### Average load
Expected operating rate.

### Stress
Increasing event rate.

### Breakpoint
Continue increasing load until a requirement fails.

### Spike
Sudden load increase.

### Soak
Extended sustained load.

### Cold start
Invoke after an idle period.

### Backlog drain
Create a backlog and measure recovery.

### Fault recovery
Interrupt a component and measure behavior.

### Duplicate event
Send identical event IDs.

## Metrics
List each metric, its units, and how it is calculated.

## Variables
List independent, dependent, and controlled variables.

## Repetition strategy
State the warm-up period, number of measured runs, experiment duration,
and reset procedure.

## Result-processing method
Explain how raw logs become tables and plots.

## Pass/fail criteria
Map tests to provisional non-functional requirements.

## Threats to validity
Describe limitations that may affect interpretation.