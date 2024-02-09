from pydantic import BaseModel, Field
from typing import List, Optional
from pydantic.types import constr



class TokenDataUser(BaseModel):
    username: Optional[str]= None

class SignUp(BaseModel):
    username: str
    password: str


class TokenAddWallet(BaseModel):
    id: str
    token_key: str



class TokenWallet(BaseModel):
    date_and_time_of_sample: str
    id: str
    token_key: str



class Users(BaseModel):
    activated: str
    id: int
    username: str
    role: str
    password: str
    registration_date: str
    
    user_tokens: List[TokenWallet]
