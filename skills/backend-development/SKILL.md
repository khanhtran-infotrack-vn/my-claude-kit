---
name: backend-development
description: Build robust backend systems with Node.js/TypeScript, Python, Go, Rust, and C#/.NET. Covers ASP.NET Core with Clean Architecture, Entity Framework Core, MediatR/CQRS patterns, NestJS, FastAPI, databases (PostgreSQL, MongoDB, SQL Server, Redis), APIs (REST, GraphQL, gRPC), OAuth 2.1/JWT authentication, xUnit/Vitest testing, OWASP Top 10 security, Docker/Kubernetes DevOps, and monitoring. Use for API design, authentication, database optimization, CI/CD, security vulnerabilities, microservices, or production-ready systems. Activates for: .NET, C#, ASP.NET Core, Entity Framework Core, EF Core, MediatR, Clean Architecture, NestJS, FastAPI, Django, backend, API, database, authentication, security, DevOps, Kubernetes, Docker.
---

# Backend Development Skill

Production-ready backend development with modern technologies, best practices, and proven patterns.

## Core Principles

Always follow **YAGNI**, **KISS**, **DRY**, and **SOLID**:
- See `backend-code-quality.md` for detailed SOLID examples (TypeScript and C#/.NET)

## When to Use

- Designing RESTful, GraphQL, or gRPC APIs
- Building authentication/authorization systems
- Optimizing database queries and schemas
- Implementing caching and performance optimization
- OWASP Top 10 security mitigation
- Designing scalable microservices
- Testing strategies (unit, integration, E2E)
- CI/CD pipelines and deployment
- Monitoring and debugging production systems

## Technology Selection Guide

**Languages:** Node.js/TypeScript (full-stack), Python (data/ML), Go (concurrency), Rust (performance), C#/.NET (enterprise)
**Frameworks:** NestJS, FastAPI, Django, Express, Gin, ASP.NET Core, Entity Framework Core
**Databases:** PostgreSQL (ACID), MongoDB (flexible schema), Redis (caching), SQL Server (enterprise)
**APIs:** REST (simple), GraphQL (flexible), gRPC (performance)

See: `references/backend-technologies.md` for detailed comparisons

## Reference Navigation

**Core Technologies:**
- `backend-technologies.md` - Languages, frameworks, databases, message queues, ORMs
- `backend-api-design.md` - REST, GraphQL, gRPC patterns and best practices

**Security & Authentication:**
- `backend-security.md` - OWASP Top 10 2025, security best practices, input validation
- `backend-authentication.md` - OAuth 2.1, JWT, RBAC, MFA, session management

**Performance & Architecture:**
- `backend-performance.md` - Caching, query optimization, load balancing, scaling
- `backend-architecture.md` - Microservices, event-driven, CQRS, saga patterns

**Quality & Operations:**
- `backend-testing.md` - Testing strategies, frameworks, tools, CI/CD testing
- `backend-code-quality.md` - SOLID principles, design patterns, clean code
- `backend-devops.md` - Docker, Kubernetes, deployment strategies, monitoring
- `backend-debugging.md` - Debugging strategies, profiling, logging, production debugging
- `backend-mindset.md` - Problem-solving, architectural thinking, collaboration

**.NET/C# Specific:**
- `backend-dotnet-architecture.md` - Clean Architecture, CQRS, MediatR patterns
- `backend-dotnet-efcore.md` - Entity Framework Core, queries, migrations
- `backend-dotnet-apis.md` - Controller-based APIs, Result pattern, versioning
- `backend-dotnet-auth.md` - JWT authentication, ASP.NET Core Identity

## Key Best Practices (2025)

**Security:** Argon2id passwords, parameterized queries (98% SQL injection reduction), OAuth 2.1 + PKCE, rate limiting, security headers

**Performance:** Redis caching (90% DB load reduction), database indexing (30% I/O reduction), CDN (50%+ latency cut), connection pooling

**Testing:** 70-20-10 pyramid (unit-integration-E2E), Vitest 50% faster than Jest, xUnit/NUnit for .NET, contract testing for microservices, 83% migrations fail without tests

**DevOps:** Blue-green/canary deployments, feature flags (90% fewer failures), Kubernetes 84% adoption, Prometheus/Grafana monitoring, OpenTelemetry tracing

## Quick Decision Matrix

| Need | Choose |
|------|--------|
| Fast development | Node.js + NestJS |
| Data/ML integration | Python + FastAPI |
| High concurrency | Go + Gin |
| Max performance | Rust + Axum |
| Enterprise/.NET ecosystem | C# + ASP.NET Core |
| .NET data access | Entity Framework Core |
| ACID transactions | PostgreSQL or SQL Server |
| Flexible schema | MongoDB |
| Caching | Redis |
| Internal services | gRPC |
| Public APIs | GraphQL/REST |
| Real-time events | Kafka |
| .NET real-time | SignalR |

## Resources

OWASP Top 10: https://owasp.org/www-project-top-ten/ | OAuth 2.1: https://oauth.net/2.1/ | OpenTelemetry: https://opentelemetry.io/
