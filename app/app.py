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
from models import Objective, Datatype, Kpi


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
    """Returns a collection of Strategy Class resources using GET HTTP method.

    Returns:
        if the query returns Strategy Objects:
            JSON: A list of dictionaries in a JSON format
                  , 200 STATUS CODE is also sent.
        else:
            JSON: A dictionary of 'error', and 'Not found' pair
                  , 404 STATUS CODE is also sent.
    """
    # SQLAlchemy ORM Query to select all of the Strategy Objects.
    stmt = db.select(Strategy)
    instances = db.session.execute(stmt).all()

    # Returning an error if the query returns nothing.
    if not instances:
        return (jsonify({"error": "Not found"}), 404)
    strategies_list = list()

    # Converting Strategy Objects into dictionaries and adding it to a list.
    for instance in instances:
        for obj in instance:
            strategies_list.append(obj.to_dict())

    # Returning the converted Strategy objects in JSON format.
    return (jsonify(strategies_list), 200)


@app.route("/api/v1/strategies", methods=["POST"], strict_slashes=False)
def create_strategy():
    """Creates a resource of Strategy Class using POST HTTP method.

    Returns:
        if the Strategy Object was created (SUCCESS):
            JSON: Dicitonary of the created Strategy Object in a JSON format
                  , 201 STATUS CODE is also sent.
        if the Strategy Object wasn't created (FAILURE):
            JSON: Dictionary representing the error in JSON format
                  , 400 STATUS CODE is also sent.
        if the Content-type of the Request isn't in JSON format:
            JSON: Dictionary representing the error and what is missing in
                  JSON format, 400 STATUS CODE is also sent.
    """
    json_request = request.get_json()

    # Checking on the data sent in the Request.
    if json_request is None:
        return (jsonify({'error': "Not a JSON"}), 400)
    elif ("name" not in list(json_request)):
        return (jsonify({'error': "Missing name"}), 400)
    elif ("created_by" not in list(json_request)):
        return (jsonify({'error': "Missing created_by"}), 400)
    strategy_name = json_request["name"]
    strategy_creator = json_request["created_by"]

    # Creating the Strategy Object.
    strategy_obj = Strategy(name=strategy_name, created_by=strategy_creator)
    if not strategy_obj:
        return (jsonify({"error": "Failed to create"}), 400)
    db.session.add(strategy_obj)

    # Converting the Object to a dictionary before commiting.
    # Conversion should be done first because of the Object's state change.
    strategy_dict = strategy_obj.to_dict()
    db.session.commit() # Object's state changes once the commit is done.
    return (jsonify(strategy_dict), 201)


@app.route("/api/v1/strategies/<uuid:strategy_id>", methods=["GET"],
           strict_slashes=False)
def get_strategy(strategy_id):
    """Returns a resource of Strategy Class for a given strategy_id using GET
       HTTP method.

    Args:
        strategy_id (UUID or str): Id of the Strategy the user wants to use.

    Returns:
        if the Strategy Object was found (SUCCESS):
            JSON: Dicitonary of the returned Strategy Object in a JSON format
                  , 200 STATUS CODE is also sent.
        if the Strategy Object wasn't found (FAILURE):
            JSON: Dictionary of the 'error', and 'Not found' pair
                  , 404 STATUS CODE is also sent.
        if the datatype of the entered Resource ID wasn't correct:
            JSON: Dictionary of the 'error', and 'Not found' pair
                  , 404 STATUS CODE is also sent.
    """
    # Checking on the ID datatype of the Strategy Object to be returned.
    if not isinstance(strategy_id, UUID):
        return (jsonify({"error": "Not found"}), 404)

    # SQLAlchemy ORM Query to select the Strategy Object
    # according to the given strategy_id.
    stmt = db.select(Strategy).where(
        Strategy.id == db.bindparam("strategy_id"))
    try:
        instance = db.session.execute(stmt,
                                       {"strategy_id": strategy_id}).one()
    except db.exc.NoResultFound:
        return (jsonify({"error": "Not found"}), 404) # No Object with this id.

    # Converting the returned Strategy Object into a dictionary.
    for obj in instance:
        strategy_dict = obj.to_dict()
    return (jsonify(strategy_dict), 200)


