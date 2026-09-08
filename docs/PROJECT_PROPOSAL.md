# Project Proposal and Objectives

## Title

**DecoyAI: Explainable Local Cyber-Deception Honeypot System**

## Problem Statement

Beginners need a safe way to understand how defensive decoy services collect
and transform interaction data into security intelligence. Internet-exposed
honeypots introduce operational, privacy, and legal risks. DecoyAI therefore
provides a reproducible localhost laboratory for studying the complete pipeline.

## Aim

Design and evaluate a controlled cyber-deception system that records safe
laboratory interactions, explains suspicious behavior, summarizes activity, and
visualizes findings without exposing a service outside the host computer.

## Objectives

1. Implement a controlled fake service restricted to `127.0.0.1`.
2. Record timestamped, sanitized interaction previews in SQLite.
3. Classify behavior using transparent rules and risk scores.
4. Calculate totals, unique sources, categories, high-risk events, and top sources.
5. Present statistics and recent activity on a local web dashboard.
6. Prevent command execution, credential validation, and automatic retaliation.
7. Document ethical, privacy, authorization, and legal boundaries.
8. Evaluate classification against labeled synthetic laboratory data.
9. Test safety controls, storage, classification, and evaluation behavior.

## Methodology

The project follows a defensive engineering lifecycle: define safety boundaries,
design normalized events, implement collection and rules, persist data, build
visualizations, simulate controlled interactions, evaluate expected labels, and
document limitations.

## Success Criteria

- Both services reject non-loopback bind addresses.
- No submitted content is executed.
- Each interaction receives a UTC timestamp, category, risk score, and reason.
- Dashboard statistics match stored events.
- Automated tests pass.
- Evaluation accuracy on the supplied labeled dataset is at least 80%.

## Future Research

After instructor approval, future work could compare rules with an offline
machine-learning classifier using a properly documented public dataset. Any
network exposure would require separate authorization, isolation, monitoring,
data-governance review, and institutional approval.
