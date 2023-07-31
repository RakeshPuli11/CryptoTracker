import requests as rq
import tkinter as tk
from datetime import datetime
import sqlite3


def creating_table():
    con = sqlite3.connect("cryptocurrency.db")
    my_cursor = con.cursor()
    my_cursor.execute(
        '''CREATE TABLE IF NOT EXISTS prices(id INTEGER PRIMARY KEY AUTOINCREMENT, symbol TEXT, usd_price REAL, inr_price REAL)''')
    con.commit()
    con.close()


def insert_prices(symbol, usd_price, inr_price):
    con = sqlite3.connect("cryptocurrency.db")
    my_cursor = con.cursor()
    my_cursor.execute(
        '''INSERT INTO prices(symbol, usd_price, inr_price) VALUES(?,?,?)''', (symbol, usd_price, inr_price))
    con.commit()
    con.close()


def get_data_from_api():
    crypto_symbols = ["BTC", "ETH", "LTC", "XRP", "ADA", "DOT", "BCH", "BNB", "LINK", "DOGE",
                      "MATIC", "XLM", "EOS", "USDT", "TRX", "XMR", "MIOTA", "VET", "ETC",
                      "XTZ", "ATOM"]
    fsyms = ",".join(crypto_symbols)
    api_url = f"https://min-api.cryptocompare.com/data/pricemultifull?fsyms={fsyms}&tsyms=USD,INR"
    response = rq.get(api_url).json()
    return response["RAW"]


def display_data_in_gui(data):
    result_str = ""
    for symbol in data:
        symbol_data = data[symbol]
        if "USD" in symbol_data and "INR" in symbol_data:
            usd_price = symbol_data["USD"]["PRICE"]
            inr_price = symbol_data["INR"]["PRICE"]
            result_str += f"{symbol}         >         USD {usd_price}       ,       INR {inr_price}\n\n"

    text_widget.delete("1.0", tk.END)
    text_widget.insert(tk.END, result_str)

    time = datetime.now().strftime("%H:%M:%S")
    label_time.config(text="updated at : " + time)


def update_data_in_db(data):
    for symbol in data:
        symbol_data = data[symbol]
        if "USD" in symbol_data and "INR" in symbol_data:
            usd_price = symbol_data["USD"]["PRICE"]
            inr_price = symbol_data["INR"]["PRICE"]
            insert_prices(symbol, usd_price, inr_price)


def display():
    con = sqlite3.connect("cryptocurrency.db")
    my_cursor = con.cursor()
    my_cursor.execute('''SELECT symbol, usd_price, inr_price FROM prices''')
    rows = my_cursor.fetchall()
    for k in rows:
        print(k)


def tracker():
    data = get_data_from_api()
    display_data_in_gui(data)
    update_data_in_db(data)

    root.after(5000, tracker)  # Updates every 5 seconds (5000 milliseconds)
    display()


root = tk.Tk()
root.geometry("500x600")
root.title("CRYPTOCURRENCY TRACKER")

# Create the database and table
creating_table()

root.config(bg="black")
f1 = ("poppins", 20, "bold")
f2 = ("poppins", 12, "bold")
f3 = ("poppins", 18, "bold")

label = tk.Label(root, text="Cryptocurrency prices",
                 font=f1, fg="white", bg="black")
label.pack(pady=15)

text_widget = tk.Text(root, font=f2, fg="white", bg="black")
text_widget.pack(pady=5)

label_time = tk.Label(root, font=f3, fg="white", bg="black")
label_time.pack(pady=5)

tracker()

root.mainloop()
