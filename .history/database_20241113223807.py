import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Check if running inside a Docker container
def is_running_in_docker():
    if os.path.exists('/proc/self/cgroup'):
        with open('/proc/self/cgroup', 'rt') as f:
            return 'docker' in f.read()
    return False

# Retrieve the database URL from environment variables or use defaults
if is_running_in_docker():
    # If inside Docker, use Docker-specific database URL
    URL_DATABASE = os.getenv("DATABASE_URL_DOCKER")
else:
    # If running locally, use localhost database URL
    URL_DATABASE = os.getenv("DATABASE_URL_LOCAL")

# Initialize SQLAlchemy engine and session
engine = create_engine(URL_DATABASE, pool_recycle=28000)  # Adjust to your wait_timeout value
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()





















'''
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
    # Update this with your AWS RDS MySQL endpoint if running inside Docker
    URL_DATABASE =  "mysql+pymysql://aervion1_ymzaidi:0123456789@aervion.com:3306/aervion1_weather"
else:
    URL_DATABASE = "mysql+pymysql://aervion1_ymzaidi:0123456789@aervion.com:3306/aervion1_weather"
    
# Initialize SQLAlchemy engine and session
engine = create_engine(URL_DATABASE, pool_recycle=28000)  # Adjust to your wait_timeout value
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
'''









"""
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
    URL_DATABASE = "mysql+pymysql://root:admin@host.docker.internal:3306/weather"
else:
    URL_DATABASE = "mysql+pymysql://root:admin@localhost:3306/weather"

engine = create_engine(URL_DATABASE)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
"""