# MIT License © 2025 Jeon Yunsik
# See LICENSE file for details.

import yfinance as yf
import json

def get_cash_flow(ticker):
    """
    Fetches Free Cash Flow (FCF) for the given ticker.
    FCF = Operating Cash Flow - |Capital Expenditure|
    """
    stock = yf.Ticker(ticker)
    cashflow = stock.cashflow
    if cashflow.empty:
        raise ValueError("No cash flow data available")
    ocf = cashflow.loc['Operating Cash Flow'].iloc[0] if 'Operating Cash Flow' in cashflow.index else 0
    capex = cashflow.loc['Capital Expenditure'].iloc[0] if 'Capital Expenditure' in cashflow.index else 0
    return ocf - abs(capex)

def get_shares_outstanding(ticker):
    """
    Fetches number of shares outstanding for the given ticker.
    """
    stock = yf.Ticker(ticker)
    info = stock.info
    shares = info.get('sharesOutstanding')
    if shares is None:
        raise ValueError("No shares outstanding data available")
    return float(shares)

def get_current_price(ticker):
    """
    Fetches the latest closing price for the given ticker.
    """
    stock = yf.Ticker(ticker)
    hist = stock.history(period="1d")
    if hist.empty:
        raise ValueError("No current price data available")
    return hist['Close'][-1]

def dcf_value_per_share(fcf, discount_rate, growth_rate, years, shares):
    """
    Calculates intrinsic value per share using a DCF model with
    a constant growth rate (Gordon Growth Model).
    """
    pv_fcf = sum([fcf * ((1 + growth_rate) ** t) / ((1 + discount_rate) ** t) for t in range(1, years + 1)])
    terminal_value = (fcf * (1 + growth_rate) ** (years + 1)) / (discount_rate - growth_rate)
    pv_terminal = terminal_value / ((1 + discount_rate) ** years)
    enterprise_value = pv_fcf + pv_terminal
    return enterprise_value / shares

def intrinsic_values(tickers):
    """
    Calculates intrinsic values and price ratios for a list of tickers.
    """
    discount_rate = 0.044  # example: 4.4%
    growth_rate = 0.03     # 3%
    years = 10
    results = {}
    for t in tickers:
        try:
            fcf = get_cash_flow(t)
            shares = get_shares_outstanding(t)
            current_price = get_current_price(t)
            iv = dcf_value_per_share(fcf, discount_rate, growth_rate, years, shares)
            ratio = iv / current_price if current_price != 0 else None
            results[t] = {
                "DCF Value": round(iv, 2),
                "Current Price": round(current_price, 2),
                "Value/Price": round(ratio, 2) if ratio is not None else "N/A"
            }
        except ValueError as e:
            results[t] = f"Error: {e}"
        except Exception:
            results[t] = "Error: Data retrieval failed"
    return results

if __name__ == "__main__":
    # Example ticker list; you can edit this JSON string
    tickers_json = '["AAPL", "AXP", "KO", "BAC", "CVX", "OXY", "MCO", "KHC", "CB"]'
    tickers = json.loads(tickers_json)

    values = intrinsic_values(tickers)
    for ticker, value in values.items():
        if isinstance(value, dict):
            print(f"{ticker} | DCF: {value['DCF Value']}, Current Price: {value['Current Price']}, Ratio: {value['Value/Price']}")
        else:
            print(f"{ticker} | {value}")
