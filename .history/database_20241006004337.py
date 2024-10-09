from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Correct the URL_DATABASE to use 'pymysql'
#URL_DATABASE = 'mysql+pymysql://root:admin@localhost:3369/weather'
URL_DATABASE = "mysql+pymysql://root:admin@host.docker.internal:3369/weather"

engine = create_engine(URL_DATABASE)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
