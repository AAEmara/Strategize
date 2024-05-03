#!/usr/bin/python3
"""flask Module."""


from datetime import datetime
from flask import Flask, render_template, abort, jsonify, request, url_for
from flask import redirect
from flask_cors import CORS
from forms import StrategyForm, DirectionForm
from uuid import UUID
import json
from models import db, Strategy, Framework, Direction, Perspective, Goal


# Create the app.
app = Flask(__name__)

# Using a Secret Key.
app.config["SECRET_KEY"] = "Thisisasecret!"

CORS(app, resources={r"/*":{'origins': "*"}}) 

# Configuring the MYSQL database, relative to the app instance folder.
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqlconnector:\
//strategize_main_dev:strategize_main_pwd@localhost/strategize"


# Initialize app with the extension.
db.init_app(app)

# Creating the table schema in the database.
with app.app_context():
    db.create_all()


# Strategy_Resource API.
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


# Framework_Resource API.
@app.route("/api/v1/frameworks", methods=["GET"], strict_slashes=False)
def frameworks():
    """Returns a collection of framework resources."""
    stmt = db.select(Framework)
    instances = db.session.execute(stmt).all()
    if not instances:
        return (jsonify({"error": "Not found"}), 404)
    records = list()
    for instance in instances:
        for obj in instance:
            records.append(obj.to_dict())
    return (jsonify(records), 200)


@app.route("/api/v1/frameworks/<int:framework_id>", methods=["GET"],
           strict_slashes=False)
def get_framework(framework_id):
    """Returns a  framework resource for a given framework_id."""
    if not isinstance(framework_id, int):
        return (jsonify({"error": "Not found"}), 404)
    stmt = db.select(Framework).where(
        Framework.id == db.bindparam("framework_id"))
    try:
        instance = db.session.execute(stmt,
                                      {"framework_id": framework_id}).one()
    except db.exc.NoResultFound:
        return (jsonify({"error": "Not found"}), 404)

    for obj in instance:
        record = obj.to_dict()
    return (jsonify(record), 200)


# Direction_Resource API.
@app.route("/api/v1/strategies/<uuid:strategies_id>/directions",
           methods=["GET"],
           strict_slashes=False)
def directions(strategies_id):
    """Returns a collection of direction resources."""
    if not isinstance(strategies_id, UUID):
        return (jsonify({"error": "Not found"}), 404)
    stmt = db.select(Direction).join_from(
                    Strategy, Direction,
                    Strategy.id == Direction.strategy_id).where(
                    Strategy.id == db.bindparam("strategies_id"))
    try:
        instances = db.session.execute(stmt,
                                       {"strategies_id": strategies_id}).all()
    except db.exc.NoResultFound:
        return (jsonify({"error": "Not found"}), 404)
    records = list()
    for instance in instances:
        for obj in instance:
            records.append(obj.to_dict())
    return (jsonify(records), 200)


@app.route("/api/v1/strategies/<uuid:strategies_id>/directions",
           methods=["POST"], strict_slashes=False)
def create_direction(strategies_id):
    """Create a direction resource."""
    if not isinstance(strategies_id, UUID):
        return (jsonify({"error": "Not found"}), 404)
    json_request = request.get_json()
    if json_request is None:
        return (jsonify({"error": "Not found"}), 404)
    elif "name" not in list(json_request):
        return (jsonify({"error": "Not found"}), 404)
    elif "result" not in list(json_request):
        return (jsonify({"error": "Not found"}), 404)

    direction_name = json_request["name"]
    direction_result = json_request["result"]
    try:
        direction_def = json_request["definition"]
    except KeyError:
        direction_def = None
    direction = Direction(name=direction_name,
                          result=direction_result,
                          definition=direction_def)
    setattr(direction, "strategy_id", strategies_id)
    if not direction:
        return (jsonify({"error": "Not found"}), 404)
    direction_dict = direction.to_dict()
    db.session.add(direction)
    stmt = db.select(Strategy).where(
        Strategy.id == db.bindparam("strategy_id"))
    instance = db.session.execute(stmt,
                                  {"strategy_id": strategies_id}).one()
    for obj in instance:
        obj.update_date = datetime.utcnow()
    db.session.commit()
    direction_dict["id"] = direction.id
    return (jsonify(direction_dict), 201)


