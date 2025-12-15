import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    RPC_URL = os.getenv("RPC_URL")
    PRIVATE_KEY = os.getenv("PRIVATE_KEY")
    SENDER = os.getenv("SENDER_ADDRESS")
    MAX_THRESHOLD = float(os.getenv("MAX_GWEI_THRESHOLD", 100))
    INTERVAL = int(os.getenv("CHECK_INTERVAL", 30))

    @staticmethod
    def validate():
        if not all([Config.RPC_URL, Config.PRIVATE_KEY, Config.SENDER]):
            raise ValueError("Missing critical ENV variables.")
