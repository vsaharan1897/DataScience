import pandas as pd


def read_file(file):
    data=pd.read_csv(file)
    data=data[1:]
    return data


def filter_company(data,company):
    filtered_data = data[data['symbol'] == company]
    return filtered_data

def read_stock_data(symbol):
    data = pd.read_csv('psa.csv')  #### Contact for CSV File
    stock_data = data[data['symbol'] == symbol]
    return stock_data['close'].tolist()

def read_ticker_symbols():
    data = pd.read_csv('securities.csv')
    symbols = data.set_index('Ticker symbol')['Security'].to_dict()
    return symbols

# ticker_symbol=read_ticker_symbols()
# stock_name=ticker_symbol['AAPL']
# print(stock_name)
# test_key=[key for key, val in ticker_symbol.items() if val==stock_name]
# test_key2=test_key[0]
# test_key3="'"+test_key2+"'"
# print(test_key3)

def find_best_stock_profit(prices):
    buy_day, sell_day = 0, 0
    max_profit = 0.0

    for i in range(len(prices)):
        for j in range(i + 1, len(prices)):
            profit = prices[j] - prices[i]
            if profit > max_profit:
                max_profit = profit
                buy_day = i
                sell_day = j

    return buy_day, sell_day, max_profit

def best_stock():
    ticker_symbols = read_ticker_symbols()
    best_stock_name = None
    best_profit = 0.0
    best_buy_day = 0
    best_sell_day = 0

    for symbol in ticker_symbols.keys():
        # stock_data=read_file('psa.csv')
        prices = read_stock_data(symbol)
        if len(prices) > 0:
            buy_day, sell_day, profit = find_best_stock_profit(prices)
            if profit > best_profit:
                best_stock_name = ticker_symbols[symbol]
                best_stock_symbol=[key for key, val in ticker_symbols.items() if val==best_stock_name][0]
                symbol_for_filter="'"+best_stock_symbol+"'"
                best_profit = profit
                best_buy_day = buy_day
                best_sell_day = sell_day
    return [best_stock_name, best_stock_symbol, symbol_for_filter, best_profit,best_buy_day,best_sell_day]            


stock_data=read_file('psa.csv')
Winning_stock=best_stock()
#['Priceline.com Inc', 'PCLN', "'PCLN'", 1402.940003, 108, 1725]

winning_company_name=Winning_stock[0]
winning_company_symbol=Winning_stock[1]
symbol_for_filter=Winning_stock[2]
winning_profit=Winning_stock[3]
winning_buy_day=Winning_stock[4]
winning_sell_day=Winning_stock[5]
best_stock_data=filter_company(stock_data,winning_company_symbol)
best_buy_date = best_stock_data.iloc[winning_buy_day]['date']
best_sell_date = best_stock_data.iloc[winning_sell_day]['date']
print(f"Best stock to buy: {winning_company_name} ({winning_company_symbol}) on day: {winning_buy_day} ({best_buy_date}) and sell on day: {winning_sell_day} ({best_sell_date}) with profit of {winning_profit}")




##Output

#Best stock to buy: Priceline.com Inc (PCLN) on day: 108 (6/9/2010) and sell on day: 1725 (11/8/2016) with profit of 1402.940003
