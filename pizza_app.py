import json
import bson.errors
from flask import Flask, jsonify, request, make_response
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId
import pika

pizza_app = Flask(__name__)
Mongo_URI = "mongodb://localhost:27017/pizza_house"
pizza_app.config['MONGO_URI'] = Mongo_URI
mongo = PyMongo(pizza_app)


@pizza_app.errorhandler(404)
def notFound(error=None):
    message = {
        "status": 404,
        "message": "Not Found" + request.url
    }
    response = jsonify(message)
    response.status_code = 404
    return response


@pizza_app.route("/welcome", methods=['GET'])
def welcome():
    welcome_message = "Welcome to Pizza House"
    return jsonify(welcome_message)


'''
@pizza_app.route("/order", methods=['POST'])
def acceptOrder():
    __json = request.json
    __order = __json["orders"]
    if request.method == "POST":
        id = mongo.db.orders.insert_one({"orders":__order}).inserted_id
        response = jsonify("Order added successfully")
        response.status_code = 200
        orderID = jsonify({"orderID": str(id), "status": response.status_code})
        return orderID
    else:
        return notFound()
'''


@pizza_app.route('/order', methods=['POST'])
def acceptOrder():
    content = request.json
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='saveOrder')
    channel.basic_publish(exchange='',
                          routing_key='saveOrder',
                          body=str(content))  # sending the order to the message queue
    connection.close()
    return make_response(jsonify("Order Placed!"), 201)


@pizza_app.route("/getorders", methods=["GET"])
def fetchAllOrders():
    allData = mongo.db.orders.find()
    allData = json.loads(dumps(allData))
    return allData


@pizza_app.route("/getorders/<order_id>", methods=["GET"])
def fetchOrder(order_id):
    try:
        data = mongo.db.orders.find_one({"_id": ObjectId(order_id)})
        data = dumps(data)
        return data
    except bson.errors.InvalidId:
        return notFound()


if __name__ == "__main__":
    pizza_app.run(debug=True)
