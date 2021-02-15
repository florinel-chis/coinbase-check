#Check coinbase for potential buy/sell patterns

* Pull latest feed using pull.py


#Pull:
saves locally a json file, at specified granularity (900 = 15 minutes, 3600 = 1 hour)
```
python3 pull.py 900 FIL-EUR NU-EUR
```


#Check
checks for potential patterns.

This is for learning purposes, not indended to be used in other ways.
