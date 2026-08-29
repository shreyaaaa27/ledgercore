# LedgerCore Benchmarks

## Rate Limiter Enforcement
- Config: 10 burst, 2 tokens/sec refill
- Load: 329 RPS offered (Locust, 100 users)
- Result: 99% correctly rejected (429), median latency 2ms, p95 4ms
- Confirms atomic enforcement holds under 150x overload with no latency degradation

## Throughput Capacity (rate limit raised for testing)
- Load: 100 users, spawn rate 10/s, 2 min
- RPS: 329.5
- p50 / p95 / p99 latency: 2ms / 4ms / 8ms
- Total Requests: 37,640 (0 failures)
- Average Latency: 2.31ms