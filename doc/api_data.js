define({ "api": [  {    "type": "post",    "url": "/create_comment",    "title": "Add a comment to specific post, auth-cookie required",    "group": "Content",    "name": "CreateComment",    "version": "0.1.0",    "parameter": {      "fields": {        "Parameter": [          {            "group": "Parameter",            "type": "<p>String</p> ",            "optional": false,            "field": "vkid",            "description": "<p>User VK id</p> "          },          {            "group": "Parameter",            "type": "<p>String</p> ",            "optional": false,            "field": "post_id",            "description": "<p>Post id</p> "          },          {            "group": "Parameter",            "type": "<p>String</p> ",            "optional": false,            "field": "text",            "description": ""          }        ]      }    },    "filename": "./blueprints/main.py",    "groupTitle": "Content",    "sampleRequest": [      {        "url": "http://127.0.0.1:8080/create_comment"      }    ]  },  {    "type": "post",    "url": "/create_post",    "title": "Create a post at a specific (your) position, auth-cookie required",    "group": "Content",    "name": "CreatePost",    "version": "0.1.0",    "parameter": {      "fields": {        "Parameter": [          {            "group": "Parameter",            "type": "<p>String</p> ",            "optional": false,            "field": "vkid",            "description": "<p>User VK id</p> "          },          {            "group": "Parameter",            "type": "<p>String</p> ",            "optional": false,            "field": "text",            "description": ""          },          {            "group": "Parameter",            "type": "<p>File</p> ",            "optional": false,            "field": "pic",            "description": ""          },          {            "group": "Parameter",            "type": "<p>String</p> ",            "optional": false,            "field": "latitude",            "description": ""          },          {            "group": "Parameter",            "type": "<p>String</p> ",            "optional": false,            "field": "longitude",            "description": ""          }        ]      }    },    "filename": "./blueprints/main.py",    "groupTitle": "Content",    "sampleRequest": [      {        "url": "http://127.0.0.1:8080/create_post"      }    ]  },  {    "type": "post",    "url": "/dislike_post",    "title": "Dislike the Post, auth-cookie required",    "group": "Content",    "name": "DislikePost",    "version": "0.1.0",    "parameter": {      "fields": {        "Parameter": [          {            "group": "Parameter",            "type": "<p>String</p> ",            "optional": false,            "field": "vkid",            "description": "<p>User VK id</p> "          },          {            "group": "Parameter",            "type": "<p>String</p> ",            "optional": false,            "field": "post_id",            "description": "<p>Specific Post id</p> "          }        ]      }    },    "filename": "./blueprints/main.py",    "groupTitle": "Content",    "sampleRequest": [      {        "url": "http://127.0.0.1:8080/dislike_post"      }    ]  },  {    "type": "get",    "url": "/get_feed",    "title": "Get feed of all persons I am following, auth-cookie required",    "group": "Content",    "name": "GetGlobalFeed",    "version": "0.1.0",    "parameter": {      "fields": {        "Parameter": [          {            "group": "Parameter",            "type": "<p>String</p> ",            "optional": false,            "field": "vkid",            "description": "<p>User VK id</p> "          }        ]      }    },    "filename": "./blueprints/main.py",    "groupTitle": "Content",    "sampleRequest": [      {        "url": "http://127.0.0.1:8080/get_feed"      }    ]  },  {    "type": "get",    "url": "/get_feed",    "title": "Get Person feed by VKID, auth-cookie required",    "group": "Content",    "name": "GetPersonFeed",    "version": "0.1.0",    "parameter": {      "fields": {        "Parameter": [          {            "group": "Parameter",            "type": "<p>String</p> ",            "optional": false,            "field": "vkid",            "description": "<p>User VK id</p> "          },          {            "group": "Parameter",            "type": "<p>String</p> ",            "optional": false,            "field": "person_id",            "description": "<p>Person VK id</p> "          },          {            "group": "Parameter",            "type": "<p>String</p> ",            "optional": false,            "field": "order",            "description": "<p>[date, like]</p> "          }        ]      }    },    "filename": "./blueprints/main.py",    "groupTitle": "Content",    "sampleRequest": [      {        "url": "http://127.0.0.1:8080/get_feed"      }    ]  },  {    "type": "get",    "url": "/get_likes_to_post",    "title": "Get detailed list of the Post-Likes contributors",    "group": "Content",    "name": "GetPostLikers",    "version": "0.1.0",    "parameter": {      "fields": {        "Parameter": [          {            "group": "Parameter",            "type": "<p>String</p> ",            "optional": false,            "field": "post_id",            "description": "<p>Specific Post id</p> "          }        ]      }    },    "filename": "./blueprints/main.py",    "groupTitle": "Content",    "sampleRequest": [      {        "url": "http://127.0.0.1:8080/get_likes_to_post"      }    ]  },  {    "type": "get",    "url": "/get_map",    "title": "Get all posts at specific position",    "group": "Content",    "name": "GetPostsAtPosition",    "version": "0.1.0",    "parameter": {      "fields": {        "Parameter": [          {            "group": "Parameter",            "type": "<p>Decimal</p> ",            "optional": false,            "field": "latitude",            "description": ""          },          {            "group": "Parameter",            "type": "<p>Decimal</p> ",            "optional": false,            "field": "longitude",            "description": ""          },          {            "group": "Parameter",            "type": "<p>Int</p> ",            "optional": false,            "field": "distance",            "description": "<p>Circle diameter in miles</p> "          }        ]      }    },    "filename": "./blueprints/main.py",    "groupTitle": "Content",    "sampleRequest": [      {        "url": "http://127.0.0.1:8080/get_map"      }    ]  },  {    "type": "post",    "url": "/like_post",    "title": "Like the Post, auth-cookie required",    "group": "Content",    "name": "LikePost",    "version": "0.1.0",    "parameter": {      "fields": {        "Parameter": [          {            "group": "Parameter",            "type": "<p>String</p> ",            "optional": false,            "field": "vkid",            "description": "<p>User VK id</p> "          },          {            "group": "Parameter",            "type": "<p>String</p> ",            "optional": false,            "field": "post_id",            "description": "<p>Specific Post id</p> "          }        ]      }    },    "filename": "./blueprints/main.py",    "groupTitle": "Content",    "sampleRequest": [      {        "url": "http://127.0.0.1:8080/like_post"      }    ]  },  {    "type": "post",    "url": "/register_user",    "title": "Register & get auth cookie in responce",    "group": "User",    "name": "RegisterUser",    "description": "<p>Pass everything to register a new user before using the API</p> ",    "version": "0.1.0",    "parameter": {      "fields": {        "Parameter": [          {            "group": "Parameter",            "type": "<p>String</p> ",            "optional": false,            "field": "vkid",            "description": "<p>User VK id</p> "          },          {            "group": "Parameter",            "type": "<p>String</p> ",            "optional": false,            "field": "auth_token",            "description": "<p>VK-API auth token</p> "          },          {            "group": "Parameter",            "type": "<p>String</p> ",            "optional": false,            "field": "recovery_code",            "description": "<p>VK-API code to renew auth token when expires</p> "          }        ]      }    },    "filename": "./blueprints/security.py",    "groupTitle": "User",    "sampleRequest": [      {        "url": "http://127.0.0.1:8080/register_user"      }    ]  },  {    "type": "post",    "url": "/renew_cookie",    "title": "Set new cookie",    "description": "<p>Sets new cookie in responce. Call if 401</p> ",    "group": "User",    "name": "RenewUserCookie",    "version": "0.1.0",    "parameter": {      "fields": {        "Parameter": [          {            "group": "Parameter",            "type": "<p>String</p> ",            "optional": false,            "field": "vkid",            "description": "<p>User VK id</p> "          },          {            "group": "Parameter",            "type": "<p>String</p> ",            "optional": false,            "field": "recovery_code",            "description": "<p>VK-API code to renew auth token when expires</p> "          }        ]      }    },    "filename": "./blueprints/security.py",    "groupTitle": "User",    "sampleRequest": [      {        "url": "http://127.0.0.1:8080/renew_cookie"      }    ]  },  {    "type": "post",    "url": "/subscribe",    "title": "Follow a user with id=target_id",    "group": "User",    "name": "SubscribeOnUser",    "version": "0.1.0",    "parameter": {      "fields": {        "Parameter": [          {            "group": "Parameter",            "type": "<p>String</p> ",            "optional": false,            "field": "vkid",            "description": "<p>User VK id</p> "          },          {            "group": "Parameter",            "type": "<p>String</p> ",            "optional": false,            "field": "target_id",            "description": "<p>Targer user VK id</p> "          }        ]      }    },    "filename": "./blueprints/security.py",    "groupTitle": "User",    "sampleRequest": [      {        "url": "http://127.0.0.1:8080/subscribe"      }    ]  },  {    "success": {      "fields": {        "Success 200": [          {            "group": "Success 200",            "optional": false,            "field": "varname1",            "description": "<p>No type.</p> "          },          {            "group": "Success 200",            "type": "<p>String</p> ",            "optional": false,            "field": "varname2",            "description": "<p>With type.</p> "          }        ]      }    },    "type": "",    "url": "",    "version": "0.0.0",    "filename": "./doc/main.js",    "group": "_Users_vladimir_Desktop_wmfe_backend_doc_main_js",    "groupTitle": "_Users_vladimir_Desktop_wmfe_backend_doc_main_js",    "name": ""  }] });