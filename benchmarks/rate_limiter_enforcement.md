# Rate Limiter Enforcement Test

## Test Objective
Validate that the Redis Token Bucket middleware correctly blocks excessive traffic during a massive sudden spike without crashing or degrading response times.

## Test Setup
- **Config:** `max_tokens = 10`, `refill_rate = 2/sec`
- **Locust Load:** 100 concurrent users (spawn rate: 10/sec)
- **Offered Traffic:** ~329 RPS (Requests Per Second)

## Results
- **Total Requests:** ~37,500
- **Rejection Rate:** 99.3% (HTTP 429 Too Many Requests)
- **Median Latency:** 2 ms
- **p99 Latency:** 10 ms

## Key Takeaway
The rate limiter operates effectively under 150x overload, cleanly dropping malicious/unthrottled traffic at the gateway layer within 2ms without letting traffic overload downstream services.