@app.route("/api/v1/strategies/<uuid:strategy_id>", methods=["PUT"],
           strict_slashes=False)
def update_strategy(strategy_id):
    """Updates a Strategy resource for a given strategy_id using PUT
       HTTP method.

    Args:
        strategy_id (UUID or str): Id of the Strategy the user wants to use.

    Returns:
        if the Strategy Object was updated (SUCCESS):
            JSON: Dicitonary of the updated Strategy Object in a JSON format
                  , 200 STATUS CODE is also sent.
        if the Strategy Object to update wasn't found (FAILURE):
            JSON: Dictionary of the 'error', and 'Not found' pair
                  , 404 STATUS CODE is also sent.
        if the request is empty:
            JSON: Dictionary of the 'error' and 'Not found' pair
                  , 400 STATUS CODE is also sent.
        if the datatype of the entered Resource ID wasn't correct:
            JSON: Dictionary of the 'error', and 'Not found' pair
                  , 404 STATUS CODE is also sent.
    """
    # Checking on the ID datatype of the Strategy Object to be updated.
    if not isinstance(strategy_id, UUID):
        return (jsonify({"error": "Not found"}), 404)

    json_request = request.get_json()

    # Checking on the data sent in the Request.
    # TODO: Add checks on the updated data.
    if json_request is None:
        return (jsonify({'error': "Not a JSON"}), 400)

    # SQLAlchemy ORM Query to select the Strategy Object
    # according to the given strategy_id.
    stmt = db.select(Strategy).where(
        Strategy.id == db.bindparam("strategy_id"))
    try:
        instance = db.session.execute(stmt,
                                       {"strategy_id": strategy_id}).one()
    except db.exc.NoResultFound:
        return (jsonify({"error": "Not found"}), 404)

    # TODO: use an update_status variable with a false boolean.
    allowed_list = ["name", "created_by"]

    # Updating the returned Strategy Object with the given data in the Request
    # with respect to the allowed values to be updated.
    for obj in instance:
        for key, value in json_request.items():
            if key in allowed_list:
                setattr(obj, key, value)
                setattr(obj, "update_date", datetime.utcnow())
        strategy_dict = obj.to_dict() # Converting Object into a dictionary.
    db.session.commit()
    return (jsonify(strategy_dict), 200)


@app.route("/api/v1/strategies/<uuid:strategy_id>", methods=["DELETE"],
           strict_slashes=False)
def delete_strategy(strategy_id):
    """Deletes a Strategy resource for a given strategy_id using DELETE
       HTTP method.

    Args:
        strategy_id (UUID or str): Id of the Strategy the user wants to use.

    Returns:
        if the Strategy Object was deleted (SUCCESS):
            JSON: Empty dictionary, 200 STATUS CODE is also sent.
        if the Strategy Object to delete wasn't found (FAILURE):
            JSON: Dictionary of the 'error', and 'Not found' pair
                  , 404 STATUS CODE is also sent.
        if the datatype of the entered Resource ID wasn't correct:
            JSON: Dictionary of the 'error', and 'Not found' pair
                  , 404 STATUS CODE is also sent.
    """
    # Checking on the ID datatype of the Strategy Object to be deleted.
    if not isinstance(strategy_id,  UUID):
        return (jsonify({"error": "Not found"}), 404)

    # SQLAlchemy ORM Query to select the Strategy Object
    # according to the given strategy_id.
    stmt = db.select(Strategy).where(
        Strategy.id == db.bindparam("strategy_id"))
    try:
        instance = db.session.execute(stmt,
                                       {"strategy_id": strategy_id}).one()
    except db.exc.NoResultFound:
        return (jsonify({"error": "Not found"}), 404)

    # Deleting the returned Strategy Object.
    for obj in instance:
        db.session.delete(obj)
        db.session.commit()

    # Returning an empty dictionary representing the deleted Strategy Object.
    return ({}, 200)


