import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
import numpy as np
import requests
import json
import matplotlib
import mplcursors
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime

matplotlib.use("TkAgg")


# API methods
# information about a cryptocurrency
def crypto_info(type):
    request = requests.get("https://api.coingecko.com/api/v3/coins/{}".format(type))
    return request.json()


# price of the cryptocurrency in specified interval
def crypto_price_range(coin, interval):
    request = requests.get("https://api.coingecko.com/api/v3/coins/{}/"
                           "market_chart?vs_currency=usd&days={}".format(coin, interval))
    return request.json()


# status of the cryptocurrency API
def api_status():
    status = requests.get("https://api.coingecko.com/api/v3/ping")
    return status


# App classes
# window with choice of graph interval
class ChoiceWin(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master=master)
        self.geometry("200x200")
        message_label = tk.Label(self, text="Select coin type")
        message_label.pack()
        coin_type = tk.StringVar(self)
        coin_options = ttk.OptionMenu(self, coin_type, coins[0], *coins)
        coin_options.pack()

        message_label = tk.Label(self, text="Select time range")
        message_label.pack()
        button_a = tk.Button(self, text="1 day", pady=5, padx=5)
        button_a.bind("<Button>", lambda e: PlotWin(self, 1, coin_type.get()))
        button_a.pack(fill='x')

        button_b = tk.Button(self, text="7 days", pady=5, padx=5)
        button_b.bind("<Button>", lambda e: PlotWin(self, 7, coin_type.get()))
        button_b.pack(fill='x')

        button_c = tk.Button(self, text="30 days", pady=5, padx=5)
        button_c.bind("<Button>", lambda e: PlotWin(self, 30, coin_type.get()))
        button_c.pack(fill='x')

# window with price change graph
class PlotWin(tk.Toplevel):
    def __init__(self, master, time, coin):
        super().__init__(master=master)
        global label

        if time == 1:
            message = "Buy price change: 1 day"
        elif time == 7:
            message = "Buy price change: 7 days"
        else:
            message = "Buy price change: 30 days"
        high = 0
        low = np.inf

        try:
            info = crypto_price_range(coin, time)
        except:
            label["text"] = "API currently not operational\nConnect to the internet or try again later"
            master.destroy()
        else:
            list_buy = []
            list_date = []
            for i in range(len(info["prices"])):
                price = info["prices"][i][1]
                unix_date = info["prices"][i][0]
                unix_date /= 1000
                unix_date += 7200
                human_date = datetime.utcfromtimestamp(unix_date).strftime("%d.%m %H:%M")
                list_buy.append(price)
                list_date.append(human_date)
                if price < low:
                    low = price
                if price > high:
                    high = price
            first_price = info["prices"][0][1]
            last_price = info["prices"][-1][1]
            change_percent = ((last_price - first_price) / first_price) * 100

            data_message = "Low: {}, High: {}\nChange percentage: {}%".format(round(low, 4), round(high, 4),
                                                                              change_percent)

            figure = Figure(figsize=(8, 6), dpi=100)
            plot_prices = figure.add_subplot(1, 1, 1)
            plot_prices.plot(list_date, list_buy)
            plot_prices.set_xlabel("Time")
            plot_prices.set_ylabel("Price")
            plot_prices.tick_params(axis="x", which="both", bottom=False, top=False, labelbottom=False)
            plot_label = tk.Label(self, text=message + "\n" + data_message)
            plot_label.pack()
            canvas = FigureCanvasTkAgg(figure, self)
            canvas.get_tk_widget().pack()
            label["text"] = "Showing graph"

            mplcursors.cursor(plot_prices)

# App methods
# add cryptocurrency amount to the wallet
def add_to_wallet():
    global my_wallet
    global label

    try:
        if float(entry_amount.get()) <= 0:
            label["text"] = "Amount cant be below or equal zero"
        else:
            list_of_coins = []
            for coin, val in my_wallet.items():
                list_of_coins.append(coin)

            if entry_type.get() in list_of_coins:
                wallet_data = my_wallet[entry_type.get()]
                wallet_data = float(wallet_data)
                to_add = float(entry_amount.get()) + wallet_data
                to_add = str(to_add)
                my_wallet.update({entry_type.get(): to_add})
                wallet = ",".join("{}: {}".format(k, v) for k, v in my_wallet.items())
                label["text"] = "added {} more {} to wallet\nCurrent wallet contents:\n{}" \
                    .format(entry_amount.get(), entry_type.get(), wallet)

            else:
                my_wallet[entry_type.get()] = entry_amount.get()
                wallet = ",".join("{}: {}".format(k, v) for k, v in my_wallet.items())
                label["text"] = "added to wallet\n\nCurrent wallet contents:\n{}.".format(wallet)
    except:
        label['text'] = "Please input correct cryptocurrency amount"


# reset the wallet
def reset_wallet():
    global my_wallet
    global label

    question = messagebox.askyesno("Notice", "Are you sure you want to reset your wallet?", icon="warning")

    if question:
        my_wallet = {}
        label["text"] = "Wallet reset"


