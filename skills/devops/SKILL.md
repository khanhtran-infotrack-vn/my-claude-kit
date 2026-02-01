---
name: devops
description: Deploy and manage cloud infrastructure on Cloudflare (Workers, R2, D1, KV, Pages, Durable Objects, Browser Rendering), Docker containers, and Google Cloud Platform (Compute Engine, GKE, Cloud Run, App Engine, Cloud Storage). Use when deploying serverless functions to the edge, configuring edge computing solutions, managing Docker containers and images, setting up CI/CD pipelines, optimizing cloud infrastructure costs, implementing global caching strategies, working with cloud databases, or building cloud-native applications.
---

# DevOps Skill

Deploy and manage cloud infrastructure across Cloudflare, Docker, and Google Cloud Platform.

## Quick Start

```bash
# Cloudflare Workers
npm install -g wrangler && wrangler init my-worker && cd my-worker && wrangler deploy

# Docker
docker build -t myapp . && docker run -p 3000:3000 myapp

# Google Cloud
gcloud run deploy my-service --image gcr.io/project/image --region us-central1
```

## Platform Selection

| Need | Choose |
|------|--------|
| Sub-50ms latency globally | Cloudflare Workers |
| Large file storage (zero egress) | Cloudflare R2 |
| SQL database (global reads) | Cloudflare D1 |
| Containerized workloads | Docker + Cloud Run/GKE |
| Enterprise Kubernetes | GKE |
| Managed relational DB | Cloud SQL |
| Static site + API | Cloudflare Pages |
| WebSocket/real-time | Cloudflare Durable Objects |
| ML/AI pipelines | GCP Vertex AI |
| Browser automation | Cloudflare Browser Rendering |

## Reference Documentation

### Cloudflare Platform
| Document | Description |
|----------|-------------|
| [cloudflare-platform.md](references/cloudflare-platform.md) | Edge computing overview, key components |
| [cloudflare-workers-basics.md](references/cloudflare-workers-basics.md) | Getting started, handlers, basic patterns |
| [cloudflare-workers-advanced.md](references/cloudflare-workers-advanced.md) | Performance optimization, advanced patterns |
| [cloudflare-workers-apis.md](references/cloudflare-workers-apis.md) | Runtime APIs, bindings, integrations |
| [cloudflare-r2-storage.md](references/cloudflare-r2-storage.md) | R2 object storage, S3 compatibility |
| [cloudflare-d1-kv.md](references/cloudflare-d1-kv.md) | D1 SQLite database, KV store |
| [browser-rendering.md](references/browser-rendering.md) | Puppeteer/Playwright automation |

### Docker & GCP
| Document | Description |
|----------|-------------|
| [docker-basics.md](references/docker-basics.md) | Dockerfile, images, containers |
| [docker-compose.md](references/docker-compose.md) | Multi-container apps, networking |
| [gcloud-platform.md](references/gcloud-platform.md) | GCP overview, gcloud CLI, auth |
| [gcloud-services.md](references/gcloud-services.md) | Compute Engine, GKE, Cloud Run |

## Best Practices

**Security:** Run containers as non-root; use service accounts; store secrets in env vars

**Performance:** Multi-stage Docker builds; edge caching with KV; R2 for zero egress

**Cost:** Use R2 over S3 for large egress; implement caching; right-size resources

## Common Patterns

```dockerfile
# Multi-stage Docker build
FROM node:20-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:20-alpine
WORKDIR /app
COPY --from=build /app/dist ./dist
USER node
CMD ["node", "dist/server.js"]
```

## Resources

- [Cloudflare Docs](https://developers.cloudflare.com) | [Wrangler CLI](https://developers.cloudflare.com/workers/wrangler/)
- [Docker Docs](https://docs.docker.com) | [GCP Docs](https://cloud.google.com/docs)
