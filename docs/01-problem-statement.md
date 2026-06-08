# Problem Statement

## Context
What is an agentic AI portfolio-management system? And what is the best configuration - in terms of architecture and infrastructure -  to deploy it to the cloud?

## Problem
Why might architecture/infrastructure affect whether such a system is usable and feasible given the problem context?

## Why the problem matters
Discuss latency, scalability, reliability, resilience, cost, and auditability. Why does this specific thesis project/design require fast handling and scalability, etc.?

## Gap
What is not yet clear in the current market?
- Which deployment model is most appropriate?
- Is serverless suitable for latency-sensitive decisions?
- Does an event-driven design improve resilience enough to justify queueing overhead?
- How should the system be evaluated before adding complex AI agents?

## Proposed response
I will deploy a controlled surrogate workload using several cloud-native architectures. Each architecture will be teste on their appropriateness for the task at hand, in terms of the primary requirements for the task. The requirements will be ranked from lest to most important. We are primarily testing the non-functional requiremnts, as an archotecture is invalid if it can't even meet the functional requirements. A lot of the functional requirements also do not relate to cloud deployment but rather system design.

## Expected contribution
The result is an evidence-based design specification and thesis evaluation plan which gives informed decisions on how best to deploy a financial system to the cloud.