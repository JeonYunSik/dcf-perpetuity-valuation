
# 📈 Intrinsic Value Screener

A simple Python script to calculate the intrinsic value of multiple tickers using the Gordon Growth Model (Perpetuity Growth Model).

---

## Features

- Fetches financial data automatically with `yfinance`
- Calculates Free Cash Flow (FCF) from Operating Cash Flow and CAPEX
- Projects 10 years of FCF and Terminal Value
- Computes intrinsic value per share and compares with the current price

---

## Tech Stack

- Python 3.x  
- yfinance  
- JSON  

---

## Formula

**Gordon Growth Model (Perpetuity Growth Model):**

```
Enterprise Value = PV(FCF for 10 years) + PV(Terminal Value)

Terminal Value = FCF * (1 + g) / (r - g)
```

- **Discount Rate:** US 10-Year Treasury Yield (example: 4.4%)  
- **Growth Rate:** 3% (adjustable)  
- **Projection Period:** 10 years + terminal value  

---

## Usage

1️⃣ Install dependencies:

```bash
pip install yfinance
```

2️⃣ Edit ticker list:

```python
tickers_json = '["AAPL", "KO", "CVX"]'
```

3️⃣ Run the script:

```bash
python intrinsic_value.py
```

4️⃣ Example output:

```
AAPL | DCF: 183.52, Current Price: 175.25, Ratio: 1.05
```

---

## Notes

- `yfinance` uses Yahoo Finance; sometimes data may be missing.  
- You can adjust the discount rate and growth rate for different scenarios.  
- CAPEX is treated as an absolute value for FCF calculation.  

---

## License

MIT License © 2025 Jeon Yunsik
