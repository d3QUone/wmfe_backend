# coding: utf-8
import os
import random
import uuid

from flask_peewee.db import DoesNotExist
from loremipsum import generate_sentence
import requests
from werkzeug.utils import secure_filename

from blueprints.models import Person, Post, Comment, Likes, PersonSubscriptions


def generate_cookie():
    return "wmfe-{}".format(uuid.uuid4())


# TODO: use cache
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
    path = os.path.join("media", file_name)
    pic.save(path)
    return "http://188.226.142.44:5000/media/{0}".format(file_name)


def prepare_feed_from_query_result(query):
    res = []
    append = res.append
    for item in query:
        append({
            "post_id": item[0],
            "author_id": item[1],
            "text": item[2],
            "pic_url": item[3],
            "date": item[4].strftime("%Y-%m-%d %H:%M:%S"),
            "latitude": float(item[5]),
            "longitude": float(item[6]),
            "likes": item[7],
            "comments": item[8],
        })
    return res


def like_post(person_id, post_id):
    """ Helper func to add a entry (or add back) in the Like table and update the Post entry
    :param person_id: int
    :param post_id: int
    :return: bool
    """
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


def dislike_post(person_id, post_id):
    """ Helper func to remove Like from Post and update the Post entry
    :param person_id: int
    :param post_id: int
    :return: bool
    """
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
