import logging
from django_redis import get_redis_connection

logger = logging.getLogger(__name__)

def get_redis_cache_metrics():
    try:
        # Connect to Redis
        redis_conn = get_redis_connection("default")
        info = redis_conn.info()

        # Extract hit/miss stats
        hits = info.get("keyspace_hits", 0)
        misses = info.get("keyspace_misses", 0)
        total_requests = hits + misses

        # Calculate hit ratio
        hit_ratio = hits / total_requests if total_requests > 0 else 0

        # Log metrics
        logger.info(f"Redis Cache Metrics - Hits: {hits}, Misses: {misses}, Hit Ratio: {hit_ratio:.2f}")

        return {
            "hits": hits,
            "misses": misses,
            "hit_ratio": hit_ratio
        }

    except Exception as e:
        logger.error(f"Error retrieving Redis metrics: {e}")
        return {"hits": 0, "misses": 0, "hit_ratio": 0}
