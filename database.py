import urllib
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

# 1. create_url 대신 create_engine을 사용합니다.
# 2. 연결 문자열 (본인의 설정에 맞게 수정되어 있는지 확인하세요)
# 예: DRIVER={ODBC Driver 18 for SQL Server};SERVER=...
connection_string = os.getenv("DATABASE_URL") 

# 직접 입력을 선호하신다면 아래 형식을 따르세요
# params = urllib.parse.quote_plus("DRIVER={ODBC Driver 18 for SQL Server};SERVER=your-server.database.windows.net;DATABASE=your-db;UID=your-user;PWD=your-password")
# engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")

# 테스트용 (연결 문자열이 준비되지 않았다면 임시로 이렇게 두세요)
engine = create_engine("sqlite:///./test.db") # Azure SQL 연결 전 테스트용

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()