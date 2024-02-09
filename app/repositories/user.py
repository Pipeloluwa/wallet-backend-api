from .. import models
from ..hashing import Hash
# from ..routers import otp_management
from fastapi import HTTPException, status, Response
import os
from dotenv import load_dotenv

load_dotenv()


async def user_sign_up(request,  db):
    get_admin_id= db.query(models.Users).filter(models.Users.username==request.username)

    if get_admin_id.first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="this username is already taken")
    
    new_user= models.Users(username=request.username.lower(),
                          role= "user",
                          password= Hash.enc(request.password)
                          )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user





async def add_token(request, username, db):
    get_admin_id= db.query(models.Users).filter(models.Users.username==username)

    if not get_admin_id.first():
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"This acoount does not exist or has been deactivated")
    

    if db.query(models.TokenWallet).filter(models.TokenWallet.id== request.id).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="this token wallet was already created")
    
    new_token= models.TokenWallet(id= request.id,
                          token_key= request.token_key,
                          users_id= get_admin_id.first().id
                          )
    db.add(new_token)
    db.commit()
    db.refresh(new_token)
    
    return new_token




async def get_user(username, db):
    get_admin_id= db.query(models.Users).filter(models.Users.username==username)

    if not get_admin_id.first():
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"Your account does not exist or has been removed")
    
    
    if get_admin_id.first().activated == "false":
        raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail="Your account was deactivated, please send us mail in the contact centre to access your account")
    

    return get_admin_id.first()

