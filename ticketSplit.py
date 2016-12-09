import requests
from lxml import html 
from pyquery import PyQuery
import  urllib
import datetime
import re



class Station:
  def __init__(self,name,abbr):
    self.name = name
    self.abbr = abbr
  
  def __str__(self):
    return(self.name + ' [' + self.abbr + ']')
    


class CallingPoint:
  def __init__(self,station,arr,dep):
    self.station = station
    self.arr = arr
    self.dep = dep
    if self.dep == '' and self.arr != '':
      print('\nWARNING: No departure time was specified for {}, arrival time will be used.\n'.format(self.station))
      self.dep = self.arr
    elif self.dep != '' and self.arr == '':
      print('\nWARNING: No arrival time was specified for {}, departure time will be used.\n'.format(self.station))
      self.arr = self.dep
    elif self.dep == '' and self.arr == '':
      print('No departure or arrival time specified for {}.\nExiting...'.format(station))
      exit()
  
  def __str__(self):
    return('{:>40} {}\t{}'.format(str(self.station),str(self.arr),str(self.dep)))
    
  

class Route:
  def __init__(self,stationfrom,stationto,date,dep,arr):
    self.callingpoints = []
    self.changes = []
    self.fromst = stationfrom
    self.tost = stationto
    self.date = date
    self.dep = dep
    self.arr = arr
  
  def addCallingPoint(self,cp):
    self.callingpoints.append(cp)
  
  
  def __str__(self):
    cpstr = 'From: {:30}\tTo:{:30}\n'.format(str(self.fromst),str(self.tost))
    cpstr += '      {:30}\t   {:30}\n'.format(str(self.dep),str(self.arr))
    
    if len(self.callingpoints) > 0 :
      cpstr += '\nCalling Points:'
    
    for cp in self.callingpoints:
      cpstr += '\n' + str(cp)
    
    if len(self.changes) > 0:
      cpstr += '\n\nChanges: '
    for ch in self.changes:
      cpstr += str(ch) + ', '
    if len(self.changes) > 0:
      cpstr = cpstr[:-2]
    cpstr += '\n'
        
    return( cpstr )