@app.route("/api/v1/strategies/<uuid:strategies_id>/directions\
/<int:direction_id>", methods=["GET"], strict_slashes=False)
def get_direction(strategies_id, direction_id):
    """Returns a direction resource for a given direction_id."""
    if not isinstance(strategies_id, UUID):
        return (jsonify({"error": "Not found"}), 404)
    elif not isinstance(direction_id, int):
        return (jsonify({"error": "Not found"}), 404)
    stmt = db.select(Direction).join_from(
                    Strategy, Direction,
                    Strategy.id == Direction.strategy_id).where(
                    Strategy.id == db.bindparam("strategies_id")).where(
                    Direction.id == db.bindparam("direction_id"))
    try:
        instance = db.session.execute(stmt,
                                      {"strategies_id": strategies_id,
                                       "direction_id": direction_id}).one()
    except db.exc.NoResultFound:
        return (jsonify({"error": "Not found"}), 404)

    for obj in instance:
        record_dict = obj.to_dict()
    return (jsonify(record_dict), 200)


@app.route("/api/v1/strategies/<uuid:strategies_id>/directions\
/<int:direction_id>", methods=["PUT"], strict_slashes=False)
def update_direction(strategies_id, direction_id):
    """Updates a direction resource for a given direction_id."""
    if not isinstance(strategies_id, UUID):
        return (jsonify({"error": "Not found"}), 404)
    elif not isinstance(direction_id, int):
        return (jsonify({"error": "Not found"}), 404)
    json_request = request.get_json()
    if json_request is None:
        return (jsonify({"error": "Not found"}), 404)
    stmt = db.select(Direction, Strategy).join_from(
                    Strategy, Direction,
                    Strategy.id == Direction.strategy_id).where(
                    Strategy.id == db.bindparam("strategies_id")).where(
                    Direction.id == db.bindparam("direction_id"))
    try:
        instance = db.session.execute(stmt,
                                      {"strategies_id": strategies_id,
                                       "direction_id": direction_id}).one()
    except db.exc.NoResultFound:
        return (jsonify({"error": "Not found"}), 404)
    allowed_list = ["name", "result", "definition"]
    for obj in instance:
        for key, value in json_request.items():
            if isinstance(obj, Direction) and key in allowed_list:
                setattr(obj, key, value)
            elif isinstance(obj, Strategy):
                obj.update_date = datetime.utcnow()
        if isinstance(obj, Direction):
            record_dict = obj.to_dict()
    db.session.commit()
    return (jsonify(record_dict), 200)


@app.route("/api/v1/strategies/<uuid:strategies_id>/directions\
/<int:direction_id>", methods=["DELETE"], strict_slashes=False)
def delete_direction(strategies_id, direction_id):
    """Deletes a direction resource for a given direction_id."""
    if not isinstance(strategies_id, UUID):
        return (jsonify({"error": "Not found"}), 404)
    elif not isinstance(direction_id, int):
        return (jsonify({"error": "Not found"}), 404)
    stmt = db.select(Direction).join_from(
                    Strategy, Direction,
                    Strategy.id == Direction.strategy_id).where(
                    Strategy.id == db.bindparam("strategies_id")).where(
                    Direction.id == db.bindparam("direction_id"))
    try:
        instance = db.session.execute(stmt,
                                      {"strategies_id": strategies_id,
                                       "direction_id": direction_id}).one()
    except db.exc.NoResultFound:
        return (jsonify({"error": "Not found"}), 404)
    for obj in instance:
        db.session.delete(obj)
    db.session.commit()
    return ({}, 200)


# Perspective_Resource API.
@app.route(f"/api/v1/perspectives", methods=["GET"], strict_slashes=False)
def perspectives():
    """Returns a collection of perspective resources."""
    stmt = db.select(Perspective)
    instances = db.session.execute(stmt).all()
    records = list()
    for instance in instances:
        for obj in instance:
            records.append(obj.to_dict())
    return (jsonify(records), 200)


@app.route(f"/api/v1/perspectives/<int:perspective_id>",
           methods=["GET"], strict_slashes=False)
def get_perspective(perspective_id):
    """Returns a perspective resource for a given perspective_id."""
    if not isinstance(perspective_id, int):
        return (jsonify({"error": "Not found"}), 404)
    stmt = db.select(Perspective).where(
        Perspective.id == db.bindparam("perspective_id"))
    try:
        instance = db.session.execute(stmt,
                                      {"perspective_id": perspective_id}).one()
    except db.exc.NoResultFound:
        return (jsonify({"error": "Not found"}), 404)
    for obj in instance:
        record_dict = obj.to_dict()
    return (jsonify(record_dict), 200)


