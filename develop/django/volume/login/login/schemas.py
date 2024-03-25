from ninja import Schema, ModelSchema, Field
from pydantic import validator
from . import models
from ninja.errors import HttpError
from django.core.validators import validate_email
from transcendence.settings import logger
import re, base64

username_regex='^[A-Za-z0-9_]+$'

class Username(Schema):
    
    username: str = Field(max_length=32, pattern=username_regex, examples=["walter"])
    
    @validator('username')
    def validate_username_length(cls, v):
        if len(v) > 16:
            raise HttpError(status_code=400, message="Username is too long")
        return v

class UserLogin(Username):

    password: str = Field(min_length=12, max_length=32, examples=["This_is_my_password1!"])

    @validator('password')
    def validate_password(cls, v, values):

        username = values.get('username')

        if username is None:
            raise HttpError(status_code=400, message="Missing username")
        if not re.search(r'[0-9]', v):
            raise HttpError(status_code=404, message="Password: must contain at least one number")
        if not re.search(r'[A-Za-z]', v):
            raise HttpError(status_code=404, message="Password: must contain at least one uppercase letter")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
            raise HttpError(status_code=404, message="Password: must contain at least one symbol")
        if values['username'] in v:
            raise HttpError(status_code=404, message="Password: cannot contain the username")

        return v

class UserCreateSchema(UserLogin):
    email: str = Field(max_length=256, examples=["walter@gmail.com"])
    mode: int=Field(ge=0,le=2)
    
    @validator('email')
    def validate_email(cls, v):

        try:
            validate_email(v)
        except Exception as err:
            raise HttpError(status_code=404, message="Email: bad format")
        return v
            
class UserReturnSchema(ModelSchema):

    class Meta:

        model = models.user_login
        fields = ['id', 'username']

class LoginLogSchema(Schema):
    browserName: str
    browserVersion: str
    language: str
    platform: str
    screenResolution: str
    userAgent: str

########
# MAIL #
########

class Mail(Schema):

    sender: str
    receiver: str
    message: str = None

    def _encode_image(self, src: str) -> str:

        try:
            with open(src, 'rb') as fd:
                encoded = base64.b64encode(fd.read())
                return encoded.decode('utf-8')

        except FileNotFoundError as err:
            logger.error(f"Error: File not found {err}")
        except Exception as err:
            logger.error(f"Error: Unhandled {err}")

        return None

    def build(self, otp_code: int = 1234):
        subject = "Your Verification Code"

    # Sample email body with OTP code
        body_text = f"""\
Dear User,

Your OTP is {otp_code}. This code is valid for 10 minutes.

Best regards,
[Your Company Name]
"""

        body_html = f"""\
<html>
  <head></head>
  <body>
    <p>Dear User,</p>
    <p>Your OTP is <b>{otp_code}</b>. This code is valid for 10 minutes.</p>
    <p><img src="cid:verification_image"></p>
    <p>Best regards,<br>[Your Company Name]</p>
  </body>
</html>
"""

        encoded_image = self._encode_image("/app/login/mail/web_otp.jpg")
        image_cid = 'verification_image'  # CID used in the HTML body

    # Construct the email with both plain text and HTML parts
        self.message = f"""From: {self.sender}
To: {self.receiver}
Subject: {subject}
MIME-Version: 1.0
Content-Type: multipart/related; boundary="sep"

--sep
Content-Type: text/plain; charset="UTF-8"
Content-Transfer-Encoding: 7bit

{body_text}

--sep
Content-Type: text/html; charset="UTF-8"
Content-Transfer-Encoding: 7bit

{body_html}

--sep
Content-Type: image/jpeg
Content-ID: <{image_cid}>
Content-Transfer-Encoding: base64

{encoded_image}

--sep--
"""