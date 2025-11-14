# config.py
import os

META_APP_ID = os.getenv("META_APP_ID")
META_APP_SECRET = os.getenv("META_APP_SECRET")
META_ACCESS_TOKEN = os.getenv("META_ACCESS_TOKEN")

if not all([META_APP_ID, META_APP_SECRET, META_ACCESS_TOKEN]):
    raise RuntimeError("Meta API env vars not set")
