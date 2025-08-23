"""
Redis integration example with LangChain
"""
import os
import sys

import redis
from dotenv import load_dotenv
from langchain.globals import set_llm_cache
from langchain_community.cache import RedisCache

# Load environment variables
load_dotenv()

def get_redis_url():
    """Get the Redis URL from environment variables"""
    redis_url = os.getenv("REDIS_URL", None)
    if not redis_url:
        print("❌ REDIS_URL not set! Please check your .env file.")
        sys.exit(1)
    return redis_url


def test_redis_connection():
    """Test Redis connection and basic operations"""

    redis_url = get_redis_url()
    print(f"🔗 Connecting to Redis: {redis_url}")

    try:
        # Connect to Redis
        r = redis.from_url(redis_url, decode_responses=True)

        # Test connection
        r.ping()
        print("✅ Redis connection successful!")

        # Basic operations
        r.set("test_key", "Hello from LangChain dev container!")
        value = r.get("test_key")
        print(f"📝 Stored and retrieved: {value}")

        # LangChain cache example
        r.hset("langchain_cache", "prompt_1", "This is a cached response")
        cached = r.hget("langchain_cache", "prompt_1")
        print(f"💾 Cache example: {cached}")

        # Clean up
        r.delete("test_key")
        r.delete("langchain_cache")
        print("🧹 Cleaned up test data")

        return True

    except redis.ConnectionError as e:
        print(f"❌ Redis connection failed: {e}")
        print("Make sure Redis container is running!")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def demo_langchain_redis_cache():
    """Demonstrate using Redis as LangChain cache"""
    try:

        # Set up Redis connection
        redis_url = get_redis_url()
        redis_client = redis.from_url(redis_url, decode_responses=True)

        # Set up Redis cache for LangChain (correct parameter name)
        cache = RedisCache(redis_=redis_client)
        set_llm_cache(cache)

        print("✅ LangChain Redis cache configured!")
        print("💡 Now your LLM calls will be cached in Redis")

        # Test the cache setup
        print("🧪 Testing cache setup...")
        test_key = "langchain:cache:test"
        redis_client.set(test_key, "Cache is working!")
        result = redis_client.get(test_key)
        print(f"📦 Cache test result: {result}")
        redis_client.delete(test_key)

        return True

    except ImportError as e:
        print(f"⚠️  LangChain Redis cache not available: {e}")
        print("This is normal - Redis cache is an optional feature")
        return False
    except Exception as e:
        print(f"❌ Error setting up LangChain cache: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Testing Redis integration...\n")

    # Test basic Redis connection
    if test_redis_connection():
        print("\n" + "="*50 + "\n")

        # Test LangChain Redis cache
        demo_langchain_redis_cache()

    print("\n🎉 Redis testing complete!")
