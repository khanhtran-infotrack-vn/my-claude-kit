---
name: databases
description: Work with MongoDB (document database, BSON documents, aggregation pipelines, Atlas cloud) and PostgreSQL (relational database, SQL queries, psql CLI, pgAdmin). Use when designing database schemas, writing queries and aggregations, optimizing indexes for performance, performing database migrations, configuring replication and sharding, implementing backup and restore strategies, managing database users and permissions, analyzing query performance, or administering production databases.
---

# Databases Skill

MongoDB (document-oriented) and PostgreSQL (relational) database operations.

## Database Selection

| Choose MongoDB When | Choose PostgreSQL When |
|---------------------|------------------------|
| Schema flexibility, frequent changes | Strong consistency, ACID critical |
| Document-centric JSON data | Complex relationships, referential integrity |
| Horizontal scaling (sharding) | SQL requirement, BI tools |
| High write throughput (IoT, logging) | Complex queries (CTEs, window functions) |

## Quick Start

```bash
# MongoDB (Atlas recommended)
mongosh "mongodb+srv://cluster.mongodb.net/mydb"

# PostgreSQL
psql -U postgres -d mydb
```

## CRUD Comparison

| Operation | MongoDB | PostgreSQL |
|-----------|---------|------------|
| Insert | `db.users.insertOne({name:"Bob"})` | `INSERT INTO users (name) VALUES ('Bob')` |
| Read | `db.users.find({age:{$gte:18}})` | `SELECT * FROM users WHERE age >= 18` |
| Update | `db.users.updateOne({name:"Bob"},{$set:{age:25}})` | `UPDATE users SET age=25 WHERE name='Bob'` |
| Delete | `db.users.deleteOne({name:"Bob"})` | `DELETE FROM users WHERE name='Bob'` |
| Index | `db.users.createIndex({email:1})` | `CREATE INDEX idx_email ON users(email)` |

## Reference Documentation

### MongoDB
| Document | Description |
|----------|-------------|
| [mongodb-crud.md](references/mongodb-crud.md) | CRUD, query operators, atomic updates |
| [mongodb-aggregation.md](references/mongodb-aggregation.md) | Pipeline stages, operators, patterns |
| [mongodb-indexing.md](references/mongodb-indexing.md) | Index types, compound indexes, optimization |
| [mongodb-atlas.md](references/mongodb-atlas.md) | Atlas setup, clusters, monitoring |

### PostgreSQL
| Document | Description |
|----------|-------------|
| [postgresql-queries.md](references/postgresql-queries.md) | JOINs, CTEs, window functions |
| [postgresql-psql-cli.md](references/postgresql-psql-cli.md) | psql commands, scripting |
| [postgresql-performance.md](references/postgresql-performance.md) | EXPLAIN, optimization, vacuum |
| [postgresql-administration.md](references/postgresql-administration.md) | Users, backups, replication |

## Best Practices

**MongoDB:** Embed for 1-to-few, reference for 1-to-many; index query fields; use aggregation for transforms

**PostgreSQL:** Normalize to 3NF; index foreign keys; use EXPLAIN ANALYZE; regular VACUUM; connection pooling

## Scripts

```bash
python scripts/db_migrate.py --db mongodb --generate "add_index"
python scripts/db_backup.py --db postgres --output /backups/
python scripts/db_performance_check.py --db mongodb --threshold 100ms
```

## Resources

- MongoDB: https://www.mongodb.com/docs/ | https://learn.mongodb.com/
- PostgreSQL: https://www.postgresql.org/docs/ | https://www.postgresqltutorial.com/
