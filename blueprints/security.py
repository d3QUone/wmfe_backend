__author__ = 'vladimir'

import uuid
import json
import random

import requests
from flask import Blueprint, request

from . import VKID_NAME
from .decorators import check_cookie
from .models import Person, PersonSubscriptions, DoesNotExist


security = Blueprint("security_module", __name__)


def generate_cookie():
    return "wmfe-{0}".format(uuid.uuid4())


def get_friend_list(user_id, auth_token):
    base_url = "https://api.vk.com/method/"
    endpoint = "friends.get"
    data = {
        "user_id": user_id,
        "auth_token": auth_token,
        "v": "5.37",
    }
    r = requests.get(base_url + endpoint, params=data, verify=False)
    print "Got VK status-code={0}".format(r.status_code)
    return r.json()


"""
@api {post} /register_user Register & get auth cookie in responce
@apiGroup User
@apiName RegisterUser
@apiDescription Pass everything to register a new user before using the API
@apiVersion 0.1.0

@apiParam {String} vkid User VK id
@apiParam {String} auth_token VK-API auth token
@apiParam {String} recovery_code VK-API code to renew auth token when expires
"""
@security.route("/register_user", methods=["POST"])
def reg_user():
    vkid = request.form.get(VKID_NAME, None)
    auth_token = request.form.get("auth_token", None)
    r_code = request.form.get("recovery_code", None)
    if vkid and auth_token and r_code:
        new_cookie = generate_cookie()
        p, _ = Person.get_or_create(vkid=vkid)
        p.auth_cookie = new_cookie
        p.auth_token = auth_token
        p.recovery_code = r_code

        # update friend list
        friend_id_list = get_friend_list(user_id=vkid, auth_token=auth_token)
        for p_id in friend_id_list["response"]["items"]:
            try:
                f = Person.get(Person.vkid == p_id)
                f.following += 1
                f.my_followers += 1
                f.save()
                PersonSubscriptions.get_or_create(owner=vkid, follower=p_id)
                PersonSubscriptions.get_or_create(owner=p_id, follower=vkid)

                p.following += 1
                p.my_followers += 1
            except DoesNotExist:
                pass
            except Exception as e:
                print "Problem parsing JSON: {0}".format(e)
        p.save()
        return json.dumps({"auth": new_cookie})
    else:
        return json.dumps({"message": "POST parameters 'vkid', 'recovery_code', 'auth_token' are required"})


"""
@api {post} /renew_cookie Set new cookie
@apiDescription Sets new cookie in responce. Call if 401
@apiGroup User
@apiName RenewUserCookie
@apiVersion 0.1.0

@apiParam {String} vkid User VK id
@apiParam {String} recovery_code VK-API code to renew auth token when expires
"""
@security.route("/renew_cookie", methods=["POST"])
def renew_cookie():
    vkid = request.form.get(VKID_NAME, None)
    r_code = request.form.get("recovery_code", None)
    if vkid and r_code:
        try:
            p = Person.get(Person.vkid == vkid, Person.recovery_code == r_code)
            new_cookie = generate_cookie()
            p.auth_cookie = new_cookie
            p.save()
            return json.dumps({"auth": new_cookie})
        except DoesNotExist:
            return json.dumps({"message": "this person doesn't exist"})
        except Exception as e:
            return json.dumps({"message": "internal error: {0}".format(repr(e))})


"""
@api {post} /subscribe Follow a user with id=target_id
@apiGroup User
@apiName SubscribeOnUser
@apiVersion 0.1.0

@apiParam {String} vkid User VK id
@apiParam {String} target_id Targer user VK id
"""
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
    vkid = str(random.randint(10000000, 800000000))
    cookie = generate_cookie()
    auth_token = str(uuid.uuid4())[:23]
    r_code = str(uuid.uuid4())[:23]
    try:
        _, res = Person.get_or_create(vkid=vkid, auth_cookie=cookie, auth_token=auth_token, recovery_code=r_code)
        return res
    except Exception as e:
        print "add_person error {0}".format(repr(e))
        return False


def demo_random_subs(amount):
    all_p = Person.select()
    count = all_p.count() - 1
    for _ in range(amount):
        owner = all_p[random.randint(0, count)]
        follower = all_p[random.randint(0, count)]
        if owner.vkid != follower.vkid:
            subscribe_on_target_person(owner_id=owner.vkid, follower_id=follower.vkid)
        else:
            print "LOL, owner==follower"
