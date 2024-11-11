from flask_restful import Resource
from flask import request
from db import rideshare_db

class Users(Resource):
    """Gets account data
    
    Takes one query paramter, id, for more precise data fetching"""
    def get(self):
        id = request.args.get('id')
        if (id):
            return rideshare_db.get_one_account(id)
        else:
            return rideshare_db.list_accounts()
    
    """Adds a user to the database"""
    def post(self):
        data = request.get_json()
        accounts = rideshare_db.list_accounts()
        for account in accounts:
            if (data.get('userID') == account[1]):
                return {'message': 'user already exists'}, 500

        return rideshare_db.create_user(data.get('name'), data.get('special_instructions'), data.get('is_driver'), data.get('userID')), 201
    
    """Edits the data of an existing user"""
    def put(self):
        id = int(request.args.get('id'))
        accounts = rideshare_db.list_accounts()
        data = request.get_json()
        for account in accounts:
            if (id == account[0]):
                return rideshare_db.update_user(id, data.get('name'), data.get('special_instructions'), data.get('is_driver'), data.get('userID')), 200
            elif (data.get('userID') == account[1]):
                return {'message': 'userID already exists'}, 500
        
        return {'message': 'user not found'}, 500
    
    """Deletes an existing user"""
    def delete(self):
        id = int(request.args.get('id'))
        accounts = rideshare_db.list_accounts()
        for account in accounts:
            if (id == account[0]):
                return rideshare_db.delete_user(id), 200
        
        return {'message': 'user not found'}, 500
    
class Rides(Resource):
    """Gets all rides"""
    def get(self):
        return rideshare_db.list_rides()
    
    """"Adds a ride to the database"""
    def post(self):
        data = request.get_json()
        return rideshare_db.create_ride(data.get('driver_id'), data.get('cost'), data.get('riders')), 201
    
class Receipt(Resource):
    """Gets the receipts for riders in riders
    
    Takes a limit query paramter for how many receipts to list"""
    def get(self):
        limit = request.args.get('limit')
        if (limit):
            return rideshare_db.list_receipts(limit)
        else:
            return {'message': 'limit not given'}, 500