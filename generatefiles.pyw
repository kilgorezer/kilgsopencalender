weekday = 6 # Invalid = 0, Sunday = 1, Monday = 2,... Friday = 6, Saturday = 7
day = 15 # Day
month = 10 # Month as number
relyear = 1582 # Start date is October 15, 1582, Friday
leap = False
daytrack = open("daymap.json", "w")
daytrack.write("{")
loop = 1022679
total = 1048576

startyear = relyear

def divisible(n, d):
    return n / d == n // d

def isleap(year):
    return divisible(year, 4) and ((not divisible(year, 100)) or divisible(year, 400))

def maxday(d, m, l): #day, month, leap
    if m == 1:
        return 31
    if m == 2:
        return 28+l # A hacky way to implement a leap day, as True is 1 when converted to a number, while False is 0 in the same way
    if m == 3:
        return 31
    if m == 4:
        return 30
    if m == 5:
        return 31
    if m == 6:
        return 30
    if m == 7:
        return 31
    if m == 8:
        return 31
    if m == 9:
        return 30
    if m == 10:
        return 31
    if m == 11:
        return 30
    if m == 12:
        return 31
    if m == 0:
        return 31 # Month 0 is used internally for the overflow

for dayid in range(loop):
    inp = '"' + str(dayid) + '": {"weekday": ' + str(weekday) + ', "day": ' + str(day) + ', "month": ' + str(month) + ', "relyear": ' + str(relyear-startyear) + ', "isleap": ' + str(leap+0) + ', "valid": 1}, '
    print(inp)
    daytrack.write(inp)
    if weekday == 7:
        weekday = 1
    else:
        weekday+=1
    if day == 31 and month == 12:
        relyear+=1
        leap = isleap(relyear)
        month = 0
    if day == maxday(day, month, leap):
        month += 1
        day = 1
    else:
        day += 1

for dayid in range(loop, total-1):
    print('"' + str(dayid) + '": {"relyear": -1582, "valid": 0}, ')
    daytrack.write('"' + str(dayid) + '": {"relyear": -1582, "valid": 0}, ')
    
print('"' + str(total-1) + '": {"relyear": -1582, "valid": 0}')
daytrack.write('"' + str(total-1) + '": {"relyear": -1582, "valid": 0}' + "}")
daytrack.close()

i = open("truestartday.txt", "w")
i.write('"161350": {"weekday": 6, "day": 19, "month": 7, "relyear": 442, "isleap": 1, "valid": 1}')
i.close()

i = open("generate_debug.bat", "w")
i.write("""@python generatefiles.pyw > output.txt
@type output.txt
@echo Press any key to exit.
@pause > nul""")
i.close()

i = open("getdayn.py", "w")
i.write("""
from sys import argv as arg
import json
daysf = open("daymap.json", "r")
days = json.load(daysf)
days[arg[1]]["year"] = days[arg[1]]["relyear"]+1582+(int(arg[2])*2800)
print(days[arg[1]])
daysf.close()
days.clear()
""")
i.close()

i = open("getdaynpy.py", "w")
i.write("""def getdayn(n, n2):
    import json
    daysf = open("daymap.json", "r")
    days = json.load(daysf)
    days[str(n)]["year"] = days[str(n)]["relyear"]+1582+(n2*2800)
    return days[str(n)]
    daysf.close()
    days.clear()
""")

i = open("getday.py", "w")
i.write("""
from getdaynpy import getdayn as getday
from sys import argv
hex = argv[1]
daynum = int("0x"+hex[0:5], 0)
loopnum = 0
if len(hex) > 5:
    loopnum = int("0x"+hex[5:len(hex)][::-1], 0)
print(getday(daynum, loopnum))
""")

quit(0)
