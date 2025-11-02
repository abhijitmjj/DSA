import sys
import logging
from pathlib import Path

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

for path in sys.path:
    logger.info(f"Current sys.path entry: {Path(path)}")
