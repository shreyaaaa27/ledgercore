-- KEYS[1] = bucket key (e.g. "bucket:client123")
-- ARGV[1] = max_tokens
-- ARGV[2] = refill_rate (tokens per second)
-- ARGV[3] = current timestamp (seconds, float)

local key = KEYS[1]
local max_tokens = tonumber(ARGV[1])
local refill_rate = tonumber(ARGV[2])
local now = tonumber(ARGV[3])

local bucket = redis.call("HMGET", key, "tokens", "last_refill")
local tokens = tonumber(bucket[1])
local last_refill = tonumber(bucket[2])

if tokens == nil then
    -- first request from this client: bucket starts full
    tokens = max_tokens
    last_refill = now
end

-- refill based on elapsed time
local elapsed = now - last_refill
local refill_amount = elapsed * refill_rate
tokens = math.min(max_tokens, tokens + refill_amount)

local allowed = 0
if tokens >= 1 then
    tokens = tokens - 1
    allowed = 1
end

redis.call("HMSET", key, "tokens", tokens, "last_refill", now)
redis.call("EXPIRE", key, 3600)  -- clean up inactive buckets after 1hr

return allowed