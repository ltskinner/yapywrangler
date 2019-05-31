
import os
import requests
import time
import csv
import datetime

def readExisting(symbols, end=None, epoch=False):
    #reads from path and tries to open csv
    #   if not existing call collect data
    #reads the csv and searches back for a day that is less than the given end date
    #returns the data
    data = {}
    for sym in symbols:
        try:
            newget = False
            buffer = []
            path = os.getcwd() + '/YPData/' + sym.upper() + '.csv'
            with open(path, 'r') as f:
                infile = csv.reader(f)
                ct = 0
                for line in infile:
                    if ct > 0:
                        buffer.append([line[0], float(line[1]), float(line[2]), float(line[3]), float(line[4]), float(line[5])])
                    ct+=1
            #determines if most recent data row is less than a day old
            if (int(time.time()) - int(buffer[0][0])) < 86400:
                if end != None:
                    dt = datetime.datetime.strptime(end, '%Y-%m-%d')
                    epend = int(time.mktime(dt.timetuple()))
                    #determines if the end date specified is in the offline data
                    if int(buffer[-1][0]) < epend:
                        for i in range(0, len(buffer)):
                            if int(buffer[i][0]) < epend:
                                #picks data within date range to return to user
                                data[sym] = buffer[:i]
                                break
                            
                    else:
                        #print("[-] Failed backboard [-]")
                        newget = True
                else:
                    #print("[+] no end specified [+]")
                    data[sym] = buffer[:]

            else:
                #print("[-] Failed most recent day [-]")
                newget = True
        except:
            newget = True

        if newget:
            datagrab = securityData([sym], end=end, save=True, epoch=epoch)
            data[sym] = datagrab[sym]
        elif not epoch:
            for d in data[sym]:
                d[0] = time.strftime('%Y-%m-%d', time.localtime(int(d[0])))

    return data



def securityData(symbols, end=None, save=False, epoch=False):
    #unless specified, farthest back date is Jan 1 2000
    # converts user input to epoch time
    if end != None:
        dt = datetime.datetime.strptime(end, '%Y-%m-%d')
        end = str(int(time.mktime(dt.timetuple())))
    else:
        end="946684800"

    data = {}
    for sym in symbols:
        parsed = getReq(sym, end)
        data[sym] = dataOrganizer(parsed)

    if save:
        for sym in symbols:
            writeCsv(sym, data[sym])
    
    if epoch == False:
        for sym in symbols:
            for d in data[sym]:
                d[0] = time.strftime('%Y-%m-%d', time.localtime(int(d[0])))

    return data

#---------------------------------------------------
#---------------- SUPPORT FUNCTIONS ----------------
#---------------------------------------------------


def dataOrganizer(raw):
    data = []
    for i in range(0, len(raw)):
        if "amount" not in raw[i]:
            each = raw[i].split(',')
            if i == 0:
                each[0] = each[0].strip("[{")

            buffer = [  int(each[0].strip('"date":')), 
                        each[1].strip('"open":'), 
                        each[2].strip('"high":'), 
                        each[3].strip('"low":'), 
                        each[4].strip('"close":'), 
                        each[5].strip('"volume":').strip('}]')]
            #sequence to catch null, nu, na, nan values
            if nullCatch(buffer):
                buffer = [buffer[0], float(buffer[1]), float(buffer[2]), float(buffer[3]), float(buffer[4]), float(buffer[5])]
                data.append(buffer)

    return data
    

def getReq(sym, end):
    try:
        r = requests.get("https://finance.yahoo.com/quote/" + sym + "/history?period1=" + end + "&period2=" + str(int(time.time())) + "&interval=1d&filter=history&frequency=1d")
        lvl1 = (str(r.content).split("HistoricalPriceStore")[1]).split(',"isPending"')[0] #root.App.main does not play well w/ bs4
        return lvl1.split('{"prices":')[1].split('},{')
    except:
        #if no data and more than a year away from last search time, iterate again
        if ((int(end) + 31536000) < int(time.time())):
            new = str(int(end) + 31536000)
            getReq(sym, new)
        else:
            print("[-] NO DATA AVAILABLE [-]")
            return []


def writeCsv(sym, data):
    directory = os.getcwd() + '/YPData/'
    try:
        os.stat(directory)
    except:
        os.mkdir(directory)

    with open(directory + sym.upper() + '.csv', 'w', newline="") as f:
        writer = csv.writer(f, delimiter=",")
        writer.writerow(['date', 'open', 'high', 'low', 'close', 'volume'])
        for line in data:
            writer.writerow(line)
    
    print('[+]', sym.upper(), 'saved [+]')


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


