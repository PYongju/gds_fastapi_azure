from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func # 서버 시간 사용을 위해 추가
from database import Base

# 1. 유저 테이블
class User(Base):
    __tablename__ = "users"
    # primary_key=True 설정이 MSSQL의 IDENTITY와 자동 연동됩니다.
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255)) # nvarchar(255) 대응
    role = Column(String(50))     # nvarchar(50) 대응
    # default 대신 server_default를 쓰면 DB가 직접 getdate()를 실행합니다.
    created_at = Column(DateTime, server_default=func.now())

    posts = relationship("Post", back_populates="author")
    comments = relationship("Comment", back_populates="author")

# 2. 게시글 테이블
class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    title = NVARCHAR(String(255))
    body = Column(Text) 
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(String(50))
    created_at = Column(DateTime, server_default=func.now())

    author = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post")

# 3. 댓글 테이블
class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    content = Column(Text) # 긴 텍스트를 위해 Text 혹은 String 명시
    image_url = Column(String(500))
    toxicity_score = Column(Float)
    created_at = Column(DateTime, server_default=func.now())
    label = Column(String(20))

    post = relationship("Post", back_populates="comments")
    author = relationship("User", back_populates="comments")
    admin_logs = relationship("AdminLog", back_populates="comment")

# 4. 관리자 로그 테이블
class AdminLog(Base):
    __tablename__ = "admin_log"
    id = Column(Integer, primary_key=True, index=True)
    comments_id = Column(Integer, ForeignKey("comments.id"), nullable=False)

    comment = relationship("Comment", back_populates="admin_logs")

# 5. 모델 관리 테이블
class MLModel(Base):
    __tablename__ = "ml_model"
    model_version = Column(String(50), primary_key=True) 
    inference_time = Column(Float)
    # 모델 등록 시간도 있으면 관리하기 편합니다.
    created_at = Column(DateTime, server_default=func.now())