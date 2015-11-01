__author__ = 'vladimir'

import os
import json
import random
import uuid

from werkzeug.utils import secure_filename
from flask import Blueprint, request
from loremipsum import generate_sentence

from . import VKID_NAME
from .decorators import check_cookie
from .models import Person, Post, Comment, Likes, DoesNotExist, database

main_app = Blueprint("api", __name__)

# TODO: add Picture handler on front-end server

"""
@api {post} /create_post Create a post at a specific (your) position, auth-cookie required
@apiGroup Content
@apiName CreatePost
@apiVersion 0.1.0

@apiParam {String} vkid User VK id
@apiParam {String} text
@apiParam {File} pic
@apiParam {String} latitude
@apiParam {String} longitude
"""
@main_app.route("/create_post", methods=["POST"])
@check_cookie()
def create_new_post():
    vkid = request.form.get(VKID_NAME)
    text = request.form.get("text", None)
    # pic = request.files.get("pic", None)
    latitude = request.form.get("latitude", None)
    longitude = request.form.get("longitude", None)
    if text and latitude and longitude:
        # pic_url = save_picture(pic)
        author = Person.get(Person.vkid == vkid)
        author.posts += 1
        author.save()
        Post.create(author=author, text=text, pic_url="", latitude=latitude, longitude=longitude)
        return json.dumps({"success": 1})
    else:
        return json.dumps({"success": 0})


"""
@api {post} /create_comment Add a comment to specific post, auth-cookie required
@apiGroup Content
@apiName CreateComment
@apiVersion 0.1.0

@apiParam {String} vkid User VK id
@apiParam {String} post_id Post id
@apiParam {String} text
"""
@main_app.route("/create_comment", methods=["POST"])
@check_cookie()
def create_new_comment():
    vkid = request.form.get(VKID_NAME)
    post_id = request.form.get("post_id", None)
    text = request.form.get("text", None)
    if post_id and text:
        try:
            p = Post.get(Post.post_id == post_id)
            p.comments += 1
            p.save()
            Comment.create(post=p, author=vkid, text=text)
            return json.dumps({"success": 1})
        except DoesNotExist as e:
            print "Post with id='{0}' doesn't exist: {0}".format(e)
    return json.dumps({"success": 0})


# TODO: pagination
"""
@api {get} /get_feed Get Person feed by VKID, auth-cookie required
@apiGroup Content
@apiName GetPersonFeed
@apiVersion 0.1.0

@apiParam {String} vkid User VK id
@apiParam {String} person_id Person VK id
@apiParam {String} order [date, like]
"""
@main_app.route("/get_feed", methods=["GET"])
@check_cookie()
def get_news_feed():
    person_id = request.args.get("person_id", None)
    order = request.args.get("order", "date")  # [date, likes]
    # page = request.args.get("page", 1)
    # limit = request.args.get("limit", 10)
    # if limit > 10 or limit <= 0:
    #     limit = 10
    if person_id:
        try:
            if order == "date":
                query = Post.select(Post.post_id, Post.author, Post.text, Post.pic_url, Post.date, Post.latitude, Post.longitude, Post.likes, Post.comments)\
                    .where(Post.author == person_id, Post.is_deleted == False)\
                    .order_by(Post.date.desc())\
                    .tuples()
            else:
                query = Post.select(Post.post_id, Post.author, Post.text, Post.pic_url, Post.date, Post.latitude, Post.longitude, Post.likes, Post.comments)\
                    .where(Post.author == person_id, Post.is_deleted == False)\
                    .order_by(Post.likes.desc())\
                    .tuples()
        except DoesNotExist:
            query = []
        res = prepare_feed_from_query_result(query)
        return json.dumps(res)
    else:
        return json.dumps({"message": "This person does not exist"})


# TODO: pagination
"""
@api {get} /get_feed Get feed of all persons I am following, auth-cookie required
@apiGroup Content
@apiName GetGlobalFeed
@apiVersion 0.1.0

@apiParam {String} vkid User VK id
"""
@main_app.route("/global_feed", methods=["GET"])
@check_cookie()
def get_global_feed():
    person_id = request.args.get(VKID_NAME)
    # TODO: add search by lat & lon
    sql = """
SELECT p.`post_id`, p.`author_id`, p.`text`, p.`pic_url`, p.`date`, p.`latitude`, p.`longitude`, p.`likes`, p.`comments` FROM `post` p
JOIN `personsubscriptions` ps ON p.`author_id` = ps.`owner_id`
WHERE ps.`follower_id` = %s AND p.`is_deleted` IS NOT TRUE
"""
    query = database.execute_sql(sql, person_id)
    res = prepare_feed_from_query_result(query)
    return json.dumps(res)


