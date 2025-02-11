from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base




DATABASE_URL = "mysql+pymysql://root:Petrucci@localhost/user_todos"

engine = create_engine(DATABASE_URL)

Sessionlocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base = declarative_base()

def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally: 
        db.close()