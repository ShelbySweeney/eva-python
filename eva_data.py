import sqlite3
import ssl
import urllib.request, urllib.parse, urllib.error
from urllib.parse import urljoin
from urllib.parse import urlparse
import re

# this code takes the duration time (hours:minutes) and converts it to hours
def parsedur(dur):
    bits = dur.split(':')
    hors = int(bits[0])
    mints = int(bits[1])
    hrs = hors + (mints/60)
    return hrs

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# API for NASA data "Extra-vehicular Activity (EVA) - US and Russia" (6/3/1965-8/22/2013)
# data can be seen online: 'https://data.nasa.gov/Raw-Data/Extra-vehicular-Activity-EVA-US-and-Russia/9kcy-zwvn/data'
baseurl = 'https://data.nasa.gov/resource/q8u9-7uq7.json'



# open url with a timeout of 30 seconds
document = urllib.request.urlopen(baseurl, None, 30, context=ctx)
text = document.read().decode()

# split the data into a list
text_list = text.split('{')
# get rid of the first one because it's just '['
text_list2 = text_list[1:]

list3 = []
for item in text_list2:
    pieces = item.split(',')
    dura_present1 = re.findall('duration', pieces[2])
    dura_present2 = re.findall('duration', pieces[3])
    # if "duration" is not in the entry, skip it. otherwise, pull it from the entry
    if bool(dura_present1):
        dura = pieces[2].split(':\"')[1].rstrip('\"')
    elif bool(dura_present2):
        dura = pieces[3].split(':\"')[1].rstrip('\"')
    else: continue

    # pull out the crew from the entry
    crew = pieces[1].split(':\"')[1].rstrip('\"').rstrip()

    # clean up crew formatting differences and misspellings:
    if crew == 'Doug Wheellock Tracy Caldwell Dyson':
        crew = 'Doug Wheelock  Tracy Caldwell Dyson'
    elif crew == 'Thuot/Hieb/Akers':
        crew = 'Pierre Thuot  Rick Hieb  Tom Akers'
    else:
        crew = crew
    # convert duration into hours
    dura_hours = parsedur(dura)

    multiple_crew = re.findall('  ', crew)
    crew_membs = []
    if not bool(multiple_crew):
        crew_membs = [crew]
    else:
        crew_mems = crew.split('  ')
        crew_membs = []
        for mem in crew_mems:
            mems = mem.strip()
            if len(mems) >= 1:
                membs = mems
                crew_membs.append(membs)
            else: continue

    ret = [crew_membs, dura_hours]
    list3.append(ret)

# create a separate entry for each crewmember in each entry
list4 = []
for entry in list3:
    duratn = entry[1]
    crewmems = entry[0]
    for x in crewmems:
        ret = [x, duratn]
        list4.append(ret)

# clean up misspellings in crew names
for item in list4:
    if item[0] == 'Anatoli Solovyov':
        item[0] = 'Anatoly Solovyev'
    if item[0] == 'Christer Fugelsang':
        item[0] = 'Christer Fuglesang'
    if item[0] == 'Clay Anderson':
        item[0] = 'Clayton Anderson'
    if item[0] == 'Fyodor Yurchikin':
        item[0] = 'Fyodor Yurchikhin'
    if item[0] == 'Pat Forrester':
        item[0] = 'Patrick Forrester'
    if item[0] == 'Valeri Tsibliev':
        item[0] = 'Valeri Tsibliyev'
    if item[0] == 'Yuri Malenchecko':
        item[0] = 'Yuri Malenchenko'
    if item[0] == 'Yuri Onufrenko':
        item[0] = 'Yuri Onufrienko'
    if item[0] == 'Yri Onufrienko':
        item[0] = 'Yuri Onufrienko'
    if item[0] == 'G. Padelka':
        item[0] = 'Gennady Padalka'
    if item[0] == 'Mike Lopez-Alegria':
        item[0] = 'Michael Lopez-Alegria'
    if item[0] == 'Alexandr Kaleri':
        item[0] = 'Aleksandr Kaleri'
    if item[0] == 'Alexander Kaleri':
        item[0] = 'Aleksandr Kaleri'
    if item[0] == 'Alexandr	Ivanchenkov':
        item[0] = 'Aleksandr Ivanchenkov'
    if item[0] == 'Mike Good':
        item[0] = 'Michael Good'
    if item[0] == 'Bob Curbeam':
        item[0] = 'Robert Curbeam'
    if item[0] == 'Bob Behnken':
        item[0] = 'Robert Behnken'

# connect to database eva.sqlite
conn = sqlite3.connect('eva.sqlite')
cur = conn.cursor()
# drop existing database table Eva, and create a new one
cur.execute('''DROP TABLE IF EXISTS Eva ''')
cur.execute('''CREATE TABLE IF NOT EXISTS Eva
    (id INTEGER UNIQUE PRIMARY KEY, astronaut TEXT, duration INTEGER)
''')

count = 0
# insert data from list4 into Eva table
for item in list4:
    cur.execute('''INSERT OR IGNORE INTO Eva (astronaut, duration) VALUES (?, ?)''',
    (item[0], item[1]))
    # commit to db every 50 entries:
    if count % 50 == 0 : conn.commit()
    count = count + 1
# commit to db when done
conn.commit()

# drop existing totals table and create a new table to calculate total duration
cur.execute('''DROP TABLE IF EXISTS totals ''')
cur.execute('''CREATE TABLE IF NOT EXISTS totals
    (astronaut TEXT UNIQUE PRIMARY KEY, total_duration INTEGER)
''')
# insert distinct astronauts into totals table so there's one entry per astronaut
cur.execute('''INSERT INTO totals (astronaut) SELECT DISTINCT astronaut FROM Eva''')

# commit data when program ends
conn.commit()
cur.close()