# Goal_Resource API.
@app.route("/api/v1/strategies/<uuid:strategies_id>/directions\
/<int:directions_id>/goals",
           methods=["GET"], strict_slashes=False)
def goals(strategies_id, directions_id):
    """Returns a collection of goal resources."""
    # Checking on the datatypes of the inserted ids.
    if not isinstance(strategies_id, UUID):
        return (jsonify({"error": "Not found"}), 404)
    elif not isinstance(directions_id, int):
        return (jsonify({"error": "Not found"}), 404)

    # Querying on the given goal_id to return the goal resources later on.
    stmt = db.select(Goal).join_from(
                    Strategy, Direction,
                    Strategy.id == Direction.strategy_id).join_from(
                    Direction, Goal,
                    Direction.id == Goal.direction_id).where(
                    Strategy.id == db.bindparam("strategies_id")).where(
                    Direction.id == db.bindparam("directions_id"))
    try:
        instances = db.session.execute(stmt,
                                       {"strategies_id": strategies_id,
                                        "directions_id": directions_id}).all()
    except db.exc.NoResultFound:
        return (jsonify({"error": "Not found"}), 404)

    # Converting the Goal objects into a dictionaries to return in JSON format.
    goals_list = list()
    for instance in instances:
        for obj in instance:
            if isinstance(obj, Goal):
                goals_list.append(obj.to_dict())

    # Returning the converted Goal objects in JSON format.
    return (jsonify(goals_list), 200)


@app.route("/api/v1/strategies/<uuid:strategies_id>/directions\
/<int:directions_id>/goals",
           methods=["POST"], strict_slashes=False)
def create_goal(strategies_id, directions_id):
    """Creates goal resource."""
    # Checking on the datatypes of the inserted ids.
    if not isinstance(strategies_id, UUID):
        return (jsonify({"error": "Not found"}), 404)
    elif not isinstance(directions_id, int):
        return (jsonify({"error": "Not found"}), 404)

    # Checking on the JSON inputs in the request sent.
    json_request = request.get_json()
    if json_request is None:
        return (jsonify({"error": "Not found"}), 404)
    elif "name" not in list(json_request):
        return ("Missing name", 404)
    elif "perspective_id" not in list(json_request):
        return ("Missing perspective", 404)

    # Checking on perspective_id in range or not.
    goal_perspective = json_request["perspective_id"]
    if goal_perspective not in range(1, 5):
        return ("Wrong perspective_id", 404)
    goal_name = json_request["name"]
    try:
        goal_note = json_request["note"]
    except KeyError:
        goal_note = None

    # Querying on the given strategy_id to Update its update_date later.
    stmt = db.select(Strategy).where(
                Strategy.id == db.bindparam("strategies_id"))
    try:
        instance = db.session.execute(stmt,
                                      {"strategies_id": strategies_id}).one()
    except db.exc.NoResultFound:
        return (jsonify({"error": "Not found"}), 404)

    # Creating the Goal object and getting dictionary data representation.
    goal = Goal(name=goal_name, note=goal_note, direction_id=directions_id,
                perspective_id=goal_perspective)
    goal_dict = goal.to_dict()

    # Updating the update_date attribute in the Strategy object.
    for obj in instance:
        setattr(obj, "update_date", datetime.utcnow())

    # Adding the Goal object in the database and commiting.
    try:
        db.session.add(goal)
        db.session.commit()
    except db.exc.IntegrityError:
        return ("Wrong input", 404)

    # Giving the Goal object the id generated in database and returning JSON.
    goal_dict["id"] = goal.id
    return (jsonify(goal_dict), 201)


@app.route("/api/v1/strategies/<uuid:strategy_id>/directions\
/<int:direction_id>/goals/<int:goal_id>",
           methods=["GET"], strict_slashes=False)
def get_goal(strategy_id, direction_id, goal_id):
    """Returns a goal resource for a given goal_id."""
    # Checking on the datatypes of the inserted ids.
    if not isinstance(strategy_id, UUID):
        return (jsonify({"error": "Not found"}), 404)
    elif not isinstance(direction_id, int):
        return (jsonify({"error": "Not found"}), 404)
    elif not isinstance(goal_id, int):
        return (jsonify({"error": "Not found"}), 404)

    # Querying on the given ids to Return the goal resource later on.
    stmt = db.select(Goal).join_from(
                Strategy, Direction,
                Strategy.id == Direction.strategy_id).join_from(
                Direction, Goal,
                Direction.id == Goal.direction_id).where(
                Strategy.id == db.bindparam("strategy_id")).where(
                Direction.id == db.bindparam("direction_id")).where(
                Goal.id == db.bindparam("goal_id"))
    try:
        instance = db.session.execute(stmt,
                                      {"strategy_id": strategy_id,
                                       "direction_id": direction_id,
                                       "goal_id": goal_id}).one()
    except db.exc.NoResultFound:
        return (jsonify({"error": "Not found"}), 404)

    # Preparing the dictionary data representation of the Goal object.
    for obj in instance:
        goal_dict = obj.to_dict()
    return (jsonify(goal_dict), 200)


