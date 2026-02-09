# Specification Structure Overview

This repository follows a **Spec-Driven Development (SDD)** approach.

## Canonical Specs

All hackathon requirements, constraints, and acceptance criteria
are defined in:

**/specs/**

This directory is the **single source of truth** for evaluation.

## Phase References

Each phase directory contains a **specification reference file** that:

- Links to the canonical spec on GitHub
- Contains no requirements or behavior
- Exists for local discoverability and traceability

## Evaluation Guidance

When reviewing a phase submission:

1. Open the relevant phase directory
2. Locate the specification reference file
3. Follow the GitHub link to the canonical spec
4. Evaluate the implementation strictly against that spec
