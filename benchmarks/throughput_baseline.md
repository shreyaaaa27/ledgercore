# Throughput Baseline Test

## Objective
Measure unthrottled API throughput and latency baseline for the gateway architecture under steady concurrent load.

## Setup
- **Config:** `max_tokens = 1000`, `refill_rate = 500/sec` (Limits temporarily raised)
- **Load Test:** 100 concurrent users via Locust

## Results
- **Total Requests:** 37,599
- **Failures:** 0 (0.0% failure rate)
- **Sustained Throughput:** 321.9 RPS
- **Median Latency:** 2 ms
- **p95 Latency:** 6 ms
- **p99 Latency:** 22 ms
- **Average Latency:** 2.96 ms

## Key Takeaway
Establishes baseline unthrottled service capacity: processing over 320 requests/sec with a 100% success rate and p95 latency under 6ms.