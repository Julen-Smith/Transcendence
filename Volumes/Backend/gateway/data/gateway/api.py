#CORE

from transcendence.settings import TRANSCENDENCE, logger
from django.http import HttpResponseRedirect

import hashlib, os, requests, jwt, datetime, aiohttp
from . import schemas

from ninja import Router
from ninja.errors import HttpError
from django.core.validators import validate_email

router = Router()

BEARER_OFFSET = 7
SECRET = TRANSCENDENCE['JWT']['secret']
ALGORITHM = TRANSCENDENCE['JWT']['algorithm']
REFRESH = TRANSCENDENCE['JWT']['refresh']


def encode_token(jwt_input: schemas.JWTInput) -> str:

    exp_date = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=jwt_input.expire_time)

    payload = {
        "email": jwt_input.email,
        "exp": exp_date
    }

    return jwt.encode(payload, SECRET, algorithm=ALGORITHM)

def decode_token(token: str) -> dict:

    try:
        decoded = jwt.decode(token, SECRET, algorithms=ALGORITHM)
    except jwt.exceptions.InvalidSignatureError:
        raise HttpError(status_code=400, message="Error: Invalid Token")

    except jwt.exceptions.ExpiredSignatureError:
        raise HttpError(status_code=403, message="Error: Expired Token")

    except jwt.exceptions.DecodeError:
        raise HttpError(status_code=400, message="Error: Bad Token")

    except Exception as err:
        raise HttpError(status_code=404, message="Error: Unhandled Error")

    email = decode_token.get("email")
    if email is None or not validate_email(email):
        raise HttpError(status_code=403, message="Error: User Unauthorized")

    if decoded.get("exp") is None:
        raise HttpError(status_code=403, message="Error: No Time Expedition")
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
        email=email,
        expire_time=30
    )

    jwt_token.token = encode_token(jwt_input)
    return jwt_token

@router.get('/test/login', tags=['test connection'])
async def test_login_connectio(request):

    async with aiohttp.ClientSession() as session:
        async with session.get('http://login:25671/api/login/test') as res:
            return await res.json()

import os

S_LOGIN_GOOGLE_LOGIN_URL = os.environ['S_LOGIN_GOOGLE_LOGIN']
S_LOGIN_GOOGLE_CALLBACK_URL = os.environ['S_LOGIN_GOOGLE_CALLBACK']

@router.get('/login/google', tags=['login'])
def login_google(request):

    state = hashlib.sha256(os.urandom(1024)).hexdigest()
    request.session["google_oauth2_state"] = state

    payload = {"state": state}

    logger.warning(S_LOGIN_GOOGLE_LOGIN_URL)
    res = requests.get(S_LOGIN_GOOGLE_LOGIN_URL, params=payload)

    try:
        info = res.json()
    except Exception as err:
        raise HttpError(status_code=500, message="Error: Login Service Failed")


    if not res.ok:
        detail = info.get('detail')
        if detail is None:
            raise HttpError(status_code=400, message="Error: Unknown error")
        raise HttpError(status_code=res.status_code, message=detail)

    url = info.get('url')
    if url is None:
        raise HttpError(status_code=400, message="Error: url not found")

    return HttpResponseRedirect(url)

@router.get('/login/google/callback', tags=['login'])
def login_google_callback(request, code: str, state: str, error: str | None = None):

    if error:
        raise HttpError(status_code=401, message=f"Error found: {error}")

    user_state = request.session.get('google_oauth2_state')
    if not user_state or state != user_state:
        raise HttpError(status_code=401, message="Error: Unautorithed")
    del request.session['google_oauth2_state']

    params = {
        "code": code,
        "state": state,
    }

    res = requests.get(S_LOGIN_GOOGLE_CALLBACK, params=params)

    try:
        info = res.json()
    except Exception as err:
        raise HttpError(status_code=500, message="Error: Login Service Failed")

    url = info.get('url')
    email = info.get('email')

    #HANDLE OTP
    logger.warning(email)
    logger.warning(info)
    jwt_input = schemas.JWTInput(email=email)

    if not res.ok:
        jwt_input.permission = 0
        jwt_input.expire_time = 5

    jwt_token = create_jwt(jwt_input)
    response = HttpResponseRedirect(url)
    response.set_cookie('token', jwt_token.token)
    response.set_cookie('refresh', jwt_token.refresh)
    return response

@router.get('/opt')
async def check_otp(request):

    """
    jwt_input = schemas.JWTInput(email=email)

    if not res.ok:
        jwt_input.permission = 0
        jwt_input.expire_time = 5

    jwt_token = create_jwt(jwt_input)

    response.set_cookie('token', jwt_token.token)
    response.set_cookie('refresh', jwt_token.refresh)
    """

    return 