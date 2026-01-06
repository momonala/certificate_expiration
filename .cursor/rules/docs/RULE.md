---

description: Documentation standards optimized for both human and LLM context quality and long-term maintainability
globs:

- "**/*"
alwaysApply: true

---

# Documentation Management

- Treat documentation as structured project context, not prose.
- Optimize for both human skim readers and LLM context ingestion.
- Remove outdated or misleading information immediately.

# When to Create or Update README.md

- Create README when starting a project.
- Update README in the same commit as major changes (features, APIs, architecture, etc)
- Do NOT update for minor bug fixes, refactors without behavior change, comments, or patch-level dependency bumps.

# Writing Style

- Limit each section to 1–3 sentences.
- Be direct, factual, and concrete; avoid marketing language.
- Prefer executable examples and commands over abstract descriptions.
- Use informative headings that fully describe the section’s content.
- Remove all template placeholders (e.g., `{{VAR}}`).
- No need to document the API, if one exists

# Required README Structure

See file in root of project: `README.md.template`

# Structural Documentation Rules

- Skip and remove empty sections entirely.
- Use consistent semantic section patterns (what, how, tradeoffs, limitations).
- Reference concrete files, functions, or entry points where relevant.
- Prefer explicit file paths and function names over vague descriptions.

# Decision & Context Docs

Create auxiliary docs when complexity warrants:

- `decision-log.md`: Architectural or technical decisions with rationale.
- `changelog.md`: Human-readable summary of meaningful changes.

Keep these concise and factual; separate *what* from *why*.

# README Update Rules

- Update the “Last Updated” date to today’s date on every meaningful change in ISO formatting
- Ensure examples are copy-paste plausible and reflect current behavior.
- Document tradeoffs and constraints for major design choices.

# Maintenance Rules

- Keep README in sync with the codebase.
- Remove obsolete architecture diagrams or explanations immediately.
- Update diagrams when data flow or system boundaries change.
- Place a single README.md in the project root only.
- Avoid per-directory READMEs unless explicitly required.

# Development Workflow Integration

When generating or modifying code that affects project structure or behavior:

1. Check whether a README exists.
2. Determine if changes meet README update criteria.
3. Update documentation in the same response or commit.
4. Explicitly note when documentation was updated.

