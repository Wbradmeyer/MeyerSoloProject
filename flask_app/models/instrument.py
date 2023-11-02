from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
from flask_app.models import user


class Instrument:
    db = "solo_project_db"
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.quality = data['quality']
        self.price = data['price']
        self.description = data['description']
        self.image = data['image']
        self.sold = data['sold']
        self.user_id = data['user_id']
        self.seller_id = data['seller_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.owner = None
        self.seller = None


    #Create Instruments Models
    @classmethod
    def create_new_instrument(cls, data, image_file):
        if not cls.validate_instrument(data):
            return False
        data['image'] = image_file
        query = """
        INSERT INTO instruments (name, quality, price, description, image,
                    sold, user_id, seller_id)
        VALUES (%(name)s, %(quality)s, %(price)s, %(description)s, %(image)s,
                    %(sold)s, %(user_id)s, %(seller_id)s)
        ;"""
        instrument_id = connectToMySQL(cls.db).query_db(query, data)
        return instrument_id
    

    #Read Instruments Models
    @classmethod
    def get_instrument_by_id(cls, id):
        data = {'id': id}
        query = """
        SELECT * FROM instruments
        JOIN users ON instruments.user_id = users.id
        WHERE instruments.id = %(id)s
        ;"""
        result = connectToMySQL(cls.db).query_db(query, data)
        this_instrument = cls(result[0])
        this_instrument.owner = user.User(result[0])
        return this_instrument
    

    @classmethod
    def get_all_instruments_with_users(cls):
        query = """
        SELECT * FROM instruments
        JOIN users ON instruments.user_id = users.id
        ;"""
        results = connectToMySQL(cls.db).query_db(query)
        all_instruments = []
        if results:
            for row in results:
                this_instrument = cls(row)
                this_instrument.owner = user.User(row)
                all_instruments.append(this_instrument)
        return all_instruments
    
    @classmethod
    def get_all_instruments_with_sellers(cls):
        query = """
        SELECT * FROM instruments
        JOIN users ON instruments.seller_id = users.id
        WHERE instruments.sold = 1
        ;"""
        results = connectToMySQL(cls.db).query_db(query)
        all_sold = []
        if results:
            for row in results:
                this_instrument = cls(row)
                this_instrument.seller = user.User(row)
                all_sold.append(this_instrument)
        return all_sold


    # Update Instruments Models
    @classmethod
    def update_instrument(cls, data):
        if not cls.validate_instrument(data):
            return False
        query = """
        UPDATE instruments
        SET name = %(name)s, quality = %(quality)s, price = %(price)s, 
                    description = %(description)s, image = %(image)s
        WHERE id = %(id)s
        ;"""
        connectToMySQL(cls.db).query_db(query, data)
        return True
    
    @classmethod
    def change_owner(cls, id):
        data = {'id': id,
                'sold': 1,
                'user_id': session['user_id']}
        this_instrument = cls.get_instrument_by_id(id)
        # if session['user_id'] != this_instrument.user_id:
        #     return False
        query = """
        UPDATE instruments
        SET sold = %(sold)s, user_id = %(user_id)s
        WHERE id = %(id)s
        ;"""
        connectToMySQL(cls.db).query_db(query, data)
        return True

    # Delete Instruments Models
    @classmethod
    def delete_instrument_by_id(cls, id):
        data = {'id': id}
        this_instrument = cls.get_instrument_by_id(id)
        if session['user_id'] != this_instrument.user_id:
            return False
        query = """
        DELETE FROM instruments
        WHERE id = %(id)s
        ;"""
        connectToMySQL(cls.db).query_db(query, data)
        return True

    #Helper Instruments Methods
    @staticmethod
    def validate_instrument(data):
        is_valid = True
        inst_list = ["Keyboard", "Trumpet", "Trombone", "Tuba", "Violin", 
                    "Viola", "Cello", "Flute", "Clarinet", "Oboe", "Saxophone"]
        quality_list = ["New", "Excellent", "Very Good", "Good", "Fair"]

        if data['name'] not in inst_list:
            flash('Please select one of the given instruments.')
            is_valid = False
        if data['quality'] not in quality_list:
            flash('Please select one of the given conditions.')
            is_valid = False
        if int(data['price']) < 1 or int(data['price']) > 100000:
            flash('Price must be between $1 and $99999.')
            is_valid = False
        if len(data['description']) < 3:
            flash('Description must be at least 3 characters.')
            is_valid = False

        return is_valid
    
    @staticmethod
    def get_instrument_select():
        inst_list = [
            {"inst_name": "Keyboard"}, 
            {"inst_name": "Trumpet"}, 
            {"inst_name": "Trombone"}, 
            {"inst_name": "Tuba"}, 
            {"inst_name": "Violin"}, 
            {"inst_name": "Viola"}, 
            {"inst_name": "Cello"}, 
            {"inst_name": "Flute"}, 
            {"inst_name": "Clarinet"}, 
            {"inst_name": "Oboe"}, 
            {"inst_name": "Saxophone"}
        ]
        return inst_list

    @staticmethod
    def get_quality_select():
        quality_list = [
            {"quality": "New"}, 
            {"quality": "Excellent"}, 
            {"quality": "Very Good"}, 
            {"quality": "Good"}, 
            {"quality": "Fair"}
        ]
        return quality_list