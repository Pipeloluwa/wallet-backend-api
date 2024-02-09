from fastapi import APIRouter, Depends, status, HTTPException
from .. import schemas, database, oauth2, models
from sqlalchemy.orm import Session
from ..repositories import user
from . import authentication
from fastapi.security import OAuth2PasswordRequestForm
from typing import List

import os
from dotenv import load_dotenv
from ..hashing import Hash

load_dotenv()

router= APIRouter(prefix="/user", tags= ["Users"])
get_db= database.get_database


USERNAME= os.getenv('ADMIN_USER') ,
ROLE=  os.getenv('ADMIN_ROLE') ,
try:
    PASSWORD= Hash.enc(os.getenv('ADMIN_PASSWORD'))
except:
    pass

@router.get('/auto-create-admin', status_code= status.HTTP_201_CREATED)
async def auto_create_admin( db: Session= Depends(get_db)):
    if db.query(models.Users).filter(models.Users.username== USERNAME).first():
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN)
    admin_as_user= models.Users(username= USERNAME, role= ROLE, password= PASSWORD)
    db.add(admin_as_user)
    db.commit()
    db.refresh(admin_as_user)




@router.get('/manual_verify_user',status_code= status.HTTP_200_OK)
def manual_verify(db: Session= Depends(get_db), current_user: schemas.SignUp= Depends(oauth2.get_current_user)):
    if db.query(models.Users).filter(models.Users.username == current_user.username).first() == None:
        raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED)


@router.post('/register', status_code= status.HTTP_201_CREATED)
async def user_sign_up(request: schemas.SignUp, db: Session= Depends(get_db)):
    return await user.user_sign_up(request, db)


@router.post('/add-token', status_code= status.HTTP_201_CREATED)
async def add_token(request: schemas.TokenAddWallet, db: Session= Depends(get_db), current_user: schemas.SignUp= Depends(oauth2.get_current_user)):
    return await user.add_token(request, current_user.username, db)


@router.get('/get-user', response_model= schemas.Users, status_code= status.HTTP_200_OK)
async def get_user(db: Session= Depends(get_db), current_user: schemas.SignUp= Depends(oauth2.get_current_user)):
    return await user.get_user(current_user.username, db)

