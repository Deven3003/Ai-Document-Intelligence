import os
from dotenv import load_dotenv
import redis

load_dotenv()

redis_url = os.getenv("REDIS_URL")

if not redis_url:
    raise RuntimeError("REDIS URL is not found in .env")

client =redis.Redis.from_url(
    redis_url,
    decode_responses=True,
    socket_connect_timeout=5,
    socket_timeout=5,
)

try:
    print("Redis PING:",client.ping())
    print("Redis connection successful !")
except redis.RedisError as exc:
    print(f"Redis onnection Failed:{type(exc).__name__}:{exc}")
finally:
    client.close()