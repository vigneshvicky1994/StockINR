# StockINR

This repository contains a simple proof-of-concept intraday trading simulator
for the Indian stock market. The goal is to demonstrate how a large language
 model (LLM) such as OpenAI's GPT series or Google's Gemini can be integrated
 with a paper-trading workflow. The app can connect to a real broker if an API key is supplied or run
in a dummy mode for evaluation.

## Features

- Dummy broker interface for paper trading with real-time prices
- Optional real broker stub if `BROKER_API_KEY` is set
- SQLite database to log all trades
- LLM-driven decision engine to choose buy/sell/hold actions
- Automated scheduler that runs during market hours
- Command line app in `src/app.py`

## Requirements

- Python 3.10+
- `openai` or `google-generativeai` depending on which LLM provider you use
- `yfinance` and `schedule` packages

Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Choose the LLM provider via the `LLM_PROVIDER` environment variable (`openai` or
`gemini`) and set the corresponding API key (`OPENAI_API_KEY` or
`GEMINI_API_KEY`). Optionally export `BROKER_API_KEY` to route trades to a real
broker implementation. Then run:

```bash
python -m src.app
```

The application will run continuously, making LLM driven decisions every minute
during Indian market hours. Trades are logged in `trades.db`.
