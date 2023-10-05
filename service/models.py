"""
Models for YourResourceModel

All of the models are stored in this module
"""
import logging
from enum import Enum
from flask_sqlalchemy import SQLAlchemy
from datetime import date

logger = logging.getLogger("flask.app")

# Create the SQLAlchemy object to be initialized later in init_db()
db = SQLAlchemy()


# Function to initialize the database
def init_db(app):
    """ Initializes the SQLAlchemy app """
    YourResourceModel.init_db(app)


class DataValidationError(Exception):
    """ Used for an data validation errors when deserializing """

class Condition(Enum):
    """Enumeration of valid product Conditions"""

    NEW = 0
    OPEN_BOX = 1
    USED = 2

class YourResourceModel(db.Model):
    """
    Class that represents a YourResourceModel
    """

    app = None

    # Table Schema
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, nullable=False)
    # default name is product_id
    name = db.Column(db.String(63)) 
    quantity = db.Column(db.Integer, nullable=False)
    restock_level = db.Column(db.Integer, nullable=False, default=0)
    restock_count = db.Column(db.Integer, nullable=False, default=0)
    condition = db.Column(
        db.Enum(Condition), nullable=False, server_default=(Condition.NEW.name)
    )
    first_entry_date = db.Column(db.Date(), nullable=False, default=date.today())
    last_restock_date = db.Column(db.Date(), nullable=False, default=date.today())


    def __repr__(self):
        return f"<YourResourceModel {self.product_id} id=[{self.id}]>"

    def create(self):
        """
        Creates a YourResourceModel to the database
        """
        logger.info("Creating %s", self.product_id)
        self.id = None  # pylint: disable=invalid-name
        db.session.add(self)
        db.session.commit()

    def update(self):
        """
        Updates a YourResourceModel to the database
        """
        logger.info("Saving %s", self.product_id)
        db.session.commit()

    def delete(self):
        """ Removes a YourResourceModel from the data store """
        logger.info("Deleting %s", self.product_id)
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        """ Serializes a YourResourceModel into a dictionary """
        return {"id": self.id, 
                "name": self.name,
                "product_id": self.product_id,
                "quantity":self.quantity, 
                "restock_level":self.restock_level,
                "restock_count":self.restock_count,
                "condition":self.condition,
                "first_entry_date": self.first_entry_date.isoformat(),
                "last_restock_date": self.last_restock_date.isoformat()
                }

    def deserialize(self, data):
        """
        Deserializes a YourResourceModel from a dictionary

        Args:
            data (dict): A dictionary containing the resource data
        """
        try:

            self.product_id = data["product_id"]
            if "name" in data: 
                self.name = data["name"]
            else:
                self.name = self.product_id
            self.quantity = data["quantity"]
            self.restock_level = data["restock_level"]
            self.restock_count = data["restock_count"]
            self.condition = getattr(Condition, data["condition"])
            self.first_entry_date = date.fromisoformat(data["first_entry_date"])
            self.last_restock_date = date.fromisoformat(data["last_restock_date"])
            
        except KeyError as error:
            raise DataValidationError(
                "Invalid YourResourceModel: missing " + error.args[0]
            ) from error
        except TypeError as error:
            raise DataValidationError(
                "Invalid YourResourceModel: body of request contained bad or no data - "
                "Error message: " + error
            ) from error
        return self

    @classmethod
    def init_db(cls, app):
        """ Initializes the database session """
        logger.info("Initializing database")
        cls.app = app
        # This is where we initialize SQLAlchemy from the Flask app
        db.init_app(app)
        app.app_context().push()
        db.create_all()  # make our sqlalchemy tables

    @classmethod
    def all(cls):
        """ Returns all of the YourResourceModels in the database """
        logger.info("Processing all YourResourceModels")
        return cls.query.all()

    @classmethod
    def find(cls, by_id):
        """ Finds a YourResourceModel by it's ID """
        logger.info("Processing lookup for id %s ...", by_id)
        return cls.query.get(by_id)

    @classmethod
    def find_by_name(cls, name):
        """Returns all YourResourceModels with the given name

        Args:
            name (string): the name of the YourResourceModels you want to match
        """
        logger.info("Processing name query for %s ...", name)
        return cls.query.filter(cls.name == name)
