from ninja import Schema, Field

###############
# JWT Achemas #
###############

class JWTInput(Schema):
    username: str = Field(max_length=32, examples=["lugonzal"])
    user_id: int = Field()
    expire_time: int = Field(ge=5, default=30)
    permission: int = Field(default=1)

class JWTToken(Schema):

    token: str
    refresh: str

class UserLogin(Schema):

    username: str
    password: str

class UserRegister(UserLogin):

    email: str