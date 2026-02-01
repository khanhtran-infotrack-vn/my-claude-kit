---
name: web-frameworks
description: Build modern full-stack web applications with Next.js (App Router, Server Components, RSC, PPR, SSR, SSG, ISR), Turborepo (monorepo management, task pipelines, remote caching, parallel execution), and RemixIcon (3100+ SVG icons in outlined/filled styles). Use when creating React applications, implementing server-side rendering, setting up monorepos with multiple packages, optimizing build performance and caching strategies, adding icon libraries, managing shared dependencies, or working with TypeScript full-stack projects.
---

# Web Frameworks

Next.js + Turborepo + RemixIcon for modern full-stack applications.

## Stack Selection

**Single App**: Next.js + RemixIcon
**Monorepo**: Next.js + Turborepo + RemixIcon

## Quick Start

### Single Application
```bash
npx create-next-app@latest my-app
cd my-app && npm install remixicon
```

### Monorepo
```bash
npx create-turbo@latest my-monorepo
# Structure: apps/, packages/, turbo.json
```

### RemixIcon Usage
```tsx
// Webfont
<i className="ri-home-line"></i>

// React component
import { RiHomeLine } from "@remixicon/react"
<RiHomeLine size={24} />
```

## Monorepo Structure

```
my-monorepo/
├── apps/web/, apps/admin/, apps/docs/
├── packages/ui/, packages/config/, packages/types/
└── turbo.json
```

**turbo.json**:
```json
{
  "pipeline": {
    "build": { "dependsOn": ["^build"], "outputs": [".next/**", "dist/**"] },
    "dev": { "cache": false, "persistent": true }
  }
}
```

## Best Practices

**Next.js**: Default Server Components, proper loading/error states, Image optimization
**Turborepo**: Clear separation (apps/packages), correct task dependencies, remote caching
**RemixIcon**: Line for minimal, fill for emphasis; 24x24 grid; aria-labels

## Reference Documentation

**Next.js**:
- `references/nextjs-app-router.md` - Routing, layouts, pages
- `references/nextjs-server-components.md` - RSC patterns, streaming
- `references/nextjs-data-fetching.md` - Caching, revalidation
- `references/nextjs-optimization.md` - Images, fonts, PPR

**Turborepo**:
- `references/turborepo-setup.md` - Installation, workspace config
- `references/turborepo-pipelines.md` - Dependencies, parallel execution
- `references/turborepo-caching.md` - Local/remote cache

**RemixIcon**:
- `references/remix-icon-integration.md` - Installation, customization

## Resources

- Next.js: https://nextjs.org/docs/llms.txt
- Turborepo: https://turbo.build/repo/docs
- RemixIcon: https://remixicon.com