# Framework_Resource API.
@app.route("/api/v1/frameworks", methods=["GET"], strict_slashes=False)
def frameworks():
    """Returns a collection of Framework Class resources using GET HTTP method.

    Returns:
        if the query returns Framework Objects:
            JSON: A list of dictionaries in a JSON format
                  , 200 STATUS CODE is also sent.
        else:
            JSON: A dictionary of 'error', and 'Not found' pair
                  , 404 STATUS CODE is also sent.
    """
    # SQLAlchemy ORM Query to select all of the Framework Objects.
    stmt = db.select(Framework)
    instances = db.session.execute(stmt).all()

    # Returning an error if the query returns nothing.
    if not instances:
        return (jsonify({"error": "Not found"}), 404)
    frameworks_list = list()

    # Converting Framework Objects into dictionaries and adding it to a list.
    for instance in instances:
        for obj in instance:
            frameworks_list.append(obj.to_dict())

    # Returning the converted Framework objects in JSON format.
    return (jsonify(frameworks_list), 200)


@app.route("/api/v1/frameworks/<int:framework_id>", methods=["GET"],
           strict_slashes=False)
def get_framework(framework_id):
    """Returns a resource of Framework Class for a given framework_id using GET
       HTTP method.

    Args:
        framework_id (int): Id of the Framework the user wants to use.

    Returns:
        if the Framework Object was found (SUCCESS):
            JSON: Dicitonary of the returned Framework Object in a JSON format
                  , 200 STATUS CODE is also sent.
        if the Framework Object wasn't found (FAILURE):
            JSON: Dictionary of the 'error', and 'Not found' pair
                  , 404 STATUS CODE is also sent.
        if the datatype of the entered Resource ID wasn't correct:
            JSON: Dictionary of the 'error', and 'Not found' pair
                  , 404 STATUS CODE is also sent.
    """
    # Checking on the ID datatype of the Framework Object to be returned.
    if not isinstance(framework_id, int):
        return (jsonify({"error": "Not found"}), 404)

    # SQLAlchemy ORM Query to select the Framework Object
    # according to the given framework_id.
    stmt = db.select(Framework).where(
        Framework.id == db.bindparam("framework_id"))
    try:
        instance = db.session.execute(stmt,
                                      {"framework_id": framework_id}).one()
    except db.exc.NoResultFound:
        return (jsonify({"error": "Not found"}), 404) # No Object with this id.

    # Converting the returned Framework Object into a dictionary.
    for obj in instance:
        framework_dict = obj.to_dict()
    return (jsonify(framework_dict), 200)


# Direction_Resource API.
@app.route("/api/v1/strategies/<uuid:strategy_id>/directions",
           methods=["GET"], strict_slashes=False)
def directions(strategy_id):
    """Returns a collection of Direction Class resources for a given
       strategy_id using GET HTTP method.

    Returns:
        if the query returns Direction Objects (SUCCESS):
            JSON: A list of dictionaries in a JSON format
                  , 200 STATUS CODE is also sent.
        if the query doesn't return Direction Objects (FAILURE):
            JSON: A dictionary of 'error', and 'Not found' pair
                  , 404 STATUS CODE is also sent.
        if the datatype of the entered Strategy Object ID wasn't correct:
            JSON: Dictionary of the 'error', and 'Not found' pair
                  , 404 STATUS CODE is also sent.
    """
    # Checking on the ID datatype of the Strategy Object for the 
    # Direction Objects to be returned.
    if not isinstance(strategy_id, UUID):
        return (jsonify({"error": "Not found"}), 404)

    # SQLAlchemy ORM Query to select all of the Direction Objects.
    stmt = db.select(Direction).join_from(
                    Strategy, Direction,
                    Strategy.id == Direction.strategy_id).where(
                    Strategy.id == db.bindparam("strategy_id"))
    try:
        instances = db.session.execute(stmt,
                                       {"strategy_id": strategy_id}).all()
    except db.exc.NoResultFound:
        return (jsonify({"error": "Not found"}), 404) # No Object with this id.
    directions_list = list()

    # Converting Direction Objects into dictionaries and adding it to a list.
    for instance in instances:
        for obj in instance:
            directions_list.append(obj.to_dict())

    # Returning the converted Direction Objects in JSON format.
    return (jsonify(directions_list), 200)


@app.route("/api/v1/strategies/<uuid:strategy_id>/directions",
           methods=["POST"], strict_slashes=False)
