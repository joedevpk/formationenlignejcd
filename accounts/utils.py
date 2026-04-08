from django.core.cache import cache

#  Nombre max de tentatives
MAX_ATTEMPTS = 5

#  durée blocage (secondes)
BLOCK_TIME = 300  # 5 minutes


def is_blocked(ip):
    attempts = cache.get(ip, 0)
    return attempts >= MAX_ATTEMPTS


def add_attempt(ip):
    attempts = cache.get(ip, 0) + 1
    cache.set(ip, attempts, timeout=BLOCK_TIME)


def reset_attempts(ip):
    cache.delete(ip)