# save the wallet to a file
def save_wallet():
    global my_wallet
    global label

    question = messagebox.askyesno("Notice", "Are you sure you want to save ?\nSaving will overwrite the data",
                                   icon="warning")

    if question:
        with open("wallet_file.json", "w") as json_file:
            json.dump(my_wallet, json_file)
        label["text"] = "Wallet saved"


# upload the wallet from a file
def upload_wallet():
    global my_wallet

    with open("wallet_file.json") as json_file:
        data = json.load(json_file)

    my_wallet = data

    label["text"] = "Wallet loaded"


# Show the value of the wallet
def wallet_value():
    global my_wallet
    global label
    global coins

    wallet_sum = 0
    compare_value = 0
    error = False

    try:
        api_status()
    except:
        label["text"] = "API currently not operational\nConnect to the internet or try again later"
    else:
        for coin, val in my_wallet.items():

            if coin not in coins:
                error = True
                break

            info_price_range = crypto_price_range(coin, 1)
            coin_info = crypto_info(coin)

            wallet_val = float(val)
            first_price = info_price_range["prices"][0][1]
            first_price = float(first_price)
            current_price = coin_info["market_data"]["current_price"]["usd"]
            current_price = float(current_price)

            to_add = wallet_val * current_price

            wallet_sum += to_add

            difference = (wallet_val * current_price) - (wallet_val * first_price)
            compare_value += difference

        if error:
            label["text"] = "Error: The wallet doesn't support your cryptocurrency or please name it accordingly"
        else:
            wallet = ",".join("{}: {}".format(k, v) for k, v in my_wallet.items())
            compare_value = round(compare_value, 3)

            label["text"] = "your current wallet value: {} USD\n\nDiffrence in value based on your wallet and prices " \
                            "from 24his:\n {} USD\n your wallet:\n {}".format(wallet_sum, compare_value, wallet)


# change amount of the cryptocurrencies in wallet
def Change_wallet():
    global my_wallet
    global label
    list_of_coins = []

    try:
        if float(entry_amount.get()) < 0:
            label["text"] = "Amount cant be below or equal zero"
        else:
            for coin, val in my_wallet.items():
                list_of_coins.append(coin)

            if entry_type.get() in list_of_coins:
                my_wallet.update({entry_type.get(): entry_amount.get()})
                if my_wallet[entry_type.get()] == "0":
                    my_wallet.pop(entry_type.get(), None)
                wallet = ",".join("{}: {}".format(k, v) for k, v in my_wallet.items())
                if wallet == "":
                    label["text"] = "Wallet changed\nWallet is empty"
                else:
                    label["text"] = "Wallet changed\nCurrent wallet contents:\n{}".format(wallet)

            else:
                label["text"] = "First add an item to wallet to change it"
    except:
        label["text"] = "Please input correct cryptocurrency amount"


# Main
if __name__ == "__main__":
    # wallet file
    my_wallet = {}

    root = tk.Tk()

    root.title("Wallet")

    # supported cryptocurrencies
    coins = ["bitcoin", "dogecoin", "ethereum", "ripple", "litecoin"]

    entry_amount_label = tk.Label(root, text="Enter your crypto currency amount")
    entry_amount_label.pack()

    # cryptocurrency amount entry
    entry_amount = tk.Entry(root, width=50)
    entry_amount.pack()

    entry_type_label = tk.Label(root, text="Specify crypto currency")
    entry_type_label.pack()

    # cryptocurrency type option menu
    entry_type = tk.StringVar(root)
    entry_type_option_menu = ttk.OptionMenu(root, entry_type, coins[0], *coins)
    entry_type_option_menu.pack()

    # buttons
    # adds to wallet
    button1 = tk.Button(root, text="add to wallet", command=add_to_wallet, pady=5, padx=5)
    button1.pack(fill="x")

    # Change wallet
    button7 = tk.Button(root, text="Change value in your wallet", command=Change_wallet, padx=5, pady=5)
    button7.pack(fill="x")

    # upload existing wallet button
    button4 = tk.Button(root, text="Upload last wallet", command=upload_wallet, padx=5, pady=5)
    button4.pack(fill="x")

    # show wallet value button
    button5 = tk.Button(root, text="Wallet value in USD", command=wallet_value, padx=5, pady=5)
    button5.pack(fill="x")

    # saves wallet to json button
    button3 = tk.Button(root, text="Save your wallet \n Warning!: saving will override existing data",
                        command=save_wallet)
    button3.pack(fill="x")

    # reset wallet button
    button6 = tk.Button(root, text="Reset wallet", command=reset_wallet, padx=5, pady=5)
    button6.pack(fill="x")

    # show price graph button
    button8 = tk.Button(root, text="Show price change graph", padx=5, pady=5)
    button8.bind("<Button>", lambda e: ChoiceWin(root))
    button8.pack(fill="x")

    # exits program
    exit_button = tk.Button(root, text="Exit Program", command=root.quit, padx=5, pady=5)
    exit_button.pack(fill="x")

    # Notice
    notice_bar = tk.Label(root, text="Notice:")
    notice_bar.pack()

    # Label
    label = tk.Label(root, text="hello")
    label.pack()

    root.mainloop()
