import sqlite3

conn = sqlite3.connect('emaildb.sqlite')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS Counts')

cur.execute('''CREATE TABLE Counts (org TEXT, count INTEGER)''')

file_name = input('Enter file name: ')
if len(file_name) < 1: file_name = 'mbox-short.txt'
fh = open(file_name)
for line in fh:
    if not line.startswith('From: '): continue
    pieces = line.split()
    email = pieces[1]  # grab emails
    parts = email.split('@')  # split the emails at '@'
    org = parts[-1]  # get the organisation part (which is the last item in the array) with a slice notation
    cur.execute('SELECT count FROM Counts WHERE org = ? ', (org,))  # this line does not retrieve the data
    row = cur.fetchone()  # grab that first one and give it back in row which is the information from the DB
    # if row is None, run insert statement
    if row is None:  # and if there are no records there than the row is going to be None
        cur.execute('''INSERT INTO Counts (org, count) 
                VALUES (?, 1)''', (org,))  # set count to 1 into the new record
    else:  # handles the case where there are already record with the number of emails
        cur.execute('UPDATE Counts SET count = count + 1 WHERE org = ?',
                    (org,))
    conn.commit()

sqlstr = 'SELECT org, count FROM Counts ORDER BY count DESC LIMIT 10'

for row in cur.execute(sqlstr):
    print(str(row[0]), row[1])

cur.close()
"""
Output:

Enter file name: mbox.txt
iupui.edu 536
umich.edu 491
indiana.edu 178
caret.cam.ac.uk 157
vt.edu 110
uct.ac.za 96
media.berkeley.edu 56
ufp.pt 28
gmail.com 25
et.gatech.edu 17
"""