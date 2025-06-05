# StockINR

This repository contains a simple proof-of-concept intraday trading simulator
for the Indian stock market. The goal is to demonstrate how a large language
 model (LLM) such as OpenAI's GPT series or Google's Gemini can be integrated
 with a paper-trading workflow. The app can connect to a real broker if an API key is supplied or run
in a dummy mode for evaluation.

## Features

- Dummy broker interface for paper trading with real-time prices
- Optional Zerodha broker integration if Zerodha credentials are provided
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

Copy `.env.example` to `.env` and fill in your credentials. The key settings ar
`LLM_PROVIDER` (`openai` or `gemini`) and the matching API key (`OPENAI_API_KEY`
or `GEMINI_API_KEY`). To trade using Zerodha provide `ZERODHA_API_KEY`,
`ZERODHA_API_SECRET` and `ZERODHA_ACCESS_TOKEN`. After configuring the
environment, run:

```bash
python -m src.app
```

The application will run continuously, making LLM driven decisions every minute
during Indian market hours. Trades are logged in `trades.db`.
