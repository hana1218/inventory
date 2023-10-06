"""
TestYourResourceModel API Service Test Suite

Test cases can be run with the following:
  nosetests -v --with-spec --spec-color
  coverage report -m
"""
import os
import logging
from unittest import TestCase
from service import app
from service.models import db, init_db, Inventory
from service.common import status  # HTTP Status Codes
from tests.factories import ProductFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/testdb"
)
BASE_URL = "/inventory"

######################################################################
#  T E S T   C A S E S
######################################################################
# pylint: disable=too-many-public-methods
class TestYourResourceServer(TestCase):
    """ REST API Server Tests """

    @classmethod
    def setUpClass(cls):
        """ This runs once before the entire test suite """
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        # Set up the test database
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        init_db(app)

    @classmethod
    def tearDownClass(cls):
        """ This runs once after the entire test suite """
        db.session.close()

    def setUp(self):
        """ This runs before each test """
        self.client = app.test_client()
        db.session.query(Inventory).delete()  # clean up the last tests
        db.session.commit()

    def tearDown(self):
        """ This runs after each test """
        db.session.remove()

    def _create_products(self, count):
        """Factory method to create products in bulk"""
        products = []
        for _ in range(count):
            test_pet = ProductFactory()
            response = self.client.post(BASE_URL, json=test_pet.serialize())
            self.assertEqual(
                response.status_code, status.HTTP_201_CREATED, "Could not create test pet"
            )
            new_pet = response.get_json()
            test_pet.id = new_pet["id"]
            products.append(test_pet)
        return products

    ######################################################################
    #  P L A C E   T E S T   C A S E S   H E R E
    ######################################################################

    def test_index(self):
        """ It should call the home page """
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_create_product(self):
        """It should Create a new Product"""
        test_product = ProductFactory()
        logging.debug("Test Product: %s", test_product.serialize())
        response = self.client.post(BASE_URL, json=test_product.serialize(),content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Make sure location header is set
        # location = response.headers.get("Location", None)
        # self.assertIsNotNone(location)

        # Check the data is correct
        new_product = response.get_json()
        self.assertEqual(new_product["name"], test_product.name)
        self.assertEqual(new_product["quantity"], test_product.quantity)
        self.assertEqual(new_product["restock_level"], test_product.restock_level)
        self.assertEqual(new_product["restock_count"], test_product.restock_count)
        self.assertEqual(new_product["condition"], test_product.condition.name)
        self.assertEqual(new_product["first_entry_date"], test_product.first_entry_date.isoformat())
        self.assertEqual(new_product["last_restock_date"], test_product.last_restock_date.isoformat())

        # Check that the location header was correct
        # response = self.client.get(location)
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        # new_product = response.get_json()
        # self.assertEqual(new_product["name"], test_product.name)
        # self.assertEqual(new_product["quantity"], test_product.quantity)
        # self.assertEqual(new_product["restock_level"], test_product.restock_level)
        # self.assertEqual(new_product["restock_count"], test_product.restock_count)
        # self.assertEqual(new_product["condition"], test_product.condition)
        # self.assertEqual(new_product["first_entry_date"], test_product.first_entry_date)
        # self.assertEqual(new_product["last_restock_date"], test_product.last_restock_date)