def create_direction(strategy_id):
    """Creates a resource of Direction Class using POST HTTP method.

    Returns:
        if the Direction Object was created (SUCCESS):
            JSON: Dicitonary of the created Direction Object in a JSON format
                  , 201 STATUS CODE is also sent.
        if the Strategy Object wasn't created (FAILURE):
            JSON: Dictionary representing the error in JSON format
                  , 400 STATUS CODE is also sent.
        if the Content-type of the Request isn't in JSON format:
            JSON: Dictionary representing the error and what is missing in
                  JSON format, 400 STATUS CODE is also sent.
    """
    # Checking on the ID datatype of the Strategy Object for the 
    # Direction Object to be returned.
    if not isinstance(strategy_id, UUID):
        return (jsonify({"error": "Not found"}), 400)

    # SQLAlchemy ORM Query to select the Strategy Object
    # according to the given strategy_id.
    stmt = db.select(Strategy).where(
        Strategy.id == db.bindparam("strategy_id"))
    try:
        instance = db.session.execute(stmt,
                                      {"strategy_id": strategy_id}).one()
    except db.exc.NoResultFound:
        return (jsonify({"error": "Not found"}), 404) # No Object with this id.

    json_request = request.get_json()

    # Checking on the data sent in the Request.
    if json_request is None:
        return (jsonify({"error": "Not a JSON"}), 400)
    elif "name" not in list(json_request):
        return (jsonify({"error": "Missing name"}), 400)
    elif "result" not in list(json_request):
        return (jsonify({"error": "Missing result"}), 400)
    direction_name = json_request["name"]
    direction_result = json_request["result"]

    # Checking on optional fields if they have a value sent in the Request.
    try:
        direction_def = json_request["definition"]
    except KeyError:
        direction_def = None # Assiging optional definition field None value.

    # Creating the Direction Object.
    direction = Direction(name=direction_name,
                          result=direction_result,
                          definition=direction_def)
    setattr(direction, "strategy_id", strategy_id)
    if not direction:
        return (jsonify({"error": "Failed to create"}), 400) # wasn't created.
    direction_dict = direction.to_dict() # Converting before state change.
    db.session.add(direction) # Adding the Direction Object to the database.

    # Updating the update_date since Direction Object is created.
    for obj in instance:
        obj.update_date = datetime.utcnow()
    db.session.commit()
    direction_dict["id"] = direction.id

    # Returning the converted Direction Object in JSON format.
    return (jsonify(direction_dict), 201)


