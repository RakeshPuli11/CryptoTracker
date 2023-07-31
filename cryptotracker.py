import requests as rq
import tkinter as tk
from datetime import datetime


def tracker():
    crypto_symbols = ["BTC", "ETH", "LTC", "XRP", "ADA", "DOT", "BCH", "BNB", "LINK", "DOGE",
                      "MATIC", "XLM", "EOS", "USDT", "TRX", "XMR", "MIOTA", "VET", "ETC",
                      "XTZ", "ATOM"]
    fsyms = ",".join(crypto_symbols)
    api_url = f"https://min-api.cryptocompare.com/data/pricemultifull?fsyms={fsyms}&tsyms=USD,INR"
    response = rq.get(api_url).json()

    result_str = ""
    for i, symbol in enumerate(crypto_symbols):
        data = response["RAW"][symbol]
        usd_price = data["USD"]["PRICE"]
        inr_price = data["INR"]["PRICE"]
        result_str += f"{symbol}         >         USD {usd_price}       ,       INR {inr_price}\n"
        if i < len(crypto_symbols) - 1:
            result_str += "\n"

    # Clear the previous text and insert the new data
    text_widget.delete("1.0", tk.END)
    text_widget.insert(tk.END, result_str)

    time = datetime.now().strftime("%H:%M:%S")
    label_time.config(text="updated at : " + time)

    root.after(5000, tracker)  # Updates every 5 seconds (5000 milliseconds)


root = tk.Tk()
root.geometry("500x600")
root.title("CRYPTOCURRENCY TRACKER")

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
