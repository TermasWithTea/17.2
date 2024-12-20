from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.backend.db_depends import get_db
from typing import Annotated
from app.models import User
from app.schemas import CreateUser, UpdateUser
from sqlalchemy import select, insert, update, delete

router = APIRouter(prefix='/user', tags=['user'])


@router.get('/')
async def all_users(db: Annotated[Session, Depends(get_db)]):
    users = db.execute(select(User)).scalars().all()
    return users


@router.get('/{user_id}')
async def user_by_id(user_id: int, db: Annotated[Session, Depends(get_db)]):
    user = db.execute(select(User).where(User.id == user_id)).scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="User  was not found")
    return user


@router.post('/create')
async def create_user(user: CreateUser, db: Annotated[Session, Depends(get_db)]):
    existing_user = db.execute(select(User).where(User.username == user.username)).scalar_one_or_none()
    if existing_user:
        raise HTTPException(status_code=400, detail="User  with this username already exists")

    new_user = User(**user.dict())
    db.execute(insert(User).values(new_user.__dict__))
    db.commit()
    return {'status_code': status.HTTP_201_CREATED, 'transaction': 'Successful'}


@router.put('/update/{user_id}')
async def update_user(user_id: int, user: UpdateUser, db: Annotated[Session, Depends(get_db)]):
    stmt = update(User).where(User.id == user_id).values(**user.dict())
    result = db.execute(stmt)
    db.commit()

    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="User  was not found")

    return {'status_code': status.HTTP_200_OK, 'transaction': 'User  update is successful!'}


@router.delete('/delete/{user_id}')
async def delete_user(user_id: int, db: Annotated[Session, Depends(get_db)]):
    stmt = delete(User).where(User.id == user_id)
    result = db.execute(stmt)
    db.commit()
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="User  was not found")

    return {'status_code': status.HTTP_200_OK, 'transaction': 'User  deleted successfully!'}