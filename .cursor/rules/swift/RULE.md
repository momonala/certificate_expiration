---
description: "Swift/iOS coding standards and best practices for clean code and maintainability"
globs: ["*.swift", "*.m", "*.h"]
alwaysApply: false
---

# Swift/iOS - Clean Code & Maintainability

## Swift Language

- Prefer value types (`struct`, `enum`) over reference types (`class`) when possible.
- Use `let` by default; only use `var` when mutation is required.
- Leverage Swift's type system: use enums with associated values, optionals, and generics appropriately.
- Prefer `guard` statements for early returns over nested `if` statements.
- Use `defer` for cleanup operations that must execute regardless of return path.

## Type Safety & Optionals

- Avoid force unwrapping (`!`) and force casting (`as!`); use optional binding or `guard let`.
- Prefer `if let` or `guard let` over optional chaining when you need the unwrapped value.
- Use `nil` coalescing operator (`??`) for default values.
- Consider `Result<Success, Failure>` for operations that can fail, rather than throwing or returning optionals.

## Error Handling

- Fail loudly; don't swallow errors silently.
- Use specific error types (conform to `Error` protocol) rather than generic `NSError`.
- Prefer `throws`/`try` over returning optional or boolean success indicators for recoverable errors.
- Use `Result` type for async operations where throwing isn't appropriate.
- Document which errors can be thrown in function documentation.

## Memory Management

- Understand retain cycles; use `weak` or `unowned` references in closures and delegates.
- Prefer `[weak self]` over `[unowned self]` unless you're certain the object will outlive the closure.
- Use `unowned` only when the reference is guaranteed to be valid for the closure's lifetime.
- Clean up observers, timers, and notifications in `deinit` or appropriate lifecycle methods.

## Side Effects & State

- Don't mutate inputs or external state unless explicitly documented.
- Prefer immutable data structures; use `let` collections and value types.
- Minimize shared mutable state; prefer explicit state ownership.
- Use dependency injection rather than accessing singletons or global state directly.

## Architecture & Design

- Apply Single Responsibility Principle: each type should have one reason to change.
- Prefer composition over inheritance; use protocols for abstraction.
- Design for testability: dependencies should be injectable via initializers or properties.
- Use protocols to define contracts; prefer protocol-oriented programming over class hierarchies.
- Keep view controllers thin; move business logic to separate types (ViewModels, Services, Repositories).

## SwiftUI

- Extract complex views into separate components; avoid deeply nested view hierarchies.
- Use `@State`, `@Binding`, `@StateObject`, `@ObservedObject`, and `@EnvironmentObject` appropriately.
- Prefer `@StateObject` over `@ObservedObject` for view-owned observable objects.
- Use `@Environment` for dependency injection of system values (e.g., `managedObjectContext`).
- Keep view modifiers composable and reusable.

## UIKit

- Use Auto Layout programmatically or via Interface Builder consistently; avoid mixing approaches.
- Implement proper lifecycle methods (`viewDidLoad`, `viewWillAppear`, etc.) without side effects in wrong places.
- Clean up resources in `deinit` or appropriate lifecycle methods (e.g., remove observers in `viewWillDisappear`).
- Use weak references for delegates and data sources to avoid retain cycles.

## Concurrency

- Prefer `async`/`await` over completion handlers for new code (iOS 15+).
- Use `Task` and `async let` for concurrent operations when appropriate.
- Avoid blocking the main thread; move heavy work to background queues.
- Use `@MainActor` to ensure UI updates happen on the main thread.
- Be explicit about thread safety; document if types are not thread-safe.

## Networking & Data

- Use `Codable` for JSON encoding/decoding; avoid manual parsing when possible.
- Handle network errors explicitly; don't assume requests always succeed.
- Use URLSession with proper error handling and timeout configuration.
- Cache data appropriately; consider memory and disk caching strategies.
- Validate and sanitize data at boundaries (API responses, user input).

## Testing

- Write unit tests for business logic; test behavior, not implementation details.
- Use dependency injection to make code testable; avoid hard-coded dependencies.
- Prefer XCTest; use `@testable import` sparingly and only when necessary.
- Test edge cases: empty collections, nil values, network failures, invalid input.
- Keep tests fast and isolated; avoid dependencies on external systems.

## Code Quality

- Avoid code duplication; extract shared logic into functions, extensions, or protocols.
- Keep functions and types focused and small; aim for single responsibility.
- Use meaningful names; prefer clarity over brevity.
- Avoid deep nesting; use early returns and guard statements.
- Extract magic numbers and strings into constants or configuration.

## Documentation

- Use Swift doc comments (`///`) for public APIs.
- Document complex algorithms, non-obvious behavior, and important constraints.
- Include parameter and return value descriptions for public functions.
- When making architectural changes, update relevant documentation.

## Modern Swift Features

- Use Swift 5.9+ features when appropriate: macros, typed throws, noncopyable types.
- Prefer `some Protocol` over generic constraints when the concrete type isn't needed.
- Use `@preconcurrency` imports when bridging with older APIs that aren't Sendable-aware.
- Leverage property wrappers (`@Published`, `@State`, etc.) appropriately.

## Examples

### Good: Value types and guard statements
```swift
struct User {
    let id: UUID
    let name: String
    let email: String
}

func validateUser(_ user: User) throws {
    guard !user.name.isEmpty else {
        throw ValidationError.emptyName
    }
    guard user.email.contains("@") else {
        throw ValidationError.invalidEmail
    }
}
```

### Good: Weak references in closures
```swift
class ViewController: UIViewController {
    func fetchData() {
        apiService.fetchData { [weak self] result in
            guard let self = self else { return }
            self.handleResult(result)
        }
    }
}
```

### Good: Protocol-oriented design
```swift
protocol DataService {
    func fetchData() async throws -> Data
}

class APIDataService: DataService {
    func fetchData() async throws -> Data {
        // Implementation
    }
}

class ViewModel {
    private let dataService: DataService
    
    init(dataService: DataService) {
        self.dataService = dataService
    }
}
```

### Good: Result type for async operations
```swift
func loadUser(id: UUID) async -> Result<User, NetworkError> {
    do {
        let user = try await apiClient.fetchUser(id: id)
        return .success(user)
    } catch {
        return .failure(.requestFailed(error))
    }
}
```

### Good: Proper cleanup in deinit
```swift
class DataManager {
    private var observer: NSObjectProtocol?
    
    init() {
        observer = NotificationCenter.default.addObserver(
            forName: .dataDidUpdate,
            object: nil,
            queue: .main
        ) { [weak self] _ in
            self?.handleUpdate()
        }
    }
    
    deinit {
        if let observer = observer {
            NotificationCenter.default.removeObserver(observer)
        }
    }
}
```

