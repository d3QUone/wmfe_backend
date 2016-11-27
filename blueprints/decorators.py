# coding: utf-8
import logging
from functools import wraps

from flask import request, Response
from flask_peewee.db import DoesNotExist

from blueprints import AUTH_COOKIE_NAME, VKID_NAME
from blueprints.models import Person


logger = logging.getLogger(__name__)


def check_cookie(f):
    """ Get auth-cookie from request and check authorization
        parameter 'vkid' (VKID_NAME) is required in every GET/POST request
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth_cookie = request.cookies.get(AUTH_COOKIE_NAME, None)
        vkid = request.values.get(VKID_NAME, None)  # get arg from any request type
        logger.debug(u"checking VKID '{}'".format(vkid))
        if auth_cookie and vkid:
            try:
                # TODO: use cache
                Person.get(Person.vkid == vkid, Person.auth_cookie == auth_cookie)
                return f(*args, **kwargs)
            except DoesNotExist:
                logger.info(u"User '{}' bad cookie OR does not exist".format(vkid))
        return Response(status=401)

    return wrapper
