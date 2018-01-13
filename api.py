import requests
import json
import timeit

# normalize string to make float variable
def remove_punc(str):
    return str.replace('$', '').replace(',', '')

# get price by symbol
def get_price(symbol):
    result = {}
    coin_data = requests.get('https://min-api.cryptocompare.com/data/pricemulti?fsyms={}&tsyms=ETH,USD,BTC'.format(symbol)).text
    # No API response
    if 'HasWarning' in coin_data:
        return None
    coin_data = json.loads(coin_data)

    for sym, price in coin_data[symbol].items():
        result[sym] = price

    return result

# get maicoin price, only support BTC, ETH, LTC
def get_maicoin_price(symbol, market_price):
    result = {}
    symbol = symbol.lower()
    coin_data = requests.get('http://exwd.csie.org:3333/maicoin/{}-usd'.format(symbol)).text
    coin_data = json.loads(coin_data)

    buy_price = float(remove_punc(coin_data['formatted_buy_price']))
    sell_price = float(remove_punc(coin_data['formatted_sell_price']))
    avg_price = float(remove_punc(coin_data['formatted_price']))

    # compare with market data
    buy_percentage = round(((buy_price - market_price) / market_price) * 100, 2) 
    sell_percentage = round(((market_price - sell_price) / market_price) * 100, 2)

    result = {'buy': buy_price, 'sell': sell_price, 'avg': avg_price, 'buy_p': buy_percentage,
        'sell_p': sell_percentage}

    return result

def collect_data(symbol):
    symbol = symbol.upper()    
    price_data = get_price(symbol)
    if price_data == None:
        return 'There is no data for the coin {}'.format(symbol)

    # format return message    
    result_message = symbol + '\n' + \
        '[USD] {}\n'.format(price_data['USD']) + \
        '[BTC] {}\n'.format(price_data['BTC']) + \
        '[ETH] {}\n'.format(price_data['ETH'])

    if symbol in ['BTC', 'ETH', 'LTC']:
        maicoin_price = get_maicoin_price(symbol, price_data['USD'])
        result_message = result_message + '\n[Maicoin]\n[Buy] ' + \
            str(maicoin_price['buy']) + ' +' + str(maicoin_price['buy_p']) + '%\n[Sell] ' + \
            str(maicoin_price['sell']) + ' -' + str(maicoin_price['sell_p']) + '%'

    return result_message.strip()

if __name__ == '__main__':
    start = timeit.default_timer()
    
    print(collect_data('btc'))
    print(collect_data('eth'))
    print(collect_data('ltc'))
    print(collect_data('ada'))
    
    end = timeit.default_timer()
    print("spend {} secs".format(end-start))
