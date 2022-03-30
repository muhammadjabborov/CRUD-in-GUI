import sqlite3
conn = sqlite3.connect('db/car.db')
cursor=conn.cursor()
cursor.execute(f"Select Name from brands")
for item in cursor:
    print(item)
# create
#cursor.execute(f"INSERT INTO brands (Name) VALUES ('Daewoo')")
# Updating
#cursor.execute(f"Update brands set Name='Audi' Where Id=1")
# Deleting
cursor.execute(f"Delete From brands Where Id=1")
conn.commit()
conn.close()