import urllib
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# .env 파일이 로컬에 있을 경우 환경 변수를 로드합니다.
load_dotenv()

# Azure App Service 설정(환경 변수)에서 DATABASE_URL을 가져옵니다.
# 형식: Driver={ODBC Driver 18 for SQL Server};Server=tcp:...
connection_string = os.getenv("DATABASE_URL")

if connection_string:
    try:
        # SQLAlchemy는 ODBC 문자열을 직접 인식하지 못하므로 특수 인코딩이 필요합니다.
        quoted_params = urllib.parse.quote_plus(connection_string)
        # mssql+pyodbc 형식을 사용하여 엔진을 생성합니다.
        engine = create_engine(
            f"mssql+pyodbc:///?odbc_connect={quoted_params}",
            echo=True, # 로그에 SQL 실행문을 출력 (디버깅용)
            pool_pre_ping=True # 연결 유효성을 자동으로 체크
        )
        print("✅ Azure SQL Database에 연결할 준비가 되었습니다.")
    except Exception as e:
        print(f"❌ 엔진 생성 중 오류 발생: {e}")
        # 오류 발생 시 안전하게 SQLite로 폴백(Fallback)
        engine = create_engine("sqlite:///./test.db", connect_args={"check_same_thread": False})
else:
    # 환경 변수가 설정되지 않은 경우 (로컬 개발 환경 등)
    print("⚠️ DATABASE_URL이 없습니다. 로컬 SQLite를 사용합니다.")
    engine = create_engine("sqlite:///./test.db", connect_args={"check_same_thread": False})

# 세션 관리 및 베이스 클래스 생성
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# FastAPI에서 DB 세션을 사용할 때 호출할 함수
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()