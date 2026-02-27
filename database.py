from sqlalchemy import create_url
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import urllib

# 1. 연결 정보 설정 (Azure Portal의 '연결 문자열'에서 복사 가능)
server = 'your-server-name.database.windows.net'
database = 'your-db-name'
username = 'your-username'
password = 'your-password'
driver = '{ODBC Driver 18 for SQL Server}' # 설치된 드라이버 버전에 맞춰 수정

# 2. ODBC 연결 문자열 생성
params = urllib.parse.quote_plus(
    f"DRIVER={driver};SERVER={server};DATABASE={database};"
    f"UID={username};PWD={password};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
)
conn_str = f"mssql+pyodbc:///?odbc_connect={params}"

# 3. SQLAlchemy 엔진 생성
engine = create_engine(conn_str)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# DB 세션 의존성
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()