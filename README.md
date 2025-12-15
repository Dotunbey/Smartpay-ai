# ⚡ SmartPay AI Engine

**A fault-tolerant, gas-optimized Ethereum payment automaton.**

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Web3.py](https://img.shields.io/badge/Web3.py-EIP1559-green)](https://web3py.readthedocs.io/)

## 📖 Overview

SmartPay is a headless backend daemon designed to automate batch cryptocurrency payments (payroll, airdrops, vendor settlements). Instead of executing transactions immediately, it employs a **reactive monitoring agent** that builds a statistical model of the network's gas fees in real-time.

It executes payments only when current network fees drop below a dynamic threshold (e.g., 10% below the moving average), ensuring operational cost savings of **15-40%** compared to blind execution.

## 🏗 Architecture

The system operates on a continuous polling cycle:

1.  **Monitor:** Queries RPC nodes for `baseFeePerGas` and `priorityFee` every 30 seconds.
2.  **Analyze:** Updates an internal deque of historical gas data.
3.  **Optimize:** Compares current fees against a configurable Moving Average (MA).
4.  **Execute:** If conditions are met, loads the `payroll.csv` vector and broadcasts batched EIP-1559 transactions.

## 🚀 Features

-   **EIP-1559 Native:** Calculates optimal `maxFeePerGas` and `maxPriorityFeePerGas` automatically.
-   **Adaptive Sensitivity:** Uses statistical thresholds rather than hardcoded prices.
-   **Nonce Management:** Automatically manages transaction sequencing to prevent "stuck" transactions.
-   **Modular Design:** Separated logic for chain interaction, optimization engine, and config.
-   **Fault Tolerant:** Robust error handling for RPC disconnects and transaction reverts.

## 📂 Project Structure

```text
smartpay-ai/
├── src/
│   ├── engine.py       # Optimization logic (The "Brain")
│   ├── chain_ops.py    # Web3 interaction (The "Hands")
│   ├── config.py       # Env loader
│   └── utils.py        # CSV parsing & Logging
├── .env.example        # Secrets template
├── payroll.csv         # Payment target list
├── agent.py             # Entry point
└── requirements.txt    # Dependencies
```
## 🛠️ Installation & Setup 
1. Clone the Repository
```bash
git clone [https://github.com/YOUR_USERNAME/smartpay-ai.git](https://github.com/YOUR_USERNAME/smartpay-ai.git)
cd smartpay-ai
```
2. Install Dependencies
```bash
pip install -r requirements.txt
```
3. Configuration
Copy the example environment file:
```bash
cp .env.example .env
```
Edit .env and populate your keys:
```bash
RPC_URL=[https://sepolia.infura.io/v3/YOUR_KEY](https://sepolia.infura.io/v3/YOUR_KEY)
PRIVATE_KEY=0xYourPrivateKey
SENDER_ADDRESS=0xYourWalletAddress
MAX_GWEI_THRESHOLD=100
CHECK_INTERVAL=30
```
4. Define Payments
Edit payroll.csv to define who gets paid:
```bash
address,amount_eth
0xUser1Address...,0.05
0xUser2Address...,0.12
```
## 🏃 Usage
​Run the engine in your terminal:
```bash
python agent.py
```
What happens next: 
1. The bot initializes and validates the connection.
2. ​It begins a "Warmup Phase" (collecting 5 data points).
3. ​It logs the current Gas Price vs. the Target Price.
4. Once the price dips below the target, it processes the CSV and shuts down.

## ​⚠️ Disclaimer
​This software handles private keys and financial transactions.

​Always test on Sepolia/Goerli testnets first.

​Never commit your .env file to GitHub.
## ​🤝 Contribution
​Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
