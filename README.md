# yapywrangler
Stock market historical data collection and management system, pulling data from the updated Yahoo Finance backend, 2018


Usage:

readExisting(symbols, end=None)
    Attempts to pull data from the /YPData/ folder.
    If a specified symbol does not have any data, creates a new get request and saves the data
    If data for specifed symbol does exist, makes sure it is the most up to dat day, and if not creates a new get request to update existing
    
    Returns dict

securityData(symbols, end, save, epoch)
    A direct get request with optional parameters to save

    Returns dict



data = readExisting(['MSFT'], end='2007-01-01')

data2 = collectData(symbols=['ADBE', 'AMD'], end='2010-01-01', save=True, epoch=False)
