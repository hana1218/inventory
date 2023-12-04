"""
My Service

Describe what your service does here
"""

from datetime import datetime
from flask import jsonify, request, abort
from flask_restx import Resource, fields
from service.common import status  # HTTP Status Codes
from service.models import Inventory, Condition

# Import Flask application
from . import app, api


############################################################
# Health Endpoint
############################################################
@app.route("/health")
def health():
    """Health Status"""
    return jsonify(status="OK"), status.HTTP_200_OK


######################################################################
# Configure the Root route before OpenAPI
######################################################################

@app.route("/")
def index():
    # """Root URL response"""
    # return (
    #     jsonify(
    #         name="Inventory Demo REST API Service",
    #         version="1.0",
    #         paths=url_for("list_products", _external=True),
    #     ),
    #     status.HTTP_200_OK,
    # )
    """Base URL for our service"""
    return app.send_static_file("index.html")

# Define the model so that the docs reflect what can be sent


inventory_model = api.model(
    "Inventory",
    {
        "id": fields.Integer(required=True, description="The ID of the Inventory"),
        "name": fields.String(required=True, description="The name of the Inventory"),
        "quantity": fields.Integer(
            required=True, description="The quantity of the Inventory"
        ),
        "restock_level": fields.Integer(
            required=True, description="The restock level of the Inventory"
        ),
        "restock_count": fields.Integer(
            required=True, description="The restock count of the Inventory"
        ),
        # pylint: disable=protected-access
        "condition": fields.String(
            enum=Condition._member_names_,
            description="The condition of the inventory item (NEW, USED, OPEN_BOX)",
        ),
        "first_entry_date": fields.Date(
            required=True, description="The first entry date of the inventory"
        ),
        "last_restock_date": fields.Date(
            required=True, description="The last restock date of the inventory"
        ),
    },
)

# inventory_model = api.inherit(
#     "InventoryModel",
#     create_model,
#     {
#         "id": fields.String(
#             readOnly=True, description="The unique id assigned internally by service"
#         ),
#     },
# )

######################################################################
#  PATH: /Inventory/{id}
######################################################################


@api.route("/inventory/<iid>")
@api.param("iid", "The inventory identifier")
class InventoryResource(Resource):

    """
    InventoryResource class

    Allows the manipulation of a single inventory item
    GET /inventory{id} - Returns an item with the id
    PUT /inventory{id} - Update an item with the id
    DELETE /inventory{id} -  Deletes an item with the id
    """

    # ------------------------------------------------------------------
    # RETRIEVE A INVENTORY
    # ------------------------------------------------------------------
    @api.doc("get_inventory")
    @api.response(404, "Item not found")
    @api.marshal_with(inventory_model)
    def get(self, iid):
        """Gets a product with specified id"""
        app.logger.info("Request to get product with id %s...", iid)
        ans = Inventory.find(iid)
        if ans is None:
            abort(status.HTTP_404_NOT_FOUND, f"Product {iid} does not exist")
        app.logger.info("Returning: product %s...", iid)
        return ans.serialize(), status.HTTP_200_OK

    # ------------------------------------------------------------------
    # UPDATE AN EXISTING INVENTORY
    # ------------------------------------------------------------------
    @api.doc("update_inventory")
    @api.response(404, "Inventory not found")
    @api.response(400, "The posted Inventory data was not valid")
    @api.expect(inventory_model)
    @api.marshal_with(inventory_model)
    def put(self, iid):
        """
        Update a product

        This endpoint will update a product based the body that is posted
        """
        app.logger.info("Request to update product with id: %s", iid)
        check_content_type("application/json")

        product = Inventory.find(iid)
        if not product:
            abort(status.HTTP_404_NOT_FOUND, f"Product with id '{iid}' was not found.")

        product.deserialize(request.get_json())
        product.id = iid  # to undo deserialize's id field, so update won't change id
        product.update()

        app.logger.info("Product with ID [%s] updated.", product.id)
        return product.serialize(), status.HTTP_200_OK

    # ------------------------------------------------------------------
    # DELETE A INVENTORY
    # ------------------------------------------------------------------
    @api.doc("delete_inventory_id")
    @api.response(204, "Inventory deleted")
    def delete(self, iid):
        """Delete a product from the inventory"""
        app.logger.info("Request to delete product with id: %s", iid)

        product = Inventory.find(iid)
        if not product:
            return "", status.HTTP_204_NO_CONTENT

        product.delete()

        app.logger.info("Product with ID [%s] deleted.", iid)
        return "", status.HTTP_204_NO_CONTENT


######################################################################
#  PATH: /inventory
######################################################################
@api.route("/inventory", strict_slashes=False)
class InventoryCollection(Resource):
    """Handles all interactions with collections of Inventory"""

    # ------------------------------------------------------------------
    # LIST ALL INVENTORY
    # ------------------------------------------------------------------
    @api.doc("list_inventory")
    @api.marshal_list_with(inventory_model)
    def get(self):
        """Retrieves all products from the inventory"""
        app.logger.info("Request to list all products")
        products = Inventory.find_by_queries(**request.args)
        results = [product.serialize() for product in products]
        app.logger.info("Returning %d products", len(results))
        return results, status.HTTP_200_OK

    # ------------------------------------------------------------------
    # ADD A NEW INVENTORY
    # ------------------------------------------------------------------
    @api.doc("create_inventory")
    @api.response(400, "The posted data was not valid")
    @api.expect(inventory_model)
    @api.marshal_with(inventory_model, code=201)
    def post(self):
        """
        Creates a product into the inventory
        This endpoint will create a product based the data in the body that is posted
        """
        app.logger.info("Request to create a product...")
        product = Inventory()
        app.logger.debug("Payload = %s", api.payload)
        product.deserialize(api.payload)
        if Inventory.find(product.id) is not None:
            abort(status.HTTP_409_CONFLICT, f"Product {product.id} already exists")
        product.create()
        app.logger.info("Product with ID [%s] created.", product.id)
        location_url = api.url_for(InventoryResource, iid=product.id, _external=True)
        return product.serialize(), status.HTTP_201_CREATED, {"Location": location_url}

######################################################################
#  PATH: /inventory/{id}/restock
######################################################################


@api.route("/inventory/<iid>/restock")
@api.param("iid", "The Inventory identifier")
class PurchaseResource(Resource):
    """Restock actions on an item"""
    @api.doc("Restock_inventory")
    @api.response(404, "Inventory not found")
    def put(self, iid):
        """Restocks product with certain id by count or up to level + count"""
        app.logger.info("Request to restock product with id %s...", iid)
        ans = Inventory.find(iid)
        if ans is None:
            abort(status.HTTP_404_NOT_FOUND, f"Product {iid} does not exist")
        cur = ans.quantity
        need = ans.restock_level
        added = 0
        if cur < need:
            added = need - cur
        else:
            added = ans.restock_count
        ans.quantity += added
        # ans.restock_count = added
        ans.last_restock_date = datetime.today()
        app.logger.info("Restock %d units of product %d", added, need)
        ans.update()
        return ans.serialize(), status.HTTP_200_OK


######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################

def check_content_type(content_type):
    """Checks that the media type is correct"""
    if "Content-Type" not in request.headers:
        app.logger.error("No Content-Type specified.")
        abort(
            status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            f"Content-Type must be {content_type}",
        )

    if request.headers["Content-Type"] == content_type:
        return

    app.logger.error("Invalid Content-Type: %s", request.headers["Content-Type"])
    abort(
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        f"Content-Type must be {content_type}",
    )
