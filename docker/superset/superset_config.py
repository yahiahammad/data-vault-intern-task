import os

# Signs sessions/CSRF tokens. Superset refuses to start without one.
SECRET_KEY = os.environ["SUPERSET_SECRET_KEY"]

# Superset's OWN metadata DB: dashboards, charts, users, saved DB connections.
# Unrelated to the data-vault postgres — that gets added later, as a
# "Database" connection inside the Superset UI, not here.
SQLALCHEMY_DATABASE_URI = (
    "postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}".format(
        user=os.environ["SUPERSET_DB_USER"],
        password=os.environ["SUPERSET_DB_PASSWORD"],
        host=os.environ["SUPERSET_DB_HOST"],
        port=os.environ["SUPERSET_DB_PORT"],
        db=os.environ["SUPERSET_DB_NAME"],
    )
)

# --- Redis-backed caching: the actual point of this file ---
REDIS_HOST = os.environ.get("REDIS_HOST", "redis")
REDIS_PORT = os.environ.get("REDIS_PORT", "6379")

CACHE_CONFIG = {
    "CACHE_TYPE": "RedisCache",
    "CACHE_DEFAULT_TIMEOUT": 300,  # seconds a cached result is served before Superset re-queries
    "CACHE_KEY_PREFIX": "superset_",
    "CACHE_REDIS_HOST": REDIS_HOST,
    "CACHE_REDIS_PORT": REDIS_PORT,
    "CACHE_REDIS_DB": 1,
}
# DATA_CACHE_CONFIG is specifically the chart/dashboard query-result cache —
# this is the setting that makes "dashboards don't re-query on every load" true.
DATA_CACHE_CONFIG = CACHE_CONFIG
