# ticketsplit

This script takes advantage of the way the rail tickets are priced in UK and finds the cheapest splitting. If you don't know what is ticket splitting and you live in UK, you should google it.

The script was written for Python 2 and requires the following modules: requests, lxml, pyquery, urllib, datetime, re.

Python 2 was chosen because I couldn't make pyquery work in Python 3.

In order to use the script you need to go to a website for booking tickets. There you can see the abbreviation of the departure and arrival stations. For example the abbriviation of Birmingham New Street is BHM.

Once you have these, run the script. You need to enter the abbreviation of the 2 stations. This can upper case or lower case letters. Then you need to add the date in the form DD/MM/YYYY or just type +X to search for X days later. Finally you need to specify the time by writting HH:MM or just HH.

Then you will have the choice of 5 different choices and by choosing one the script will run and eventually return the cheapest combination. The data used are taken from the website of National Rail which means of course that if the website changes layout the script will be broken.


A typical output of the script looks like this:


```
Travelling from (type the 3 letter abbrevation for the station, press enter for BHM): 
exc
Travelling to (type the 3 letter abbrevation for the station, press enter for EDB): 

Travelling date (press enter for next week, 17/12/16, type the date that you want or type +n to search n days after today):
+2
12/12/16
Travelling time (press enter for 09:00): 




5 trains were found.                                                                                                                                                         
    Dep:    From: To:   Arr:    Dur:    Chg: Price:                                                                                                                          
 1: 09:53   EXC   EDB   17:36   7h43m   3    193.30
 2: 09:53   EXC   EDB   18:07   8h14m   1    193.30
 3: 10:52   EXC   EDB   18:22   7h30m   2    193.30
 4: 10:52   EXC   EDB   19:06   8h14m   1    193.30
 5: 11:19   EXC   EDB   19:20   8h01m   3    129.50
URL: http://ojp.nationalrail.co.uk/service/timesandfares/exc/EDB/121216/0900/dep
Choose trip: 2

From: Exeter Central [EXC]              To:Edinburgh [EDB]               
      09:53                                18:07                         

Calling Points:
                 Exeter St David's [EXD] 09:56  10:24
                  Tiverton Parkway [TVP] 10:36  10:37
                           Taunton [TAU] 10:49  10:51
              Bristol Temple Meads [BRI] 11:24  11:30
                   Bristol Parkway [BPW] 11:38  11:39
                    Cheltenham Spa [CNM] 12:09  12:11
             Birmingham New Street [BHM] 12:56  13:03
                   Burton-on-Trent [BUT] 13:26  13:28
                             Derby [DBY] 13:39  13:44
                      Chesterfield [CHD] 14:02  14:03
                         Sheffield [SHF] 14:18  14:21
                Wakefield Westgate [WKF] 14:46  14:47
                             Leeds [LDS] 15:01  15:08
                              York [YRK] 15:30  15:32
                        Darlington [DAR] 15:57  16:00
                            Durham [DHM] 16:15  16:17
                         Newcastle [NCL] 16:29  16:37
                          Alnmouth [ALM] 17:00  17:02
                            Dunbar [DUN] 17:42  17:43

Changes: Exeter St David's [EXD]

Fetching prices...
Progress:  0/20
2 trains were matched. URL: http://ojp.nationalrail.co.uk/service/timesandfares/EXC/EDB/121216/0948/dep
Arrival time matched. Price: 193.3
Progress:  1/20
2 trains were matched. URL: http://ojp.nationalrail.co.uk/service/timesandfares/EXD/EDB/121216/1019/dep
Arrival time matched. Price: 96.6
Progress:  2/20
2 trains were matched. URL: http://ojp.nationalrail.co.uk/service/timesandfares/TVP/EDB/121216/1032/dep
Arrival time matched. Price: 96.6
Progress:  3/20
2 trains were matched. URL: http://ojp.nationalrail.co.uk/service/timesandfares/TAU/EDB/121216/1046/dep
Arrival time matched. Price: 92.2
Progress:  4/20
2 trains were matched. URL: http://ojp.nationalrail.co.uk/service/timesandfares/BRI/EDB/121216/1125/dep
Arrival time matched. Price: 168.8
Progress:  5/20
2 trains were matched. URL: http://ojp.nationalrail.co.uk/service/timesandfares/BPW/EDB/121216/1134/dep
Arrival time matched. Price: 83.9
Progress:  6/20
2 trains were matched. URL: http://ojp.nationalrail.co.uk/service/timesandfares/CNM/EDB/121216/1206/dep
Arrival time matched. Price: 151.0
Progress:  7/20
Progress:  8/20
Progress:  9/20
Progress: 10/20
Progress: 11/20
Progress: 12/20
Progress: 13/20
Progress: 14/20
Progress: 15/20
Progress: 16/20
Progress: 17/20
Progress: 18/20
Progress: 19/20
Progress: 20/20

Ticket prices:
        EXD    TVP    TAU    BRI    BPW    CNM    BHM    BUT    DBY    CHD    SHF    WKF    LDS    YRK    DAR    DHM    NCL    ALM    DUN    EDB  
  EXC   1.2    5.5   11.4   15.8   27.4   58.6   89.1   92.3  111.2  126.5  131.7  139.3  145.0  150.3  167.1  178.7  180.1  180.1  192.1  193.3  
  EXD  . . .   5.5    7.5   13.6   25.7   57.0   85.5   88.7  108.7  124.6  131.7  139.3  145.0  150.3   83.4   88.9   89.9   89.9  191.1   96.6  
  TVP  . . .  . . .  10.0   12.5   23.4  46.45   85.5   92.3  108.7  124.6  131.7  139.3  145.0  150.3   83.4   88.9   89.9   89.9   99.3   96.6  
  TAU  . . .  . . .  . . .   9.1   11.4   40.5   57.6   81.8   87.8  110.3  111.9  118.8  131.7  137.5   79.0   83.9   85.5   85.5   92.2   92.2  
  BRI  . . .  . . .  . . .  . . .   3.7    9.0   51.6   56.5   69.0   86.1   92.8  105.8  110.3  113.6  133.8  145.0  148.7   74.0  163.1  168.8  
  BPW  . . .  . . .  . . .  . . .  . . .   9.0   51.6   56.5   69.0   86.1   92.8  105.8  110.3  113.6  133.8  145.0  148.7   74.0  163.1   83.9  
  CNM  . . .  . . .  . . .  . . .  . . .  . . .  23.4   39.5   43.0   62.0   72.5   82.8   85.5   86.1  115.2  124.2  132.2  133.4  151.0  151.0  
  BHM  . . .  . . .  . . .  . . .  . . .  . . .  . . .  12.2   16.6   32.8   41.1   49.3   58.1   61.8   86.1   98.1  103.4  103.4  107.6   64.7  
  BUT  . . .  . . .  . . .  . . .  . . .  . . .  . . .  . . .   6.8   10.3   24.6   35.5   42.2   46.4   75.4   87.8   91.8   97.7  101.2  101.2  
  DBY  . . .  . . .  . . .  . . .  . . .  . . .  . . .  . . .  . . .   7.5   11.2   27.8   33.6   41.3   73.0   83.9   88.9   89.7  101.2  101.2  
  CHD  . . .  . . .  . . .  . . .  . . .  . . .  . . .  . . .  . . .  . . .   5.1   10.2   13.0   13.0   54.8   63.3   63.3   67.5   87.6   94.9  
  SHF  . . .  . . .  . . .  . . .  . . .  . . .  . . .  . . .  . . .  . . .  . . .   9.2   10.6   13.0   44.8   57.6   59.2   67.5   87.6   94.9  
  WKF  . . .  . . .  . . .  . . .  . . .  . . .  . . .  . . .  . . .  . . .  . . .  . . .   3.5   13.7   34.0   38.3   38.3   38.3   62.0   93.2  
  LDS  . . .  . . .  . . .  . . .  . . .  . . .  . . .  . . .  . . .  . . .  . . .  . . .  . . .  13.0   25.7   31.3   38.3   38.3   62.0   80.0  
  YRK  . . .  . . .  . . .  . . .  . . .  . . .  . . .  . . .  . . .  . . .  . . .  . . .  . . .  . . .  12.2   18.8   20.4   24.4   37.7   34.3  
  DAR  . . .  . . .  . . .  . . .  . . .  . . .  . . .  . . .  . . .  . . .  . . .  . . .  . . .  . . .  . . .   7.0   12.5   11.0   16.4   30.7  
  DHM  . . .  . . .  . . .  . . .  . . .  . . .  . . .  . . .  . . .  . . .  . . .  . . .  . . .  . . .  . . .  . . .   6.1   14.1   16.4   29.0  
  NCL  . . .  . . .  . . .  . . .  . . .  . . .  . . .  . . .  . . .  . . .  . . .  . . .  . . .  . . .  . . .  . . .  . . .  10.3   16.4   24.9  
  ALM  . . .  . . .  . . .  . . .  . . .  . . .  . . .  . . .  . . .  . . .  . . .  . . .  . . .  . . .  . . .  . . .  . . .  . . .  16.4   18.8  
  DUN  . . .  . . .  . . .  . . .  . . .  . . .  . . .  . . .  . . .  . . .  . . .  . . .  . . .  . . .  . . .  . . .  . . .  . . .  . . .   8.0  

Cheapest combination:
From: Exeter Central [EXC]           09:53      To: Exeter St David's [EXD]       09:56         Price:  1.2
From: Exeter St David's [EXD]        10:24      To: Edinburgh [EDB]               18:07         Price: 96.6
Total cost: 97.8
```


Finally the script is released with the GPLv3 licence because why not?
