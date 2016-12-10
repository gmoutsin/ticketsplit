# ticketsplit

This script takes advantage of the way the rail tickets are priced in UK and finds the cheapest splitting. If you don't know what is ticket splitting and you live in UK, you should google it.

The script was written for Python 2 and requires the following modules: requests, lxml, pyquery, urllib, datetime, re.

Python 2 was chosen because I couldn't make pyquery work in Python 3.

In order to use the script you need to go to a website for booking tickets. There you can see the abbreviation of the departure and arrival stations. For example the abbriviation of Birmingham is BMI.

Once you have these, run the script. You need to enter the abbreviation of the 2 stations. This can upper case or lower case letters. Then you need to add the date in the form DD/MM/YYYY or just type +X to search for X days later. Finally you need to specify the time by writting HH:MM or just HH.

Then you will have the choice of 5 different choices and by choosing one the script will run and eventually return the cheapest combination. The data used are taken from the website of National Rail which means of course that if the website changes layout the script will be broken.


A typical output of the script looks like this:


```
Travelling from (type the 3 letter abbrevation for the station, press enter for BHI): 

Travelling to (type the 3 letter abbrevation for the station, press enter for EDB): 

Travelling date (press enter for next week, 16/12/16, type the date that you want or type +n to search n days after today):

Travelling time (press enter for 09:00): 14




5 trains were found.
    Dep:    From: To:   Arr:    Dur:    Chg: Price: 
 1: 14:05   BHI   EDB   19:20   5h15m   2    105.50
 2: 14:53   BHI   EDB   19:40   4h47m   1    130.00
 3: 15:05   BHI   EDB   20:22   5h17m   2    112.90
 4: 15:53   BHI   EDB   20:23   4h30m   0    118.00
 5: 16:05   BHI   EDB   21:28   5h23m   1    112.90
URL: http://ojp.nationalrail.co.uk/service/timesandfares/BHI/EDB/161216/1400/dep
Choose trip: 2


WARNING: No departure time was specified for Haymarket [HYM], arrival time will be used.

From: Birmingham International [BHI]    To:Edinburgh [EDB]
      14:53                                19:40                         

Calling Points:
             Birmingham New Street [BHM] 15:08  15:15
                 Sandwell & Dudley [SAD] 15:24  15:24
                     Wolverhampton [WVH] 15:37  15:37
                             Crewe [CRE] 16:07  16:09                                                                                                                        
              Warrington Bank Quay [WBQ] 16:26  16:27                                                                                                                        
               Wigan North Western [WGN] 16:37  16:38
                   Preston (Lancs) [PRE] 16:51  16:53
                         Lancaster [LAN] 17:07  17:14
           Oxenholme Lake District [OXN] 17:29  17:29
             Penrith (North Lakes) [PNR] 17:54  17:54
                          Carlisle [CAR] 18:10  18:11
                         Lockerbie [LOC] 18:30  18:30
                         Haymarket [HYM] 19:31  19:31

Changes: Lancaster [LAN]

Fetching prices...
Progress:  0/14
Progress:  1/14
Progress:  2/14
Progress:  3/14
Progress:  4/14
Progress:  5/14
Progress:  6/14
No trains were matched. URL: http://ojp.nationalrail.co.uk/service/timesandfares/WGN/LOC/161216/1633/dep
The train leaving at 16:43 was chosen with price 26.0.
No trains were matched. URL: http://ojp.nationalrail.co.uk/service/timesandfares/WGN/HYM/161216/1633/dep
The train leaving at 16:43 was chosen with price 29.5.
No trains were matched. URL: http://ojp.nationalrail.co.uk/service/timesandfares/WGN/EDB/161216/1633/dep
The train leaving at 16:43 was chosen with price 29.5.
Progress:  7/14
No trains were matched. URL: http://ojp.nationalrail.co.uk/service/timesandfares/PRE/LOC/161216/1648/dep
The train leaving at 16:58 was chosen with price 16.0.
No trains were matched. URL: http://ojp.nationalrail.co.uk/service/timesandfares/PRE/HYM/161216/1648/dep
The train leaving at 16:58 was chosen with price 26.0.
No trains were matched. URL: http://ojp.nationalrail.co.uk/service/timesandfares/PRE/EDB/161216/1648/dep
The train leaving at 16:58 was chosen with price 26.0.
Progress:  8/14
Progress:  9/14
Progress: 10/14
Progress: 11/14
Progress: 12/14
Progress: 13/14
No trains were matched. URL: http://ojp.nationalrail.co.uk/service/timesandfares/HYM/EDB/161216/1926/dep
The train leaving at 19:39 was chosen with price 2.3.
Progress: 14/14

Ticket prices:
        BHM    SAD    WVH    CRE    WBQ    WGN    PRE    LAN    OXN    PNR    CAR    LOC    HYM    EDB  
  BHI   3.0    5.0    4.5   21.0   21.0   21.0   28.0   28.0   43.0   43.0   52.0   93.5  130.0  130.0  
  BHM  . . .   3.2    3.8   21.0   21.0   21.0   28.0   28.0   43.0   43.0   52.0   93.5  112.9  112.9  
  SAD  . . .  . . .   3.3   21.0   21.0   21.0   28.0   28.0   43.0   43.0   52.0   93.5  112.9  112.9  
  WVH  . . .  . . .  . . .  18.5   21.0   21.0   28.0   28.0   43.0   43.0   52.0   81.0  120.5  120.5  
  CRE  . . .  . . .  . . .  . . .  11.6   13.2   23.0   36.5   42.5   48.5   31.0   63.5   91.5   91.5  
  WBQ  . . .  . . .  . . .  . . .  . . .   5.0   12.2   19.5   22.4   41.0   31.0   57.0   76.0   76.0  
  WGN  . . .  . . .  . . .  . . .  . . .  . . .   6.4   13.9   17.7   30.5   31.0   26.0   29.5   29.5  
  PRE  . . .  . . .  . . .  . . .  . . .  . . .  . . .   7.4   17.9   20.5   23.4   16.0   26.0   26.0  
  LAN  . . .  . . .  . . .  . . .  . . .  . . .  . . .  . . .   8.3    8.0   10.5   12.0   20.5   20.5  
  OXN  . . .  . . .  . . .  . . .  . . .  . . .  . . .  . . .  . . .  10.2   10.5    8.0   15.5   15.5  
  PNR  . . .  . . .  . . .  . . .  . . .  . . .  . . .  . . .  . . .  . . .   7.5   21.0   15.5   15.5  
  CAR  . . .  . . .  . . .  . . .  . . .  . . .  . . .  . . .  . . .  . . .  . . .   6.9   11.5   11.5  
  LOC  . . .  . . .  . . .  . . .  . . .  . . .  . . .  . . .  . . .  . . .  . . .  . . .   9.5    9.5  
  HYM  . . .  . . .  . . .  . . .  . . .  . . .  . . .  . . .  . . .  . . .  . . .  . . .  . . .   2.3  

Cheapest combination:
From: Birmingham International [BHI] 14:53      To: Lancaster [LAN]               17:07         Price: 28.0
From: Lancaster [LAN]                17:14      To: Edinburgh [EDB]               19:40         Price: 20.5
Total cost: 48.5
```


Finally the script is released with the GPLv3 licence because why not?
