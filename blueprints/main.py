
from flask import Blueprint

from .decorators import check_cookie


main_app = Blueprint("api", __name__)


@main_app.route("/news_feed", methods=["GET"])
@check_cookie
def get_news_feed():
    return


# get my_feed

# get ...
