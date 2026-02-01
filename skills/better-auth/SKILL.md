---
name: better-auth
description: Implement authentication and authorization with Better Auth - a framework-agnostic TypeScript authentication framework. Features include email/password authentication with verification, OAuth providers (Google, GitHub, Discord, etc.), two-factor authentication (TOTP, SMS), passkeys/WebAuthn support, session management, role-based access control (RBAC), rate limiting, and database adapters. Use when adding authentication to applications, implementing OAuth flows, setting up 2FA/MFA, managing user sessions, configuring authorization rules, or building secure authentication systems for web applications.
---

# Better Auth

Framework-agnostic TypeScript authentication with email/password, OAuth, and plugins.

## Quick Start

```bash
npm install better-auth
npx @better-auth/cli generate  # Generate schema
```

```ts
// auth.ts (server)
import { betterAuth } from "better-auth";
export const auth = betterAuth({
  database: { /* see references/database-integration.md */ },
  emailAndPassword: { enabled: true },
  socialProviders: {
    github: { clientId: process.env.GITHUB_CLIENT_ID!, clientSecret: process.env.GITHUB_CLIENT_SECRET! }
  }
});

// auth-client.ts (client)
import { createAuthClient } from "better-auth/client";
export const authClient = createAuthClient({ baseURL: "http://localhost:3000" });

// Usage
await authClient.signUp.email({ email: "user@example.com", password: "secure123", name: "John" });
await authClient.signIn.email({ email: "user@example.com", password: "secure123" });
await authClient.signIn.social({ provider: "github" });
const { data: session } = authClient.useSession();
```

## Feature Matrix

| Feature | Plugin Required | Reference |
|---------|----------------|-----------|
| Email/Password | No | [email-password-auth.md](references/email-password-auth.md) |
| OAuth (GitHub, Google) | No | [oauth-providers.md](references/oauth-providers.md) |
| Email Verification | No | email-password-auth.md |
| Two-Factor (TOTP) | Yes (`twoFactor`) | [advanced-features.md](references/advanced-features.md) |
| Passkeys/WebAuthn | Yes (`passkey`) | advanced-features.md |
| Magic Link | Yes (`magicLink`) | advanced-features.md |
| Organizations | Yes (`organization`) | advanced-features.md |

## Auth Method Selection

- **Email/Password**: Standard web app, full credential control
- **OAuth**: Quick signup, social profiles
- **Passkeys**: Passwordless, modern browsers, high security
- **Magic Link**: Passwordless without WebAuthn complexity

## Reference Documentation

| Document | Description |
|----------|-------------|
| [email-password-auth.md](references/email-password-auth.md) | Email/password, verification, reset |
| [oauth-providers.md](references/oauth-providers.md) | Social login, provider config |
| [database-integration.md](references/database-integration.md) | Adapters, schema, migrations |
| [advanced-features.md](references/advanced-features.md) | 2FA, passkeys, magic links, orgs |

## Implementation Checklist

- [ ] Install and set env vars (SECRET, URL)
- [ ] Create auth server with database config
- [ ] Run `npx @better-auth/cli generate`
- [ ] Mount API handler in framework
- [ ] Create client instance
- [ ] Implement sign-up/sign-in UI
- [ ] Add session management and protected routes

## Resources

- Docs: https://www.better-auth.com/docs
- GitHub: https://github.com/better-auth/better-auth
