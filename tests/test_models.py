"""
Test cases for Inventory Model

"""
import os
import logging
import unittest
from datetime import date
from service.models import Inventory, DataValidationError, db, Condition
from tests.factories import ProductFactory
from service import app


DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/testdb"
)


######################################################################
#  INVENTORY   M O D E L   T E S T   C A S E S
######################################################################
# pylint: disable=too-many-public-methods
class TestProductModel(unittest.TestCase):
    """ Test Cases for Inventory Model """

    @classmethod
    def setUpClass(cls):
        """ This runs once before the entire test suite """
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        Inventory.init_db(app)

    @classmethod
    def tearDownClass(cls):
        """ This runs once after the entire test suite """
        db.session.close()

    def setUp(self):
        """ This runs before each test """
        db.session.query(Inventory).delete()  # clean up the last tests
        db.session.commit()

    def tearDown(self):
        """ This runs after each test """
        db.session.remove()

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    
    def test_create_a_product(self):
        """It should Create a pet and assert that it exists"""
        product = Inventory(id=5, name="computer", quantity=3, restock_level=10,restock_count=20,
                          condition= Condition.NEW,first_entry_date=date(2011, 2, 2),
                          last_restock_date=date(2011, 2, 2))
        
        self.assertEqual(str(product), "<Product 5 id=[5]>")
        self.assertTrue(product is not None)
        self.assertEqual(product.id, 5)
        self.assertEqual(product.name, "computer")
        self.assertEqual(product.quantity, 3)
        self.assertEqual(product.restock_level, 10)
        self.assertEqual(product.restock_count, 20)
        self.assertEqual(product.condition, Condition.NEW)
        self.assertEqual(product.first_entry_date, date(2011, 2, 2))
        self.assertEqual(product.last_restock_date, date(2011, 2, 2))

        product = Inventory(id=5, name="computer", quantity=3, restock_level=10,restock_count=20,
                          condition= Condition.OPEN_BOX,first_entry_date=date(2011, 2, 2),
                          last_restock_date=date(2011, 2, 2))
        self.assertEqual(product.condition, Condition.OPEN_BOX)

        product = Inventory(id=5, name="computer", quantity=3, restock_level=10,restock_count=20,
                          condition= Condition.USED,first_entry_date=date(2011, 2, 2),
                          last_restock_date=date(2011, 2, 2))
        self.assertEqual(product.condition, Condition.USED)
