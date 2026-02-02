---
name: backend-development
description: Build robust backend systems with Node.js/TypeScript, Python, Go, Rust, and C#/.NET. Covers ASP.NET Core with Controller-based architecture and Clean Architecture, Entity Framework Core, MediatR/CQRS patterns, NestJS, FastAPI, databases (PostgreSQL, MongoDB, SQL Server, Redis), APIs (REST, GraphQL, gRPC), OAuth 2.1/JWT authentication, xUnit/Vitest testing, OWASP Top 10 security, Docker/Kubernetes DevOps, and monitoring. Use for API design, authentication, database optimization, CI/CD, security vulnerabilities, microservices, or production-ready systems.
---

# Backend Development Skill

Production-ready backend development with modern technologies, best practices, and proven patterns.

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
- **.NET/C# development** with ASP.NET Core, Entity Framework Core, Clean Architecture
- **SOLID principles** application in any language/framework

## Test-First Development (MANDATORY)

**All backend code MUST follow Test-First Development:**

**Workflow:** Write failing tests → Implement minimal code → Refactor while green

**Coverage:** All handlers, validators, domain logic. NO "Arrange/Act/Assert" comments.

**Why TFD:**
- 40-80% fewer bugs in production
- Forces clear API design before implementation
- Provides regression safety during refactoring
- Documents expected behavior through tests

See: `references/backend-testing.md` for comprehensive testing strategies

## Technology Selection Guide

**Languages:** Node.js/TypeScript (full-stack), Python (data/ML), Go (concurrency), Rust (performance), **C#/.NET (enterprise)**
**Frameworks:** NestJS, FastAPI, Django, Express, Gin, **ASP.NET Core**
**Databases:** PostgreSQL (ACID), MongoDB (flexible schema), Redis (caching), **SQL Server**
**APIs:** REST (simple), GraphQL (flexible), gRPC (performance)

See: `references/backend-technologies.md` for detailed comparisons

## Reference Navigation

**Core Technologies:**
- `backend-technologies.md` - Languages, frameworks, databases, message queues, ORMs
- `backend-api-design.md` - REST, GraphQL, gRPC patterns and best practices
- `backend-dotnet.md` - **ASP.NET Core, Entity Framework Core, MediatR/CQRS, Clean Architecture, C# patterns**

**Testing (MANDATORY):**
- `test-first-development.md` - **Complete TFD guide with examples (READ THIS FIRST)**
- `backend-testing.md` - Testing strategies, frameworks, tools, CI/CD testing

**Security & Authentication:**
- `backend-security.md` - OWASP Top 10 2025, security best practices, input validation
- `backend-authentication.md` - OAuth 2.1, JWT, RBAC, MFA, session management

**Performance & Architecture:**
- `backend-performance.md` - Caching, query optimization, load balancing, scaling
- `backend-architecture.md` - Microservices, event-driven, CQRS, saga patterns

**Quality & Operations:**
- `backend-code-quality.md` - **SOLID principles**, design patterns, clean code
- `backend-devops.md` - Docker, Kubernetes, deployment strategies, monitoring
- `backend-debugging.md` - Debugging strategies, profiling, logging, production debugging
- `backend-mindset.md` - Problem-solving, architectural thinking, collaboration

## Key Best Practices (2025)

**Security:** Argon2id passwords, parameterized queries (98% SQL injection reduction), OAuth 2.1 + PKCE, rate limiting, security headers

**Performance:** Redis caching (90% DB load reduction), database indexing (30% I/O reduction), CDN (50%+ latency cut), connection pooling

**Testing:** 70-20-10 pyramid (unit-integration-E2E), Vitest 50% faster than Jest, contract testing for microservices, 83% migrations fail without tests

**DevOps:** Blue-green/canary deployments, feature flags (90% fewer failures), Kubernetes 84% adoption, Prometheus/Grafana monitoring, OpenTelemetry tracing

## Quick Decision Matrix

| Need | Choose |
|------|--------|
| Fast development | Node.js + NestJS |
| Data/ML integration | Python + FastAPI |
| High concurrency | Go + Gin |
| Max performance | Rust + Axum |
| **Enterprise/.NET** | **C# + ASP.NET Core** |
| ACID transactions | PostgreSQL / SQL Server |
| Flexible schema | MongoDB |
| Caching | Redis |
| Internal services | gRPC |
| Public APIs | GraphQL/REST |
| Real-time events | Kafka / SignalR (.NET) |

## Implementation Checklist

**API:** Choose style → Design schema → Validate input → Add auth → Rate limiting → Documentation → Error handling

**Database:** Choose DB → Design schema → Create indexes → Connection pooling → Migration strategy → Backup/restore → Test performance

**Security:** OWASP Top 10 → Parameterized queries → OAuth 2.1 + JWT → Security headers → Rate limiting → Input validation → Argon2id passwords

**Testing:** Unit 70% → Integration 20% → E2E 10% → Load tests → Migration tests → Contract tests (microservices)

**Deployment:** Docker → CI/CD → Blue-green/canary → Feature flags → Monitoring → Logging → Health checks

## Resources

- OWASP Top 10: https://owasp.org/www-project-top-ten/
- OAuth 2.1: https://oauth.net/2.1/
- OpenTelemetry: https://opentelemetry.io/
- ASP.NET Core Docs: https://learn.microsoft.com/aspnet/core
- Entity Framework Core: https://learn.microsoft.com/ef/core
- Clean Architecture Template: https://github.com/jasontaylordev/CleanArchitecture
