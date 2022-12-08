from boto3 import client, resource
from aws_lambda_powertools.event_handler import api_gateway
from aws_lambda_powertools.event_handler import APIGatewayHttpResolver
from aws_lambda_powertools.event_handler import exceptions
import os
import uuid

app = api_gateway.ApiGatewayResolver(
    proxy_type=api_gateway.ProxyEventType.APIGatewayProxyEventV2
)


table_name = os.environ["DYNAMODB_TABLE_NAME"]


ddb_resource = resource("dynamodb")
ddb_order_table = ddb_resource.Table(table_name)


def lambda_handler(event, context):
    print("event: ", event)
    return app.resolve(event, context)


@app.post("/orders")
def create_order():
    order_attributes = app.current_event.json_body
    print("order_attributes: ", order_attributes)
    orderid = uuid.uuid4()
    order_attributes["orderid"] = str(orderid)
    created_order = ddb_order_table.put_item(Item=order_attributes)
    print("created_order", created_order)
    return {"msg": "order created", "response": created_order}


@app.put("/orders/<orderid>")
def update_order(orderid: str):
    if orderid is None:
        raise exceptions.NotFoundError(f"Invalid request")
    order_attributes = app.current_event.json_body
    order = ddb_order_table.get_item(Key={"orderid": str(orderid)})
    del order["ResponseMetadata"]
    if not bool(order):
        raise exceptions.NotFoundError(f"order does not exist")
    updated_order = ddb_order_table.put_item(Item=order_attributes)
    return {"msg": "order updated", "response": updated_order}


@app.get("/orders/<orderid>")
def get_order(orderid: str):
    print("orderid: ", orderid)
    order = ddb_order_table.get_item(Key={"orderid": str(orderid)})
    print("order:", order)
    del order["ResponseMetadata"]
    if not bool(order):
        raise exceptions.NotFoundError(f"order does not exist")
    return order


@app.delete("/orders/<orderid>")
def delete_order(orderid: str):
    order = ddb_order_table.get_item(Key={"orderid": str(orderid)})
    del order["ResponseMetadata"]
    if not bool(order):
        raise exceptions.NotFoundError(f"order {order} does not exist")
    deleted_order = ddb_order_table.delete_item(Key={"order": str(order)})
    return {"msg": "order deleted", "response": deleted_order}
