
from flask import Flask

from blueprints.decorators import check_cookie
from blueprints.security import security
from blueprints.main import main_app


app = Flask("MainAPI")
app.register_blueprint(main_app)
app.register_blueprint(security)
app.config["DEBUG"] = True


if app.config["DEBUG"]:
    from blueprints.models import init_database, clear_db
    @app.before_first_request
    def cr_db():
        # init_database()
        clear_db()


@app.route("/test", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
@check_cookie(verbose=False)
def test():
    return "tttttttt"


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080)
