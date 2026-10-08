import os
from redis import Redis
from redis.exceptions import RedisError
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

#Redis Client
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
REDIS_DB = int(os.getenv("REDIS_DB", "0"))

redis=Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=REDIS_DB,
    decode_responses=True
)

#set value
def set_value(key,value):
    try:
        return redis.set(key,value)
    except RedisError as e:
        print("Error:",e)
        return False

#set value with TTl
def set_with_ttl(key,value,minutes):
    try:
        return redis.set(key,value,ex=minutes*60)
    except RedisError as e:
        print("Error:",e)
        return False

#get value
def get_value(key):
    try:
        return redis.get(key)
    except RedisError as e:
        print("Error:",e)
        return None

#Delete value
def delete(key):
    try:
        return redis.delete(key)
    except RedisError as e:
        print("Error:",e)
        return False

#increment
def increment(key):
    try:
        return redis.incr(key)
    except RedisError as e:
        print("Error:",e)
        return False

#Set TTL
def set_ttl(key,minutes):
    try:
        return redis.expire(key,minutes*60)
    except RedisError as e:
        print("Error:",e)
        return False

#get remaining TTL
def get_ttl(key):
    try:
        return redis.ttl(key)
    except RedisError as e:
        print("Error:",e)
        return None

#exists
def exists(key):
    try:
        return redis.exists(key)==1
    except RedisError as e:
        print("Error:",e)
        return False

