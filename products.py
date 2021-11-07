
import coinbasepro as cbp
import sys

if(len(sys.argv)>0):    
    quoteCurrency = sys.argv[1]
else:
    print("Usage: products.py EUR")
    sys.exit(1)


client = cbp.PublicClient()    


for k in client.get_products():
    if(k['quote_currency'] == quoteCurrency):
        print(k['id'])