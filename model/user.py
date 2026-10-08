#user.py
from sqlalchemy import Integer,String,DateTime,func,Index
from sqlalchemy.orm import Mapped,mapped_column
from datetime import datetime
from base import Base

class User(Base):
    __tablename__="users"

    # Equivalent of @Table(indexes={...})
    __table_args__=(
        Index("idx_user_role","role"),
        Index("idx_user_created_at","created_at"),
    )

    #id
    id:Mapped[int]=mapped_column(Integer,primary_key=True,autoincrement=True)

    #email
    email:Mapped[str]=mapped_column(String,unique=True,nullable=False)

    #username
    username:Mapped[str]=mapped_column(String(255),unique=True,nullable=False)

    #role 1:ADMIN,2:USER
    role:Mapped[int]=mapped_column(Integer,nullable=False)

    #status
    status:Mapped[int]=mapped_column(Integer,nullable=False)

    #password
    password:Mapped[str]=mapped_column(String(255),nullable=False)

    #created_at, Record insertion time
    created_at:Mapped[datetime]=mapped_column(DateTime,nullable=False,server_default=func.now())

    #updated_at, Record updated time
    updated_at:Mapped[datetime]=mapped_column(DateTime,server_default=func.now(),onupdate=func.now())


