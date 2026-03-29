# The stremlit version work on any browser more ineractive andgui based 


import streamlit as st
import plotly.graph_objects as go
import yfinance as yf
from mainv1 import load_portfolio, save_portfolio, buy_stock, sell_stock, get_stock_price

st.title("Welcome To PaperTradeX")
st.subheader("By Vinayak")

st.write(f"Your current balance is ${load_portfolio()['balance']:.2f}")

page = st.sidebar.selectbox("Navigate", ["Portfolio", "Buy", "Sell", "History"])

if page == "Portfolio":
    data = load_portfolio()
    st.subheader("Your Holdings")

    if not data["holdings"]:
        st.write("No stocks in portfolio.")
    else:
        for ticker in data["holdings"]:
            currprice = get_stock_price(ticker)

            if currprice is None:
                st.error(f"Could not fetch price for {ticker}.")
                continue

            buy_price = data["holdings"][ticker]["buy_price"]
            quantity = data["holdings"][ticker]["quantity"]
            p_l = (currprice - buy_price) * quantity

            st.metric(
                label=ticker,
                value=f"${currprice:.2f}",
                delta=f"${p_l:.2f}"
            )

elif page == "Buy":
    data = load_portfolio()
    st.subheader("Buy Stock")

    ticker = st.text_input("Enter ticker symbol (e.g. AAPL)").upper()
    quantity = st.number_input("Enter quantity", min_value=1, step=1)

    if ticker:
        price = get_stock_price(ticker)
        if price:
            st.write(f"Current price: ${price:.2f}")
            st.write(f"Total cost: ${price * quantity:.2f}")

            # Candlestick chart
            df = yf.download(ticker, period="1mo", interval="1d", auto_adjust=True)
            df.columns = df.columns.get_level_values(0)
            if not df.empty:
                fig = go.Figure(data=[go.Candlestick(
                    x=df.index,
                    open=df['Open'],
                    high=df['High'],
                    low=df['Low'],
                    close=df['Close']
                )])
                fig.update_layout(
                    title=f"{ticker} - Last 30 Days",
                    xaxis_rangeslider_visible=False
                )
                st.plotly_chart(fig)

            if st.button("Buy"):
                buy_stock(ticker, int(quantity))
                st.success(f"Successfully bought {int(quantity)} shares of {ticker}!")
                st.rerun()
        else:
            st.error("Invalid ticker. Please try again.")

elif page == "Sell":
    data = load_portfolio()
    st.subheader("Sell Stock")

    if not data["holdings"]:
        st.write("No stocks to sell.")
    else:
        ticker = st.selectbox("Select stock to sell", list(data["holdings"].keys()))
        owned_qty = data["holdings"][ticker]["quantity"]
        st.write(f"You own {owned_qty} shares of {ticker}")

        quantity = st.number_input("Enter quantity to sell", min_value=1, max_value=owned_qty, step=1)

        if st.button("Sell"):
            sell_stock(ticker, int(quantity))
            st.success(f"Sold {int(quantity)} shares of {ticker}!")
            st.rerun()

elif page == "History":
    data = load_portfolio()
    st.subheader("Trade History")

    if not data["trade_history"]:
        st.write("No trades yet.")
    else:
        for trade in data["trade_history"]:
            p_l = trade['p_l']
            color = "🟢" if p_l >= 0 else "🔴"
            st.write(f"{color} {trade['date']} | {trade['ticker']} | Qty: {trade['qty']} | Buy: ${trade['buy_price']:.2f} | Sell: ${trade['sell_price']:.2f} | P&L: ${p_l:.2f}")



