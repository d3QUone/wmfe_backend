# coding: utf-8
import json

from flask import Blueprint, request
from flask_peewee.db import DoesNotExist

from blueprints import VKID_NAME
from blueprints.decorators import check_cookie
from blueprints.functions import generate_cookie
from blueprints.functions import get_friend_list
from blueprints.functions import subscribe_on_target_person
from blueprints.models import Person
from blueprints.models import PersonSubscriptions


security = Blueprint("security_module", __name__)


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
@check_cookie
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
