import requests
import json
import timeit

# normalize string to make float variable
def remove_punc(str):
    return str.replace('$', '').replace(',', '').strip()

def add_plus(pct):
    if '-' not in pct:
        pct = '+' + pct
    return '(' + pct + '%)'

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

def get_price_full(symbol):
    result = {}
    info = {}
    coin_data = requests.get('https://min-api.cryptocompare.com/data/pricemultifull?fsyms={}&tsyms=USD,BTC,ETH'.format(symbol)).json()

    for sym, data in coin_data['RAW'][symbol].items():
        result[sym] = data['PRICE']

    usd_pct = coin_data['DISPLAY'][symbol]['USD']['CHANGEPCT24HOUR']
    btc_pct = coin_data['DISPLAY'][symbol]['BTC']['CHANGEPCT24HOUR']
    eth_pct = coin_data['DISPLAY'][symbol]['ETH']['CHANGEPCT24HOUR']

    usd_pct = add_plus(usd_pct)
    btc_pct = add_plus(btc_pct)
    eth_pct = add_plus(eth_pct)

    return result, usd_pct, btc_pct, eth_pct

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

def collect_data(symbol, enable_maicoin=False):
    symbol = symbol.upper()    
    # price_data = get_price(symbol)
    price_data, usd_pct, btc_pct, eth_pct = get_price_full(symbol)
    if price_data == None:
        return 'There is no data for the coin {}'.format(symbol)

    # format return message    
    result_message = symbol + '\n' + \
        '[USD] {}'.format(price_data['USD']) + ' ' + usd_pct + \
        '\n[BTC] {}'.format(price_data['BTC']) + ' ' + btc_pct + \
        '\n[ETH] {}'.format(price_data['ETH']) + ' ' + eth_pct + '\n'

    if symbol in ['BTC', 'ETH', 'LTC'] and enable_maicoin:
        maicoin_price = get_maicoin_price(symbol, price_data['USD'])
        result_message = result_message + '\n[Maicoin]\n[Buy] ' + \
            str(maicoin_price['buy']) + ' +' + str(maicoin_price['buy_p']) + '%\n[Sell] ' + \
            str(maicoin_price['sell']) + ' -' + str(maicoin_price['sell_p']) + '%'

    return result_message.strip()

if __name__ == '__main__':
    start = timeit.default_timer()

    # print(get_price_full('BTC'))
    
    # print(collect_data('btc'))
    # print(collect_data('eth'))
    # print(collect_data('ltc'))
    print(collect_data('xrp'))
    # print(collect_data('ada'))
    
    end = timeit.default_timer()
    print("spend {} secs".format(end-start))
