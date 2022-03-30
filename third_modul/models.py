from abc import ABC, abstractmethod
import shelve
from datetime import datetime

from utilities import getAbsolutePath
import os
import sqlite3
from settings import db_name


class BaseModel(ABC):
    table = ''

    def __init__(self, id) -> None:
        self.id = id
        self.created_date = None
        self.updated_date = None
        self.__isValid = True

    @abstractmethod
    def save(self):
        pass

    def delete(self):
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute(f"Delete From {self.table} Where Id='{self.id}'")
        conn.commit()
        conn.close()

    @property
    def isValid(self):
        return self.__isValid

    @isValid.setter
    def isValid(self, isValid):
        self.__isValid = isValid
        pass

    @abstractmethod
    def print():
        pass

    @abstractmethod
    def get_by_id(id):
        pass


class Region(BaseModel):
    table = "Region"

    def __init__(self, name, id=None) -> None:
        super().__init__(id)
        self.name = name

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        if isinstance(name, str):
            self.__name = name
        else:
            self.__name = ''

    def save(self):
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        if self.id is None:
            cursor.execute(f"INSERT INTO Region (Name) VALUES ('{self.name}')")
            self.id = cursor.lastrowid
        else:
            cursor.execute(f"UPDATE Region set Name = '{self.name}' where Id = {self.id}")
        conn.commit()
        conn.close()

    def get_by_id(id):
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor = conn.execute(f"SELECT *from {Region.table} Where Id={id}")

        sql_row = list(cursor)[0]
        sel_region = Region(sql_row[1], sql_row[0])

        conn.commit()
        conn.close()

        return sel_region

    def print():
        for item in BaseModel.objects(Region.table):
            print(item)

    def __str__(self) -> str:
        return self.name

    def objects():
        conn = sqlite3.connect(db_name)
        cursor = conn.execute(f"SELECT *from {Region.table}")
        for row in cursor:
            yield Region(row[1], row[0])
        conn.close()

    def rows():
        conn = sqlite3.connect(db_name)
        cursor = conn.execute(f"SELECT *from {Region.table}")
        row_s = cursor.fetchall()
        conn.close()

        return row_s


class District(BaseModel):
    table = 'District'

    def __init__(self, name, regionId, id=None) -> None:
        super().__init__(id)
        self.name = name
        self.regionId = regionId

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        if isinstance(name, str):
            self.__name = name
        else:
            self.__name = ''

    @property
    def regionId(self):
        return self.__regionId

    @regionId.setter
    def regionId(self, regionId):
        self.__regionId = regionId

    @property
    def region(self):
        return Region.get_by_id(self.regionId)

    def print():
        for item in BaseModel.objects(District.table):
            print(item)

    def update(self):
        pass

    def get_by_id(id):
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor = conn.execute(f"SELECT *from {District.table} Where Id={id}")

        sql_row = list(cursor)[0]
        sel_region = District(sql_row[1], sql_row[2], sql_row[0])

        conn.commit()
        conn.close()

        return sel_region

    def save(self):
        print(db_name)
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        if self.id is None:
            cursor.execute(
                f"INSERT INTO District (Name, regionId) VALUES ('{self.name}', {self.regionId})")
            self.id = cursor.lastrowid
        else:
            cursor.execute(
                f"UPDATE District set Name = '{self.name}', regionId={self.regionId} where Id = {self.id}")
        conn.commit()
        conn.close()

    def __str__(self) -> str:
        return f'{self.region.name} {self.name}'

    def objects():
        conn = sqlite3.connect(db_name)
        cursor = conn.execute(f"SELECT *from {District.table}")
        for row in cursor:
            yield District(row[1], row[2], row[0])
        conn.close()
