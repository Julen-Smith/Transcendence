#Errores
from django.db.utils import IntegrityError
from ninja.errors import HttpError
from django.core.exceptions import MultipleObjectsReturned

from transcendence.settings import logger
from user.models import user_login, Friends

def get_user_by_name(username: str):
    try:
        logger.warning(f"Searching for username: {username}")
        db_user = user_login.objects.filter(username=username).get()
        logger.warning(f"User found: {db_user.username}")
    except user_login.DoesNotExist:
        logger.error(f"User not found: {username}")
        raise HttpError(status_code=403, message="Error: Unauthorized")
    except MultipleObjectsReturned:
        logger.error(f"Multiple users found for: {username}")
        raise HttpError(status_code=409, message="Error: Multiple users found")
    except IntegrityError:
        logger.error(f"Integrity error for: {username}")
        raise HttpError(status_code=500, message="Integrity error")
    except Exception as e:
        logger.error(f"Unexpected error for {username}: {e}")
        raise HttpError(status_code=500, message=f"Internal Server Error: {e}")

    return db_user

def add_friend(user_id: int, db_user: user_login):

    try:
        relation_1 = Friends(
            user_id=user_id,
            friend_id=db_user.id,
            status=0
        )
        relation_1.save()

        relation_2 = Friends(
            user_id=db_user.id,
            friend_id=user_id,
            status=1
        )
        relation_2.save()
    except Exception as err:
        logger.error(err)
        return False

    return True

def delete_friend(user_id: int, friend_id: int):

    try:
        relation_1 = Friends.objects.filter(user_id=user_id, friend_id=friend_id)
        relation_2 = Friends.objects.filter(user_id=friend_id, friend_id=user_id)

        relation_1.delete()
        relation_2.delete()

    except Exception as err:
        logger.error(err)
        return False
    return True