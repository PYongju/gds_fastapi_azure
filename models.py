from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

# 1. 유저 테이블
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    role = Column(String)
    created_at = Column(DateTime, default=datetime.now)

    posts = relationship("Post", back_populates="author")
    comments = relationship("Comment", back_populates="author")

# 2. 게시글 테이블
class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    body = Column(Text) # DBML의 [note: 'Content of the post'] 부분
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(String)
    created_at = Column(DateTime, default=datetime.now)

    author = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post")

# 3. 댓글 테이블
class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("posts.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    content = Column(String) # NVARCHAR(MAX) 대응
    image_url = Column(String)
    toxicity_score = Column(Float)
    created_at = Column(DateTime, default=datetime.now)
    label = Column(String(20))

    post = relationship("Post", back_populates="comments")
    author = relationship("User", back_populates="comments")
    admin_logs = relationship("AdminLog", back_populates="comment")

# 4. 관리자 대쉬보드 테이블 (추가됨)
class AdminLog(Base):
    __tablename__ = "admin_log"
    id = Column(Integer, primary_key=True, index=True)
    comments_id = Column(Integer, ForeignKey("comments.id"))

    comment = relationship("Comment", back_populates="admin_logs")

# 5. 모델 관리 테이블 (추가됨)
class MLModel(Base):
    __tablename__ = "ml_model"
    # 이 테이블은 PK가 DBML에 명시되지 않았지만, SQLAlchemy 연동을 위해 
    # 보통 하나 이상의 컬럼을 primary_key로 잡아야 합니다.
    model_version = Column(String(50), primary_key=True) 
    inference_time = Column(Float)