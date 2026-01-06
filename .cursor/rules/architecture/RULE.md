---
description: "Architecture, planning, and feedback practices for technical decision-making"
alwaysApply: true

# Architecture, Planning & Feedback

## Requirements Clarification

- Ask the minimum clarifying questions needed to avoid wrong work.
- Treat requests as underspecified if unclear: objective, definition of done, scope, constraints, environment, or safety/reversibility.
- Ask **1–5** questions that eliminate entire branches of work, not cosmetic details.
- Optimize for fast answers: numbered questions, multiple-choice with defaults, allow compact replies (e.g., `1b 2a`).
- Never assume unstated requirements silently.
- If answering a question wouldn't change code structure, dependencies, or behavior, don't ask it.

## Before Implementation

- Do not run commands, edit files, or create designs that depend on unknowns.
- You may do clearly labeled, low-risk discovery (read configs, docs).
- If asked to proceed without answers, state assumptions as a short numbered list and proceed only after confirmation.
- Once answers are received, restate requirements in **1–3 sentences** (constraints + success criteria) before beginning.

## Architecture Decisions

- Prefer composition over inheritance; favor interfaces/protocols over concrete implementations.
- Design for change: identify what varies and encapsulate it.
- Consider the cost of abstraction; don't abstract prematurely.
- Make dependencies explicit and invert them when appropriate (dependency inversion).
- Design for testability: dependencies should be injectable, side effects should be isolated.
- Document why specific technologies or patterns were chosen, including the rationale and trade-offs.
- List alternatives that were considered and explain why they weren't selected.
- Explicitly explain why common or obvious alternatives were avoided, especially when the choice is non-obvious.

## Planning & Scope

- Start with the smallest change that delivers value.
- Identify migration paths and rollback strategies before major changes.
- Consider incremental delivery over big-bang releases.
- Document architectural decisions and trade-offs, especially when choosing non-obvious solutions.
- When documenting decisions, include alternatives considered and why they were not chosen.
- Plan for failure: design error handling, retries, and degradation strategies.

## Feedback & Iteration

- Seek feedback early on architecture and approach, not just implementation details.
- Present alternatives with trade-offs when multiple reasonable approaches exist.
- When receiving feedback, clarify intent before defending decisions.
- Iterate on the approach if feedback reveals fundamental issues; don't just patch symptoms.

## Examples

### Good: Clarifying requirements
```
Before I start, I need:
1. Scope: Minimal change (default) / Refactor / New feature
2. Performance: Any specific requirements? If none, I'll optimize for maintainability.
3. Backward compatibility: Required? (default: yes)

Reply: defaults (or 1a 2none 3yes)
```

### Good: Stating assumptions
```
Proceeding with these assumptions:
1. Python 3.12+ only (per pyproject.toml)
2. No breaking API changes
3. Using existing database schema

Proceed?
```

### Good: Architecture decision documentation
```
Chose event-driven approach over polling because:
- Lower latency for real-time updates
- Better scalability (decoupled components)
- Trade-off: More complex error handling
```

### Good: Documenting alternatives

```
Why PostgreSQL?
- Need ACID guarantees for financial transactions
- Supports JSON columns for flexible metadata
- Team has deep PostgreSQL expertise

Alternatives considered:
- MongoDB: Better for unstructured data, but lacks strong ACID guarantees
- MySQL: Simpler, but weaker JSON support and less robust for complex queries
- DynamoDB: Great scalability, but adds vendor lock-in and team unfamiliar

Why not Redis as primary store?
- Excellent for caching, but persistence guarantees insufficient for critical data
- Better suited as complementary cache layer (which we're also using)
```

