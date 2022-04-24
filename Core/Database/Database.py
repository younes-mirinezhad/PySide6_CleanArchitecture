# sqlalchemy tutorial: https://docs.sqlalchemy.org/en/14/tutorial/index.html
import os
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import declarative_base
# from sqlalchemy import MetaData, Table

Base = declarative_base()


class Database():
    def __init__(self):
        super(Database, self).__init__()
        print("-- Database")
        self._dbPath = os.getcwd() + "/data.db"
        self.engine = create_engine('sqlite+pysqlite:///' + self._dbPath, future=True)
#        self.alterEngine = create_engine('sqlite+pysqlite:///' + self._dbPath)
        print("---- Database Loaded")

    def createTables(self):
        print("---- createTables")
        Base.metadata.create_all(self.engine)
        print("------ Done")

        # ---------- can use this to add new fields into table
        # (Need to line: 5, 16)
        # meta = MetaData()
        # meta.reflect(bind=self.alterEngine)
        # tbl = meta.tables['user_account']
        # if('name' not in tbl.columns.keys()):
        #     self.alterEngine.execute('alter table user_account add column name String(30)')


class Projects(Base):
    print("-- Projects")
    __tablename__ = 'projects_tbl'

    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    description = Column(String, nullable=True)

    def __repr__(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
            }
