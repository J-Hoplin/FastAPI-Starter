from pydantic import BaseModel, EmailStr


class SigninRequest(BaseModel):
    email: EmailStr
    password: str
