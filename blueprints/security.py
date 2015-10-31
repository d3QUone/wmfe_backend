__author__ = 'vladimir'

import time
import datetime
import uuid
import json
import random

from flask import Blueprint, Response, request

from . import VKID_NAME
from .decorators import check_cookie
from .models import Person, PersonSubscriptions, DoesNotExist


security = Blueprint("security_module", __name__)


def generate_cookie():
    return "wmfe-{0}".format(uuid.uuid4())


# pass 'vkid' and 'recovery_code' to register a new user before using API
@security.route("/register_user", methods=["POST"])
def reg_user():
    vkid = request.form.get(VKID_NAME, None)
    r_code = request.form.get("recovery_code", None)
    friend_id_list = request.values.getlist("fr")
    if vkid and r_code:
        try:
            Person.get(Person.vkid == vkid)
            message = "Person with VKID {0} was already registered, use /renew_cookie to get new auth cookie"
        except DoesNotExist:
            new_cookie = generate_cookie()
            p = Person.create(vkid=vkid, recovery_code=r_code, auth_cookie=new_cookie)
            # follow all friends and add all to followers
            do_save = False
            for flwr in friend_id_list:
                try:
                    f = Person.get(Person.vkid == flwr)
                    f.following += 1
                    f.my_followers += 1
                    f.save()
                    PersonSubscriptions.get_or_create(owner=vkid, follower=flwr)
                    PersonSubscriptions.get_or_create(owner=flwr, follower=vkid)

                    p.following += 1
                    p.my_followers += 1
                    do_save = True
                except DoesNotExist:
                    print "Friend with id='{0}' doesn't exist".format(flwr)
            if do_save:
                p.save()
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
    vkid = request.form.get(VKID_NAME, None)
    r_code = request.form.get("recovery_code", None)
    r = Response()
    if vkid and r_code:
        try:
            p = Person.get(Person.vkid == vkid, Person.recovery_code == r_code)
            new_cookie = generate_cookie()
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


@security.route("/subscribe", methods=["POST"])
@check_cookie()
def subscribe():
    vkid = request.form.get(VKID_NAME, None)
    target_id = request.form.get("target_id", None)
    if vkid and target_id:
        if subscribe_on_target_person(owner_id=target_id, follower_id=vkid):
            return json.dumps({"success": 1})
        else:
            return json.dumps({
                "success": 0,
                "message": "User with id='{0}' does not exist".format(target_id)
            })


# ########################## HELPERS ##########################

def subscribe_on_target_person(owner_id, follower_id):
    try:
        t = Person.get(Person.vkid == owner_id)
        t.following += 1
        t.save()

        p = Person.get(Person.vkid == follower_id)
        p.my_followers += 1
        p.save()

        _, res = PersonSubscriptions.get_or_create(owner=t, follower=p)
        return res
    except DoesNotExist as e:
        print "Person with id='{0}' doesn't exist\nError: {1}".format(owner_id, repr(e))
        return False


# ########################## DEMO ##########################

def demo_add_person():
    vkid = "id{0}".format(random.randint(1000, 9999))
    cookie = generate_cookie()
    r_code = str(uuid.uuid4())[:23]
    try:
        _, res = Person.get_or_create(vkid=vkid, auth_cookie=cookie, recovery_code=r_code)
        return res
    except Exception as e:
        print "add_person error {0}".format(repr(e))
        return False


def demo_random_subs(amount):
    all_p = Person.select()
    count = all_p.count() - 1
    # print dir(count), count
    for _ in range(amount):
        owner = all_p[random.randint(0, count)]
        follower = all_p[random.randint(0, count)]
        if owner.vkid != follower.vkid:
            subscribe_on_target_person(owner_id=owner.vkid, follower_id=follower.vkid)
        else:
            print "LOL, owner==follower"
