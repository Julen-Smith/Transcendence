import hashlib, os , requests, jwt, random, datetime, smtplib
from django.http import HttpResponseRedirect
from urllib.parse import urlencode
from django.contrib.auth.hashers import check_password
#from ninja.responses import JSONResponse
from ninja.errors import HttpError
from django.conf import settings
from django.core.cache import cache
from . import schemas, crud, models
from transcendence.settings import logger, INTRA, GOOGLE, TRANSCENDENCE
#CORE
from django.utils import timezone
from ninja import Router
from typing import List

router = Router()

@router.post('/register', response=schemas.UserReturnSchema)
def create_user(request, user: schemas.UserCreateSchema):
    return crud.create_user(user)


@router.get('/get_user', response=schemas.UserReturnSchema)
def get_user(request, user: schemas.Username):

    db_user = crud.get_user(user.username)
    if db_user is None:
        raise HttpError(status_code=404, message="Error: user does not exists")
    return db_user



################
# CUSTOM LOGIN #
################

def send_email(sender: dict, receiver: str, otp_code: int):

    try:
        mail = schemas.Mail(
            sender=sender.get("email"),
            receiver=receiver,
        )
    except ValueError as err:
        logger.warning(f"Error: Missing Value(s) {err}")
        return False

    mail.build(otp_code)

    try:
        server = sender.get("server")
        port = sender.get("port")
        sender_email = sender.get("email")
        sender_password = sender.get("password")

        logger.warning("Sending email: ")
        logger.warning(f"sender: {server} - password: {port}")
        with smtplib.SMTP_SSL(server, port) as server:

            logger.warning(f"sender: {sender_email} - password: {sender_password}")
            retval = server.login(sender_email, sender_password)
            logger.warning(f"Login: {retval}")

            server.sendmail(sender_email, receiver, mail.message)

        return True

    except Exception as err:
        logger.error(f"Error: Unhandled {err}")

    return False

def handle_otp(db_user: models.user_login) -> bool:

    otp_code=random.randint(0000, 9999)
    cache.add(db_user.username, otp_code, 30)
    return send_email(
        sender=TRANSCENDENCE['SMTP'],
        receiver=db_user.email,
        otp_code=otp_code
    )

@router.post('/default', response={200: schemas.UserReturnSchema, 428: schemas.UserReturnSchema}) #Creacion de endpoint
def login_user(request, user: schemas.UserLogin): #Creacion de funcion que se ejecuta al llamar al endpoint, crea el obj user y lo valida con el schema DE CREACION DE USER definido en schemas

   #llama a la funcion get_user de crud.py y le devuelve el user objeto con la validacion del schema UserLogin
    db_user = crud.get_user(user.username) 
    if db_user is None:
        raise HttpError(status_code=404, message="Error: user does not exist")

    if db_user.mode != TRANSCENDENCE['LOGIN']['LOCAL']:
        raise HttpError(status_code=404, message="Error: User already used other authentication method")

    #Comprobacion de contraseña (De momento compara las strings, ya vendra tema HASH)
    if not check_password(user.password, db_user.password):
        raise HttpError(status_code=401, message="Error: incorrect password")

    if check_user(db_user):
        handle_otp()
        return 428, db_user

     # Devolver la información del usuario (el schema de UserReturnSchema ya filtra lo que devolver, el usuario y el mail en un diccionario
    return 200, db_user


############
# 42 LOGIN #
############


#Construye la URI que se usa para hacer la peticion a la intra.
@router.get('/intra')
def redirect_intra(request): 

    uid = LOGIN['INTRA_UID']
    auth_url = LOGIN['INTRA_AUTH_URL']
    redirect_uri = LOGIN['INTRA_REDIRECT_URI']

    # Construir la URI (la f indica que esta utilizando una cadena de formato f-string en Python.Las expresiones dentro de las llaves se evalúan y se insertan en la cadena resultante.)
    uri = f"{auth_url}?client_id={uid}&redirect_uri={redirect_uri}&response_type=code"

    return ({"url":uri})

