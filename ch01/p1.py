from sqlalchemy import create_engine
from sqlalchemy import types
from sqlalchemy.dialects.postgresql import JSON, NUMRANGE

engine1 = create_engine('sqlite:///cookies.db')
engine2 = create_engine('mysql+pymysql://root:123456@localhost:3306/cookies', pool_recycle=3600)

connection1 = engine1.connect()
connection2 = engine2.connect()
