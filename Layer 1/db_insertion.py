import mysql.connector

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='ransomware'
)

cursor = conn.cursor()

with open('C:\\Users\\Tejaswini\\Downloads\\IDS.txt', 'r') as file:
    for line in file:
        
        values = tuple(line.strip().split(';'))

        insert_query = '''
            INSERT INTO signature (id, sha1, md5, rw, rwfamily)
            VALUES (%s, %s, %s, %s, %s)
        '''

        cursor.execute(insert_query, values)

conn.commit()
cursor.close()
conn.close()