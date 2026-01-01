from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

#for sqlite database use this
# SQLALCHEMY_DATABASE_URL = 'sqlite:///./todosapp.db'
# engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

#For postgresql database use this
# SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:bhavana%4023@localhost/TodoAppDatabase'
# engine = create_engine(SQLALCHEMY_DATABASE_URL)

#For mysql database use this
SQLALCHEMY_DATABASE_URL = 'mysql+pymysql://root:bhavana23@127.0.0.1:3306/todos'
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()




