from prettytable import PrettyTable
import sqlite3

def expwrite (filename, table):
    conn = sqlite3.connect(filename)
    curs = conn.cursor()
    query = 'SELECT USN, Name, PC AS Percent, SGPA, Fail FROM {}'.format(table)
    curs.execute()

    col_names = [cn[0] for cn in curs.description]
    rows = curs.fetchall()

    x = PrettyTable(col_names)
    x.align[col_names[1]] = "l"
    x.align[col_names[2]] = "r"
    x.padding_width = 1
    for row in rows:
        x.add_row(row)

    print(x)
    tabstring = x.get_string()

    output=open("export.txt","w")
    output.write("Results"+"\n")
    output.write(tabstring)
    output.close()

    conn.close()
