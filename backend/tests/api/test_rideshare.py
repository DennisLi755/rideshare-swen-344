import unittest
from tests.test_utils import *
import json


class TestExample(unittest.TestCase):

    def setUp(self):  
        """Initialize DB using API call"""
        post_rest_call(self, 'http://localhost:5000/manage/init')
        print("DB Should be reset now")

    #rest 1
    def test_get_accounts(self):
        """Get all the accounts inserted"""
        result = len(get_rest_call(self, 'http://localhost:5000/account'))
        self.assertEqual(4, result)

    def test_get_rides(self):
        """Get all the rides inserted"""
        result = len(get_rest_call(self, 'http://localhost:5000/rides'))
        self.assertEqual(3, result)

    def test_get_one_account(self):
        """Get one account with query paramter 1"""
        result = get_rest_call(self, 'http://localhost:5000/account?id=1')
        self.assertEqual([[1, 'Tom123', 'Tom Magliozzi', "Don't drive like my brother"]], result)
    
    def test_get_one_account_not_exist(self):
        """Get one account with query paramter 5 (does not exist)"""
        result = get_rest_call(self, 'http://localhost:5000/account?id=5')
        self.assertEqual([], result)

    # rest 2
    def test_create_user(self):
        """Creates a user"""
        body = {
            "name": "Dennis",
            "userID": "djl6347",
            "is_driver": False
        }
        result = post_rest_call(self, 'http://localhost:5000/account', json.dumps(body), {'Content-Type': 'application/json'}, 201)
        self.assertEqual({'message': 'user created successfully'}, result)

    def test_create_user_already_exists(self):
        """Creates a user with the same userID as an existing user"""
        body = {
            "name": "Tom",
            "userID": "Tom123",
            "is_driver": False
        }
        result = post_rest_call(self, 'http://localhost:5000/account', json.dumps(body), {'Content-Type': 'application/json'}, 500)
        self.assertEqual({'message': 'user already exists'}, result)

    def test_edit_user(self):
        """Edits the data of an existing user"""
        body = {
            "name": "Dennis",
            "userID": "djl6347",
            "is_driver": True,
            "special_instructions": "I drive like crazy."
        }
        result = put_rest_call(self, 'http://localhost:5000/account?id=4', json.dumps(body), {'Content-Type': 'application/json'}, 200)
        self.assertEqual({'message': 'user data updated successfully'}, result)

    def test_edit_user_not_exist(self):
        """Try to edit the data of a user that does not exist"""
        body = {
            "name": "Dennis",
            "userID": "djl6347",
            "is_driver": True,
            "special_instructions": "I drive like crazy."
        }
        result = put_rest_call(self, 'http://localhost:5000/account?id=5', json.dumps(body), {'Content-Type': 'application/json'}, 500)
        self.assertEqual({'message': 'user not found'}, result)

    def test_edit_user_same_id(self):
        """Try to change userID to another users userID"""
        body = {
            "name": "Dennis",
            "userID": "michael78",
            "is_driver": False
        }
        result = put_rest_call(self, 'http://localhost:5000/account?id=4', json.dumps(body), {'Content-Type': 'application/json'}, 500)
        self.assertEqual({'message': 'userID already exists'}, result)

    def test_delete_user(self):
        """Delete an existing user"""
        result = delete_rest_call(self, 'http://localhost:5000/account?id=4', {}, 200)
        self.assertEqual({'message': 'user deleted successfully'}, result)

    def test_delete_user_not_exist(self):
        """Try to delete a user that does not exist"""
        result = delete_rest_call(self, 'http://localhost:5000/account?id=5', {}, 500)
        self.assertEqual({'message': 'user not found'}, result)
    
    def test_create_ride(self):
        """Creates a ride"""
        body = {
            "driver_id": 2,
            "cost": 20,
            "riders": [1, 4, 3]
        }
        result = post_rest_call(self, 'http://localhost:5000/rides', json.dumps(body), {'Content-Type': 'application/json'}, 201)
        self.assertEqual({'message': 'ride created successfully'}, result)

    def test_list_receipts_limit_3(self):
        """List receipts with a limit of 3"""
        expected = [
            [1, "Mike Easter", 5.0],
            [1, "Darren Jiang", 5.0],
            [2, "Mike Easter", 12.0]
        ]
        result = get_rest_call(self, 'http://localhost:5000/receipt?limit=3')
        self.assertEqual(expected, result)

    def test_list_receipts_limit_7(self):
        """List receipts with a limit of 7 (including new ride created in test_create_ride())"""
        self.test_create_ride()
        expected = [
            [1, "Mike Easter", 5.0],
            [1, "Darren Jiang", 5.0],
            [2, "Mike Easter", 12.0],
            [3, "Ray Magliozzi", 8.0],
            [4, "Tom Magliozzi", 6.67],
            [4, "Darren Jiang", 6.67],
            [4, "Mike Easter", 6.67]
        ]
        result = get_rest_call(self, 'http://localhost:5000/receipt?limit=7')
        self.assertEqual(expected, result)