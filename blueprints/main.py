# coding: utf-8
import json

from flask import Blueprint, request
from flask_peewee.db import DoesNotExist

from blueprints import VKID_NAME
from blueprints.decorators import check_cookie
from blueprints.models import Person, Post, Comment, Likes, database
from blueprints.functions import prepare_feed_from_query_result
from blueprints.functions import dislike_post
from blueprints.functions import like_post


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
@check_cookie
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
@check_cookie
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
@check_cookie
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
@check_cookie
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
        sql = """
SELECT p.`post_id`, p.`author_id`, p.`text`, p.`pic_url`, p.`date`, p.`latitude`, p.`longitude`, p.`likes`, p.`comments` FROM `post` p
WHERE p.`date` BETWEEN DATE_SUB(NOW(), INTERVAL 1 DAY) AND NOW() ORDER BY p.`date` DESC LIMIT 7
"""
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
@check_cookie
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
@check_cookie
def dislike_post_request():
    person_id = request.form.get(VKID_NAME)
    post_id = request.form.get("post_id", None)
    if person_id and post_id:
        r = dislike_post(person_id=person_id, post_id=post_id)
        if r:
            return json.dumps({"success": 1})
        else:
            return json.dumps({"success": 0})
