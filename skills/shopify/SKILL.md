---
name: shopify
description: Build Shopify applications, extensions, and themes using GraphQL/REST APIs, Shopify CLI, Polaris UI components, and Liquid templating. Capabilities include app development with OAuth authentication, checkout UI extensions for customizing checkout flow, admin UI extensions for dashboard integration, POS extensions for retail, theme development with Liquid, webhook management, billing API integration, product/order/customer management. Use when building Shopify apps, implementing checkout customizations, creating admin interfaces, developing themes, integrating payment processing, managing store data via APIs, or extending Shopify functionality.
---

# Shopify Development

Build apps, extensions, and themes on the Shopify platform.

## Quick Start

```bash
# Install Shopify CLI
npm install -g @shopify/cli@latest

# Create app
shopify app init && cd my-app && shopify app dev

# Create theme
shopify theme init && shopify theme dev

# Generate extension
shopify app generate extension --type checkout_ui_extension
```

## When to Build What

| Build | Use Case |
|-------|----------|
| **App** | External integrations, admin tools, multi-store features, billing |
| **Extension** | Checkout customization, admin fields, POS actions, discount/payment rules |
| **Theme** | Custom storefront, brand layouts, product pages |
| **App + Theme Extension** | Backend logic + storefront UI (reviews, wishlists) |

## Extension Types

- `checkout_ui_extension` - Customize checkout flow
- `admin_action` / `admin_block` - Extend admin dashboard
- `pos_ui_extension` - Point of Sale customization
- `function` - Discounts, payment, delivery, validation rules

## Essential Commands

```bash
shopify app dev          # Start development server with tunnel
shopify app deploy       # Build and upload to Shopify
shopify theme pull       # Download theme from store
shopify theme push       # Upload theme to store
```

## Best Practices

- **API**: Prefer GraphQL over REST; request only needed fields
- **Security**: Store credentials in env vars; verify webhook signatures
- **Performance**: Cache responses; optimize images; monitor query costs
- **Testing**: Use development stores; test mobile; check accessibility

## Reference Documentation

| Document | Description |
|----------|-------------|
| [App Development](references/app-development.md) | OAuth, APIs, webhooks, billing integration |
| [Extensions](references/extensions.md) | Checkout, Admin, POS, Functions development |
| [Themes](references/themes.md) | Liquid templating, sections, deployment |

## Scripts

```bash
python scripts/shopify_init.py  # Initialize Shopify projects interactively
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Rate limits | Monitor `X-Shopify-Shop-Api-Call-Limit`; use bulk operations |
| Auth failures | Verify token validity; check scopes granted |
| Extension missing | Check target correct; verify published; ensure app installed |
| Webhook issues | Verify URL accessible; check signature validation |

## Resources

- [Shopify Docs](https://shopify.dev/docs) | [GraphQL API](https://shopify.dev/docs/api/admin-graphql)
- [Shopify CLI](https://shopify.dev/docs/api/shopify-cli) | [Polaris](https://polaris.shopify.com)
- API versioning: Quarterly releases (YYYY-MM), 12-month support per version
