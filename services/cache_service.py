import redis
import json
import logging
from config import Config

class CacheService:
    def __init__(self):
        self.config = Config()
        self.redis_client = None
        
        try:
            self.redis_client = redis.from_url(self.config.REDIS_URL)
            # Test connection
            self.redis_client.ping()
            logging.info("Redis connected")
        except Exception as e:
            logging.error(f"Redis connection failed: {e}")
    
    def get(self, key):
        """Get value from cache"""
        if not self.redis_client:
            return None
        
        try:
            value = self.redis_client.get(key)
            return json.loads(value) if value else None
        except Exception as e:
            logging.error(f"Cache get failed: {e}")
            return None
    
    def set(self, key, value, expire=3600):
        """Set value in cache with expiration"""
        if not self.redis_client:
            return False
        
        try:
            self.redis_client.setex(
                key, 
                expire, 
                json.dumps(value)
            )
            return True
        except Exception as e:
            logging.error(f"Cache set failed: {e}")
            return False
    
    def get_session_data(self, session_id):
        """Get session data"""
        return self.get(f"session:{session_id}")
    
    def set_session_data(self, session_id, data, expire=7200):
        """Set session data (2 hour default)"""
        return self.set(f"session:{session_id}", data, expire)
    
    def increment_rate_limit(self, identifier, window=3600):
        """Increment rate limit counter"""
        if not self.redis_client:
            return 1
        
        try:
            key = f"rate_limit:{identifier}"
            current = self.redis_client.incr(key)
            if current == 1:
                self.redis_client.expire(key, window)
            return current
        except Exception as e:
            logging.error(f"Rate limit increment failed: {e}")
            return 1