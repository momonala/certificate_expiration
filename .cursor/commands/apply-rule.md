# Apply Rule (Meta-Rule)

## Purpose

Force explicit application of a single, named project rule to guide **code generation, documentation changes** etc, even when automatic rule scoping would not normally apply.

- You want to enforce documentation, architecture, or style constraints explicitly
This meta-rule exists to reduce ambiguity, override default heuristics, and ensure consistent standards in cross-cutting or mixed-context tasks.

## Available Rules

Rules are defined in:

```
.cursor/rules/<rule-name>/RULE.md
```

## Usage

After typing `/apply-rule`, specify exactly one rule name:

Ex:

- `/apply-rule python`
- `/apply-rule swift`
- `/apply-rule webdev`
- `/apply-rule architecture`
- `/apply-rule docs`
- `/apply-rule cleancode`

If multiple standards are required, choose multiple.

## Execution Semantics

When this command is invoked:

1. **Resolve the rule**
  - Load `.cursor/rules/<rule-name>/RULE.md`
  - Treat it as authoritative for the remainder of the task
2. **Override defaults**
  - Ignore conflicting or less-specific rules
  - Ignore file-glob–based auto-application unless explicitly compatible
3. **Apply strictly**
  - All generated code, edits, reviews, and suggestions must conform
  - Existing code touched by the task must be brought into compliance
4. **Surface conflicts**
  - If existing code cannot be made compliant without semantic changes, explain the conflict explicitly
  - Do not silently violate the rule

## Enforcement Guarantees

- No partial application: the rule applies to the entire task
- No silent exceptions: deviations must be justified or rejected
- No dilution: avoid mixing guidance from multiple rules unless one explicitly allows it

## Output Expectations

- Generated output should visibly reflect the rule’s constraints
- Reviews should cite the rule when rejecting or requesting changes
- Documentation updates should align with the rule’s structure and tone

## Notes

- This command is declarative, not advisory
- Prefer explicit failure over implicit non-compliance
- If the rule is underspecified, follow its intent conservatively and note assumptions

