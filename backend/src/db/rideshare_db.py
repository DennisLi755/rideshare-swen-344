import os
from .swen344_db_utils import *
import json
import decimal

class Encoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal): return float(obj)

def rebuild_tables():
    exec_sql_file('src/db/schema.sql')
    exec_sql_file('src/db/test_data.sql')

# rest1
def list_accounts():
    """Gets the userId, name, and special instructions from all users"""
    return exec_get_all('SELECT id, userID, name, special_instructions FROM users')

def get_one_account(id):
    """Gets the id, name, and special instructions from one user
    
    Arguments:
    id - id of the user to get"""
    return exec_get_all('SELECT id, userID, name, special_instructions FROM users WHERE id=%s', (id,))

def list_rides():
    """Gets the ride id, driver name, and rider names from all rides"""
    return exec_get_all('''SELECT rides.id, d.name, ARRAY_AGG(r.name) FROM rides
        INNER JOIN riders ON riders.ride_id = rides.id
        INNER JOIN users AS d on d.id = rides.driver_id
        INNER JOIN users AS r on r.id = riders.rider_id
        GROUP BY rides.id, d.name;''')

#rest2

def create_user(name, special_instructions, is_driver, userID):
    """Creates a new user
    
    Arguments:
    name - name of the new user
    special_instructions - any special_instructions for the user
    is_driver - boolean that indicates if the user is a driver or not
    userID - unique ID set by the user to identify themselves"""
    if (not special_instructions):
        exec_commit("""
            INSERT INTO users (name, special_instructions, is_driver, userID)
            VALUES (%s, DEFAULT, %s, %s)
        """, (name, is_driver, userID))
    else:
        exec_commit("""
            INSERT INTO users (name, special_instructions, is_driver, userID)
            VALUES (%s, %s, %s, %s)
        """, (name, special_instructions, is_driver, userID))
    return {'message': 'user created successfully'}

def update_user(id, name, special_instructions, is_driver, userID):
    """Updates an existing users data
    
    Arguments:
    id - id of the user to update
    name - new name value of the user
    special_instructions - new special_instructions value
    is_driver - whether or not the user is a driver or not,
    userID - unique ID set to the user to identify themselves"""
    exec_commit("""
        UPDATE users
        SET name=%s, special_instructions=%s, is_driver=%s, userID=%s
        WHERE id=%s
    """, (name, special_instructions, is_driver, userID, id))
    return {'message': 'user data updated successfully'}

def delete_user(id):
    """Deletes a user
    
    Arguments:
    id - id of the user to delete"""
    exec_commit("""
        DELETE FROM users
        WHERE id=%s
    """, (id,))
    return {'message': 'user deleted successfully'}

def generate_receipt(ride_id):
    """Generates a receipt using the total riders and total cost of the trip
    
    Arguments:
    ride_id -- the id of the ride
    """
    total_riders = exec_get_one("""
        SELECT COUNT(*) FROM riders
        WHERE ride_id=%s
    """, (ride_id,))
    total_cost = exec_get_one("""
        SELECT cost FROM rides
        WHERE id=%s
    """, (ride_id,))
    receipt = round(total_cost[0]/total_riders[0], 2)
    exec_commit("""
        UPDATE riders
        SET receipt=%s
        WHERE ride_id=%s
    """, (receipt, ride_id))

def list_receipts(limit):
    """Lists the receipts for each rider in a ride
    
    Arguments:
    limit - the limit of results to get"""
    ride_count = exec_get_one("""
        SELECT COUNT(*) FROM rides
    """)
    for ride in range(1, (ride_count[0] + 1)):
        generate_receipt(ride)
    return exec_get_all("""
        SELECT rides.id, users.name, receipt FROM riders
        INNER JOIN users ON users.id = riders.rider_id
        INNER JOIN rides ON rides.id = riders.ride_id
        LIMIT %s
    """, (limit,))

def create_ride(driver_id, cost, riders):
    """Creates a ride and adds it to the database
    
    Arguments:
    driver_id - driver id of the ride
    cost - cost of the ride
    riders - array of ids that correlate to user ids"""
    id = exec_commit_return("""
        INSERT INTO rides(driver_id, cost)
        VALUES(%s, %s) RETURNING id
    """, (driver_id, cost))

    for rider in riders:
        exec_commit("""
            INSERT INTO riders(rider_id, ride_id)
            VALUES(%s, %s)
        """, (rider, id))
    
    return {'message': 'ride created successfully'}
