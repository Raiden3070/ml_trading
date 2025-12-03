import os
import sys
import datetime as dt

# Ensure project root is on sys.path when running from scripts/
ROOT = os.path.dirname(os.path.dirname(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from alpha_data import fetch_daily_close

def main():
    key = os.getenv("ALPHAVANTAGE_API_KEY")
    if not key:
        print("ALPHAVANTAGE_API_KEY not set", file=sys.stderr)
        sys.exit(1)
    sd = dt.datetime(2024, 1, 1)
    ed = dt.datetime(2024, 6, 30)
    for sym in ["AAPL", "MSFT", "GOOG"]:
        try:
            s = fetch_daily_close(sym, sd, ed, outputsize="compact")
            print(f"{sym}: fetched {len(s)} points; {s.index.min().date()} → {s.index.max().date()}")
        except Exception as e:
            print(f"{sym}: error: {e}")

if __name__ == "__main__":
    main()
