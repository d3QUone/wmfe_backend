__author__ = 'vladimir'

from flask import request, Response

from . import AUTH_COOKIE_NAME, VKID_NAME
from .models import Person, DoesNotExist


def check_cookie(verbose=True):
    """Get auth-cookie from request and check authorization
    parameter 'vkid' (VKID_NAME) is required in every GET/POST request
    """
    def wrapper_without_args(f):

        def wrapper(**kwargs):
            if verbose:
                print "kw keys: {0}\ncookies keys: {1}\nMethod: {2}".format(kwargs.keys(), request.cookies.keys(), request.method)
            auth_cookie = request.cookies.get(AUTH_COOKIE_NAME, None)
            vkid = request.values.get(VKID_NAME, None)  # get arg from any request type
            print "checking VKID {0}".format(vkid)
            if auth_cookie and vkid:
                try:
                    Person.get(Person.vkid == vkid, Person.auth_cookie == auth_cookie)
                    return f(**kwargs)
                except DoesNotExist:
                    print "User {0} bad cookie OR does not exist".format(vkid)
            return Response(status=401)

        return wrapper

    return wrapper_without_args
