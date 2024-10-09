import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Check if running inside a Docker container
def is_running_in_docker():
    if os.path.exists('/proc/self/cgroup'):
        with open('/proc/self/cgroup', 'rt') as f:
            return 'docker' in f.read()
    return False

# Set the database URL based on environment
if is_running_in_docker():
    URL_DATABASE = "mysql+pymysql://root:admin@host.docker.internal:3369/weather"
else:
    URL_DATABASE = "mysql+pymysql://root:admin@localhost:3369/weather"

engine = create_engine(URL_DATABASE)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
