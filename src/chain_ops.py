from web3 import Web3
from web3.middleware import geth_poa_middleware
from src.config import Config
from src.utils import logger

class ChainManager:
    def __init__(self):
        self.w3 = Web3(Web3.HTTPProvider(Config.RPC_URL))
        if not self.w3.is_connected():
            raise ConnectionError("Failed to connect to RPC Node.")
        
        # Middleware for PoA chains (like Sepolia/Polygon)
        self.w3.middleware_onion.inject(geth_poa_middleware, layer=0)
        self.chain_id = self.w3.eth.chain_id

    def get_gas_metrics(self):
        """Returns EIP-1559 gas metrics in Gwei."""
        block = self.w3.eth.get_block("latest")
        base_fee = block["baseFeePerGas"]
        priority_fee = self.w3.eth.max_priority_fee
        
        # Calculate total max fee (Base + Priority)
        max_fee_gwei = self.w3.from_wei(base_fee + priority_fee, 'gwei')
        return float(max_fee_gwei), base_fee, priority_fee

    def execute_batch(self, payroll: list, base_fee: int, priority_fee: int):
        """Executes batched transactions with correct nonce management."""
        sender = Web3.to_checksum_address(Config.SENDER)
        current_nonce = self.w3.eth.get_transaction_count(sender)

        logger.info(f"🚀 Starting batch execution for {len(payroll)} recipients.")

        for i, entry in enumerate(payroll):
            try:
                recipient = Web3.to_checksum_address(entry['address'])
                amount_wei = self.w3.to_wei(entry['amount_eth'], 'ether')

                tx_params = {
                    'nonce': current_nonce + i,
                    'to': recipient,
                    'value': amount_wei,
                    'gas': 21000,
                    'maxFeePerGas': base_fee + priority_fee,
                    'maxPriorityFeePerGas': priority_fee,
                    'chainId': self.chain_id,
                    'type': '0x2'
                }

                signed_tx = self.w3.eth.account.sign_transaction(tx_params, Config.PRIVATE_KEY)
                tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
                
                logger.info(f"✅ Sent {entry['amount_eth']} ETH to {recipient[:6]}... | Hash: {self.w3.to_hex(tx_hash)}")
            
            except Exception as e:
                logger.error(f"❌ Transaction failed for {entry.get('address')}: {e}")

        logger.info("Batch execution cycle completed.")
