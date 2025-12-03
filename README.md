# ML trading Demo

A lightweight demo ML trading running on live Alpha Vantage daily close data. Includes:
- Alpha Vantage fetcher with on-disk cache (`.av_cache/`)
- Predict-today runner (`predict_today.py`)
- Streamlit web app (`streamlit_app.py`) to pick symbol/dates and see BUY/SELL/HOLD and charts

## Setup

1) Create/activate the project virtual environment :
- VS Code should auto-activate `.venv` in this folder. If not, create one:

```powershell
# from this folder
python -m venv .venv
.venv\Scripts\Activate.ps1
```

2) Install dependencies (pinned for consistent runs):

```powershell
pip install -r requirements.txt
```

3) Set your Alpha Vantage API key (PowerShell, per session):

```powershell
$env:ALPHAVANTAGE_API_KEY = "YOUR_KEY"
```

Alternatively for Streamlit Cloud, add this key in the app’s Secrets as `ALPHAVANTAGE_API_KEY`.

## Run a quick prediction in terminal

Train on GOOG 2023 and print the latest BUY/SELL/HOLD for the most recent trading day:

```powershell
.venv\Scripts\python.exe .\predict_today.py
```

## Run the Streamlit web app locally

```powershell
.venv\Scripts\python.exe -m streamlit run .\streamlit_app.py
```

Then open the printed URL (usually http://localhost:8501) and click "Train + Predict".


## Notes

- Data source: Alpha Vantage TIME_SERIES_DAILY (unadjusted close). Cached under `.av_cache/` per symbol.
- The model is a bagged randomized tree learner over technical indicators (SMA ratio, %B, MACD, PPO, Momentum), outputting {-1,0,1}.
- This code is for educational/demo purposes only and not financial advice.
