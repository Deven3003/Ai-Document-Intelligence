import os
import redis
from dotenv import load_dotenv

from pathlib import Path

# PROJECT_ROOT =Path(__file__).resolve().parents[2]
load_dotenv()

REDIS_URL =os.getenv("REDIS_URL")

if not REDIS_URL:
    raise RuntimeError("Redis URL is missing from project .env")

def get_redis_client() ->redis.Redis:
    """create a redis client using the configured connection URL"""
    return redis.Redis.from_url(
        REDIS_URL,
        decode_responses=True,
        socket_connect_timeout=5,
        socket_timeout=5,
        health_check_interval=30,
    )

def check_redis_connection()->bool:
    """Return True if Redis responds to PING."""
    client = get_redis_client()

    try:
        return bool(client.ping())
    finally:
        client.close()