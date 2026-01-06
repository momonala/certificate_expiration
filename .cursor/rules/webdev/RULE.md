---
description: "Web development coding standards and best practices for JavaScript, HTML, and CSS"
globs: ["*.js", "*.ts", "*.jsx", "*.tsx", "*.html", "*.css"]
alwaysApply: false
---

# Web Development - Coding Standards

## TypeScript

- Use built-in JS/TS types; avoid `any` and unnecessary generics.
- Prefer discriminated unions for state machines and variant types.
- Use branded types for domain primitives (e.g., `UserId`, `Email`).
- Leverage `satisfies` operator for type inference with explicit constraints.

## Control Flow & Errors

- Fail loudly; do not swallow errors.
- Avoid broad `catch` blocks; catch specific error types.
- Throw meaningful errors; use custom error classes for domain logic.
- Implement error boundaries/recovery strategies for user-facing failures.

## Side Effects & State

- Do not mutate inputs unless explicitly documented.
- Minimize shared and global state; prefer explicit state ownership.
- Use event delegation for dynamic lists instead of attaching listeners to each element.
- Clean up side effects: remove event listeners, clear timers/intervals, cancel AbortControllers.

## Async & Performance

- Handle async explicitly (`async/await`); avoid mixing sync and async in the same layer.
- Use `AbortController` for cancellable async operations.
- Prefer `Promise.allSettled()` over `Promise.all()` when partial failures are acceptable.
- Consider code splitting and lazy loading for large dependencies.
- Use `requestIdleCallback` or `IntersectionObserver` for non-critical work.

## Memory & Resources

- Avoid closures over large objects; prefer explicit parameters.
- Use `WeakMap`/`WeakSet` for caches that shouldn't prevent garbage collection.
- Clean up subscriptions, observers, and event listeners to prevent leaks.
- Profile memory usage in long-running applications.

## HTML & Accessibility

- Use semantic HTML; avoid div-heavy markup.
- Implement proper focus management for modals, dropdowns, and dynamic content.
- Use ARIA attributes when semantic HTML is insufficient, not as a replacement.
- Ensure keyboard navigation works without mouse interaction.
- Test with screen readers; don't rely solely on automated accessibility checkers.

## CSS Architecture

- Prefer composition over deep nesting.
- Use CSS custom properties for theming; avoid hard-coded values.
- Consider CSS containment for performance-critical components.
- Use `:where()` for lower specificity when appropriate.
- Avoid `!important`; refactor specificity issues instead.

## Security

- Sanitize user input before rendering HTML; use `DOMPurify` or similar.
- Use Content Security Policy headers; avoid `eval()` and inline scripts.
- Validate and sanitize data at boundaries (API responses, form inputs).
- Use `rel="noopener noreferrer"` for external links opened via `window.open()`.

## Logging & Debugging

- Log at boundaries and failure points, not inside tight loops.
- Never log secrets, passwords, tokens, or sensitive user data.
- Use structured logging with context (request IDs, user IDs) for traceability.
- Emojis are acceptable for fast log scanning in development.

## Examples

### Good: Discriminated union for state machine
```typescript
type LoadingState = 
    | { status: 'idle' }
    | { status: 'loading' }
    | { status: 'success'; data: Data }
    | { status: 'error'; error: Error };

function handleState(state: LoadingState) {
    switch (state.status) {
        case 'idle':
            return null;
        case 'loading':
            return <Spinner />;
        case 'success':
            return <DataView data={state.data} />;
        case 'error':
            return <ErrorView error={state.error} />;
    }
}
```

### Good: Event delegation for dynamic lists
```javascript
// Attach one listener to parent instead of N listeners
document.getElementById('list').addEventListener('click', (e) => {
    if (e.target.matches('.item')) {
        handleItemClick(e.target.dataset.id);
    }
});
```

### Good: AbortController for cancellable operations
```javascript
const controller = new AbortController();

async function fetchWithTimeout(url, timeoutMs) {
    const timeoutId = setTimeout(() => controller.abort(), timeoutMs);
    try {
        const response = await fetch(url, { signal: controller.signal });
        return await response.json();
    } catch (error) {
        if (error.name === 'AbortError') {
            throw new Error('Request timeout');
        }
        throw error;
    } finally {
        clearTimeout(timeoutId);
    }
}
```

### Good: Focus management for accessibility
```javascript
function openModal(modalElement) {
    const previouslyFocused = document.activeElement;
    modalElement.showModal();
    modalElement.focus();
    
    modalElement.addEventListener('close', () => {
        previouslyFocused?.focus();
    }, { once: true });
}
```

