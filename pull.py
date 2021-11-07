import sys
import os
import json
import coinbasepro as cbp


if(len(sys.argv)>1):
    granularityVal = sys.argv[1]
    symbol = sys.argv[2:]
else:
    client = cbp.PublicClient()    
    products = client.get_products()
    symbol = []
    granularityVal = '3600'
    for p in products:
        if(p['quote_currency']=='EUR'):
            symbol.append(p['id'])
    

def pullCoinbaseData(symbol):
    client = cbp.PublicClient()    
    phistory = client.get_product_historic_rates(symbol,granularity=granularityVal)


    if(len(phistory)>0):
        oDir = './coinbase'
        if(not os.path.isdir(oDir)):
            os.mkdir(oDir)        
        filename='coinbase/'+symbol+'-'+str(granularityVal)+'.json'

        with open(filename, 'w', encoding='utf-8') as f:
            f.write(json.dumps(phistory, indent=4, default=str))
            print(filename)

list(map(lambda x:pullCoinbaseData(x),symbol))