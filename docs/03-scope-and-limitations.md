# Scope and Limitations

## In scope
- Controlled market-data replay
- Simplified portfolio-decision workload
- Cloud architecture comparisons
- Selected infrastructure tuning
- Latency, throughput, scalability, resilience, and cost
- Observability and reproducibility
- Requirements for a future agentic AI system

## Outside scope
- Real-money trading
- Brokerage integration
- Financial profitability claims
- High-frequency trading
- Production-grade cybersecurity certification
- Full regulatory compliance assessment
- Large-scale AI-model training
- Final multi-agent implementation

## Prototype assumptions
- Historical market data acts as a repeatable input workload.
- A deterministic decision workload acts as a surrogate for future agent behavior.
- Experiments use one selected cloud region.
- Architectures use equivalent business logic where possible.

## Limitations
- Cloud performance may vary between regions and time periods.
- A surrogate workload cannot reproduce every characteristic of a real AI agent.
- Preliminary experiments may use limited event rates and durations.
- Cost estimates may not reflect production-scale use.

## Future work
...