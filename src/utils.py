import logging
import csv
from typing import List, Dict

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger("SmartPay")

def load_payroll(filepath: str) -> List[Dict]:
    """Parses CSV payroll file into structured dicts."""
    try:
        with open(filepath, mode='r') as f:
            return list(csv.DictReader(f))
    except FileNotFoundError:
        logger.error(f"Payroll file {filepath} not found.")
        return []
