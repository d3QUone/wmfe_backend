__author__ = 'vladimir'

import time
import datetime

from flask import Blueprint, Response, request


security = Blueprint("security_module", __name__)


@security.route("/renew_cookie", methods=["GET"])
def renew_cookie():
    r = request.args.get("vkid", None)


@security.route("/set")
def set_cookie():
    r = Response(response="some text")
    r.set_cookie("auth", "test-time-{0}".format(time.time()), expires=time.time()+datetime.timedelta(days=1).total_seconds())
    return r
