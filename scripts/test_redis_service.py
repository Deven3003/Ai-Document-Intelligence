from src.cache.redis_client import check_redis_connection

if check_redis_connection():
    print("Redis connection is working")
else:
    print("Redis conection LOST")