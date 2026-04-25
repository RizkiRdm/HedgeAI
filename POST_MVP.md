# Post-MVP Development Roadmap

This document outlines the planned improvements and features for the next phase of CryptoHedgeAI development.

## 1. Advanced Analytics & Machine Learning
- **Sentiment Analysis v2:** Integrate LLM-based sentiment analysis for social media (X/Twitter, Farcaster).
- **Predictive Scoring:** Pilot a machine learning model to complement deterministic scorer tools.
- **Regime Detection:** Implement automatic market regime detection (Bull/Bear/Sideways) to adjust weights dynamically.

## 2. Execution Engine Enhancements
- **DEX Expansion:** Add support for more chains (Base, Arbitrum, Optimism) beyond Solana/BSC.
- **MEV Protection:** Implement Jito/Flashbots integration to minimize slippage and sandwich attacks.
- **Limit Orders:** Add support for DEX limit orders via Jupiter/OpenBook.

## 3. UI/UX & Monitoring
- **Real-time Charting:** Integrate TradingView charts into the dashboard.
- **Telegram Command Suite:** Expand `/panic` to include `/balance`, `/status`, and `/adjust-weights`.
- **Historical Analysis:** Add a "Backtest" tab to the dashboard to run Eval Agent simulations manually.

## 4. Operational Efficiency
- **Cloud Migration:** Transition from local dev to Hetzner/Oracle Cloud CX22.
- **Advanced Tax Management:** Automate profit distribution to secondary reserve wallets.
- **Security Audit:** Professional smart contract and gRPC bridge audit.

## 5. Risk Management v2
- **Dynamic Kelly:** Implement non-fixed Half-Kelly based on real-time volatility.
- **Multi-wallet Support:** Distribute capital across multiple wallets to mitigate counterparty risk.