@app.route("/api/v1/strategies/<uuid:strategy_id>/directions\
/<int:direction_id>/goals/<int:goal_id>",
           methods=["PUT"], strict_slashes=False)
def update_goal(strategy_id, direction_id, goal_id):
    """Returns a goal resource for a given goal_id."""
    # Checking on the datatypes of the inserted ids.
    if not isinstance(strategy_id, UUID):
        return (jsonify({"error": "Not found"}), 404)
    elif not isinstance(direction_id, int):
        return (jsonify({"error": "Not found"}), 404)
    elif not isinstance(goal_id, int):
        return (jsonify({"error": "Not found"}), 404)

    # Checking on the JSON inputs in the request sent.
    json_request = request.get_json()
    if json_request is None:
        return (jsonify({"error": "Not found"}), 404)

    # Querying on the given ids to Return the goal resource later on.
    stmt = db.select(Goal, Strategy).join_from(
                Strategy, Direction,
                Strategy.id == Direction.strategy_id).join_from(
                Direction, Goal,
                Direction.id == Goal.direction_id).where(
                Strategy.id == db.bindparam("strategy_id")).where(
                Direction.id == db.bindparam("direction_id")).where(
                Goal.id == db.bindparam("goal_id"))
    try:
        instance = db.session.execute(stmt,
                                      {"strategy_id": strategy_id,
                                       "direction_id": direction_id,
                                       "goal_id": goal_id}).one()
    except db.exc.NoResultFound:
        return (jsonify({"error": "Not found"}), 404)

    # Updating the Goal object according to the allowed list fields.
    allowed_list = ["name", "note", "direction_id", "perspective_id"]
    update_status = False
    for obj in instance:
        for key, value in json_request.items():
            if isinstance(obj, Goal) and key in allowed_list:
                setattr(obj, key, value)
                update_status = True
            elif isinstance(obj, Strategy) and update_status:
                setattr(obj, "update_date", datetime.utcnow())
        if isinstance(obj, Goal):
            goal_dict = obj.to_dict()

    # Saving the updates done to the object and returning it.
    db.session.commit()
    return (jsonify(goal_dict), 200)


@app.route("/api/v1/strategies/<uuid:strategy_id>/direction\
/<int:direction_id>/goals/<int:goal_id>",
           methods=["DELETE"], strict_slashes=False)
def delete_goal(strategy_id, direction_id, goal_id):
    """Returns a goal resource for a given goal_id."""
    # Checking on the datatypes of the inserted ids.
    if not isinstance(strategy_id, UUID):
        return (jsonify({"error": "Not found"}), 404)
    elif not isinstance(direction_id, int):
        return (jsonify({"error": "Not found"}), 404)
    elif not isinstance(goal_id, int):
        return (jsonify({"error": "Not found"}), 404)

    # Querying on the given ids to Return the goal resource later on.
    stmt = db.select(Goal, Strategy).join_from(
                Strategy, Direction,
                Strategy.id == Direction.strategy_id).join_from(
                Direction, Goal,
                Direction.id == Goal.direction_id).where(
                Strategy.id == db.bindparam("strategy_id")).where(
                Direction.id == db.bindparam("direction_id")).where(
                Goal.id == db.bindparam("goal_id"))
    try:
        instance = db.session.execute(stmt,
                                      {"strategy_id": strategy_id,
                                       "direction_id": direction_id,
                                       "goal_id": goal_id}).one()
    except db.exc.NoResultFound:
        return (jsonify({"error": "Not found"}), 404)

    # Deleting the Goal object according to the returned query object.
    delete_status = False
    for obj in instance:
        if isinstance(obj, Goal):
            db.session.delete(obj)
            delete_status = True
        elif isinstance(obj, Strategy) and delete_status:
            setattr(obj, "update_date", datetime.utcnow())

    # Saving the delete operation done to the object and returning empty dict.
    db.session.commit()
    return (jsonify({}), 200)


if __name__ == "__main__":
    app.run(debug=True)
