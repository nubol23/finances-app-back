import os

import dotenv

from .default import *  # noqa: F401, E402, F403, F405

dotenv.load_dotenv(f"{BASE_DIR}/.env")  # noqa F405

os.environ["DJANGO_DEBUG"] = "True"
os.environ["DJANGO_TESTING"] = "True"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.getenv("DB_NAME", "finances"),
        "USER": os.getenv("DB_USER", "postgres"),
        "PASSWORD": os.getenv("DB_PASS", "postgres"),
        "HOST": os.getenv("DB_HOST", "localhost"),
        "PORT": os.getenv("DB_PORT", 5432),
        "ATOMIC_REQUESTS": True,
        "TEST": {"NAME": "test_finances"},
    }
}

PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]

DEFAULT_FILE_STORAGE = "inmemorystorage.InMemoryStorage"
