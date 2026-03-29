# PaperTradeX

A paper trading simulator built in Python. Practice buying and selling real US stocks using live market data — without risking a single rupee.

---

## Why I built this

I wanted to learn how stock trading works but obviously didn't want to lose money doing it. So I built this instead. You get $10,000 fake money to start, and you can buy/sell any real NYSE/NASDAQ stock and see how you would've done.

---

## What it does

- Start with $10,000 virtual balance
- Search any US stock ticker (AAPL, TSLA, NVDA, whatever)
- Buy shares at the real current market price
- Come back days later, see if you're up or down
- Sell whenever you want and track your P&L
- Full trade history so you can see every move you made
- Candlestick charts so you can actually look at the stock before buying

---

## Tech I used

- **Python** — everything is built in Python
- **yfinance** — pulls live stock data from Yahoo Finance
- **Streamlit** — turns the whole thing into a web app
- **Plotly** — for the candlestick charts
- **JSON** — saves your portfolio locally so it persists between sessions

---

## How to run it

Clone the repo and install dependencies:

```bash
pip install yfinance streamlit plotly
```

Run the CLI version:
```bash
python mainv1.py
```

Run the Streamlit UI:
```bash
streamlit run appv2.py
```

## Screenshots

<img width="1919" height="980" alt="Screenshot 2026-03-29 165811" src="https://github.com/user-attachments/assets/8a627d87-40eb-42fa-95cc-7e34b760d656" />
<img width="1919" height="980" alt="Screenshot 2026-03-29 165858" src="https://github.com/user-attachments/assets/7a443e3f-dba2-4484-a142-3842b79434b1" />


---

## What I learned building this

Honestly a lot. Designing the data structure from scratch, working with a real financial API, handling persistent storage, calculating weighted average buy price, and then converting the whole thing into a web app with Streamlit. Built the entire logic on paper before writing a single line of code.

---

## What's next

- Deploy it online so anyone can use it
- Add more chart types
- Portfolio performance graph over time

---

If you want to contribute or have ideas to make this better — feel free to reach out. 