class RouteGraph:
  def populateStops(self):
    self.stops.append([self.route.fromst,self.route.dep,''])
    tmpn = 0
    self.routeDict[self.route.fromst] = tmpn
    for s in self.route.callingpoints:
      self.stops.append([s.station,s.dep,s.arr])
      tmpn += 1
      self.routeDict[s.station] = tmpn
      #tmpn += 1
    self.stops.append([self.route.tost,'',self.route.arr])
    tmpn += 1
    self.routeDict[self.route.tost] = tmpn
    self.optroute.append([None,0])
    for i in range(1,self.length):
      self.optroute.append([None,float('inf')])
    
  
  def makePriceTable(self):
    for i in range(self.length-1):
      self.priceTable[self.stops[i][0]] = {}
      for j in range(i+1,self.length):
        self.priceTable[self.stops[i][0]][self.stops[j][0]] = float('inf')
      
    
    
  
  def __init__(self,route):
    self.route = route
    self.length = len(route.callingpoints) + 2
    self.stops = []
    self.priceTable = {}
    self.optroute = []
    self.routeDict = {}
    self.populateStops()
    self.makePriceTable()
  

  def __str__(self):
    st = ''
    for s in self.stops:
      st += '{:>40} {:5} {:5}\n'.format( str(s[0]), str(s[1]), str(s[2]) )
    return(st)
  
  def printPrices(self):
    st = 'Ticket prices:\n      '
    
    for i in range(1,self.length):
      st += '  ' + self.stops[i][0].abbr + '  '
    st += '\n'
    
    
    for i in range(self.length-1):
      st += '  ' + self.stops[i][0].abbr
      for k in range(i):
        st += '  . . .'
      for j in range(i+1,self.length):
        st += ' {:>5} '.format(str( self.priceTable[self.stops[i][0]][self.stops[j][0]] ))
      st += ' \n'
    print(st)
  
  
  def getPrices(self):
    print('Fetching prices...')
    print('Progress: {:2}/{}'.format(0,self.length-1))
    for i in range(self.length-1):
      timestr = self.stops[i][1]
      time = timestr.replace(':','')
      tempmin = int(time[2:])
      temphour = int(time[:2])
      if tempmin < 5:
        strmin = '{}'.format(tempmin + 55)
        strhour = '{}'.format(temphour - 1)
        if len(strmin) == 1:
          strmin = '0' + strmin
        if len(strhour) == 1:
          strhour = '0' + strhour
        time = strhour + strmin
      else:
        strmin = '{}'.format(tempmin - 5)
        strhour = '{}'.format(temphour)
        if len(strmin) == 1:
          strmin = '0' + strmin
        if len(strhour) == 1:
          strhour = '0' + strhour
        time = strhour + strmin
      
      
      for j in range(i+1,self.length):
        url = 'http://ojp.nationalrail.co.uk/service/timesandfares/' + self.stops[i][0].abbr + '/' + self.stops[j][0].abbr + '/' + self.route.date + '/' + time + '/dep'
        #print(url)
        rsp = requests.get(url)
        prdoc = PyQuery(rsp.content)
        sres = prdoc('div#ctf-results table#oft tbody tr td.dep').filter(lambda i: PyQuery(this).text() == timestr ).parent()
        
        
        if len(sres) > 1:
          print('{} trains were matched. URL: {}'.format(len(sres),url))
          rowtmp = PyQuery( sres )
          temptrip = rowtmp('td.arr').filter(lambda i: PyQuery(this).text() == self.stops[j][2] ).parent()
          if len(temptrip) == 1:
            price = float(temptrip.find('td.fare label').text()[1:])
            print('Arrival time matched. Price: {}'.format(price))
          elif len(temptrip) > 1:
            print("Arrival time couldn't be matched. Choose manually.")
            temptrip = chooseTrip(session,url)
            price = float(temptrip.find('td.fare label').text()[1:])
          else:
            print('No trains were found. Exiting...')
            exit()
        elif len(sres) ==0 :
          print('No trains were matched. URL: {}'.format(url))
          if manualChoice:
            temptrip = chooseTrip(session,url)
            price = float(temptrip.find('td.fare label').text()[1:])
          else:
            sres = prdoc('div#ctf-results table#oft tbody tr td.dep').parent()
            for k in range(len(sres)):
              tm = sres.children('td.dep').eq(k).text()
              if int(tm.replace(':','')) > int(timestr.replace(':','')) :
                break
            try:
              price = float(sres.children('td.dep').eq(k).parent().find('td.fare label').text()[1:])
            except:
              print('Unforseen error\n')
              print(url)
              exit()
            print('The train leaving at {} was chosen with price {}.'.format(tm,price))
        else:
          rowtmp = PyQuery( sres )
          price = float(sres('td.fare label').text()[1:])
          
        self.priceTable[self.stops[i][0]][self.stops[j][0]] = price
      print('Progress: {:2}/{}'.format(i + 1,self.length-1))
    print('')
  
  
  def getOptRoute(self):
    for i in range(self.length-1):
      for j in range(i+1,self.length):
        if self.priceTable[self.stops[i][0]][self.stops[j][0]] +  self.optroute[i][1]  < self.optroute[j][1]:
          self.optroute[j][0] = self.stops[i][0]
          self.optroute[j][1] = self.priceTable[self.stops[i][0]][self.stops[j][0]] + self.optroute[i][1]
  
  
  def printOptRoutes(self):
    st = ''
    for i in range(self.length):
      st += '{:30} {:30} {}\n'.format( str( self.stops[i][0] ) , str( self.optroute[i][0] ) , str( self.optroute[i][1] ) )
    print(st)
  
  
  def printOptRoute(self):
    tmpLst = []
    tmpN = self.routeDict[self.optroute[-1][0]]
    tmpLst.append(tmpN)
    while self.optroute[tmpN][0] != None:
      tmpN = self.routeDict[self.optroute[tmpN][0]]
      tmpLst.append(tmpN)
    tmpLst = tmpLst[:-1][::-1]
    if len(tmpLst)==0:
      print('The direct ticket is cheaper.')
      return
    tmpstr = 'Cheapest combination:\n'
    tmpstr += 'From: {:30} {:5}'.format(str(self.route.fromst),str(self.route.dep))
    for i in range(len(tmpLst)):
      if i == 0:
        prstation = self.route.fromst
      else:
        prstation = self.route.callingpoints[tmpLst[i-1]-1].station
      
      tmpstr += '\tTo: {:30}{:5}\t\tPrice:{:>5}\n'.format(str(self.route.callingpoints[tmpLst[i]-1].station),str(self.route.callingpoints[tmpLst[i]-1].arr),self.priceTable[prstation][self.route.callingpoints[tmpLst[i]-1].station])
      tmpstr += 'From: {:30} {:5}'.format(str(self.route.callingpoints[tmpLst[i]-1].station),str(self.route.callingpoints[tmpLst[i]-1].dep))
    tmpstr += '\tTo: {:30}{:5}\t\tPrice:{:>5}\n'.format(str(self.route.tost),str(self.route.arr),self.priceTable[self.route.callingpoints[tmpLst[i]-1].station][self.route.tost])
    
    tmpstr += 'Total cost: {}'.format(self.optroute[-1][1])
    
    print(tmpstr)
      
    
    
    

