from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import MetaData
from settings import DB_URI
engine = create_async_engine(
    DB_URI,
    echo=True,
    pool_size=10,
    max_overflow=20,
    pool_timeout=10,
    pool_recycle=3600,
    pool_pre_ping=True,
) # 数据库设置

AsyncSessionFactory = sessionmaker(
    # Engine或者其子类对象
    bind=engine,
    # Session类的代替
    class_=AsyncSession,
    # 是否在查找之前执行flush操作
    autoflush=True,
    # 是否在执行commit操作后Session就过期
    expire_on_commit=False
)



# 定义命名约定的Base类
class Base(DeclarativeBase):
    metadata = MetaData(naming_convention={
        "ix": 'ix_%(column_0_label)s',
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
    })

from . import user