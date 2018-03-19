# yapywrangler

    pip install yapywrangler
    
    
Stock market historical data collection and management system, pulling data from the updated Yahoo Finance backend, 2018


Usage:


    data = securityData(symbols, end=None, save=False, epoch=True)

symbols = [], takes list [] of symbols to pull data for. note, non-existant symbols are not handled well, working on solution to this.
    
end = 'YYYY-MM-DD', specifies the furthest back day to look, defaults to 2000-01-01
    
save = False, optional flag for whether to save the downloaded data for later use in readExisting()
    
epoch = True, flag to determine if epoch time or YYYY-MM-DD time will be returned to user
    
returns dictionary with each [symbol] as primary key to list of each days stats


    data = readExisting(symbols, end=None, epoch=False)

symbols = [], takes list [] of symbols to pull data for. note, non-existant symbols are not handled well, working on solution to this.
    
end = 'YYYY-MM-DD', specifies the furthest back day to look, defaults to 2000-01-01
    
epoch = True, flag to determine if epoch time or YYYY-MM-DD time will be returned to user
    
returns dictionary with each [symbol] as primary key to list of each days stats

--------------------------------------------------------------------------------------------------

Sample Usage:

data = readExisting(['MSFT'], end='2007-01-01')

data2 = collectData(symbols=['ADBE', 'AMD'], end='2010-01-01', save=True, epoch=False)

output:
    data['MSFT'] = [
        [date, high, low, open, close, volume], 
        [], 
        [], 
        []
    ]
