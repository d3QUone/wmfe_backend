__author__ = 'vladimir'

import time
import datetime
import uuid
import json

from flask import Blueprint, Response, request

from .models import Person, DoesNotExist


security = Blueprint("security_module", __name__)


def generate_str():
    return "wmfe-{0}".format(uuid.uuid4())


# pass 'vkid' and 'recovery_code' to register a new user before using API
@security.route("/register_user", methods=["POST"])
def reg_user():
    vkid = request.form.get("vkid", None)
    r_code = request.form.get("recovery_code", None)
    message = ""
    if vkid and r_code:
        try:
            Person.get(Person.vkid == vkid)
            message = "Person with VKID {0} was already registered, use /renew_cookie to get new auth cookie"
        except DoesNotExist:
            new_cookie = generate_str()
            Person.create(vkid=vkid, recovery_code=r_code, auth_cookie=new_cookie)
            message = "Save 'auth' value, put in cookies, use in every request until it expires"
            r = Response(response=json.dumps({
                "auth": new_cookie,
                "message": message,
            }), mimetype="application/json")
            r.set_cookie("auth", new_cookie, expires=time.time()+datetime.timedelta(days=1).total_seconds())
            r.status_code = 200
            return r
        except Exception as e:
            message = "Internal error: {0}".format(repr(e))
    else:
        message = "POST parameters 'vkid' and 'r_code' are required"
    return json.dumps({"message": message})


# pass valid 'vkid' and 'recovery_code' (from vk) to get a new cookie
@security.route("/renew_cookie", methods=["POST"])
def renew_cookie():
    vkid = request.form.get("vkid", None)
    r_code = request.form.get("recovery_code", None)
    r = Response()
    if vkid and r_code:
        try:
            p = Person.get(Person.vkid == vkid, Person.recovery_code == r_code)
            new_cookie = generate_str()
            p.auth_cookie = new_cookie
            p.save()
            r.set_cookie("auth", new_cookie, expires=time.time()+datetime.timedelta(days=1).total_seconds())
            r.status_code = 200
        except DoesNotExist:
            r.status_code = 401
        except Exception as e:
            r.status_code = 500
            print "renew_cookie error: {0}".format(repr(e))
    return r
