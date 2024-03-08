import unittest
from main import app, user_manager

class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

        user_manager.users.clear()
        user_manager.next_id = 1

    def test_get_users(self):
        response = self.app.get('/users')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [])

    def test_create_user(self):
        user = {"firstName": "Jan", "lastName": "Kowalski", "birthYear": 1990, "group": "user"}
        response = self.app.post('/users', json=user)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['firstName'], "Jan")

    def test_create_user_bad_request(self):
        user = {"firstName": "Jan"}  # Niepełne dane
        response = self.app.post('/users', json=user)
        self.assertEqual(response.status_code, 400)

    def test_get_user(self):
        user = {"firstName": "Jan", "lastName": "Kowalski", "birthYear": 1990, "group": "user"}
        create_response = self.app.post('/users', json=user)
        user_id = create_response.json['id']

        response = self.app.get(f'/users/{user_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['firstName'], "Jan")

    def test_update_user(self):
        user = {"firstName": "Jan", "lastName": "Kowalski", "birthYear": 1990, "group": "user"}
        create_response = self.app.post('/users', json=user)
        user_id = create_response.json['id']

        update_data = {"firstName": "Paweł"}
        response = self.app.patch(f'/users/{user_id}', json=update_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['firstName'], "Paweł")

    def test_delete_user(self):
        user = {"firstName": "Jan", "lastName": "Kowalski", "birthYear": 1990, "group": "user"}
        create_response = self.app.post('/users', json=user)
        user_id = create_response.json['id']

        response = self.app.delete(f'/users/{user_id}')
        self.assertEqual(response.status_code, 204)

        get_response = self.app.get(f'/users/{user_id}')
        self.assertEqual(get_response.status_code, 404)

if __name__ == '__main__':
    unittest.main()

#Ksawery
