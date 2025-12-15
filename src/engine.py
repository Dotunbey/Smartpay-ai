import collections
import statistics
import time
from src.utils import logger
from src.config import Config

class OptimizationEngine:
    def __init__(self, history_len=20, sensitivity=0.90):
        self.gas_history = collections.deque(maxlen=history_len)
        self.sensitivity = sensitivity
        
    def should_execute(self, current_gwei: float) -> bool:
        """
        Decides execution based on adaptive statistical threshold.
        Logic: Execute if current price is below N% of recent moving average.
        """
        self.gas_history.append(current_gwei)
        
        # Warmup period
        if len(self.gas_history) < 5:
            return False

        avg_gas = statistics.mean(self.gas_history)
        threshold_price = avg_gas * self.sensitivity

        if current_gwei <= threshold_price:
            logger.info(f"⚡ Trigger: Current {current_gwei:.2f} < Target {threshold_price:.2f} Gwei")
            return True
            
        logger.info(f"Waiting... Current: {current_gwei:.2f} | Target: {threshold_price:.2f} Gwei")
        return False