@router.get('/intra/callback')
def login_intra(request): 
    
    # PASO 1 - GET CODE 
    # Recibe el código del parámetro GET
    code = request.GET.get('code')

    # PASO 2 - INTERCAMBIO DE CODE POR TOKEN 
    # Construye peticion (Credenciales de enviroment, las de la app intra) 
    uid = LOGIN['INTRA_UID']
    secret = LOGIN['INTRA_SECRET']
    authorization_url = LOGIN['INTRA_VERIFY_URL']
    redirect_uri = LOGIN['INTRA_REDIRECT_URI']

    data = {
        'grant_type': 'authorization_code',
        'client_id': uid,
        'client_secret': secret,
        'code': code,
        'redirect_uri': redirect_uri,
    }

    #Hace un POST para intercambio por TOKEN 
    response=requests.post(LOGIN['INTRA_VERIFY_URL'], params= data)
   
    if response.status_code != 200:
        raise HttpError(status_code=response.status_code, message="Error: Authentication code Failed")

    #PASO 3 - TOKEN POR INFO (ME)
    #Construye peticion
    access_token = response.json().get('access_token')
    headers = {
    'Authorization': f'Bearer {access_token}'   
    }
    #Hace GET para acceder a la API , endpoint "me"
    user_info = requests.get('https://api.intra.42.fr/v2/me', headers=headers)

    if user_info.status_code != 200:
        raise HttpError(status_code=user_info.status_code, message="Error: Authentication token Failed")

    #PASO 4 - Filter username info 
    username=user_info.json().get('login')
    email=user_info.json().get('email')

    #PASO 5 - Find if user is in Database
    try:
        db_user = crud.get_user_by_email(email) 
        if db_user.mode != 2: #se puede implementar como variable LOGIN MODE INTRA = 2 
            raise HttpError(status_code=404, message="Error: User already used other authentication method")
        elif check_user(db_user):
            handle_otp(db_user)
            payload['url'] = TRANSCENDENCE['URL']['otp'],
            return 428, payload
        logger.info('EXISTING USER LOGIN OK')
        lobby_url = 'http://localhost:8080/Lobby'
        return {"url":lobby_url} #OK, El usuario ya existe 
    except Exception as err:
        logger.error(err)

    #PASO 6 - Usuario no existe, Create user in Database
    logger.info('Username does not exist, starting creation...')
    user_create_data = {
    "username": username,
    "email": email,
    "password": "IntraIntra42!", #LA ÑAPA DEL SIGLO! Que pasa con la contraseña para los usuarios que acceden por intra?  
    "mode": 2,
    }
    new_user = schemas.UserCreateSchema(**user_create_data)
    db_user = crud.create_user(user=new_user) 

    #COOKIES??

    logger.warning('NEW USER LOGIN OK')
    lobby_url = 'http://localhost:8080/Lobby'
    return {"url": lobby_url}
     

################
# GOOGLE LOGIN #
################

@router.get('/google')
def google_login(request, state: str):

    logger.warning(GOOGLE)
    oauth_params = GOOGLE['GOOGLE_OAUTH']['OAUTH_PARAMS_LOGIN']
    oauth_params['scope'] = ' '.join(GOOGLE['GOOGLE_OAUTH']["SCOPES"])
    oauth_params['state'] = state
    oauth_params['redirect_uri'] = 'https://ikerketa.com/api/login/google/callback'#GOOGLE_OUATH['REDIRECT_URI']
    oauth_params['client_id'] = GOOGLE['GOOGLE_OAUTH']['CLIENT_ID']

    auth_url = f"{GOOGLE['GOOGLE_OAUTH']['AUTH_URL']}?{urlencode(oauth_params)}"
    logger.warning(f"URL: {auth_url}")
    return {"url": auth_url}

def check_user(db_user: models.user_login) -> bool:

    last_log = db_user.last_log + datetime.timedelta(minutes=30)
    now = timezone.now()
    db_user.save()

    return now > last_log

@router.get('/google/callback', response={200: dict, 428: dict})
def google_callback(request, code: str, state: str):

    oauth_params = dict(GOOGLE['GOOGLE_OAUTH']['OAUTH_PARAMS_TOKEN'])
    oauth_params['code'] = code
    oauth_params['client_id'] = GOOGLE['GOOGLE_OAUTH']['CLIENT_ID']
    oauth_params['client_secret'] = GOOGLE['GOOGLE_OAUTH']['CLIENT_SECRET']
    oauth_params['redirect_uri'] = 'https://ikerketa.com/api/login/google/callback'#GOOGLE_OUATH['REDIRECT_URI']

    res = requests.post(GOOGLE['GOOGLE_OAUTH']['ACCESS_TOKEN_URL'], data=oauth_params)
    if not res.ok:
        raise HttpError(status_code=res.status_code, message="Error: Authentication Failed")

    try:
        google_tokens = res.json()
    except Exception as err:
        raise HttpError(status_code=res.status_code, message="Error: Bad response")

    user_info = jwt.decode(google_tokens['id_token'],options={"verify_signature": False})

    email = user_info.get('email')
    username = email.split('@')[0]
    logger.warning(user_info)
    db_user = None

    try:
        db_user = crud.get_user_by_email(email)
    except Exception as err:
        logger.error(err)

    payload = {
        'url': TRANSCENDENCE['URL']['lobby'],
        'username': username
    }

    if db_user is None:
        logger.warning("Creating a new user")
        try:
            new_user = schemas.UserCreateSchema(
                username=username,
                email=email,
                password="Asdfasdfasdf$1",
                mode=TRANSCENDENCE['LOGIN']['GOOGLE']
            )
            db_user = crud.create_user(new_user)
        except Exception as err:
            logger.error(err)

        logger.warning(f"DB_USER: {db_user}")

    elif check_user(db_user):
        handle_otp(db_user)
        payload['url'] = TRANSCENDENCE['URL']['otp'],
        return 428, payload

    return 200, payload

@router.post('/test/otp')
def test_otp(request, receiver: str):

    logger.warning(f"Receiver: {receiver}")
    db_user = crud.get_user_by_email(receiver)
    logger.warning(db_user)
    retval = handle_otp(db_user)

    return {"status": retval}


@router.post('/create/list')
def create_list(request, users: List[schemas.UserCreateSchema]):

    created = 0
    for user in users:
        try:
            crud.create_user(user)
            created += 1
        except Exception as err:
            logger.warning(f"User creation failed: {err}")

    return {"message": f"Users created: {created}"}