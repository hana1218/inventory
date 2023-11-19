"""
Test cases for Inventory Model

"""
import os
import logging
import unittest
from datetime import date
from service.models import Inventory, db, Condition
from service import app

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/testdb"
)


######################################################################
#  INVENTORY   M O D E L   T E S T   C A S E S
######################################################################
# pylint: disable=too-many-public-methods
class TestProductModel(unittest.TestCase):
    """Test Cases for Inventory Model"""

    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        Inventory.init_db(app)

    @classmethod
    def tearDownClass(cls):
        """This runs once after the entire test suite"""
        db.session.close()

    def setUp(self):
        """This runs before each test"""
        db.session.query(Inventory).delete()  # clean up the last tests
        db.session.commit()

    def tearDown(self):
        """This runs after each test"""
        db.session.remove()

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_create_a_product(self):
        """Test constructor of Inventory class. It should Create a product and assert that it exists."""
        product = Inventory(
            id=5,
            name="computer",
            quantity=3,
            restock_level=10,
            restock_count=20,
            condition=Condition.NEW,
            first_entry_date=date(2011, 2, 2),
            last_restock_date=date(2011, 2, 2),
        )

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

        product = Inventory(
            id=5,
            name="computer",
            quantity=3,
            restock_level=1,
            restock_count=2,
            condition=Condition.OPEN_BOX,
            first_entry_date=date(2011, 2, 2),
            last_restock_date=date(2011, 2, 2),
        )

        self.assertEqual(str(product), "<Product 5 id=[5]>")
        self.assertTrue(product is not None)
        self.assertEqual(product.id, 5)
        self.assertEqual(product.name, "computer")
        self.assertEqual(product.quantity, 3)
        self.assertEqual(product.restock_level, 1)
        self.assertEqual(product.restock_count, 2)
        self.assertEqual(product.condition, Condition.OPEN_BOX)
        self.assertEqual(product.first_entry_date, date(2011, 2, 2))
        self.assertEqual(product.last_restock_date, date(2011, 2, 2))

    def test_create_default(self):
        """Test creating an item using not all fields of constructor
        Upon create(), missing fields should be set to default"""
        product = Inventory(id=6)
        product.create()
        self.assertEqual(product.restock_level, 0)
        self.assertIsNone(product.name)
        self.assertEqual(product.quantity, 0)
        self.assertEqual(product.restock_count, 0)
        self.assertEqual(product.condition, Condition.NEW)
        self.assertEqual(product.first_entry_date, date.today())
        self.assertEqual(product.last_restock_date, date.today())

    def test_insert_item(self):
        """Test insert an item into the database"""
        item = Inventory(
            id=114,
            name="unicorn tear",
            quantity=514,
            restock_level=8,
            restock_count=11,
            condition=Condition.NEW,
            first_entry_date=date(2019, 1, 3),
            last_restock_date=date(2019, 10, 16),
        )
        item.create()

        # Insert one item and it should be retrievable
        product = Inventory.find(114)
        self.assertEqual(str(product), "<Product 114 id=[114]>")
        self.assertTrue(product is not None)
        self.assertEqual(product.id, 114)
        self.assertEqual(product.name, "unicorn tear")
        self.assertEqual(product.quantity, 514)
        self.assertEqual(product.restock_level, 8)
        self.assertEqual(product.restock_count, 11)
        self.assertEqual(product.condition, Condition.NEW)
        self.assertEqual(product.first_entry_date, date(2019, 1, 3))
        self.assertEqual(product.last_restock_date, date(2019, 10, 16))

        # Insert another item and the two items should both be retrievable
        other_item = Inventory(
            id=1,
            name="werewolf hair",
            quantity=628,
            restock_level=8,
            restock_count=12,
            condition=Condition.OPEN_BOX,
            first_entry_date=date(2012, 4, 3),
            last_restock_date=date(2017, 9, 21),
        )
        other_item.create()
        product = Inventory.find(114)
        self.assertTrue(product is not None)
        self.assertEqual(product.name, "unicorn tear")
        other_product = Inventory.find(1)
        self.assertTrue(other_product is not None)
        self.assertEqual(other_product.name, "werewolf hair")

    def test_update_item(self):
        """Test inserting an item and then update it"""
        # self.setUp()
        product = Inventory(
            id=3,
            name="reverse bear trap",
            quantity=3,
            restock_level=10,
            restock_count=6,
            condition=Condition.USED,
            first_entry_date=date(2004, 10, 31),
            last_restock_date=date(2010, 10, 31),
        )
        product.create()
        item = Inventory.find(114)
        self.assertTrue(item is None)
        item = Inventory.find(3)
        self.assertTrue(item is not None)

        # updates on this item
        item.name = "water cube"
        item.quantity = 1
        item.first_entry_date = date(2008, 10, 31)
        item.update()

        new_item = Inventory.find(3)
        self.assertTrue(new_item is not None)
        self.assertEqual(new_item.id, 3)
        self.assertEqual(new_item.name, "water cube")
        self.assertEqual(new_item.quantity, 1)
        self.assertEqual(new_item.first_entry_date, date(2008, 10, 31))
        self.assertEqual(new_item.restock_level, 10)
        self.assertEqual(new_item.restock_count, 6)
        self.assertEqual(new_item.condition, Condition.USED)
        self.assertEqual(new_item.last_restock_date, date(2010, 10, 31))

    def test_delete_item(self):
        """Test delete an item from database"""
        prod_1 = Inventory(
            id=1,
            name="reverse bear trap",
            quantity=3,
            restock_level=10,
            restock_count=6,
            condition=Condition.USED,
            first_entry_date=date(2004, 10, 31),
            last_restock_date=date(2010, 10, 31),
        )
        prod_2 = Inventory(
            id=2,
            name="venus fly trap",
            quantity=1,
            restock_level=5,
            restock_count=2,
            condition=Condition.OPEN_BOX,
            first_entry_date=date(2005, 10, 31),
            last_restock_date=date(2005, 10, 31),
        )
        prod_3 = Inventory(
            id=3,
            name="shotgun collar",
            quantity=1,
            restock_level=1,
            restock_count=2,
            condition=Condition.USED,
            first_entry_date=date(2006, 10, 31),
            last_restock_date=date(2017, 10, 31),
        )
        prod_1.create()
        prod_2.create()
        prod_3.create()
        item_1 = Inventory.find(1)
        item_2 = Inventory.find(2)
        item_3 = Inventory.find(3)
        self.assertTrue(item_1 is not None)
        self.assertTrue(item_2 is not None)
        self.assertTrue(item_3 is not None)

        prod_2.delete()
        item_1 = Inventory.find(1)
        item_2 = Inventory.find(2)
        item_3 = Inventory.find(3)
        self.assertTrue(item_1 is not None)
        self.assertTrue(item_2 is None)
        self.assertTrue(item_3 is not None)

        prod_1.delete()
        item_1 = Inventory.find(1)
        item_2 = Inventory.find(2)
        item_3 = Inventory.find(3)
        self.assertTrue(item_1 is None)
        self.assertTrue(item_2 is None)
        self.assertTrue(item_3 is not None)

        item_3.delete()
        item_1 = Inventory.find(1)
        item_2 = Inventory.find(2)
        item_3 = Inventory.find(3)
        self.assertTrue(item_1 is None)
        self.assertTrue(item_2 is None)
        self.assertTrue(item_3 is None)

    def test_get_by_name(self):
        """Test getting all items of the same name"""
        prod1 = Inventory(id=1, name="NFA flag", quantity=3)
        prod2 = Inventory(id=2, name="NFA flag", quantity=6)
        prod3 = Inventory(id=3, name="NFA flag", quantity=9)

        prod11 = Inventory(id=11, name="billy puppet", quantity=0)
        prod22 = Inventory(id=22, name="billy the puppet", quantity=1)

        prod1.create()
        prod2.create()
        prod3.create()
        prod11.create()
        prod22.create()

        flags = Inventory.find_by_name("NFA flag")
        i = 0
        for flag in flags:
            self.assertEqual(flag.name, "NFA flag")
            i += 1
        self.assertEqual(i, 3)

        billy = Inventory.find_by_name("billy the puppet")
        for bill in billy:
            self.assertEqual(bill.id, 22)

        gators = Inventory.find_by_name("gator")
        self.assertTrue(gators, None)

    def test_get_all(self):
        """List all items in database"""
        prod_1 = Inventory(
            id=1,
            name="reverse bear trap",
            quantity=3,
            restock_level=10,
            restock_count=6,
            condition=Condition.USED,
            first_entry_date=date(2004, 10, 31),
            last_restock_date=date(2010, 10, 31),
        )
        prod_2 = Inventory(
            id=2,
            name="venus fly trap",
            quantity=1,
            restock_level=5,
            restock_count=2,
            condition=Condition.OPEN_BOX,
            first_entry_date=date(2005, 10, 31),
            last_restock_date=date(2005, 10, 31),
        )
        prod_3 = Inventory(
            id=3,
            name="shotgun collar",
            quantity=1,
            restock_level=1,
            restock_count=2,
            condition=Condition.USED,
            first_entry_date=date(2006, 10, 31),
            last_restock_date=date(2017, 10, 31),
        )
        prod_1.create()
        prod_2.create()
        prod_3.create()
        all_items = Inventory.all()
        i = 0
        for item in all_items:
            self.assertIsNotNone(item)
            i += 1
        self.assertEqual(i, 3)

    def test_deserialize(self):
        """Input a dict and try to deserialize it into an item"""

        data_full = {
            "id": 1,
            "name": "full",
            "quantity": 1,
            "restock_level": 2,
            "restock_count": 2,
            "condition": "NEW",
            "first_entry_date": "2013-11-22",
            "last_restock_date": "2015-02-03",
        }
        item_1 = Inventory(id=1)
        item_2 = Inventory(id=11)
        item_1.deserialize(data_full)
        self.assertEqual(item_1.name, "full")
        self.assertEqual(item_1.quantity, 1)
        self.assertEqual(item_1.restock_level, 2)
        self.assertEqual(item_1.restock_count, 2)
        self.assertEqual(item_1.condition, Condition.NEW)
        self.assertEqual(item_1.first_entry_date, date(2013, 11, 22))
        self.assertEqual(item_1.last_restock_date, date(2015, 2, 3))

        # item_2.deserialize(data_full)
        # self.assertEqual(item_2.id, 1)
        # self.assertRaises(DataValidationError)

        data_unnamed = {
            "id": 11,
            "quantity": 1,
            "restock_level": 2,
            "restock_count": 2,
            "condition": "NEW",
            "first_entry_date": "2013-11-22",
            "last_restock_date": "2015-02-03",
        }
        item_2.deserialize(data_unnamed)
        self.assertIsNone(item_2.name)

        # data_bad = {"id": 1111, "name": "bad", "quantity": "bad quantity", "restock_level": 2, \
        #    "restock_count": 2, "condition": "NEW", "first_entry_date": "2013-11-22", "last_restock_date": "2015-02-03"}
        # item_4 = Inventory(id = 1111)
        # item_4.deserialize(data_bad)
        # self.assertRaises(DataValidationError)

        # item_3 = Inventory(id = 111)
        # data_miss = {"id": 111, "restock_count": 2, "condition": "NEW"}
        # item_3.deserialize(data_miss)
        # self.assertRaises(DataValidationError)

    def test_find_by_queries(self):
        """It should Find inventory items by multiple fields"""
        prod_1 = Inventory(
            id=1,
            name="reverse bear trap",
            quantity=3,
            restock_level=10,
            restock_count=6,
            condition=Condition.USED,
            first_entry_date=date(2004, 10, 31),
            last_restock_date=date(2010, 10, 31),
        )
        prod_2 = Inventory(
            id=2,
            name="venus fly trap",
            quantity=1,
            restock_level=5,
            restock_count=2,
            condition=Condition.OPEN_BOX,
            first_entry_date=date(2005, 10, 31),
            last_restock_date=date(2005, 10, 31),
        )
        prod_3 = Inventory(
            id=3,
            name="shotgun collar",
            quantity=1,
            restock_level=1,
            restock_count=2,
            condition=Condition.USED,
            first_entry_date=date(2006, 10, 31),
            last_restock_date=date(2017, 10, 31),
        )
        prod_1.create()
        prod_2.create()
        prod_3.create()
        name = Inventory.find_by_queries(name="reverse bear trap")
        for i in name:
            self.assertEqual(i.id, 1)
        conditions = Inventory.find_by_queries(condition="USED")
        i = 0
        for condition in conditions:
            self.assertEqual(condition.condition.name, "USED")
            i += 1
        self.assertEqual(i, 2)
        quantities = Inventory.find_by_queries(quantity="1")
        i = 0
        for quantity in quantities:
            self.assertEqual(quantity.quantity, 1)
            i += 1
        self.assertEqual(i, 2)
