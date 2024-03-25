from ninja import NinjaAPI
from user.api import router as user


api = NinjaAPI()

api.add_router("/user/", user)