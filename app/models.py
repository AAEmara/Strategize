#!/usr/bin/python3
"""models Module."""


from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from typing import Optional, List
from uuid import UUID, uuid4


class Base(DeclarativeBase):
    """Class Base to represent the SQLAlchemy DeclarativeBase."""
    def to_dict(self):
        """Returns a dictionary of an Object."""
        obj_dict = dict()
        for key, value in self.__dict__.items():
            if key == "_sa_instance_state":
                continue
            elif key in ["creation_date", "update_date"]:
                value = value.isoformat()
            obj_dict[key] = value
        return (obj_dict)


db = SQLAlchemy(model_class=Base)


class Strategy(db.Model):
    """Class Strategy that defines general strategy metadata."""
    __tablename__ = "strategy"
    id: Mapped[UUID] = mapped_column(db.Uuid, primary_key=True,
                                     unique=True, nullable=False)
    name: Mapped[str] = mapped_column(db.String(64), nullable=False,
                                      default="Untitled")
    creation_date: Mapped[datetime] = mapped_column(db.DateTime,
                                                    nullable=False)
    update_date: Mapped[datetime] = mapped_column(db.DateTime, nullable=False)
    created_by: Mapped[str] = mapped_column(db.String(128), nullable=False)
    framework_id: Mapped[int] = mapped_column(db.ForeignKey("framework.id"),
                                              default=1)
    framework: Mapped["Framework"] = db.relationship(
                                        back_populates="strategies")
    directions: Mapped[List["Direction"]] = db.relationship(
                                        back_populates="strategy")

    def __init__(self, name="Untitled", created_by="Untitled", fwork=1):
        """Initializing the default values of a Strategy's record"""
        self.id = uuid4()
        self.creation_date = datetime.utcnow()
        self.update_date = self.creation_date
        self.name = name
        self.created_by = created_by

    def __str__(self):
        """A string representation to the Strategy Class when printed."""
        return f"{{'id': {self.id}, 'name': {self.name}, "\
               f"'creation date': {self.creation_date}, "\
               f"'update date': {self.update_date}, "\
               f"'created by': {self.created_by}}}"


class Framework(db.Model):
    """Class Framework defines the framework that the strategy follows."""
    __tablename__ = "framework"
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True,
                                    unique=True, nullable=False)
    name: Mapped[str] = mapped_column(db.String(64), nullable=False)
    strategies: Mapped[List["Strategy"]] = db.relationship(
                                                back_populates="framework")

    def __init__(self, name="Untitled"):
        """Initializing the default values of a Framework's record."""
        self.name = name

    def __str__(self):
        """A string representation to the Framwork Class when printed."""
        return f"{{'id': {self.id}, 'name': {self.name}}}"


class Direction(db.Model):
    """Class Direction that defines the general strategy theme."""
    __tablename__ = "direction"
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True,
                                    unique=True, nullable=False)
    name: Mapped[str] = mapped_column(db.String(128), nullable=False,
                                      default="Untitled")
    definition: Mapped[Optional[str]] = mapped_column(db.String(1024),
                                                      nullable=True)
    result: Mapped[str] = mapped_column(db.String(1024), nullable=False)
    strategy_id: Mapped[UUID] = mapped_column(db.ForeignKey("strategy.id"))
    strategy: Mapped["Strategy"] = db.relationship(back_populates="directions")
    goals: Mapped[List["Goal"]] = db.relationship(back_populates="direction")

    def __init__(self, name="Untitled"):
        """Initializing the default values of a Direction's record."""
        self.name = name

    def __str__(self):
        """A string representation to the Direction Class when printed."""
        return f"{{'id': {self.id}, 'name': {self.name}, "\
               f"'defintion': {self.definition}, 'result': {self.result}}}"


class Goal(db.Model):
    """Class Goal that defines a goal instance in a certain perspective\
    related to a specific direction or a strategic theme."""
    __tablename__ = "goal"
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True,
                                    unique=True, nullable=False)
    name: Mapped[str] = mapped_column(db.String(256), nullable=False,
                                      default="Untitled")
    note: Mapped[Optional[str]] = mapped_column(db.String(1024), nullable=True)
    direction_id: Mapped[int] = mapped_column(db.ForeignKey("direction.id"))
    direction: Mapped["Direction"] = db.relationship(back_populates="goals")
    perspective_id: Mapped[UUID] = mapped_column(
                                        db.ForeignKey("perspective.id"))
    perspective: Mapped["Perspective"] = db.relationship(
                                        back_populates="goals")

    def __init__(self, name="Untitled"):
        """Initializing the default values of a Goal's record."""
        self.name = name

    def __str__(self):
        """A string representation to the Goal Class when printed."""
        return f"{{'id': {self.id}, 'name': {self.name}, 'note': {self.note}}}"


class Perspective(db.Model):
    """Class Perspective that defines the main perspective category for\
    a specific strategic goal."""
    __tablename__ = "perspective"
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True,
                                    unique=True, nullable=False)
    name: Mapped[str] = mapped_column(db.String(128), nullable=False)
    goals: Mapped[List["Goal"]] = db.relationship(back_populates="perspective")

    def __str__(self):
        """A string representation to the Perspective Class when printed."""
        return f"{{'id': {self.id}, 'name': {self.name}}}"
