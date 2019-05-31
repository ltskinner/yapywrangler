# yapywrangler

### Update 05/31/2019:
This package was initally released over a year ago in the wake of Yahoo Finance updating their backend API.
At that time, the only means of retrieving data required gnarly parsing and took noticable time to process.
Because of this, on the initial release, a local file system for caching parts of retrieved files was used 
to cut down on processing time.

Since then, Yahoo Finance has revised their API resulting in much faster response times, and negating the 
need for the caching system.

Due to this, yapywrangler has been revised to include just its core request functionality.


## Install:

    pip install yapywrangler
    

## Usage:
    
    from yapywrangler import get_yahoo_data
    
    stock_ticker = "MSFT"
    data = get_yahoo_data(stock_ticker, start_date='2006-03-26', end_date='2019-05-29')
    msft = pd.DataFrame(data)
    
start_date defaults to 2000-01-01
end_date defaults to now

### Data Format:

    {
        'timestamp': [1559136600, 1559223000, 1559321620], 
        'date': ['2019-05-29', '2019-05-30', '2019-05-31'], 
        'open': [29.0, 28.399999618530273, 27.56999969482422], 
        'high': [29.31999969482422, 28.559999465942383, 28.360000610351562], 
        'low': [27.729999542236328, 27.600000381469727, 27.5], 
        'close': [28.09000015258789, 28.030000686645508, 27.940000534057617], 
        'volume': [99969600, 65072900, 40126715]
    }

Data structure preferences are very personal and project specific, so returned data is in a generic
dictionary format. 
