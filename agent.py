import time
from src.config import Config
from src.utils import logger, load_payroll
from src.chain_ops import ChainManager
from src.engine import OptimizationEngine

def main():
    try:
        Config.validate()
        chain = ChainManager()
        engine = OptimizationEngine(sensitivity=0.90) # Pays when 10% cheaper than average
        
        payroll_data = load_payroll('payroll.csv')
        if not payroll_data:
            logger.error("Payroll list is empty. Exiting.")
            return

        logger.info("🤖 SmartPay Engine Initialized. Monitoring Membrane...")

        while True:
            # 1. Fetch Data
            current_gwei, base_fee, priority_fee = chain.get_gas_metrics()
            
            # 2. Analyze & Decide
            if engine.should_execute(current_gwei):
                chain.execute_batch(payroll_data, base_fee, priority_fee)
                logger.info("🎉 Workflow Complete. Shutting down daemon.")
                break
            
            # 3. Wait
            time.sleep(Config.INTERVAL)

    except KeyboardInterrupt:
        logger.info("🛑 Manual Shutdown.")
    except Exception as e:
        logger.critical(f"🔥 Fatal Error: {e}")

if __name__ == "__main__":
    main()
