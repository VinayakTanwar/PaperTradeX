# The oignal first version of the papertradex 
# CLI based less interactive than 2nd version 



import json
import os
import yfinance as yf
from datetime import date




def load_portfolio():
    data = {"balance": 10000, "holdings": {}, "trade_history": []}
    if os.path.exists("portfolio.json"):
        with open("portfolio.json", "r") as f:
            data = json.load(f)
    else:
        with open("portfolio.json", "w") as f:
            json.dump(data, f, indent=2)
    return data


def save_portfolio(data):
    with open("portfolio.json", "w") as f:
        json.dump(data, f, indent=2)


def get_stock_price(ticker):
    try:
        stock_tick = yf.Ticker(ticker)
        info = stock_tick.info
        current_price = info.get("currentPrice")
        return current_price
    except:
        return None



def buy_stock(ticker, quantity):
    today = date.today()
    current_price = get_stock_price(ticker)

    if current_price is None:
        print("Invalid ticker. Please try again.")
        return

    total_price = current_price * quantity
    data = load_portfolio()

    if data["balance"] >= total_price:
            # if user already owns this stock
            if ticker in data["holdings"]:
                old_qty = data["holdings"][ticker]["quantity"]
                old_price = data["holdings"][ticker]["buy_price"]
                new_avg = (old_qty * old_price + quantity * current_price) / (old_qty + quantity)
                data["holdings"][ticker]["quantity"] += quantity
                data["holdings"][ticker]["buy_price"] = new_avg
            else:
                data["holdings"][ticker] = {
                    "quantity": quantity,
                    "buy_price": current_price,
                    "date": str(today)
                }

            data["balance"] -= total_price
            save_portfolio(data)
            print(f"Successfully bought {quantity} shares of {ticker}!")
    else:
        print("Not enough balance.")




def sell_stock(ticker, quantity):
    data = load_portfolio()

    if ticker in data["holdings"]:
        if data["holdings"][ticker]["quantity"] >= quantity:
            current_price = get_stock_price(ticker)

            if current_price is None:
                print(f"Could not fetch price for {ticker}.")
                return

            buy_price = data["holdings"][ticker]["buy_price"]
            p_l = (current_price - buy_price) * quantity

            data["balance"] += current_price * quantity

            if quantity == data["holdings"][ticker]["quantity"]:
                del data["holdings"][ticker]
            else:
                data["holdings"][ticker]["quantity"] -= quantity
            trade = {
                "ticker": ticker,
                "qty": quantity,
                "buy_price": buy_price,
                "sell_price": current_price,
                "p_l": round(p_l, 2),
                "date": str(date.today())
            }
            data["trade_history"].append(trade)    

            save_portfolio(data)
            print(f"Sold {quantity} shares of {ticker}.")
            print(f"P&L on this trade: ${p_l:.2f}")
        else:
            print("Not enough quantity. You don't own that much.")
    else:
        print("Stock not in portfolio.")




def view_portfolio():
    data = load_portfolio()
    currbal = data["balance"]
    print(f"\nYour current balance is: ${currbal:.2f}")

    if not data["holdings"]:
        print("No stocks in portfolio.")
        return

    print("\n--- Holdings ---")
    for ticker in data["holdings"]:
        currprice = get_stock_price(ticker)

        if currprice is None:
            print(f"Could not fetch price for {ticker}.")
            continue

        buy_price = data["holdings"][ticker]["buy_price"]
        quantity = data["holdings"][ticker]["quantity"]
        p_l = (currprice - buy_price) * quantity

        print(f"{ticker} | Qty: {quantity} | Buy: ${buy_price:.2f} | Now: ${currprice:.2f} | P&L: ${p_l:.2f}")

def view_history():
    data = load_portfolio()
    if not data["trade_history"]:
        print("No trades yet.")
        return
    for trade in data["trade_history"]:
        print(f"{trade['date']} | {trade['ticker']} | Qty: {trade['qty']} | P&L: ${trade['p_l']}")        



if __name__ == "__main__":
    print("Welcome to Paper Trading!")

    while True:
        print("\n1. View Portfolio")
        print("2. Buy Stock")
        print("3. Sell Stock")
        print("4. View History")
        print("5. Exit")

        choice = input("\nEnter choice: ")

        if choice == "1":
            view_portfolio()
        elif choice == "2":
            ticker = input("Enter ticker symbol (e.g. AAPL): ").upper()
            quantity = int(input("Enter quantity: "))
            buy_stock(ticker, quantity)
        elif choice == "3":
            ticker = input("Enter ticker symbol: ").upper()
            quantity = int(input("Enter quantity to sell: "))
            sell_stock(ticker, quantity)
            
        elif choice == "4":
            view_history()  

        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Try again.")