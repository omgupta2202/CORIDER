from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
from config import MONGODB_URI

app = Flask(__name__)
client = MongoClient(MONGODB_URI)
db = client.get_database('YOUR_DATABASE_NAME')
users_collection = db.users

@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True)
    
@app.route('/users', methods=['GET'])
def get_users():
    users = list(users_collection.find({}, {'password': 0}))
    return jsonify(users), 200

@app.route('/users/<string:user_id>', methods=['GET'])
def get_user(user_id):
    user = users_collection.find_one({'_id': ObjectId(user_id)}, {'password': 0})
    if user:
        return jsonify(user), 200
    return jsonify({'message': 'User not found'}), 404

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    user_id = users_collection.insert_one(data).inserted_id
    return jsonify({'message': 'User created', 'user_id': str(user_id)}), 201

@app.route('/users/<string:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    result = users_collection.update_one({'_id': ObjectId(user_id)}, {'$set': data})
    if result.modified_count:
        return jsonify({'message': 'User updated'}), 200
    return jsonify({'message': 'User not found'}), 404

@app.route('/users/<string:user_id>', methods=['DELETE'])
def delete_user(user_id):
    result = users_collection.delete_one({'_id': ObjectId(user_id)})
    if result.deleted_count:
        return jsonify({'message': 'User deleted'}), 200
    return jsonify({'message': 'User not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
