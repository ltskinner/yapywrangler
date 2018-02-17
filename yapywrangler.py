
import os
import requests
import bs4 as bs
import calendar
import time
import csv
import datetime


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
            #print(j)
            if "amount" not in j:
                each = j.split(',')
                if ct ==0:
                    each[0] = each[0].strip("[{")
                buffer = [  each[0].strip('"date":'), 
                            each[1].strip('"open":'), 
                            each[2].strip('"high":'), 
                            each[3].strip('"low":'), 
                            each[4].strip('"close":'), 
                            each[5].strip('"volume":').strip('}]')]

                #print(buffer)

                run = True
                for x in buffer:
                    try:
                        t = float(x)
                    except:
                        try:
                            x.is_int()
                        except:
                            run = False

                if run:
                    data['date'].append(buffer[0])
                    data['open'].append(buffer[1])
                    data['high'].append(buffer[2])
                    data['low'].append(buffer[3])
                    data['close'].append(buffer[4])
                    data['volume'].append(buffer[5])
                    
            ct+=1

        return data

    except Exception as e:
        print(e)
    
def getReq(sym, end):
    try:
        r = requests.get("https://finance.yahoo.com/quote/" + sym + "/history?period1=" + end + "&period2=" + str(int(time.time())) + "&interval=1d&filter=history&frequency=1d")
        shart = (str(r.content).split("HistoricalPriceStore")[1]).split(',"isPending"')[0]
        return shart.split('{"prices":')[1].split('},{')
    except:
        #if there is another year to bump up, it runs again, else returns empty list
        if ((int(end) + 31536000) < int(time.time())):
            new = str(int(end) + 31536000)
            getReq(sym, new)
        else:
            print("[-] NO DATA AVAILABLE [-]")
            return []


def writeCsv(sym, data):
    directory = os.getcwd() + '/YPData/'
    #print(directory)
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
            #writer.write('\n')
    
    print('[+]', sym.upper(), 'Saved. [+]')

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
            data[sym] = {}
            buffer = []
            backboard = False
            try:
                directory = '/YPData/' + sym.upper() + '_historical.csv'
                with open(directory, 'r') as f:
                    infile = csv.reader(f)
                    for line in infile:
                        if line[0] > end:
                            buffer.append(line)
                        else:
                            backboard = True
            except:
                backboard == False
            
            if backboard == False:
                getdata = collectData([sym], save=True)
                data[sym] = getdata[sym]
                print('called collectData')

            else:
                for i in buffer[0]:
                    data[sym][i] = []
                
                del buffer[0]

                for i in buffer:
                    data[sym]['date'].append(time.strftime('%Y-%m-%d', time.localtime(int(i[0]))))
                    data[sym]['open'].append(i[1])
                    data[sym]['high'].append(i[2])
                    data[sym]['low'].append(i[3])
                    data[sym]['close'].append(i[4])
                    data[sym]['volume'].append(i[5])

    else:
        for sym in symbols:
            data[sym] = {}
            buffer = []
            exists = True
            try: 
                directory = '/YPData/' + sym.upper() + '_historical.csv'
                with open(directory, 'r') as f:
                    infile = csv.reader(f)
                    for line in infile:
                        buffer.append(line)
            

                for i in buffer[0]:
                    data[sym][i] = []
                
                del buffer[0]

                for i in buffer:
                    data[sym]['date'].append(time.strftime('%Y-%m-%d', time.localtime(int(i[0]))))
                    data[sym]['open'].append(i[1])
                    data[sym]['high'].append(i[2])
                    data[sym]['low'].append(i[3])
                    data[sym]['close'].append(i[4])
                    data[sym]['volume'].append(i[5])

            except:
                getdata = collectData([sym], save=True)
                data[sym] = getdata[sym]
                print('called collectData')
                time.sleep(10)
            


    return data



def collectData(symbols, end=None, save=False, epoch=True):
    #unless specified, farthest back date is Jan 1 2008
    # converts user input to epoch time
    if end != None:
        dt = datetime.datetime.strptime(end, '%Y-%m-%d')
        end = str(int(time.mktime(dt.timetuple())))
    else:
        end="1199145600"

    #try to read in existing
    # takes the first day and if today is more than one days length ahead of it, continue in CollectData
    # else, reads in the existing file 

    #need to make this dynamic, may want to incorporate collectData(daysback) type deal then figure out that date
    #                    will also need to make some buffers and maintain local list of live symbols to reduce symbols?

    #make http handler with urllib here, pass to yahoo req, make single session so we arent reconnection ssl each time.
    #have a feeling this is the mian limiter
    #spoof user agent for maybe server priority?
    #see about turning this into a direct json 
    data = {}
    for sym in symbols:
        parsed = getReq(sym, end)
        #divvied = parsed #.split('},{')
        data[sym] = dataOrganizer(parsed)

    if save:
        for sym in symbols:
            writeCsv(sym, data[sym])
    
    if epoch == False:
        for sym in symbols:
            for d in range(0, len(data[sym]['date'])):
                data[sym]['date'][d] = time.strftime('%Y-%m-%d', time.localtime(int(data[sym]['date'][d])))


    return data

    """
    need to update these to write line by line i reckon
    df = pd.DataFrame(data) 
    csv_name = sym + "_historical.csv"
    col_order = ['date', 'open', 'high', 'low', 'close', 'volume']
    df[col_order].to_csv('/home/lee/Projects/Finance/Data/Historical/' + csv_name,index=False)
    #print "[+++] " + csv_name + " written [+++]"
    """


"""
data = readExisting(['MSFT'], end='2007-01-01')
print(data)
"""
"""
start = datetime.datetime.now()
data = collectData(symbols=['ADBE'])
print(datetime.datetime.now() - start)
for i in data:
    print(i)
"""


"""
start2 = datetime.datetime.now()
#                                    'Jul 9, 2009'
data2 = collectData(symbols=['ADBE', 'AMD'], end='2010-01-01', save=True, epoch=False)
print(datetime.datetime.now() - start2)

for i in data2:
    print(i)
print(data2)
#print('no end arg', len(data['ADBE']['open']))
print('w/ end arg', len(data2['ADBE']['open']))
"""

