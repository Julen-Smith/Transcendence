#CORE

from transcendence.settings import logger, GOOGLE
from django.http import HttpResponseRedirect

import hashlib, os, requests
from . import schemas, auth

import os
from ninja import Router
from ninja.errors import HttpError

router = Router()

logger.warning(GOOGLE)
S_LOGIN_REGISTER= GOOGLE["LOGIN_GOOGLE"]['S_LOGIN_REGISTER']
S_LOGIN_DEFAULT_LOGIN= GOOGLE["LOGIN_GOOGLE"]['S_LOGIN_DEFAULT_LOGIN']
S_LOGIN_GOOGLE_LOGIN= GOOGLE["LOGIN_GOOGLE"]['S_LOGIN_GOOGLE_LOGIN']
S_LOGIN_GOOGLE_CALLBACK= GOOGLE["LOGIN_GOOGLE"]['S_LOGIN_GOOGLE_CALLBACK']

#/log se encarga de recibir la informacion recopilada por el servidor sobre el navegador del usuario cuando entra en home y 
# redirigirla al endpoint /log del back para que la gestione. 
@router.post('/log', tags=['log'])
async def log(request):

    logger.warning('DATATOSERVER EN GATEWAY')
    return {"msg": 1}


@router.get('/login/google', tags=['login'])
def login_google(request):

    state = hashlib.sha256(os.urandom(1024)).hexdigest()
    request.session["google_oauth2_state"] = state

    payload = {"state": state}

    logger.warning(S_LOGIN_GOOGLE_LOGIN)
    res = requests.get(S_LOGIN_GOOGLE_LOGIN, params=payload)

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

    return {'url':url}

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

    logger.warning(f"Params: {params}")
    res = requests.get(S_LOGIN_GOOGLE_CALLBACK, params=params)

    try:
        info = res.json()
    except Exception as err:
        raise HttpError(status_code=500, message="Error: Login Service Failed")

    url = info.get('url')
    username = info.get('username')
    user_id = info.get('user_id')

    #HANDLE OTP
    logger.warning(f"EMAIL: {username}")
    logger.warning(info)
    jwt_input = auth.create_jwt(username=username, user_id=user_id)

    if not res.ok:
        jwt_input.permission = 0
        jwt_input.expire_time = 5

    response = HttpResponseRedirect(url)
    response.set_cookie('token', jwt_input.token)
    response.set_cookie('refresh', jwt_input.refresh)
    return response

@router.post('/test_otp')
def test_otp(request, receiver: str):

    payload = {"receiver": receiver}

    res = requests.post("http://login:25671/api/login/test/otp", params=payload)
    return res.json()

@router.get('/otp')
async def check_otp(request):

    """
    jwt_input = schemas.JWTInput(username=email)

    if not res.ok:
        jwt_input.permission = 0
        jwt_input.expire_time = 5

    jwt_token = create_jwt(jwt_input)

    response.set_cookie('token', jwt_token.token)
    response.set_cookie('refresh', jwt_token.refresh)
    """
    return 

@router.get('/intra', tags=['login']) #no entiendo el tema tags 
def login_intra(request):

    #  JWT, OTP y cookies

    res = requests.get('http://login:25671/api/login/intra')
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

@router.get('/login/intra_callback', tags=['login'])
def login_intra_callback(request, code:str):

    payload = {
        "code": code
    }
    res = requests.get('http://login:25671/api/login/intra/callback', params=payload)
    try:
        info = res.json()
    except Exception as err:
        raise HttpError(status_code=500, message="Error: Login Service Failed")

    url = info.get('url')

     # JWT, OTP y cookies

    return HttpResponseRedirect(url)

@router.post('/login/default', tags=['login'])
def login_default(request, user: schemas.UserLogin):

    res = requests.post(S_LOGIN_DEFAULT_LOGIN, json=user.__dict__)

    if not res.ok:
        raise HttpError(status_code=res.status_code, message="Error: Login failed")

    info = res.json()
    return auth.create_jwt(**info)

@router.post('/login/register', tags=['login'])
def login_register(request, user: schemas.UserRegister):

    payload = {
        'username': user.username,
        'password': user.password,
        'email': user.email,
        'mode': 0
    }

    logger.warning(S_LOGIN_REGISTER)
    res = requests.post(S_LOGIN_REGISTER, json=payload)

    if not res.ok:
        raise HttpError(status_code=res.status_code, message="Error: Register failed")

    info = res.json()
    return auth.create_jwt(**info)

@router.post('/login/unknown', tags=['login'])
def login_unknown(request, username: str):

    jwt_token = auth.create_jwt(username)
    return jwt_token

@router.get("/middleware", auth=auth.authorize)
def test_middleware(request):
    return {"msg": 1}

#USER

@router.post('/user/add/friend', auth=auth.authorize, tags=['user'])
def add_friend(request, friendname: str):

    payload = {
        'user_id': request.jwt_data.get('user_id'),
        'friendname': friendname
    }

    logger.warning(payload)
    res = requests.post('http://user:22748/api/user/add/friend', params=payload)

    if not res.ok:
        logger.error(res.json())
        raise HttpError(message='Error: Adding Friend', status_code=res.status_code)

    logger.warning(f"JWT DATA: {request.jwt_data}")
    return {"msg": 1}

@router.delete('/user/delete/friend', auth=auth.authorize, tags=['user'])
def add_friend(request, friendname: str):

    payload = {
        'user_id': request.jwt_data.get('user_id'),
        'friendname': friendname
    }

    logger.warning(payload)
    res = requests.delete('http://user:22748/api/user/delete/friend', params=payload)

    if not res.ok:
        logger.error(res.json())
        raise HttpError(message='Error: Deleting Friend', status_code=res.status_code)

    return {"msg": 1}

@router.delete('/delete/lukas')
def delete_lukas(request):

    requests.delete('http://user:22748/api/user/delete/lukas')
    return {'msg': 1}