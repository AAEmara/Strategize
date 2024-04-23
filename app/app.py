#!/usr/bin/python3
"""flask Module."""


from datetime import datetime
from flask import Flask, render_template, abort, jsonify, request, url_for
from flask import redirect
from forms import StrategyForm, DirectionForm
from uuid import UUID
import json
from models import db, Strategy, Framework, Direction, Perspective, Goal


# Create the app.
app = Flask(__name__)

# Using a Secret Key.
app.config["SECRET_KEY"] = "Thisisasecret!"

# Configuring the MYSQL database, relative to the app instance folder.
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqlconnector:\
//strategize_main_dev:strategize_main_pwd@localhost/strategize"

# Initialize app with the extension.
db.init_app(app)

# Creating the table schema in the database.
with app.app_context():
    db.create_all()


@app.route("/api/v1/strategies", methods=["GET"], strict_slashes=False)
def strategies():
    """Returns a collection of strategy resources."""
    stmt = db.select(Strategy)
    instances = db.session.execute(stmt).all()
    if not instances:
        return (jsonify({"error": "Not found"}), 404)
    records = list()
    for instance in instances:
        for obj in instance:
            records.append(obj.to_dict())
    return (jsonify(records), 200)


@app.route("/api/v1/strategies", methods=["POST"],
           strict_slashes=False)
def add_strategy():
    """Creates a strategy resource."""
    json_request = request.get_json()
    if json_request is None:
        return ("Not a JSON", 400)
    elif ("name" not in list(json_request)):
        return ("Missing name", 400)
    elif ("created_by" not in list(json_request)):
        return ("Missing created_by", 400)
    strategy_name = json_request["name"]
    strategy_creator = json_request["created_by"]
    strategy_obj = Strategy(name=strategy_name, created_by=strategy_creator)
    if not strategy_obj:
        return (jsonify({"error": "Failed to create"}), 400)
    db.session.add(strategy_obj)
    # Must be converted to dictionary before commit because state change.
    strategy_dict = strategy_obj.to_dict()
    db.session.commit()
    return (jsonify(strategy_dict), 201)


@app.route("/api/v1/strategies/<uuid:strategy_id>", methods=["GET"],
           strict_slashes=False)
def get_strategy(strategy_id):
    """Returns a strategy resource for the strategy_id given."""
    if not isinstance(strategy_id, UUID):
        return (jsonify({"error": "Not found"}), 404)
    stmt = db.select(Strategy).where(
        Strategy.id == db.bindparam("strategy_id"))
    try:
        instances = db.session.execute(stmt,
                                       {"strategy_id": strategy_id}).one()
    except db.exc.NoResultFound:
        return (jsonify({"error": "Not found"}), 404)
    records = list()
    for obj in instances:
        records.append(obj.to_dict())
    return (jsonify(records), 200)


@app.route("/api/v1/strategies/<uuid:strategy_id>", methods=["PUT"],
           strict_slashes=False)
def update_strategy(strategy_id):
    """Updates a strategy resource for the strategy_id given."""
    # Checks on URL and sent request.
    if not isinstance(strategy_id, UUID):
        return (jsonify({"error": "Not found"}), 404)
    json_request = request.get_json()
    if json_request is None:
        return ("Not a JSON", 400)

    # Querying on the given strategy_id to retrieve the strategy.
    stmt = db.select(Strategy).where(
        Strategy.id == db.bindparam("strategy_id"))
    try:
        instances = db.session.execute(stmt,
                                       {"strategy_id": strategy_id}).one()
    except db.exc.NoResultFound:
        return (jsonify({"error": "Not found"}), 404)

    # Updating the quried strategy resource for the given data in JSON.
    allowed_list = ["name", "created_by"]
    for obj in instances:
        for key, value in json_request.items():
            if key in allowed_list:
                setattr(obj, key, value)
        setattr(obj, "update_date", datetime.utcnow())
        record_dict = obj.to_dict()
    db.session.commit()
    return (jsonify(record_dict), 200)


@app.route("/api/v1/strategies/<uuid:strategy_id>", methods=["DELETE"],
           strict_slashes=False)
def delete_strategy(strategy_id):
    """Deletes a strategy resource for the strategy_id given."""
    # Checks on URL.
    if not isinstance(strategy_id,  UUID):
        return (jsonify({"error": "Not found"}), 404)

    # Querying on the given strategy_id to retrieve the strategy.
    stmt = db.select(Strategy).where(
        Strategy.id == db.bindparam("strategy_id"))
    try:
        instances = db.session.execute(stmt,
                                       {"strategy_id": strategy_id}).one()
    except db.exc.NoResultFound:
        return (jsonify({"error": "Not found"}), 404)

    # Deleting the quried strategy resource with the given strategy_id.
    for obj in instances:
        db.session.delete(obj)
        db.session.commit()
    return ({}, 200)


if __name__ == "__main__":
    app.run(debug=True)
