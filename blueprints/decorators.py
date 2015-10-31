__author__ = 'vladimir'

from functools import wraps

from flask import request, Response

from . import AUTH_COOKIE_NAME, VKID_NAME
from .models import Person, DoesNotExist


def check_cookie(verbose=True):
    """Get auth-cookie from request and check authorization
    parameter 'vkid' (VKID_NAME) is required in every GET/POST request

    when @check_cookie is used - u can be sure that 'vkid' exists
    """
    def wrapper_without_args(f):

        @wraps(f)
        def wrapper(*args, **kwargs):
            auth_cookie = request.cookies.get(AUTH_COOKIE_NAME, None)
            vkid = request.values.get(VKID_NAME, None)  # get arg from any request type
            if verbose:
                print "*"*40
                print "args keys: {0}, kwargs keys: {1}\ncookies keys: {2}\nMethod: {3}".format(args, kwargs.keys(), request.cookies.keys(), request.method)
                print "checking VKID '{0}'".format(vkid)
                print "*"*40
            if auth_cookie and vkid:
                try:
                    Person.get(Person.vkid == vkid, Person.auth_cookie == auth_cookie)
                    return f(*args, **kwargs)
                except DoesNotExist:
                    print "User '{0}' bad cookie OR does not exist".format(vkid)
            return Response(status=401)

        return wrapper

    return wrapper_without_args