def chooseTrip(ses,url):
  respPQ = PyQuery(ses.get(url).content)
  tttrips = respPQ('div#ctf-results table#oft tbody tr td.dep').parent()
  if len(tttrips) > 1:
    print( '{} trains were found.'.format(len(tttrips)) )
    print( '    {:7} {:5} {:5} {:7} {:7} {:3} {:7}'.format('Dep:','From:','To:','Arr:','Dur:','Chg:','Price:') )
    for i in range(len(tttrips)):
      print(
        '{:2}: {:7} {:5} {:5} {:7} {:7} {:3} {:>7}'.format(i+1,
                                                          tttrips.eq(i).find('td.dep').text(),
                                                          tttrips.eq(i).find('td.from abbr').text(),
                                                          tttrips.eq(i).find('td.to abbr').text(),
                                                          tttrips.eq(i).find('td.arr').text(),
                                                          tttrips.eq(i).find('td.dur').text().replace(' ',''),
                                                          tttrips.eq(i).find('td.chg').text(),
                                                          tttrips.eq(i).find('td.fare div label').text()[1:]
                                                          )
        )
    print('URL: ' + url)
    inp = ''
    while inp == '':
      inp = raw_input('Choose trip: ')
    k = int(inp)-1
    if k not in set(range(len(tttrips))):
      print('Invalid argument. Exiting...')
      exit()
    print('')
    return( PyQuery(tttrips.eq(k)) )
  elif len(tttrips) == 1:
    return( PyQuery(tttrips) )
  else:
    print('No trains found. Exiting...')
    exit()    
    
    










travelFrom = 'BHI'
travelTo = 'EDB'
traveltime = '09:00'

today = datetime.date.today()

year = ('{}'.format(today.year))[2:]
month = '{:02d}'.format(today.month)
day = '{:02d}'.format(today.day)



date = '{}/{}/{}'.format(day,month,year)



theday = today + datetime.timedelta(7)
year = ('{}'.format(theday.year))[2:]
month = '{:02d}'.format(theday.month)
day = '{:02d}'.format(theday.day)
date = '{}/{}/{}'.format(day,month,year)




print('Travelling from (type the 3 letter abbrevation for the station, press enter for {}): '.format(travelFrom))
inp = raw_input()

if inp!= '':
  travelFrom = inp



print('Travelling to (type the 3 letter abbrevation for the station, press enter for {}): '.format(travelTo))
inp = raw_input()

if inp!= '':
  travelTo = inp


print('Travelling date (press enter for next week, {}, type the date that you want or type +n to search n days after today):'.format(date))
inp = raw_input()

if inp!= '':
  if inp[0] != '+':
    lst = re.split(r'[ ,-]+',inp)
    day = lst[0]
    try:
      month = lst[1]
    except:
      pass
    try:
      year = lst[2]
    except:
      pass
    month = '{:02d}'.format(int(month))
    date = '{}/{}/{}'.format(day,month,year)
  else:
    theday = today + datetime.timedelta(int(inp[1:]))
    year = ('{}'.format(theday.year))[2:]
    month = '{:02d}'.format(theday.month)
    day = '{:02d}'.format(theday.day)
    date = '{}/{}/{}'.format(day,month,year)
    print('{}'.format(date))

  

inp = raw_input('Travelling time (press enter for {}): '.format(traveltime))

if len(inp) == 1:
  traveltime = '0{}:00'.format(inp)
elif len(inp) == 2:
  traveltime = '{}:00'.format(inp)
elif inp!= '':
  traveltime = inp







print('\n\n\n')





date = date.replace('/','')
traveltime = traveltime.replace(':','')






manualChoice = False





url = 'http://ojp.nationalrail.co.uk/service/timesandfares/{}/{}/{}/{}/dep'.format(travelFrom,travelTo,date,traveltime)

session = requests.session()

response = session.get(url)
doc = PyQuery(response.content)






trip = chooseTrip(session,url)


nexturl = trip('td.info a').attr['href']


r = Route( Station(trip('td.from').text().split('[')[0].strip(),trip('td.from abbr').text()) ,
          Station(trip('td.to').text().split('[')[0].strip(),trip('td.to abbr').text()) ,
          date ,
          trip('td.dep').text() ,
          trip('td.arr').text() )



url = 'http://ojp.nationalrail.co.uk' + nexturl



url = urllib.quote(url, safe='/:')



response = session.get(url)
doc = PyQuery(response.content)



legsnum = int(doc('table#journey tbody td.changes').text()) + 1

legs = doc('div.journey-details table#journeyLegDetails tbody tr td.method').parent()
callpointtabs = doc('div.journey-details table#journeyLegDetails tbody tr.callingpoints div.callingpointslide table tbody')

for i in range(legsnum):
  cps = callpointtabs.eq(i).find('tr')
  for cp in cps:
    cppq = PyQuery(cp)
    r.addCallingPoint( CallingPoint( Station(cppq('td.calling-points a').text().split('[')[0].strip(),cppq('td.calling-points a abbr').text()),cppq('td.arrives').text(),cppq('td.departs').text()) )
  
  if i != legsnum - 1:
    lrt = PyQuery(legs[i]) 
    lrn = PyQuery(legs[i+1])
    tmpst = Station(lrt('td.destination a').text().split('[')[0].strip() , lrt('td.destination a abbr').text() )
    r.changes.append(tmpst)
    r.addCallingPoint( CallingPoint( tmpst  , lrt('td.arriving').text() , lrn('td.leaving').text() ) )
    
  










print(r)



rg = RouteGraph(r)



rg.getPrices()

rg.printPrices()

rg.getOptRoute()

#rg.printOptRoutes()

rg.printOptRoute()

