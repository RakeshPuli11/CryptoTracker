import requests as rq
import tkinter as tk
from datetime import datetime


def tracker():
    crypto_symbols = ["BTC", "ETH", "LTC", "XRP"]  # Add more symbols as needed
    fsyms = ",".join(crypto_symbols)
    api_url = f"https://min-api.cryptocompare.com/data/pricemultifull?fsyms={fsyms}&tsyms=USD,INR"
    response = rq.get(api_url).json()

    result_str = ""
    for symbol in crypto_symbols:
        data = response["RAW"][symbol]
        usd_price = data["USD"]["PRICE"]
        inr_price = data["INR"]["PRICE"]
        result_str += f"{symbol}: USD {usd_price}, INR {inr_price}\n"

    label_price.config(text=result_str)

    time = datetime.now().strftime("%H:%M:%S")
    label_time.config(text="updated at : " + time)

    root.after(5000, tracker)  # Update every 5 seconds (5000 milliseconds)


root = tk.Tk()
root.geometry("600x400")
root.title("CRYPTOCURRENCY TRACKER")

# Change the background and text colors
root.config(bg="black")
f1 = ("poppins", 20, "bold")
f2 = ("poppins", 18, "bold")
f3 = ("poppins", 21, "bold")

label = tk.Label(root, text="Cryptocurrency prices",
                 font=f1, fg="white", bg="black")
label.pack(pady=21)

label_price = tk.Label(root, font=f2, fg="white", bg="black")
label_price.pack(pady=21)

label_time = tk.Label(root, font=f3, fg="white", bg="black")
label_time.pack(pady=21)

tracker()
root.mainloop()
