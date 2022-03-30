from settings import key_table, database
import shelve

with shelve.open(key_table) as db:
    print(db['vehical'])
