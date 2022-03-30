import os
base_path = os.getcwd()
database_folder = os.path.join(base_path, 'db')
db_name = os.path.join(database_folder, 'test.db')

print(db_name)