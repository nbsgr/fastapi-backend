#users repository
from sqlalchemy import select,or_
from model.user import User

#save user
def save(user:User,db):
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

#exists_by
def exists_by_email(email,db):
    return db.scalar(
        select(User).where(User.email==email)
    ) is not None

def exists_by_username(username,db):
    return db.scalar(
        select(User).where(User.username==username)
    ) is not None

#find_by
def find_by_email(email,db):
    return db.scalar(
        select(User).where(User.email==email)
    )

def find_by_username(username,db):
    return db.scalar(
        select(User).where(User.username==username)
    )

def find_by_email_or_username(email,username,db):
    return db.scalar(
        select(User).where(
            or_(
                User.email==email,
                User.username==username
            )
        )
    )

#find the list

def find_by_role(role,db):
    return db.scalars(
        select(User).where(User.role==role)
    ).all()

def find_by_status(status,db):
    return db.scalars(
        select(User).where(User.status==status)
    ).all()

def find_by_role_and_status(role,status,db):
    return db.scalars(
        select(User).where(
            User.role==role,
            User.status==status
        )
    ).all()

def find_by_username_and_role(username,role,db):
    return db.scalars(
        select(User).where(
            User.username==username,
            User.role==role
        )
    ).all()

def find_by_status_and_created_at_desc(status,db):
    return db.scalars(
        select(User).where(
            User.status==status
        ).order_by(User.created_at.desc())
    ).all()
