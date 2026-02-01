---
name: frontend-dev-guidelines
description: Frontend development guidelines for React/TypeScript applications. Modern patterns including Suspense, lazy loading, useSuspenseQuery, file organization with features directory, MUI v7 styling, TanStack Router, performance optimization, and TypeScript best practices. Use when creating components, pages, features, fetching data, styling, routing, or working with frontend code.
---

# Frontend Development Guidelines

Modern React development with Suspense, lazy loading, and feature-based organization.

## Quick Start Checklists

### New Component
- [ ] `React.FC<Props>` with TypeScript
- [ ] `React.lazy()` for heavy components
- [ ] `<SuspenseLoader>` wrapper
- [ ] `useSuspenseQuery` for data
- [ ] Import aliases: `@/`, `~types`, `~components`, `~features`
- [ ] `useCallback` for handlers passed to children
- [ ] No early returns with loading spinners

### New Feature
- [ ] Create `features/{name}/` with: `api/`, `components/`, `hooks/`, `helpers/`, `types/`
- [ ] API service: `api/{feature}Api.ts`
- [ ] Route: `routes/{feature-name}/index.tsx`
- [ ] Lazy load + Suspense boundaries

## Core Principles

1. **Lazy Load Heavy Components** - Routes, DataGrid, charts, editors
2. **Suspense for Loading** - Use SuspenseLoader, not early returns
3. **useSuspenseQuery** - Primary data fetching pattern
4. **Feature Organization** - Domain-specific subdirectories
5. **Styles by Size** - <100 inline, >100 separate file
6. **Import Aliases** - `@/`, `~types`, `~components`, `~features`
7. **useMuiSnackbar** - For all notifications (never react-toastify)

## Import Aliases

| Alias | Resolves To | Example |
|-------|-------------|---------|
| `@/` | `src/` | `import { apiClient } from '@/lib/apiClient'` |
| `~types` | `src/types` | `import type { User } from '~types/user'` |
| `~components` | `src/components` | `import { SuspenseLoader } from '~components/SuspenseLoader'` |
| `~features` | `src/features` | `import { authApi } from '~features/auth'` |

## Reference Guides

| Topic | Resource |
|-------|----------|
| Component patterns | `resources/component-patterns.md` |
| Data fetching | `resources/data-fetching.md` |
| File organization | `resources/file-organization.md` |
| Styling (MUI v7) | `resources/styling-guide.md` |
| Routing (TanStack) | `resources/routing-guide.md` |
| Loading/errors | `resources/loading-and-error-states.md` |
| Performance | `resources/performance.md` |
| TypeScript | `resources/typescript-standards.md` |
| Forms/Auth/DataGrid | `resources/common-patterns.md` |
| Full examples | `resources/complete-examples.md` |

## MUI v7 Grid Syntax

```typescript
<Grid size={{ xs: 12, md: 6 }}>  // ✅ v7 syntax
<Grid xs={12} md={6}>             // ❌ Old syntax
```

## Component Template

```typescript
import React, { useState, useCallback } from 'react';
import { Box, Paper } from '@mui/material';
import { useSuspenseQuery } from '@tanstack/react-query';
import { featureApi } from '../api/featureApi';

interface Props { id: number; onAction?: () => void; }

export const MyComponent: React.FC<Props> = ({ id, onAction }) => {
    const { data } = useSuspenseQuery({
        queryKey: ['feature', id],
        queryFn: () => featureApi.getFeature(id),
    });
    const handleAction = useCallback(() => onAction?.(), [onAction]);
    return <Box sx={{ p: 2 }}><Paper sx={{ p: 3 }}>{/* Content */}</Paper></Box>;
};

export default MyComponent;
```

See `resources/complete-examples.md` for full working examples.
