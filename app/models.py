#!/usr/bin/python3
"""models Module."""


from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from typing import Optional, List
from uuid import UUID, uuid4


class Base(DeclarativeBase):
    """Class Base to represent the SQLAlchemy DeclarativeBase."""
    pass


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
    framework_id: Mapped[UUID] = mapped_column(db.ForeignKey("framework.id"))
    framework: Mapped["Framework"] = db.relationship(
                                        back_populates="strategies")
    directions: Mapped[List["Direction"]] = db.relationship(
                                        back_populates="strategy")

    def __init__(self, name="Untitled", created_by="Untitled"):
        """Initializing the default values of Strategy's record"""
        self.id = uuid4()
        self.creation_date = datetime.utcnow()
        self.update_date = self.creation_date
        self.name = name
        self.created_by = created_by

    def __str__(self):
        """A string representation to the Strategy Class when printed."""
        return f"{self.id}\n{self.name}\n{self.creation_date}\n"\
               f"{self.update_date}\n{self.created_by}"


class Framework(db.Model):
    """Class Framework defines the framework that the strategy follows."""
    __tablename__ = "framework"
    id: Mapped[UUID] = mapped_column(db.Uuid, primary_key=True,
                                     unique=True, nullable=False)
    name: Mapped[str] = mapped_column(db.String(64), nullable=False)
    strategies: Mapped[List["Strategy"]] = db.relationship(
                                                back_populates="framework")

    def __init__(self, name="Untitled"):
        """Initializing the default values of Framework's record."""
        self.id = uuid4()
        self.name = name

    def __str__(self):
        """A string representation to the Framwork Class when printed."""
        return f"{self.id}\n{self.name}"


class Direction(db.Model):
    """Class Direction that defines the general strategy theme."""
    __tablename__ = "direction"
    id: Mapped[UUID] = mapped_column(db.Uuid, primary_key=True,
                                     unique=True, nullable=False)
    name: Mapped[str] = mapped_column(db.String(128), nullable=False,
                                      default="Untitled")
    definition: Mapped[Optional[str]] = mapped_column(db.String(1024),
                                                      nullable=True)
    result: Mapped[str] = mapped_column(db.String(1024), nullable=False)
    strategy_id: Mapped[UUID] = mapped_column(db.ForeignKey("strategy.id"))
    strategy: Mapped["Strategy"] = db.relationship(back_populates="directions")

    def __init__(self, name="Untitled"):
        """Initializing the default values of Direction's record."""
        self.id = uuid4()
        self.name = name

    def __str__(self):
        """A string representation to the Direction Class when printed."""
        return f"{self.id}\n{self.name}\n{self.definition}\n{self.result}"
