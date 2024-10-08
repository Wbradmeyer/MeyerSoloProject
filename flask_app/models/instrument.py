from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
from flask_app.models import user


class Instrument:
    db = "solo_project_db"
    # db = "instrument_hub_db"
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
    def create_new_instrument(cls, data):
        if not cls.validate_instrument(data):
            return False
        query = """
        INSERT INTO instruments (name, quality, price, description,
                    sold, user_id, seller_id)
        VALUES (%(name)s, %(quality)s, %(price)s, %(description)s,
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
        this_instrument.seller = user.User.get_user_by_id(this_instrument.seller_id)
        return this_instrument
    
    @classmethod
    def get_instruments_by_name(cls, name):
        data = {'name': name}
        query = """
        SELECT * FROM instruments
        JOIN users ON instruments.user_id = users.id
        WHERE instruments.name = %(name)s
        ;"""
        results = connectToMySQL(cls.db).query_db(query, data)
        filtered_instruments = []
        if results:
            for row in results:
                this_instrument = cls(row)
                this_instrument.owner = user.User(row)
                filtered_instruments.append(this_instrument)
        return filtered_instruments
    
    @classmethod
    def get_instruments_by_quality(cls, quality):
        data = {'quality': quality}
        query = """
        SELECT * FROM instruments
        JOIN users ON instruments.user_id = users.id
        WHERE instruments.quality = %(quality)s
        ;"""
        results = connectToMySQL(cls.db).query_db(query, data)
        filtered_instruments = []
        if results:
            for row in results:
                this_instrument = cls(row)
                this_instrument.owner = user.User(row)
                filtered_instruments.append(this_instrument)
        return filtered_instruments

    @classmethod
    def get_instruments_by_name_and_quality(cls, name, quality):
        data = {'name': name, 'quality': quality}
        query = """
        SELECT * FROM instruments
        JOIN users ON instruments.user_id = users.id
        WHERE instruments.name = %(name)s
        AND instruments.quality = %(quality)s
        ;"""
        results = connectToMySQL(cls.db).query_db(query, data)
        filtered_instruments = []
        if results:
            for row in results:
                this_instrument = cls(row)
                this_instrument.owner = user.User(row)
                filtered_instruments.append(this_instrument)
        return filtered_instruments
    
    @classmethod
    def get_all_instruments_for_sale(cls):
        query = """
        SELECT * FROM instruments
        JOIN users ON instruments.seller_id = users.id
        WHERE instruments.sold = 0
        ;"""
        results = connectToMySQL(cls.db).query_db(query)
        all_for_sale = []
        if results:
            for row in results:
                this_instrument = cls(row)
                this_instrument.owner = user.User(row)
                all_for_sale.append(this_instrument)
        return all_for_sale
    
    @classmethod
    def get_user_instruments(cls ,id):
        data = {"id": id}
        query = """
        SELECT * FROM instruments
        JOIN users ON instruments.user_id = users.id
        WHERE instruments.user_id = %(id)s
        OR instruments.seller_id = %(id)s
        ;"""
        results = connectToMySQL(cls.db).query_db(query, data)
        user_instruments = []
        if results:
            for row in results:
                this_instrument = cls(row)
                this_instrument.owner = user.User(row)
                this_instrument.seller = user.User.get_user_by_id(this_instrument.seller_id)
                user_instruments.append(this_instrument)
        return user_instruments

    # Update Instruments Models
    @classmethod
    def update_instrument(cls, data):
        if not cls.validate_instrument(data):
            return False
        query = """
        UPDATE instruments
        SET name = %(name)s, quality = %(quality)s, price = %(price)s, 
                    description = %(description)s
        WHERE id = %(id)s
        ;"""
        connectToMySQL(cls.db).query_db(query, data)
        return True
    
    @classmethod
    def change_owner(cls, id):
        data = {'id': id,
                'sold': 1,
                'user_id': session['user_id']}
        query = """
        UPDATE instruments
        SET sold = %(sold)s, user_id = %(user_id)s
        WHERE id = %(id)s
        ;"""
        connectToMySQL(cls.db).query_db(query, data)
        return True
    
    @classmethod
    def add_image_to_db_by_id(cls, id, image):
        data = {'id': id,
                'image': image}
        query = """
        UPDATE instruments
        SET image = %(image)s
        WHERE instruments.id = %(id)s 
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