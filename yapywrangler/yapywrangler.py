
import os
import requests
import time
import csv
import datetime

"""
NEED TO THINK ABOUT TAKING DIRECTORY ARGUMENTS
people cloning in wont want to dev in the clone, taking external directory arg would be good
"""
"""
Will want to make this a class so I can make sessin with servers as self.session = resp.sess()
this will cut down ssl sync times
"""




def dataOrganizer(raw):
    try: 
        data = {
            'date': [],
            'open': [],
            'high': [],
            'low': [],
            'close': [],
            'volume': []
        }

        ct = 0
        for j in raw:
            if "amount" not in j:
                each = j.split(',')
                if ct == 0:
                    each[0] = each[0].strip("[{")
                buffer = [  each[0].strip('"date":'), 
                            each[1].strip('"open":'), 
                            each[2].strip('"high":'), 
                            each[3].strip('"low":'), 
                            each[4].strip('"close":'), 
                            each[5].strip('"volume":').strip('}]')]

                #sequence to catch null, nu, na, nan values
                run = nullCatch(buffer)

                if run:
                    finalForm(data, [buffer], epoch=True)
                    
            ct+=1

        return data

    except Exception as e:
        print(e)
    
# OK
def getReq(sym, end):
    try:
        r = requests.get("https://finance.yahoo.com/quote/" + sym + "/history?period1=" + end + "&period2=" + str(int(time.time())) + "&interval=1d&filter=history&frequency=1d")
        lvl1 = (str(r.content).split("HistoricalPriceStore")[1]).split(',"isPending"')[0]
        return lvl1.split('{"prices":')[1].split('},{')
    except:
        #if there is another year to bump up, it runs again, else returns empty list
        if ((int(end) + 31536000) < int(time.time())):
            new = str(int(end) + 31536000)
            getReq(sym, new)
        else:
            print("[-] NO DATA AVAILABLE [-]")
            return []

# OK
def writeCsv(sym, data):
    directory = os.getcwd() + '/YPData/'
    try:
        os.stat(directory)
    except:
        os.mkdir(directory)
    writelist = [['date', 'open', 'high', 'low', 'close', 'volume']]
    for x in range(0, len(data['open'])):
        writelist.append([data['date'][x], data['open'][x], data['high'][x], data['low'][x], data['close'][x], data['volume'][x]])


    with open(directory + sym.upper() + '_historical.csv', 'w', newline="") as f:
        writer = csv.writer(f, delimiter=",")
        for line in writelist:
            writer.writerow(line)
    
    print('[+]', sym.upper(), 'saved [+]')

def readExisting(symbols, end=None):
    #reads from path and tries to open csv
    #   if not existing call collect data
    #reads the csv and searches back for a day that is less than the given end date
    #returns the data
    data = {}
    if end != None:
        dt = datetime.datetime.strptime(end, '%Y-%m-%d')
        end = str(int(time.mktime(dt.timetuple())))
        for sym in symbols:
            data[sym] = {
                'date': [],
                'open': [],
                'high': [],
                'low': [],
                'close': [],
                'volume': []
            }
            buffer = []
            backboard = False
            try:
                directory = os.getcwd() + '/YPData/' + sym.upper() + '_historical.csv'
                with open(directory, 'r') as f:
                    infile = csv.reader(f)
                    for line in infile:
                        if line[0] > end:
                            buffer.append(line)
                        else:
                            backboard = True
                        


            except Exception as e:
                #print(e)
                backboard == False
            
            if backboard == False:
                getdata = securityData([sym], save=True, epoch=False)
                data[sym] = getdata[sym]

            else:
                for i in buffer[0]:
                    data[sym][i] = []
                del buffer[0] #removes headers


                #if most recent day is more than a day old
                if (int(time.time()) - int(buffer[0][0])) > 86400:
                    getdata = securityData([sym], save=True, epoch=False)
                    data[sym] = getdata[sym]
                else:
                    finalForm(data[sym], buffer)

    else:
        for sym in symbols:
            data[sym] = {
                'date': [],
                'open': [],
                'high': [],
                'low': [],
                'close': [],
                'volume': []
            }
            buffer = []
            try: 
                directory = os.getcwd() + '/YPData/' + sym.upper() + '_historical.csv'
                with open(directory, 'r') as f:
                    infile = csv.reader(f)
                    for line in infile:
                        buffer.append(line)
            
                for i in buffer[0]:
                    data[sym][i] = []
                del buffer[0]
                
                
                #if most recent day is more than a day old
                if (int(time.time()) - int(buffer[0][0])) > 86400:
                    getdata = securityData([sym], save=True, epoch=False)
                    data[sym] = getdata[sym]
                
                else:
                    finalForm(data[sym], buffer)

            except Exception as e:
                #print(e)
                getdata = securityData([sym], save=True, epoch=False)
                daa[sym] = getdata[sym]
            


    return data

def securityData(symbols, end=None, save=False, epoch=True):
    #unless specified, farthest back date is Jan 1 2000
    # converts user input to epoch time
    if end != None:
        dt = datetime.datetime.strptime(end, '%Y-%m-%d')
        end = str(int(time.mktime(dt.timetuple())))
    else:
        end="946684800"

    #try to read in existing
    # takes the first day and if today is more than one days length ahead of it, continue in CollectData
    # else, reads in the existing file 

    data = {}
    for sym in symbols:
        parsed = getReq(sym, end)
        data[sym] = dataOrganizer(parsed)


    if save:
        for sym in symbols:
            writeCsv(sym, data[sym])
    
    if epoch == False:
        for sym in symbols:
            for d in range(0, len(data[sym]['date'])):
                data[sym]['date'][d] = time.strftime('%Y-%m-%d', time.localtime(int(data[sym]['date'][d])))


    return data

def nullCatch(buffer):
    for x in buffer:
        try:
            t = float(x)
        except:
            try:
                x.is_int()
            except:
                return False
    return True

def finalForm(data, buffer, epoch=False):
    for i in buffer:
        if epoch:
            data['date'].append(int(i[0]))
        else:
            data['date'].append(time.strftime('%Y-%m-%d', time.localtime(int(i[0]))))

        data['open'].append(i[1])
        data['high'].append(i[2])
        data['low'].append(i[3])
        data['close'].append(i[4])
        data['volume'].append(i[5])

    return data 

"""
data = readExisting(['MSFT', 'AMD', 'GGB'], end='2007-01-01')
print(data['GGB']['date'][4])
print(data['AMD']['date'][4])
print(data['MSFT']['date'][4])

start2 = datetime.datetime.now()
#                                    'Jul 9, 2009'
data2 = securityData(symbols=['ADBE', 'AMD'], end='2010-01-01', save=True, epoch=False)
print(datetime.datetime.now() - start2)

for i in data2:
    print(i)
print(data2)
#print('no end arg', len(data['ADBE']['open']))
print('w/ end arg', len(data2['ADBE']['open']))

"""