@app.route("/api/v1/strategies/<uuid:strategy_id>/directions\
/<int:direction_id>", methods=["GET"], strict_slashes=False)
def get_direction(strategy_id, direction_id):
    """Returns a direction resource for a given direction_id."""
    if not isinstance(strategy_id, UUID):
        return (jsonify({"error": "Not found"}), 404)
    elif not isinstance(direction_id, int):
        return (jsonify({"error": "Not found"}), 404)
    stmt = db.select(Direction).join_from(
                    Strategy, Direction,
                    Strategy.id == Direction.strategy_id).where(
                    Strategy.id == db.bindparam("strategy_id")).where(
                    Direction.id == db.bindparam("direction_id"))
    try:
        instance = db.session.execute(stmt,
                                      {"strategy_id": strategy_id,
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


@app.route("/api/v1/strategies/<uuid:strategy_id>/directions\
/<int:direction_id>/goals/<int:goal_id>",
           methods=["DELETE"], strict_slashes=False)
def delete_goal(strategy_id, direction_id, goal_id):
    """Deletes a goal resource for a given goal_id."""
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


# Objective_Resource API.
@app.route("/api/v1/strategies/<uuid:strategy_id>/directions\
/<int:direction_id>/goals/<int:goal_id>/objectives",
           methods=["GET"], strict_slashes=False)
def objectives(strategy_id, direction_id, goal_id):
    """Returns objective resources for a given goal_id."""
    # Checking on the datatypes of the inserted ids.
    if not isinstance(strategy_id, UUID):
        return (jsonify({"error": "Not found"}), 404)
    elif not isinstance(direction_id, int):
        return (jsonify({"error": "Not found"}), 404)
    elif not isinstance(goal_id, int):
        return (jsonify({"error": "Not found"}), 404)

    # Querying on the given ids to Return the objective resources later on.
    stmt = db.select(Objective).join_from(
                Strategy, Direction,
                Strategy.id == Direction.strategy_id).join_from(
                Direction, Goal,
                Direction.id == Goal.direction_id).join_from(
                Goal, Objective,
                Goal.id == Objective.goal_id).where(
                Strategy.id == db.bindparam("strategy_id")).where(
                Direction.id == db.bindparam("direction_id")).where(
                Goal.id == db.bindparam("goal_id"))
    try:
        instances = db.session.execute(stmt,
                                      {"strategy_id": strategy_id,
                                       "direction_id": direction_id,
                                       "goal_id": goal_id}).all()
    except db.exc.NoResultFound:
        return (jsonify({"error": "Not found"}), 404)

    # Converting the Objective objects into a dictionaries to return in
    # JSON format.
    objectives_list = list()
    for instance in instances:
        for obj in instance:
            if isinstance(obj, Objective):
                objectives_list.append(obj.to_dict())

    # Returning the converted Objective objects in JSON format.
    return (jsonify(objectives_list), 200)


@app.route("/api/v1/strategies/<uuid:strategy_id>/directions\
/<int:direction_id>/goals/<int:goal_id>/objectives/<int:objective_id>",
           methods=["GET"], strict_slashes=False)
def get_objective(strategy_id, direction_id, goal_id, objective_id):
    """Returns a objective resource for a given objective_id."""
    # Checking on the datatypes of the inserted ids.
    if not isinstance(strategy_id, UUID):
        return (jsonify({"error": "Not found"}), 404)
    elif not isinstance(direction_id, int):
        return (jsonify({"error": "Not found"}), 404)
    elif not isinstance(goal_id, int):
        return (jsonify({"error": "Not found"}), 404)
    elif not isinstance(objective_id, int):
        return (jsonify({"error": "Not found"}), 404)

    # Querying on the given ids to Return the objective resource later on.
    stmt = db.select(Objective).join_from(
                Strategy, Direction,
                Strategy.id == Direction.strategy_id).join_from(
                Direction, Goal,
                Direction.id == Goal.direction_id).join_from(
                Goal, Objective,
                Goal.id == Objective.goal_id).where(
                Strategy.id == db.bindparam("strategy_id")).where(
                Direction.id == db.bindparam("direction_id")).where(
                Goal.id == db.bindparam("goal_id")).where(
                Objective.id == db.bindparam("objective_id"))
    try:
        instance = db.session.execute(stmt,
                                      {"strategy_id": strategy_id,
                                       "direction_id": direction_id,
                                       "goal_id": goal_id,
                                       "objective_id": objective_id}).one()
    except db.exc.NoResultFound:
        return (jsonify({"error": "Not found"}), 404)

    # Preparing the dictionary data representation of the Objective object.
    for obj in instance:
        objective_dict = obj.to_dict()
    return (jsonify(objective_dict), 200)


@app.route("/api/v1/strategies/<uuid:strategy_id>/directions\
/<int:direction_id>/goals/<int:goal_id>/objectives",
           methods=["POST"], strict_slashes=False)
def create_objective(strategy_id, direction_id, goal_id):
    """Creates an objective resource."""
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
    elif "name" not in list(json_request):
        return ("Missing name", 404)
    elif "start_date" not in list(json_request):
        return ("Missing start date", 404)
    elif "end_date" not in list(json_request):
        return ("Missing end date", 404)
    elif "kpi_value" not in list(json_request):
        return ("Missing KPI value", 404)
    elif "kpi_id" not in list(json_request):
        return ("Missing kpi's id", 404)
    elif "goal_id" not in list(json_request):
        return ("Missing goal's id", 404)

    objective_goal = json_request["goal_id"]
    objective_name = json_request["name"]
    objective_start = json_request["start_date"]
    objective_end = json_request["end_date"]
    objective_kpi_id = json_request["kpi_id"]
    objective_kpi = json_request["kpi_value"]

    # Querying on the given strategy_id to Update its update_date later.
    stmt = db.select(Strategy).where(
                Strategy.id == db.bindparam("strategies_id"))
    try:
        instance = db.session.execute(stmt,
                                      {"strategies_id": strategy_id}).one()
    except db.exc.NoResultFound:
        return (jsonify({"error": "Not found"}), 404)

    # Creating the Objective object and getting dictionary data representation.
    objective = Objective(goal_id=objective_goal,
                          name=objective_name,
                          start_date=objective_start,
                          end_date=objective_end,
                          kpi_id=objective_kpi_id,
                          kpi_value=objective_kpi)
    objective_dict = objective.to_dict()

    # Updating the update_date attribute in the Strategy object.
    for obj in instance:
        setattr(obj, "update_date", datetime.utcnow())

    # Adding the Objective object in the database and commiting.
    try:
        db.session.add(objective)
        db.session.commit()
    except db.exc.IntegrityError:
        return ("Wrong input", 404)

    # Giving the Objective object the id generated in database and returning JSON.
    objective_dict["id"] = objective.id
    return (jsonify(objective_dict), 201)


@app.route("/api/v1/strategies/<uuid:strategy_id>/directions\
/<int:direction_id>/goals/<int:goal_id>/objectives/<int:objective_id>",
           methods=["PUT"], strict_slashes=False)
def update_objective(strategy_id, direction_id, goal_id, objective_id):
    """Updates an objective resource for a given objective_id."""
    # Checking on the datatypes of the inserted ids.
    if not isinstance(strategy_id, UUID):
        return (jsonify({"error": "Not found"}), 404)
    elif not isinstance(direction_id, int):
        return (jsonify({"error": "Not found"}), 404)
    elif not isinstance(goal_id, int):
        return (jsonify({"error": "Not found"}), 404)
    elif not isinstance(objective_id, int):
        return (jsonify({"error": "Not found"}), 404)

    # Checking on the JSON inputs in the request sent.
    json_request = request.get_json()
    if json_request is None:
        return (jsonify({"error": "Not found"}), 404)

    # Querying on the given ids to Return the objective resource later on.
    stmt = db.select(Objective, Strategy).join_from(
                Strategy, Direction,
                Strategy.id == Direction.strategy_id).join_from(
                Direction, Goal,
                Direction.id == Goal.direction_id).join_from(
                Goal, Objective,
                Goal.id == Objective.goal_id).where(
                Strategy.id == db.bindparam("strategy_id")).where(
                Direction.id == db.bindparam("direction_id")).where(
                Goal.id == db.bindparam("goal_id")).where(
                Objective.id == db.bindparam("objective_id"))
    try:
        instance = db.session.execute(stmt,
                                      {"strategy_id": strategy_id,
                                       "direction_id": direction_id,
                                       "goal_id": goal_id,
                                       "objective_id": objective_id}).one()
    except db.exc.NoResultFound:
        return (jsonify({"error": "Not found"}), 404)

    # Updating the Objective object according to the allowed list fields.
    allowed_list = ["name", "start_date", "end_date",
                    "goal_id", "kpi_id", "kpi_value"]
    update_status = False
    for obj in instance:
        for key, value in json_request.items():
            if isinstance(obj, Objective) and key in allowed_list:
                setattr(obj, key, value)
                update_status = True
            elif isinstance(obj, Strategy) and update_status:
                setattr(obj, "update_date", datetime.utcnow())
        if isinstance(obj, Objective):
            objective_dict = obj.to_dict()

    # Saving the updates done to the object and returning it.
    db.session.commit()
    return (jsonify(objective_dict), 200)


@app.route("/api/v1/strategies/<uuid:strategy_id>/directions\
/<int:direction_id>/goals/<int:goal_id>/objectives/<int:objective_id>",
           methods=["DELETE"], strict_slashes=False)
def delete_objective(strategy_id, direction_id, goal_id, objective_id):
    """Deletes an objective resource for a given objective_id."""
    # Checking on the datatypes of the inserted ids.
    if not isinstance(strategy_id, UUID):
        return (jsonify({"error": "Not found"}), 404)
    elif not isinstance(direction_id, int):
        return (jsonify({"error": "Not found"}), 404)
    elif not isinstance(goal_id, int):
        return (jsonify({"error": "Not found"}), 404)
    elif not isinstance(objective_id, int):
        return (jsonify({"error": "Not found"}), 404)

    # Querying on the given ids to Return the objective resource later on.
    stmt = db.select(Objective, Strategy).join_from(
                Strategy, Direction,
                Strategy.id == Direction.strategy_id).join_from(
                Direction, Goal,
                Direction.id == Goal.direction_id).join_from(
                Goal, Objective,
                Goal.id == Objective.goal_id).where(
                Strategy.id == db.bindparam("strategy_id")).where(
                Direction.id == db.bindparam("direction_id")).where(
                Goal.id == db.bindparam("goal_id")).where(
                Objective.id == db.bindparam("objective_id"))
    try:
        instance = db.session.execute(stmt,
                                      {"strategy_id": strategy_id,
                                       "direction_id": direction_id,
                                       "goal_id": goal_id,
                                       "objective_id": objective_id}).one()
    except db.exc.NoResultFound:
        return (jsonify({"error": "Not found"}), 404)

    # Deleting the Objective object according to the returned query object.
    delete_status = False
    for obj in instance:
        if isinstance(obj, Objective):
            db.session.delete(obj)
            delete_status = True
        elif isinstance(obj, Strategy) and delete_status:
            setattr(obj, "update_date", datetime.utcnow())

    # Saving the delete operation done to the object and returning empty dict.
    db.session.commit()
    return (jsonify({}), 200)


# Datatype_Resource API.
@app.route("/api/v1/datatypes", methods=["GET"], strict_slashes=True)
def datatypes():
    """Returns a collection of Datatype resources."""
    stmt = db.select(Datatype)
    instances = db.session.execute(stmt).all()
    if not instances:
        return (jsonify({"error": "Not found"}), 404)
    records = list()
    for instance in instances:
        for obj in instance:
            records.append(obj.to_dict())
    return (jsonify(records), 200)


@app.route("/api/v1/datatypes/<int:datatype_id>", methods=["GET"],
           strict_slashes=False)
def get_datatype(datatype_id):
    """Returns a Datatype resource for a given datatype_id."""
    if not isinstance(datatype_id, int):
        return (jsonify({"error": "Not found"}), 404)
    stmt = db.select(Datatype).where(
        Datatype.id == db.bindparam("datatype_id"))
    try:
        instance = db.session.execute(stmt,
                                      {"datatype_id": datatype_id}).one()
    except db.exc.NoResultFound:
        return (jsonify({"error": "Not found"}), 404)

    for obj in instance:
        record = obj.to_dict()
    return (jsonify(record), 200)


# Kpi_Resource API.
@app.route("/api/v1/strategies/<uuid:strategies_id>/kpis", methods=["GET"], strict_slashes=True)
def kpis(strategies_id):
    """Returns a collection of Kpi resources."""
    if not isinstance(strategies_id, UUID):
        return (jsonify({"error": "Not found"}), 404)
    stmt = db.select(Kpi)
    instances = db.session.execute(stmt).all()
    if not instances:
        return (jsonify({"error": "Not found"}), 404)
    records = list()
    for instance in instances:
        for obj in instance:
            records.append(obj.to_dict())
    return (jsonify(records), 200)


@app.route("/api/v1/strategies/<uuid:strategies_id>/kpis",
           methods=["POST"], strict_slashes=True)
def create_kpi(strategies_id):
    """Creates a collection of Kpi resources."""
    if not isinstance(strategies_id, UUID):
        return (jsonify({"error": "Not found"}), 404)
    json_request = request.get_json()
    if json_request is None:
        return (jsonify({"error": "Not found"}), 404)
    elif "name" not in list(json_request):
        return (jsonify({"error": "Not found"}), 404)
    elif "definition" not in list(json_request):
        return (jsonify({"error": "Not found"}), 404)
    elif "datatype_id" not in list(json_request):
        return (jsonify({"error": "Not found"}), 404)

    kpi_name = json_request["name"]
    kpi_def = json_request["definition"]
    kpi_datatype_id = json_request["datatype_id"]
    kpi = Kpi(name=kpi_name,
          definition=kpi_def,
          datatype_id=kpi_datatype_id)

    if not kpi:
        return (jsonify({"error": "Not found"}), 404)
    kpi_dict = kpi.to_dict()
    db.session.add(kpi)
        
    stmt = db.select(Strategy).where(
        Strategy.id == db.bindparam("strategy_id"))
    instance = db.session.execute(stmt,
                                  {"strategy_id": strategies_id}).one()
    for obj in instance:
        obj.update_date = datetime.utcnow()
    db.session.commit()
    kpi_dict["id"] = kpi.id
    return (jsonify(kpi_dict), 201)


@app.route("/api/v1/strategies/<uuid:strategies_id>/kpis/<int:kpi_id>",
           methods=["GET"], strict_slashes=False)
def get_kpi(strategies_id, kpi_id):
    """Returns a Kpi resource for a given kpi_id."""
    if not isinstance(strategies_id, UUID):
        return (jsonify({"error": "Not found"}), 404)
    elif not isinstance(kpi_id, int):
        return (jsonify({"error": "Not found"}), 404)
    stmt = db.select(Kpi).where(
                    Kpi.id == db.bindparam("kpi_id"))
    try:
        instance = db.session.execute(stmt,
                                      {"kpi_id": kpi_id,}).one()
    except db.exc.NoResultFound:
        return (jsonify({"error": "Not found"}), 404)

    for obj in instance:
        record_dict = obj.to_dict()
    return (jsonify(record_dict), 200)


@app.route("/api/v1/strategies/<uuid:strategies_id>/kpis/<int:kpi_id>",
           methods=["PUT"], strict_slashes=False)
def update_kpi(strategies_id, kpi_id):
    """Updates a Kpi resource for a given kpi_id."""
    if not isinstance(strategies_id, UUID):
        return (jsonify({"error": "Not found"}), 404)
    elif not isinstance(kpi_id, int):
        return (jsonify({"error": "Not found"}), 404)
    json_request = request.get_json()
    if json_request is None:
        return (jsonify({"error": "Not found"}), 404)
    stmt_1 = db.select(Kpi).where(
                    Kpi.id == db.bindparam("kpi_id"))
    stmt_2 = db.select(Strategy).where(
                    Strategy.id == db.bindparam("strategies_id"))

    try:
        kpi_instance = db.session.execute(stmt_1,
                                      {"kpi_id": kpi_id}).one()
        strategy_instance = db.session.execute(stmt_2,
                                      {"strategies_id": strategies_id}).one()

    except db.exc.NoResultFound:
        return (jsonify({"error": "Not found"}), 404)
    allowed_list = ["name", "definition", "datatype_id"]
    update_status = False
    for kpi in kpi_instance:
        for key, value in json_request.items():
            if isinstance(kpi, Kpi) and key in allowed_list:
                setattr(kpi, key, value)
                update_status = True
        kpi_dict = kpi.to_dict()
    if update_status:
        for strategy in strategy_instance:
            strategy.update_date = datetime.utcnow()
    db.session.commit()
    return (jsonify(kpi_dict), 200)


@app.route("/api/v1/strategies/<uuid:strategies_id>/kpis/<int:kpi_id>",
methods=["DELETE"], strict_slashes=False)
def delete_kpi(strategies_id, kpi_id):
    """Deletes a Kpi resource for a given kpi_id."""
    if not isinstance(strategies_id, UUID):
        return (jsonify({"error": "Not found"}), 404)
    elif not isinstance(kpi_id, int):
        return (jsonify({"error": "Not found"}), 404)

    stmt_1 = db.select(Kpi).where(
                    Kpi.id == db.bindparam("kpi_id"))
    stmt_2 = db.select(Strategy).where(
                    Strategy.id == db.bindparam("strategies_id"))
    try:
        kpi_instance = db.session.execute(stmt_1,
                                      {"kpi_id": kpi_id}).one()
        strategy_instance = db.session.execute(stmt_2,
                                      {"strategies_id": strategies_id}).one()
    except db.exc.NoResultFound:
        return (jsonify({"error": "Not found"}), 404)

    update_status = True
    for kpi_obj in kpi_instance:
        db.session.delete(kpi_obj)
    if update_status:
        for strategy_obj in strategy_instance:
            strategy_obj.update_date = datetime.utcnow()
    db.session.commit()
    return ({}, 200)


if __name__ == "__main__":
    app.run(debug=True)