"""
@api {get} /get_map Get all posts at specific position
@apiGroup Content
@apiName GetPostsAtPosition
@apiVersion 0.1.0

@apiParam {Decimal} latitude
@apiParam {Decimal} longitude
@apiParam {Int} distance Circle diameter in miles
"""
@main_app.route("/get_map", methods=["GET"])
def get_map():
    longitude = request.args.get("longitude", None)
    latitude = request.args.get("latitude", None)
    distance = request.args.get("distance", None)
    if longitude and latitude and distance:
        # sql = "CALL geodist({0}, {1}, {2});".format(longitude, latitude, distance)  # Fuck this
        sql = "SELECT p.`post_id`, p.`author_id`, p.`text`, p.`pic_url`, p.`date`, p.`latitude`, p.`longitude`, p.`likes`, p.`comments` FROM `post` p WHERE p.`date` BETWEEN DATE_SUB(NOW(), INTERVAL 1 DAY)  AND NOW()"
        query = database.execute_sql(sql)
        res = prepare_feed_from_query_result(query)
        return json.dumps(res)
    else:
        return json.dumps({"message": "Parameters 'latitude', 'longitude' and 'distance' are required"})


# TODO: pagination
"""
@api {get} /get_likes_to_post Get detailed list of the Post-Likes contributors
@apiGroup Content
@apiName GetPostLikers
@apiVersion 0.1.0

@apiParam {String} post_id Specific Post id
"""
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
        return json.dumps({"message": "This post does not exist"})


"""
@api {post} /like_post Like the Post, auth-cookie required
@apiGroup Content
@apiName LikePost
@apiVersion 0.1.0

@apiParam {String} vkid User VK id
@apiParam {String} post_id Specific Post id
"""
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


"""
@api {post} /dislike_post Dislike the Post, auth-cookie required
@apiGroup Content
@apiName DislikePost
@apiVersion 0.1.0

@apiParam {String} vkid User VK id
@apiParam {String} post_id Specific Post id
"""
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

# TODO: save pics in new subfolder every day
def save_picture(pic):
    # folder_name = datetime.now().strftime("%Y-%m-%d")
    file_name = "{0}-{1}".format(uuid.uuid4(), secure_filename(pic.filename))
    # try:
    #     b = os.path.join("media", folder_name)
    #     if not os.path.isdir(b):
    #         os.makedirs(b, exist_ok=True)
    # except Exception as e:
    #     print "create folder exception: {0}".format(e)
    drct = os.path.join("media", file_name)
    pic.save(drct)
    return "http://188.226.142.44:5000/media/{0}".format(file_name)


# p.`post_id`, p.`author_id`, p.`text`, p.`pic_url`, p.`date`, p.`latitude`, p.`longitude`, p.`likes`, p.`comments`
def prepare_feed_from_query_result(query):
    res = {}
    for item in query:
        post_id = item[0]
        if post_id not in res:
            res[post_id] = {
                # "post_id": post_id,
                "author_id": item[1],
                "text": item[2],
                "pic_url": item[3],
                "date": item[4].strftime("%Y-%m-%d %H:%M:%S"),
                "latitude": float(item[5]),
                "longitude": float(item[6]),
                "likes": item[7],
                "comments": item[8],
            }
    return res


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


# ########################## DEMO ##########################

def demo_add_post(person_id):
    _, words_amount, text = generate_sentence()
    # Piter coordinates:
    # lat, lon
    # 59.93900, 30.325896
    latitude = 59.0 + 1.0 * random.randint(850000, 999999) / 1000000
    longitude = 30.0 + 1.0 * random.randint(200000, 399999) / 1000000
    pic_url = "http://lorempixel.com/300/300/"
    try:
        if person_id:
            Person.get(Person.vkid == person_id)
        else:
            all_p = Person.select(Person.vkid)
            count = all_p.count() - 1
            person_id = all_p[random.randint(0, count)]
        Post.create(author=person_id, text=text, pic_url=pic_url, latitude=latitude, longitude=longitude)
        return True
    except DoesNotExist:
        return False


def demo_add_comment(author_id, post_id):
    _, words_amount, text = generate_sentence()
    try:
        if author_id:
            Person.get(Person.vkid == author_id)
        else:
            all_pers = Person.select(Person.vkid)
            count = all_pers.count() - 1
            author_id = all_pers[random.randint(0, count)]

        if post_id:
            p = Post.get(Post.post_id == post_id)
        else:
            all_posts = Post.select()
            count = all_posts.count() - 1
            p = all_posts[random.randint(0, count)]
            p.comments += 1
            p.save()
        Comment.create(post=p, author=author_id, text=text)
        return True
    except DoesNotExist:
        return False
