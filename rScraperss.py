def dbwrite(usn, name, pc, sem, sgpa, f, ia, ea, tm, g, scodes):

    conn = sqlite3.connect(filename)
    cur = conn.cursor()

    sem = 'Sem' + str(sem)
    query = '''
    CREATE TABLE IF NOT EXISTS {} (
    	`USN`	TEXT NOT NULL PRIMARY KEY UNIQUE,
    	`NAME`	TEXT,
    	`PC`	REAL,
    	`SGPA`	REAL,
        'Fail'  INTEGER
    )'''.format(sem)
    cur.execute(query)
    query = '''INSERT OR REPLACE INTO {} (USN, NAME, PC, SGPA, Fail) VALUES (?, ?, ?, ?, ?)'''.format(sem)
    cur.execute(query, (usn, name, pc, sgpa, f))

    for i in range(len(scodes)):
            query = '''
            CREATE TABLE IF NOT EXISTS {} (
            	`USN`	TEXT NOT NULL PRIMARY KEY UNIQUE,
            	`IA`	INTEGER,
            	`EA`	INTEGER,
            	`TM`	INTEGER,
                'GRADE'  INTEGER
            )'''.format(scodes[i])
            cur.execute(query)

            query = '''INSERT OR REPLACE INTO {} (USN, IA, EA, TM, GRADE) VALUES (?, ?, ?, ?, ?)'''.format(scodes[i])
            cur.execute(query, (usn, ia[i], ea[i], tm[i], g[i]))


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

    name  = re.findall("Student Name  : ([A-Z\s\.]+)*\s*Semester :",text)
    name = ' '.join(name)
    name = name.rstrip()
    name = name.title()

    sem = re.findall("Semester[:\s]+([0-8])",text)
    sem = ''.join(sem)
    sem = sem[0]
    sem = int(sem)

    # usn  = re.findall("University Seat Number   : ([A-Z0-9]+)\s*Stud",text)
    usn  = re.findall("University Seat Number[:\s]+(\S+)\s*Stud",text)
    usn = ' '.join(usn)
    usn = usn.rstrip()
    usn = usn.upper()

    ssscodes = re.findall("([0-9]{2,}[A-Z]{3,}[0-9]{2,})",text)
    sscodes = ''.join(ssscodes)
    scodes = re.findall("[0-9]{1,2}([A-Z]+[0-9]{1,2})", sscodes)

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

    if sem == 1 or sem == 2:
        s = (tm[0] + tm[1] + tm[2] + tm[3] + tm[4] + tm[5]/2 + tm[6]/2)
        pc = s/6
        pc = round(pc,2)
        sgpa = (g[0] + g[1] + g[2] + g[3] + g[4] + g[5]/2 + g[6]/2)/6
        sgpa = round(sgpa,2)

    elif sem == 3 or sem == 4:
        s = (tm[0] + tm[1] + tm[2] + tm[3] + tm[4] + tm[5] + tm[6]/2 + tm[7]/2)
        pc = s/7
        pc = round(pc,2)
        sgpa = (g[0] + g[1] + g[2] + g[3] + g[4] + g[5] + g[6]/2 + g[7]/2)/7
        sgpa = round(sgpa,2)

    elif sem == 5 or sem == 6:
        s = (tm[0]*4 + tm[1]*4 + tm[2]*4 + tm[3]*4 + tm[4]*3 + tm[5]*3 + tm[6]*2 + tm[7]*2)/4
        pc = s/6.5
        pc = round(pc,2)
        sgpa = (g[0]*4 + g[1]*4 + g[2]*4 + g[3]*4 + g[4]*3 + g[5]*3 + g[6]*2 + g[7]*2)/26
        sgpa = round(sgpa,2)

    elif sem == 7:
        s = (tm[0]*4 + tm[1]*4 + tm[2]*4 + tm[3]*3 + tm[4]*3 + tm[5]*2 + tm[6]*2 + tm[7]*2)/4
        pc = s/6
        pc = round(pc,2)
        sgpa = (g[0]*4 + g[1]*4 + g[2]*4 + g[3]*3 + g[4]*3 + g[5]*2 + g[6]*2 + g[7]*2)/24
        sgpa = round(sgpa,2)

    else:
        s = (tm[0]*4 + tm[1]*4 + tm[2]*3 + tm[3]*2 + tm[4]*6 + tm[5]*1)/4
        pc = s/5
        pc = round(pc,2)
        sgpa = (g[0]*4 + g[1]*4 + g[2]*3 + g[3]*2 + g[4]*6 + g[5]*1)/20
        sgpa = round(sgpa,2)

    dbwrite(usn, name, pc, sem, sgpa, f, ia, ea, tm, g, scodes)

    print(pc, '%')
    print("Semester", sem)
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
yr = input('Enter Batch year ')
br = input('Enter Branch ID ')
ran = int(input('Enter starting USN '))
filename = '1' + ci + yr + '.sqlite'

k = ran
flag = 0
while k <= 180:

    if k < 10:
        j = '00' + str(k)
    elif k < 100:
        j = '0' + str(k)
    else:
        j = str(k)

    url = 'http://results.vtu.ac.in/cbcs_17/result_page.php?usn=1' + ci + yr + br + j
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

from exp import expwrite #Generates txt database
table = 'Sem2'
expwrite(filename, table)
