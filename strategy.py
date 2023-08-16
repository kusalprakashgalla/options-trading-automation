import pandas as pd
import requests
from fyers_api import fyersModel

def tele_msg(display_string):
    base_url = 'https://api.telegram.org/botYOUR_BOT_TOKEN/sendMessage?chat_id=YOUR_CHAT_ID&text='
    requests.get(base_url + display_string)

def find_nearest_token(parValue, df):
    df_call = df.copy()
    df_call['ltp'] = df['ltp'].apply(lambda x: abs(x - parValue))
    token_call = df_call.sort_values(by='ltp').iloc[0:1].index.values
    return token_call

def get_res(symbol, fyersObj):
    data = {"symbols": symbol}
    res = fyersObj.quotes(data)
    return res['d'][0]['v']

def get_bid(symbol, fyersObj):
    data = {"symbols": symbol}
    res = fyersObj.quotes(data)
    return res['d'][0]['v']['bid']

def get_ask(symbol, fyersObj):
    data = {"symbols": symbol}
    res = fyersObj.quotes(data)
    return res['d'][0]['v']['ask']

def getLTP(symbol, fyersObj):
    data = {"symbols": symbol}
    res = fyersObj.quotes(data)
    return res['d'][0]['v']['lp']

def getQuote(symbol, fyersObj):
    data = {"symbols": symbol}
    res = fyersObj.quotes(data)
    new_series = pd.Series([res['d'][0]['n'], res['d'][0]['v']['lp'], res['d'][0]['v']['volume']],
                           index=df_ce_nifty.columns)
    new_series_df = new_series.to_frame().transpose()
    return new_series_df

def getReleventStrikes(spotltp, symbol, symbolOC, premium):
    df_ce_nifty = pd.DataFrame(columns=['symbol', 'ltp', 'volume'])
    df_pe_nifty = pd.DataFrame(columns=['symbol', 'ltp', 'volume'])
    for optn_type in ['CE', 'PE']:
        if optn_type == 'PE':
            pespotltp = spotltp * (1 + 0.03)
            filterSymbolOC = symbolOC[(symbolOC.OPT_TYPE == 'PE') & (symbolOC.STRIKE <= pespotltp) &
                                      (symbolOC.ScripName == symbol)].sort_values(by='STRIKE', ascending=False)
        else:
            cespotltp = spotltp * (1 - 0.03)
            filterSymbolOC = symbolOC[(symbolOC.OPT_TYPE == 'CE') & (symbolOC.STRIKE >= cespotltp) &
                                      (symbolOC.ScripName == symbol)].sort_values(by='STRIKE')

        x = filterSymbolOC[:49]['Symbol'].tolist()
        symbols = ""
        for i in x:
            symbols = f'{symbols}{i},'
        symbols = symbols[:-1]
        data = {"symbols": symbols}
        res = fyers.quotes(data)
        ltpdict = {}
        if 's' in res and res['s'] == 'ok':
            for i in res['d']:
                ltpdict.update({i['n']: i['v']['lp']})
                new_series = pd.Series([i['n'], i['v']['lp'], i['v']['volume']], index=df_ce_nifty.columns)
                new_series_df = new_series.to_frame().transpose()
                if optn_type == 'CE':
                    df_ce_nifty = pd.concat([df_ce_nifty, new_series_df], ignore_index=True)
                else:
                    df_pe_nifty = pd.concat([df_pe_nifty, new_series_df], ignore_index=True)

        intialValue = 100000
        filterStock = None
        for optsymbol, optltp in ltpdict.items():
            if abs(optltp - premium) < intialValue:
                intialValue = abs(optltp - premium)
                filterStock = optsymbol

    return [df_pe_nifty.iloc[find_nearest_token(premium, df_pe_nifty)],
            df_ce_nifty.iloc[find_nearest_token(premium, df_ce_nifty)]]

def checkStraddle(df_pe_bn_sell, df_ce_bn_sell):
    ceStrike = df_ce_bn_sell['symbol'].values[0].split('CE')[0].split('BANKNIFTY')[1][-5:]
    peStrike = df_pe_bn_sell['symbol'].values[0].split('PE')[0].split('BANKNIFTY')[1][-5:]

    if ceStrike <= peStrike:
        straddleFound = True
    else:
        straddleFound = False
    return straddleFound

def get_priceAndSL(startDate):
    tempVal = startDate.weekday()
    if tempVal == 0:
        price = 130
        SL = 35
    elif tempVal == 1:
        price = 100
        SL = 50
    elif tempVal == 2:
        price = 70
        SL = 70
    elif tempVal == 3:
        price = 40
        SL = 110
    else:
        print("No Trade Day")
        exit()
    return [price, SL]

def sellBN(sym, lot):
    order_id_buy = {
        "symbol": sym,
        "qty": 25 * lot,
        "type": marketOrder,
        "side": -1,
        "productType": "INTRADAY",
        "limitPrice": 0,
        "stopPrice": 0,
        "validity": "DAY",
        "disclosedQty": 0,
        "offlineOrder": "False",
        "stopLoss": 0,
        "takeProfit": 0
    }
    # Execute the order
    pass

def buyBN(sym, lot):
    order_id_buy = {
        "symbol": sym,
        "qty": 25 * lot,
        "type": marketOrder,
        "side": 1,
        "productType": "INTRADAY",
        "limitPrice": 0,
        "stopPrice": 0,
        "validity": "DAY",
        "disclosedQty": 0,
        "offlineOrder": "False",
        "stopLoss": 0,
        "takeProfit": 0
    }
    # Execute the order
    pass

def prem(strike, x):
    a = int(strike)
    # Calculate and return premium
    pass

# Initialize fyersModel with client_id and token
client_id = 'YOUR_CLIENT_ID'
token = 'YOUR_TOKEN'
fyers = fyersModel.FyersModel(client_id=client_id, token=token, log_path='LOG_PATH')

# Other parts of the code...
# ...

# Main execution
if __name__ == "__main__":
    # Your main logic here...
    pass
