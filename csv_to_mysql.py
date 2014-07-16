import csv
import MySQLdb

mydb = MySQLdb.connect(host='localhost',
    user='root',
    passwd='neo&trinity',
    db='training_data')
cursor = mydb.cursor()

fileName = raw_input("Enter csv file name: ")

csv_data = csv.reader(file(fileName))

for row in csv_data:
    cursor.execute('INSERT INTO productList(image_url, description, name, link) VALUES(%s,%s,%s,%s)', row)
#close the connection to the database.

mydb.commit()

cursor.close()
print ("Done")
