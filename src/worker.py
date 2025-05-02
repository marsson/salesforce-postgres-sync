import logging
import subprocess
from config.config import Config


logger = logging.getLogger(__name__)


def start_rq_worker():
    logger.info("starting redis queue worker")
    subprocess.run([
        "rq", "worker",
        "--url", f"redis://:{Config.REDIS_PASSWORD}@{Config.REDIS_HOST}:{Config.REDIS_PORT}",
        Config.QUEUE_NAME
    ])
