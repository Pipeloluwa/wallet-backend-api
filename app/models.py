from sqlalchemy import Column, Integer, String, ForeignKey
from .database import Base
from sqlalchemy.orm import relationship
import time

class Users(Base):
    __tablename__= "users"
    activated= Column(String, default= True)
    id= Column(Integer, primary_key=True, index= True)
    username= Column(String, unique=True)
    role= Column(String)
    password= Column(String)
    registration_date= Column(String, default= time.strftime("%Y%m%d-%H%M%S"))
    
    user_tokens= relationship("TokenWallet", back_populates="users")


class TokenWallet(Base):
    __tablename__= "tokenwallet"
    date_and_time_of_sample= Column(String, default= time.strftime("%Y%m%d-%H%M%S"))
    id= Column(String, primary_key=True, index= True, unique=True)
    token_key= Column(String, primary_key=True, index= True)
    users_id= Column(Integer, ForeignKey('users.id'))
    users= relationship("Users", back_populates="user_tokens")
