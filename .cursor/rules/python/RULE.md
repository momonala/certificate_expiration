---
description: "Python coding standards and best practices for modern Python 3.12+ development"
globs: ["*.py"]
alwaysApply: true
---


# Python Basics - Coding Standards

## Type Hints

- Prefer built-in type hints: `list[str]` over `List[str]`, `dict[str, int]` over `Dict[str, int]`.
- Use union syntax `str | None` instead of `Optional[str]`.
- Avoid the `typing` module unless needed for `Protocol`, `TypeVar`, or `Generic`.

## Docstrings

- One-line docstrings for simple functions: `"""Return the user's name."""`
- Google-style docstrings for non-trivial functions:
  ```python
  """Parse uptime from systemctl status output.

  Args:
      status_text: Raw status output from systemctl.
      
  Returns:
      Parsed uptime string or None if not found.
  """
  ```

## Error Handling

- Fail loudly. Avoid broad `except` clauses; catch specific exceptions.
- Don't swallow exceptions silently. Let real errors surface.
- Prefer `raise` over returning error codes or None for exceptional cases.

## Side Effects & State

- Don't mutate inputs or external state unless explicitly documented.
- Avoid implicit reliance on global state or environment variables.
- Use context managers for resource management.

## Data Structures

- Prefer `dataclasses` for structured data with minimal behavior.
- Use `@dataclass(frozen=True)` for immutable data.

## Logging

- Log at system boundaries and failure points, not inside tight loops.
- Never log secrets, passwords, or sensitive user data.
- Emojis are acceptable for quick visual traceability in logs.

## Configuration

- Avoid magic numbers and strings.
- Prefer explicit configuration over hard-coded values.
- High-level module globals are acceptable when scoped to a single file.

## Databases

- Always use proper database transactions.
- Ensure resources (connections, sessions, cursors) are correctly scoped and closed - use context managers.

## Code Quality

- Avoid code duplication; refactor shared logic.
- Apply the Single Responsibility Principle consistently.
- Keep functions and modules focused and small.

## Testing

- Write tests for new functionality in the tests/ directory.
- Test behavior, not implementation details.
- Minimize mocking: only mock I/O boundaries (subprocess, network, filesystem). Test pure functions directly.
- Focus on unique edge cases. Avoid redundant test variations and assertions which exercise the same logic.
- As a rule of thumb, tests are as small as possible (atomic, test one thing) and we write the fewest amount of tests as possible to cover as much as possible
- This rule can be broken for larger integration tests, but always consider if we can apply the rule before breaking it.
- Add or update tests alongside code changes.
- Use pytest and parametrization. Avoid test classes.

## Documentation

- When making structural or architectural changes, check whether the README or related docs need updating.

## Modern Python 3.12+ Features

- Pattern matching (`match`/`case`) when appropriate.
- Type parameter syntax: `def func[T](value: T) -> T:`.
- Prefer `pathlib.Path` over `os.path`.

## Examples

### Good: Modern type hints and dataclass

```python
@dataclass
class ServiceStatus:
    """Service status information."""
    name: str
    is_active: bool
    uptime: str | None = None

def get_service_status(service: str) -> ServiceStatus:
    """Get status information for a service."""
    return ServiceStatus(name=service, is_active=True)
```

### Good: Specific exception handling

```python
try:
    result = subprocess.run(cmd, check=True, text=True, capture_output=True)
except subprocess.CalledProcessError as exc:
    logger.error("Command failed: %s", exc.stderr)
    raise
```

