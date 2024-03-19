import yfinance as yf
import json
from datetime import datetime

data = {
    "budget": 100000000,
    "stock_list": {},
    # stock_list is a dictionary to store owned stock
    # each key is stock_name
    # value of that key is a list contain 2 values: number_to_buy and average_price
    "transaction_history": []
    # transaction_history is a list store transaction_history
    # each element is a list contain data, action, stock_name, price, number_to_buy,
}

def reset():
    data = {
        "budget": 10000,
        "stock_list": {},
        "transaction_history": []
    }
    with open("data.json", "w") as f:
        json.dump(data, f)


def get_stock_price(stock_name):
    # return real-time price of a given stock
    ticker = yf.Ticker(stock_name)
    current_price = ticker.history(period='1d')['Close'].iloc[-1]
    return current_price

def buy_stock(stock_name, number_to_buy):
    # load currently owned stock to data
    with open("data.json","r") as f:
        data = json.load(f)

    #calculate amount need for the purchase and check if the budget is enough for that purchase
    stock_price = get_stock_price(stock_name)
    amount_needed = stock_price * number_to_buy
    if (amount_needed > data["budget"]):
        print("Your budget is not enough for the transaction")
        return
    
    #update budget when the purcase is succesful
    data["budget"] -= amount_needed

    #update data file, which store information about owned stocks
    if (data["stock_list"].get(stock_name) is None):
        data["stock_list"][stock_name] = [number_to_buy, stock_price]
    else:
        already_owned, average_price = data["stock_list"][stock_name]
        new_owned = already_owned + number_to_buy
        new_average = (already_owned*average_price + stock_price*number_to_buy)/new_owned
        data["stock_list"][stock_name] = [new_owned, new_average]

    #update transaction_history
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    data["transaction_history"].append([current_time, "Buy", stock_name, stock_price, number_to_buy])


    #rewrite data in json file
    with open("data.json", "w") as f:
        json.dump(data, f)

    with open("data.json","r") as f:
        data = json.load(f)

    print(data)
    

def sell_stock(stock_name, number_to_sell):
    # load currently owned stock to data
    with open("data.json","r") as f:
        data = json.load(f)

    # check if quantity of shares owned is enough to sell
    if data["stock_list"].get(stock_name) is None:
        share_owned = 0
    else:
        share_owned = data["stock_list"][stock_name][0]

    if share_owned < number_to_sell:
        print
        print("Do not have enough quantity of shares to sell. Please re-enter name of stock and quantity to sell")
        return
    
    stock_price = get_stock_price(stock_name)
    #update budget when the sell is succesful
    data["budget"] += stock_price * number_to_sell

    #update data file, which store information about owned stocks

    data["stock_list"][stock_name][0] -= number_to_sell
    if data["stock_list"][stock_name][0] == 0:
        del data["stock_list"][stock_name]

    #update transaction_history
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    data["transaction_history"].append([current_time, "Sell", stock_name, stock_price, number_to_sell])


    #rewrite data in json file
    with open("data.json", "w") as f:
        json.dump(data, f)

    with open("data.json","r") as f:
        data = json.load(f)

    print(data)


import pandas as pd

def main():
    # buy_stock("TSLA", 20);
    # buy_stock("AAPL", 10);
    # buy_stock("MSFT", 3);

    with open('data.json', 'r') as file:
        json_data = json.load(file)

    # Extract the "stock_list" part from the data
    stock_data = json_data['stock_list']

    # Convert the stock_data into a list of dictionaries
    stock_list = [{'Stock': stock, 'Quantity': values[0], 'Price': values[1]} for stock, values in stock_data.items()]

    # sell_stock("TSLA", 10)



    # Create DataFrame from the list of dictionaries
    stock_df = pd.DataFrame(stock_list)
    print(stock_df)


if __name__ == "__main__":
    main()