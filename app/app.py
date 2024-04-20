#!/usr/bin/python3
"""flask Module."""


from datetime import datetime
from flask import Flask, render_template, abort
from models import db, Strategy, Framework, Direction


# Create the app.
app = Flask(__name__)

# Configuring the MYSQL database, relative to the app instance folder.
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqlconnector:\
//strategize_main_dev:strategize_main_pwd@localhost/strategize"

# Initialize app with the extension.
db.init_app(app)

# Creating the table schema in the database.
with app.app_context():
    db.create_all()

strategies = [
        {
            "strategy_id": 1,
            "metadata": {
                          "strategy_name": "My Life",
                          "creation_date": datetime.now(),
                          "updated_date": datetime.now(),
                          "created_by": "Abdelrahman Emara",
                          "framework_id": 1
                        },
        },
        {
            "strategy_id": 2,
            "metadata": {
                          "strategy_name": "Green Life Co.",
                          "creation_date": datetime.now(),
                          "updated_date": datetime.now(),
                          "created_by": "Claude Thomas",
                          "framework_id": 1
                        }
        }
    ]

directions = [
        {
            "strategy_id": 1,
            "metadata": {
                          "direction_id": 1,
                          "direction_name": "Healthy Body",
                          "direction_definition": "To have a body free from\
                          pain and chronic diseases.",
                          "creation_date": datetime.now(),
                          "updated_date": datetime.now(),
                          "created_by": "Abdelrahman Emara",
                          "strategy_id": 1
                        }
        }

    ]


@app.route("/general_strategy")
def general_strategy():
    """Shows the general strategy web page."""
    return "<p>Hello, Strategizer!</p>"


@app.route("/general_strategy/metadata/<int:strategy_id>",
           strict_slashes=False)
def get_strategy(strategy_id):
    """Returns the specified general strategy web page for the given id."""
    for strategy in strategies:
        if strategy["strategy_id"] == strategy_id:
            return render_template("general_strategy.html",
                                   strategy=strategy)
    abort(404)


@app.route("/general_strategy/directions/<int:direction_id>",
           strict_slashes=False)
def get_direction(direction_id):
    """Returns the specified strategic direction data for the given id."""
    pass


if __name__ == "__main__":
    app.run(debug=True)
