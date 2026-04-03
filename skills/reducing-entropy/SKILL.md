---
name: reducing-entropy
description: Gradually reduce codebase complexity without changing behavior. Handle deferred refactors: Props Drilling removal, useState→useReducer consolidation, duplicate code extraction.
origin: local
---

# Reducing Entropy

Safely reduce accumulated complexity in the codebase. No feature changes — structure improvements only.

## When to Activate
- "Refactor", "clean up", "reduce complexity" mentioned
- Before adding a major new feature (clear the path)
- After sprint completion with deferred refactors

## Common Entropy Sources

### 1. Props Drilling (React)
**Symptom:** State passed 3+ levels deep
```javascript
// AS-IS: prop drilling
<Parent data={data}>
  <Child data={data}>
    <GrandChild data={data} />
  </Child>
</Parent>

// TO-BE: Context
const DataContext = createContext(null)
export const DataProvider = ({ children }) => {
  const state = useData()
  return <DataContext.Provider value={state}>{children}</DataContext.Provider>
}
```

### 2. useState Explosion → useReducer
**Symptom:** 10+ related `useState` calls in one component
```javascript
// AS-IS: scattered state
const [isLoading, setIsLoading] = useState(false)
const [error, setError] = useState(null)
const [data, setData] = useState(null)
// ... more

// TO-BE: reducer
const [state, dispatch] = useReducer(reducer, { isLoading: false, error: null, data: null })
dispatch({ type: 'LOADING' })
dispatch({ type: 'SUCCESS', payload: data })
dispatch({ type: 'ERROR', payload: error })
```

### 3. Duplicated Components
**Symptom:** Two components with identical structure, different data
```javascript
// Extract shared component
const StatCard = ({ label, value, icon }) => (
  <div className="stat-card">
    <span>{icon}</span>
    <div>
      <p>{label}</p>
      <p>{value}</p>
    </div>
  </div>
)
```

### 4. Configuration Registry (Backend)
**Symptom:** Same pattern repeated for each type (role, category, etc.)
```python
# AS-IS: hardcoded per type
if role == "frontend":
    return frontend_config
elif role == "backend":
    return backend_config

# TO-BE: registry
ROLE_REGISTRY = {
    "frontend": FrontendConfig(),
    "backend": BackendConfig(),
}
return ROLE_REGISTRY[role]
```

## Safe Refactor Procedure
```
1. Verify all tests pass (baseline)
2. Limit scope: one refactor item per session
3. Intermediate commit (save before-state)
4. Re-run same tests (no regression)
5. Verify functional equivalence
```

## Rules
- No new features during refactor
- One PR = one refactor item
- Maintain or improve test coverage
