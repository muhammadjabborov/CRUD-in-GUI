from abc import ABC, abstractmethod
import shelve
from datetime import datetime

from utilities import getAbsolutePath
import os


class BaseModel(ABC):
    table = ""
    def __init__(self) -> None:
        self.id = None
        self.created_date = None
        self.updated_date = None
        self.__isValid = True
    
    def save(self):
        if self.isValid:
            path = getAbsolutePath(self.table)
            with shelve.open(path) as db:
                # Shu obj yangi yaratilayotgani
                if self.id is None:
                    self.created_date = datetime.now()
                    if os.path.exists(str(path) + '.dir'):
                        print(path)
                        self.id = int(list(db.keys())[-1]) + 1
                    else:
                        self.id = 1
                else:
                    self.updated_date = datetime.now()
                db[str(self.id)] = self
        else:
            raise ValueError("Qiymatlardan biri noto'g'iri")

    def delete(self):
        with shelve.open(getAbsolutePath(self.table)) as db:
            del db[str(self.id)]

    @property
    def isValid(self):
        return self.__isValid
    @isValid.setter
    def isValid(self, isValid):
        self.__isValid = isValid

    @abstractmethod
    def update(self):
        pass
    
    @abstractmethod
    def print():
        pass

    def objects(table):
        with shelve.open(getAbsolutePath(table)) as db:
            for obj in db.values():
                yield obj

    def get_by_id(table, id):
        with shelve.open(getAbsolutePath(table)) as db:
            return db[str(id)]
class Region(BaseModel):
    table = "regions"
    def __init__(self, name) -> None:
        super().__init__()
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

    def update(self):
        pass

    def print():
        for item in BaseModel.objects(Region.table):
            print(item)

    def __str__(self) -> str:
        return self.name

    def objects():
        return BaseModel.objects(Region.table)

class District(BaseModel):
    table='districts'

    def __init__(self, name, regionId) -> None:
        super().__init__()
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
        with shelve.open(getAbsolutePath(self.table)) as db:
            if regionId in db:
                self.__regionId = regionId
            else:
                self.__regionId = 0
                self.isValid = False
            raise Exception("Viloyat topilmadi")

    @property
    def region(self):
        with shelve.open(getAbsolutePath(Region.table)) as db:
            return db[str(self.regionId)]

    def print():
        for item in BaseModel.objects(District.table):
            print(item)

    def update(self):
        pass

    def __str__(self) -> str:
        return f'{self.region.name} {self.name}'
