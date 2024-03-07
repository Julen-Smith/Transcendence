from django.core.validators import validate_email
from ninja.errors import HttpError
from transcendence.settings import TRANSCENDENCE, logger
import datetime, jwt
from . import schemas

BEARER_OFFSET = 7
SECRET = TRANSCENDENCE['JWT']['secret']
ALGORITHM = TRANSCENDENCE['JWT']['algorithm']
REFRESH = TRANSCENDENCE['JWT']['refresh']


def encode_token(jwt_input: schemas.JWTInput) -> str:

    exp_date = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=jwt_input.expire_time)

    payload = {
        "username": jwt_input.username,
        "exp": exp_date
    }

    return jwt.encode(payload, SECRET, algorithm=ALGORITHM)

def decode_token(token: str) -> dict:

    try:
        decoded = jwt.decode(token, SECRET, algorithms=ALGORITHM)
    except jwt.exceptions.InvalidSignatureError:
        raise HttpError(status_code=401, message="Error: Invalid Token")

    except jwt.exceptions.ExpiredSignatureError:
        raise HttpError(status_code=401, message="Error: Expired Token")

    except jwt.exceptions.DecodeError:
        raise HttpError(status_code=401, message="Error: Bad Token")

    except Exception as err:
        raise HttpError(status_code=401, message="Error: Unhandled Error")

    email = decode_token.get("email")
    if email is None or not validate_email(email):
        raise HttpError(status_code=401, message="Error: User Unauthorized")

    if decoded.get("exp") is None:
        raise HttpError(status_code=401, message="Error: No Time Expedition")
    return decoded

def create_jwt(jwt_input: schemas.JWTInput):

    #TOKEN
    token = encode_token(jwt_input)

    #REFRESH_TOKEN
    refresh_token = encode_token(jwt_input)

    return schemas.JWTToken(token=token, refresh=refresh_token)

def check_jwt(request, jwt_token: schemas.JWTToken) -> bool | HttpError:

    if not jwt_token.token.startswith("Bearer "):
        raise HttpError(status_code=400, message="Error: Token does not have bearer")

    return decode_token(jwt_token.token[BEARER_OFFSET:])

def refresh_jwt(jwt_token: schemas.JWTToken):

    decoded = decode_token(jwt_token.refresh)

    email = decoded.get("email")
    if email is None:
        raise HttpError(status_code=403, message="Error: Unauthorized")

    jwt_input = schemas.JWTInput(
        username=email,
        expire_time=30
    )

    jwt_token.token = encode_token(jwt_input)
    return jwt_token

def authorize(request):

    auth = request.headers.get("Authorization")
    if auth is None:
        raise HttpError(status_code=403, message="Error: Unauthorized")

    decode_token(auth)
    return request
