
# TODO:
"""
# register
curl -v -X POST -d 'vkid=3sfddd&recovery_code=12o_pda_iod' http://127.0.0.1:8080/register_user

# register with list of vk-friends
curl -v -X POST -d 'vkid=id0013j&recovery_code=abc-check-reg&fr=id9616&&fr=id7987&fr=id6530' http://127.0.0.1:8080/register_user

# create post
curl -v -X POST --cookie 'auth=wmfe-013443b2-da9b-464c-8e74-dadd1ffef53a' -d 'vkid=3sfddd&food=iiko877&food=iiko653333&text="I like foo"' http://127.0.0.1:8080/create_post

curl -v -X POST --cookie 'auth=wmfe-013443b2-da9b-464c-8e74-dadd1ffef53a' -d 'vkid=3sfddd&food=iiko1&food=iiko32x&text="I like food, Piter food is cool!!!"' http://127.0.0.1:8080/create_post

# get personal feed
curl -v -X GET --cookie 'auth=wmfe-013443b2-da9b-464c-8e74-dadd1ffef53a' http://127.0.0.1:8080/get_feed?vkid=3sfddd

curl -v -X GET --cookie 'auth=wmfe-013443b2-da9b-464c-8e74-dadd1ffef53a' http://127.0.0.1:8080/get_feed?vkid=3sfddd&order=likes

curl -v -X GET --cookie 'auth=wmfe-013443b2-da9b-464c-8e74-dadd1ffef53a' http://127.0.0.1:8080/get_feed?vkid=3sfddd&order=date

# like
curl -v -X POST --cookie 'auth=wmfe-013443b2-da9b-464c-8e74-dadd1ffef53a' -d 'vkid=3sfddd&post_id=1' http://127.0.0.1:8080/like_post

# dislike
curl -v -X POST --cookie 'auth=wmfe-013443b2-da9b-464c-8e74-dadd1ffef53a' -d 'vkid=3sfddd&post_id=3' http://127.0.0.1:8080/dislike_post

# get detailed likes
curl -v -X GET --cookie 'auth=wmfe-013443b2-da9b-464c-8e74-dadd1ffef53a' -d 'vkid=3sfddd' http://127.0.0.1:8080/get_likes_to_post?post_id=1

# get global feed
curl -v -X GET --cookie 'auth=wmfe-013443b2-da9b-464c-8e74-dadd1ffef53a' http://127.0.0.1:8080/global_feed?vkid=3sfddd

"""
