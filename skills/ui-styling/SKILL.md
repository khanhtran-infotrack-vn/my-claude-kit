---
name: ui-styling
description: Create beautiful, accessible user interfaces with shadcn/ui components (built on Radix UI + Tailwind), Tailwind CSS utility-first styling, and canvas-based visual designs. Use when building user interfaces, implementing design systems, creating responsive layouts, adding accessible components (dialogs, dropdowns, forms, tables), customizing themes and colors, implementing dark mode, generating visual designs and posters, or establishing consistent styling patterns across applications.
---

# UI Styling Skill

shadcn/ui + Tailwind CSS + Canvas for beautiful, accessible interfaces.

## Quick Start

```bash
npx shadcn@latest init
npx shadcn@latest add button card dialog form
```

```tsx
import { Button } from "@/components/ui/button"
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card"

<Card className="hover:shadow-lg transition-shadow">
  <CardHeader>
    <CardTitle className="text-2xl font-bold">Title</CardTitle>
  </CardHeader>
  <CardContent className="space-y-4">
    <Button variant="default" className="w-full">Action</Button>
  </CardContent>
</Card>
```

## Core Stack

| Layer | Tool | Purpose |
|-------|------|---------|
| Components | shadcn/ui | Accessible Radix primitives |
| Styling | Tailwind CSS | Utility-first CSS |
| Visual Design | Canvas | Museum-quality compositions |

## Best Practices

1. **Composition** - Build complex UIs from simple primitives
2. **Utility-First** - Use Tailwind directly; extract only for true repetition
3. **Mobile-First** - Start mobile, layer responsive variants
4. **Accessibility** - Leverage Radix, add focus states, semantic HTML
5. **Design Tokens** - Consistent spacing, colors, typography
6. **Dark Mode** - Apply dark variants to all themed elements

## Reference Documentation

**Components**:
- `references/shadcn-components.md` - Complete component catalog
- `references/shadcn-theming.md` - Themes, CSS variables, dark mode
- `references/shadcn-accessibility.md` - ARIA, keyboard, screen readers

**Styling**:
- `references/tailwind-utilities.md` - Layout, spacing, typography
- `references/tailwind-responsive.md` - Breakpoints, container queries
- `references/tailwind-customization.md` - Config, custom utilities

**Visual Design**:
- `references/canvas-design-system.md` - Design philosophy, canvas workflows

## Scripts

```bash
python scripts/shadcn_add.py button card dialog
python scripts/tailwind_config_gen.py --colors brand:blue
```

## Resources

- shadcn/ui: https://ui.shadcn.com/llms.txt
- Tailwind CSS: https://tailwindcss.com/docs
- Radix UI: https://radix-ui.com
