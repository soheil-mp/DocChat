from functools import lru_cache
from typing import Dict, Any
import redis

class CacheService:
    def __init__(self):
        self.redis_client = redis.Redis(host='localhost', port=6379, db=0)
        
    async def get_cached_response(self, query: str) -> Dict[str, Any]:
        return self.redis_client.get(query)
        
    async def cache_response(self, query: str, response: Dict[str, Any]):
        self.redis_client.setex(query, 3600, response)  # Cache for 1 hour 