__author__ = 'vladimir'

import json

from flask import Blueprint, request, Response

from . import VKID_NAME
from .decorators import check_cookie
from .models import Person, Post, Meal, PostMeal, Likes, DoesNotExist

main_app = Blueprint("api", __name__)


# create Post
@main_app.route("/create_post", methods=["POST"])
@check_cookie()
def create_new_post():
    vkid = request.form.get(VKID_NAME)
    text = request.form.get("text", "")
    food_list = request.values.getlist("food")
    p = Post.create(author=vkid, text=text)
    for meal in food_list:
        m = Meal.create_or_get(iikoid=meal)  # (<blueprints.models.Meal object at 0x104a0ad50>, True)
        # print "m = {0} | {1}".format(repr(m), m[0])
        PostMeal.create(post=p.post_id, meal=meal)
    # TODO: customize return - may be it shall return the Post itself
    return json.dumps({"success": 1})


# TODO: load pics from IIKO API ...
# TODO: pagination
# get Person feed by VKID
@main_app.route("/get_feed", methods=["GET"])
@check_cookie()
def get_news_feed():
    person_id = request.args.get(VKID_NAME)
    order = request.args.get("order", "date")  # [date, likes]
    # page = request.args.get("page", 1)
    # limit = request.args.get("limit", 10)
    # if limit > 10 or limit <= 0:
    #     limit = 10
    if person_id:
        try:
            if order == "date":
                query = Post.select(Post.post_id, Post.author, Post.text, Post.date, Post.likes, Meal.iikoid)\
                    .join(PostMeal)\
                    .join(Meal)\
                    .where(Post.author == person_id, Post.is_deleted == False)\
                    .order_by(Post.date.desc())\
                    .tuples()
            else:
                query = Post.select(Post.post_id, Post.author, Post.text, Post.date, Post.likes, Meal.iikoid)\
                    .join(PostMeal)\
                    .join(Meal)\
                    .where(Post.author == person_id, Post.is_deleted == False)\
                    .order_by(Post.likes.desc())\
                    .tuples()
        except DoesNotExist:
            query = []
        # render results
        res = {}
        for item in query:
            post_id = item[0]
            if post_id not in res:
                res[post_id] = {
                    # "post_id": post_id,
                    "author_id": item[1],
                    "text": item[2],
                    "date": item[3].strftime("%Y-%m-%d %H:%M:%S"),
                    "likes": item[4],
                    "meals": {
                        item[5]: {
                            "name": "",
                            "pic_url": "",
                        }
                    }
                }
            else:
                iiko_id = item[5]
                if iiko_id not in res[post_id]["meals"]:
                    res[post_id]["meals"][iiko_id] = {
                        "name": "",
                        "pic_url": "",
                    }
        return json.dumps(res)
    else:
        return Response(status=400)


# TODO: pagination
# get detailed list of the Post-Likes contributors
@main_app.route("/get_likes_to_post", methods=["GET"])
def get_likes():
    post_id = request.args.get("post_id", None)
    if post_id:
        query = Likes.select(Likes.person).\
            where(Likes.post == post_id, Likes.is_deleted == False).\
            tuples()
        res = []
        append = res.append
        for item in query:
            append({
                "vkid": item[0],
            })
        return json.dumps(res)
    else:
        return Response(status=400)


@main_app.route("/like_post", methods=["POST"])
@check_cookie()
def like_post_request():
    person_id = request.form.get(VKID_NAME)
    post_id = request.form.get("post_id", None)
    if person_id and post_id:
        r = like_post(person_id=person_id, post_id=post_id)
        if r:
            return json.dumps({"success": 1})
        else:
            return json.dumps({"success": 0})


@main_app.route("/dislike_post", methods=["POST"])
@check_cookie()
def dislike_post_request():
    person_id = request.form.get(VKID_NAME)
    post_id = request.form.get("post_id", None)
    if person_id and post_id:
        r = dislike_post(person_id=person_id, post_id=post_id)
        if r:
            return json.dumps({"success": 1})
        else:
            return json.dumps({"success": 0})


# ########################## HELPERS ##########################

# helper to add a entry (or add back) in the Like table and update the Post entry
def like_post(person_id, post_id):
    try:
        Person.get(Person.vkid == person_id)
        try:
            l = Likes.get(Likes.person == person_id, Likes.post == post_id)
            if l.is_deleted:
                l.is_deleted = False
                l.save()
                p = Post.get(Post.post_id == post_id)
                p.likes += 1  # some day it may cause race condition
                p.save()
                return True
            else:
                return False
        except DoesNotExist:
            Likes.create(person=person_id, post=post_id)
            p = Post.get(Post.post_id == post_id)
            p.likes += 1  # some day it may cause race condition
            p.save()
        return True
    except DoesNotExist:
        print "Like on person_id='{0}', post_id='{1}' doesn't exist".format(person_id, post_id)
    except Exception as e:
        print "like_post exception: {0}".format(repr(e))
    return False


# helper to remove Like from Post and update the Post entry
def dislike_post(person_id, post_id):
    try:
        Person.get(Person.vkid == person_id)
        l = Likes.get(Likes.person == person_id, Likes.post == post_id)
        if not l.is_deleted:
            l.is_deleted = True
            l.save()
            p = Post.get(Post.post_id == post_id)
            p.likes -= 1  # some day it may cause race condition
            p.save()
            return True
    except DoesNotExist:
        print "Like on person_id='{0}', post_id='{1}' doesn't exist".format(person_id, post_id)
    except Exception as e:
        print "dislike_post exception: {0}".format(repr(e))
    return False
