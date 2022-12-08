from boto3 import client, resource
from aws_lambda_powertools.event_handler import api_gateway
from aws_lambda_powertools.event_handler import APIGatewayHttpResolver
from aws_lambda_powertools.event_handler import exceptions
import os

app = api_gateway.ApiGatewayResolver(
    proxy_type=api_gateway.ProxyEventType.APIGatewayProxyEventV2
)

table_name = os.environ["DYNAMODB_TABLE_NAME"]

ddb_resource = resource("dynamodb")
ddb_user_table = ddb_resource.Table(table_name)


def lambda_handler(event, context):
    print("event: ", event)
    return app.resolve(event, context)


@app.post("/users")
def create_user():
    user_attributes = app.current_event.json_body
    print("user_attributes: ", user_attributes)
    username = user_attributes["username"]
    user = ddb_user_table.get_item(Key={"username": str(username)})
    print("user", user, type(user))
    del user["ResponseMetadata"]
    if bool(user):
        raise exceptions.BadRequestError(f"User {username} already exists")

    created_user = ddb_user_table.put_item(Item=user_attributes)
    print("created_user", created_user)
    return {"msg": "user created", "response": created_user}


@app.put("/users/<username>")
def update_user(username: str):
    if username is None:
        raise exceptions.NotFoundError(f"Invalid request")
    user_attributes = app.current_event.json_body
    user = ddb_user_table.get_item(Key={"username": str(username)})
    del user["ResponseMetadata"]
    if not bool(user):
        raise exceptions.NotFoundError(f"User {username} does not exist")
    updated_user = ddb_user_table.put_item(Item=user_attributes)
    return {"msg": "user updated", "response": updated_user}


@app.get("/users/<username>")
def get_user(username: str):
    print("username: ", username)
    user = ddb_user_table.get_item(Key={"username": str(username)})
    print("user:", user, bool(user))
    del user["ResponseMetadata"]
    if not bool(user):
        raise exceptions.NotFoundError(f"User {username} does not exist")
    return user


@app.delete("/users/<username>")
def delete_user(username: str):
    user = ddb_user_table.get_item(Key={"username": str(username)})
    del user["ResponseMetadata"]
    if not bool(user):
        raise exceptions.NotFoundError(f"User {username} does not exist")
    deleted_user = ddb_user_table.delete_item(Key={"username": str(username)})
    return {"msg": "user deleted", "response": deleted_user}
