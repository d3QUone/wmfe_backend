__author__ = 'vladimir'

from flask import Flask

from blueprints.security import security
from blueprints.main import main_app


app = Flask("MainAPI")
app.register_blueprint(security)
app.register_blueprint(main_app)
app.config["DEBUG"] = True


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080)
