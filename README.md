# LedgerCore

[![Render Status](https://img.shields.io/badge/Render-Live-brightgreen?logo=render&style=flat-square)](https://ledgercore-api-g79m.onrender.com/docs)
[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&style=flat-square)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?logo=fastapi&style=flat-square)](https://fastapi.tiangolo.com/)
[![Redis](https://img.shields.io/badge/Redis-Token_Bucket-DC382D?logo=redis&style=flat-square)](https://redis.io/)

A distributed rate limiter and API gateway built with FastAPI, Redis, and Lua — featuring atomic token-bucket rate limiting, circuit breaking, and full observability.

## 🚀 Live Deployment

- **Interactive API Docs (Swagger):** [https://ledgercore-api-g79m.onrender.com/docs](https://ledgercore-api-g79m.onrender.com/docs)
- **Health Ping Endpoint:** [https://ledgercore-api-g79m.onrender.com/ping](https://ledgercore-api-g79m.onrender.com/ping)
- **Prometheus Metrics:** [https://ledgercore-api-g79m.onrender.com/metrics](https://ledgercore-api-g79m.onrender.com/metrics)

---

## Architecture
[Client] → [FastAPI Gateway: rate limiter → circuit breaker → routing] → [Backend service]
                    ↓                               ↓
              [Redis: atomic bucket state]   [Prometheus/Grafana]

## Features
- Atomic, race-condition-free rate limiting via Redis Lua scripts
- API gateway with request forwarding
- Circuit breaker (Closed/Open/Half-Open) to prevent cascading failures
- Prometheus metrics + Grafana dashboards
- Load-tested with Locust; async I/O + connection pooling optimizations

## Performance

| Metric | Before (Sync Redis) | After (Async + Pooling) | Improvement |
| :--- | :--- | :--- | :--- |
| **Throughput (RPS)** | 321.9 RPS | 329.5 RPS | **+2.4%** |
| **Median Latency (p50)** | 2.0 ms | 2.0 ms | **0.0%** |
| **p95 Latency** | 6.0 ms | 4.0 ms | **-33.3%** |
| **p99 Latency** | 22.0 ms | 8.0 ms | **-63.6%** |

*Note: The major win of the async refactor and connection pooling was eliminating event-loop blocking and drastically flattening tail latency (p95 dropped by 33.3% and p99 dropped by 63.6% under sustained load).*

## Rate Limiter Resilience Benchmark
- **Offered Load:** ~329 RPS (100 concurrent Locust users)
- **Bucket Config:** `max_tokens = 10`, `refill_rate = 2/sec`
- **Enforcement Result:** 99.3% of requests correctly rejected with HTTP 429
- **Rejection Latency:** Median 2 ms, p95 4 ms
- **Takeaway:** Confirms atomic token bucket enforcement cleanly drops 150x burst traffic overloads at the gateway without latency degradation or backend exhaustion.

## Tech Stack
FastAPI · Redis · Docker · Prometheus · Grafana · Locust · Pytest

## Running Locally
```bash
docker compose up --build
curl http://localhost:8000/ping
