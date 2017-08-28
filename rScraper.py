def dbwrite(usn, name, pc, sgpa, f):

    conn = sqlite3.connect('db.sqlite')
    cur = conn.cursor()

    cur.execute('''
    CREATE TABLE IF NOT EXISTS `Marks` (
    	`USN`	TEXT NOT NULL PRIMARY KEY UNIQUE,
    	`NAME`	TEXT,
    	`PC`	REAL,
    	`SGPA`	REAL,
      'Fail'  INTEGER
    )''')

    cur.execute('''INSERT OR REPLACE INTO Marks (USN, NAME, PC, SGPA, Fail) VALUES (?, ?, ?, ?, ?)''', (usn, name, pc, sgpa, f))

    conn.commit()
    cur.close()


def getd(url):

    # Ignore SSL certificate errors
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    u = re.findall('usn=(.+)',url)
    us = ''.join(u)
    us = us.upper()
    print('Retrieving', us, '...', '\n')
    html = urlopen(url, context=ctx).read()
    soup = BeautifulSoup(html, "lxml")
    text = soup.get_text()
    text = text.split('\n')
    text = ' '.join(text)
    text = text.split('\t')
    text = ' '.join(text)

    name  = re.findall("Student Name  : ([A-Z\s]+)*\s*Semester :",text)
    name = ' '.join(name)
    name = name.rstrip()
    name = name.title()

    # usn  = re.findall("University Seat Number   : ([A-Z0-9]+)\s*Stud",text)
    usn  = re.findall("University Seat Number[:\s]+(\S+)\s*Stud",text)
    usn = ' '.join(usn)
    usn = usn.rstrip()
    usn = usn.upper()

    #scodes = re.findall("([0-9]{2,}[A-Z]{3,}[0-9]{2,})",text)
    sub = re.findall("([0-9]{2,}[A-Z]{3,}[0-9]{2,}.+[PF]\s{5,}?)",text)
    mks = re.findall("[0-9]{1,2} [0-9]{1,2} [0-9]{1,3} [PFA]",text)
    mks = ' '.join(mks)
    mks = mks.split()

    ia = list()
    i = 0
    while i < len(mks):
        ia.append(int(mks[i]))
        i += 4

    ea = list()
    i = 1
    while i < len(mks):
        ea.append(int(mks[i]))
        i += 4

    tm = list()
    i = 0
    while i < len(ia):
        tm.append(ia[i] + ea[i])
        i += 1

    g = list()
    for i in tm:
        if (i >=90):
            g.append(int('10'))

        elif (i >= 80):
            g.append(int('9'))

        elif (i >= 70):
            g.append(int('8'))

        elif (i >= 60):
            g.append(int('7'))

        elif (i >= 50):
            g.append(int('6'))

        elif (i >= 40):
            g.append(int('5'))

        else:
            g.append(int('0'))

    pf = list()
    i = 3
    f = 0
    while i < len(mks):
        pf.append(mks[i])
        if mks[i] != 'P':
            f += 1
        i += 4

    s = (tm[0] + tm[1] + tm[2] + tm[3] + tm[4] + tm[5]/2 + tm[6]/2)
    pc = s/6
    pc = round(pc,2)
    sgpa = (g[0] + g[1] + g[2] + g[3] + g[4] + g[5]/2 + g[6]/2)/6
    sgpa = round(sgpa,2)

    dbwrite(usn, name, pc, sgpa, f)

    print(pc, '%')
    print(sgpa, 'SGPA')
    print(name)
    print(usn,'\n')




# import urllib.request, urllib.parse, urllib.error
from urllib.request import urlopen
from bs4 import BeautifulSoup
import lxml
import re
import sqlite3
import ssl


ci = input('Enter College ID ')
br = input('Enter Branch ID ')
ran = int(input('Enter starting USN '))

k = ran
flag = 0
while k <= 180:

    if k < 10:
        j = '00' + str(k)
    elif k < 100:
        j = '0' + str(k)
    else:
        j = str(k)

    url = 'http://results.vtu.ac.in/cbcs_17/result_page.php?usn=1' + ci + '16' + br + j
    k += 1

    try :
        getd(url)
        flag = 0

    except KeyboardInterrupt:
        print('Exiting')
        break

    except :
        print('Unable to retrieve.\n')
        flag += 1
        if flag > 4: #Max number of invalid requests
            print('No more USNs. Exiting.')
            break
        else:
            continue

import exp #Generates txt database
