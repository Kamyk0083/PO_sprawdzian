from flask import Flask, jsonify, request, abort
from datetime import datetime

app = Flask(__name__)

class UserManager:
    def __init__(self):
        self.users = {}
        self.next_id = 1

    def get_all_users(self):
        return [{**user, 'age': datetime.now().year - user['birthYear']} for user in self.users.values()]

    def get_user(self, user_id):
        return self.users.get(user_id)

    def add_user(self, user_data):
        user_data['id'] = self.next_id
        self.users[self.next_id] = user_data
        self.next_id += 1
        return user_data

    def update_user(self, user_id, update_data):
        if user_id in self.users:
            self.users[user_id].update(update_data)
            return self.users[user_id]
        return None

    def delete_user(self, user_id):
        return self.users.pop(user_id, None)

user_manager = UserManager()

@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(user_manager.get_all_users())

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = user_manager.get_user(user_id)
    if user:
        return jsonify({**user, 'age': datetime.now().year - user['birthYear']})
    else:
        abort(404)

@app.route('/users', methods=['POST'])
def create_user():
    user_data = request.json
    if not all(key in user_data for key in ('firstName', 'lastName', 'birthYear', 'group')):
        abort(400)  
    if user_data['group'] not in ['user', 'premium', 'admin']:
        abort(400)  
    return jsonify(user_manager.add_user(user_data)), 201

@app.route('/users/<int:user_id>', methods=['PATCH'])
def update_user(user_id):
    update_data = request.json
    updated_user = user_manager.update_user(user_id, update_data)
    if updated_user:
        return jsonify(updated_user)
    else:
        abort(404)

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    if user_manager.delete_user(user_id):
        return '', 204
    else:
        abort(404)

if __name__ == '__main__':
    app.run(debug=True)
